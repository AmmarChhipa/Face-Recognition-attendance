import cv2
import mediapipe as mp
from deepface import DeepFace
import os
import csv
from datetime import datetime
import time
from openpyxl import Workbook   # <-- (for Excel)

# --- 1. Setup Attendance System (SINGLE IMAGE PER PERSON) ---

db_path = "database"
master_list = set()
present_students = set()
present_time = {}   # <-- (timestamp storage)

print("Loading student database...")
try:
    image_extensions = ('.jpg', '.jpeg', '.png')
    # Look for individual image files
    for entry in os.scandir(db_path):
        if entry.is_file() and entry.name.lower().endswith(image_extensions):
            # Get name from filename (e.g., "Student1.jpg" -> "Student1")
            name = os.path.splitext(entry.name)[0]
            master_list.add(name)
    
    if not master_list:
        print(f"Warning: No student images (.jpg, .png) found in '{db_path}'.")
    else:
        print(f"Database loaded. Total students: {len(master_list)}")
        print(f"Master List: {master_list}")

except FileNotFoundError:
    print(f"ERROR: Database path not found: '{db_path}'")
    exit()
except Exception as e:
    print(f"An error occurred while scanning database: {e}")
    exit()

# --- 2. Load Models and Video ---

mp_face_detection = mp.solutions.face_detection.FaceDetection()
mp_draw = mp.solutions.drawing_utils

video_path = 0 # webcam

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print(f"Error: Could not open video source '{video_path}'")
    exit()

# --- 3. Setup Confirmation Tracker ---

fps = cap.get(cv2.CAP_PROP_FPS)
if fps == 0 or fps is None:
    print("Warning: Could not get video FPS. Defaulting to 30.")
    fps = 30.0

CONFIRMATION_SECONDS = 0.2
frames_to_confirm = int(fps * CONFIRMATION_SECONDS)

confirmation_tracker = {name: 0 for name in master_list}

print(f"\nVideo FPS: {fps:.2f}. Need {frames_to_confirm} continuous frames ({CONFIRMATION_SECONDS}s) to confirm presence.")
print("Starting video processing... Press 'x' to stop and generate report.")

# --- 4. Process Video Frame by Frame ---

while True:
    success, img = cap.read()
    if not success:
        if video_path != 0:
            print("Video ended.")
        else:
            print("Webcam feed lost.")
        break

    img = cv2.flip(img, 1)

    seen_in_this_frame = set()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = mp_face_detection.process(img_rgb)

    if results.detections:
        for detection in results.detections:
            ih, iw, _ = img.shape
            bboxC = detection.location_data.relative_bounding_box
            
            if not (bboxC and bboxC.xmin and bboxC.ymin and bboxC.width and bboxC.height):
                continue
                
            bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
            x, y, w, h = bbox
            x, y = max(0, x), max(0, y)
            w = min(w, iw - x)
            h = min(h, ih - y)
            
            mp_draw.draw_detection(img, detection)
            
            pad = 20
            face = img[max(0, y-pad):min(y+h+pad, ih), max(0, x-pad):min(x+w+pad, iw)]

            if face.size == 0:
                continue

            try:
                dfs = DeepFace.find(face, 
                                    db_path=db_path, 
                                    model_name="VGG-Face", 
                                    enforce_detection=False,
                                    silent=True)
                
                # Unknown face:
                if dfs[0].empty:
                    cv2.putText(img, "Not Found", (x, y-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 0, 255), 2)
                    continue

                identity_path = dfs[0]['identity'][0]
                    
                name = os.path.splitext(os.path.basename(identity_path))[0]

                # Already present:
                if name in present_students:
                    cv2.putText(img, f"{name} (Present)", (x, y-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 255, 0), 2)
                    continue

                if name in confirmation_tracker:
                    seen_in_this_frame.add(name)
                    confirmation_tracker[name] += 1
                    
                    if confirmation_tracker[name] >= frames_to_confirm:
                        if name not in present_students:

                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            present_time[name] = timestamp

                            print(f"*** CONFIRMED: {name} is Present at {timestamp} ***")

                            present_students.add(name)
                        
                        cv2.putText(img, f"{name} (Confirmed)", (x, y-10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (0, 255, 0), 2)
                    
                    else:
                        percent = int((confirmation_tracker[name] / frames_to_confirm) * 100)
                        cv2.putText(img, f"{name} (Confirming {percent}%)", (x, y-10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                    (0, 255, 255), 2)
                    
            except Exception as e:
                pass

    for name in master_list:
        if name not in seen_in_this_frame:
            confirmation_tracker[name] = 0

    cv2.imshow("Face Recognition Attendance - Press 'x' to Exit", img)

    if cv2.waitKey(1) & 0xFF == ord('x'):
        print("Stopping video feed.")
        break

# --- 5. Release Resources ---
cap.release()
cv2.destroyAllWindows()

# --- 6. Generate Final Attendance Report ---
print("\n--- 📝 Attendance Report ---")
absent_students = master_list - present_students

print(f"Total Students: {len(master_list)}")
print(f"Present ({len(present_students)}): {present_students if present_students else 'None'}")
print(f"Absent ({len(absent_students)}): {absent_students if absent_students else 'None'}")

today_date = datetime.now().strftime("%Y-%m-%d")
excel_filename = f"attendance_{today_date}.xlsx"
print(f"\nWriting attendance to {excel_filename}...")

try:
    # Create Excel workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Attendance"

    # Header
    ws.append(["Student", "Status", "Time"])

    # Present students
    for student in sorted(list(present_students)):
        ws.append([student, "Present", present_time.get(student, "")])

    # Absent students
    for student in sorted(list(absent_students)):
        ws.append([student, "Absent", ""])

    # Save Excel file
    wb.save(excel_filename)

    print(f"Attendance Excel file created successfully: {excel_filename}")

except Exception as e:
    print(f"An unexpected error occurred while creating Excel: {e}")