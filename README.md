<div align="center">

  <h1>🧠✨ Face Recognition Attendance System</h1>
  <h3>Automated • Contactless • AI-Powered</h3>

  <p>
    An AI-based attendance system that detects and recognizes faces in real time<br>
    and automatically logs attendance into an Excel sheet with timestamps.
  </p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.10+-blue" />
    <img src="https://img.shields.io/badge/Status-Active-success" />
    <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20MacOS-black" />
  </p>

  <!-- Optional: Add a banner or GIF if you have one -->
  <!--
  <p>
    <img src="demo.gif" alt="Project Demo" width="600" />
  </p>
  -->

</div>

<hr />

<h2>🔍 Overview</h2>

<p>
Traditional attendance systems rely on manual entry, ID cards, or QR codes —
all of which are slow, repetitive, and error-prone.
</p>

<p>
This project uses <b>Computer Vision</b> and <b>Deep Learning</b> to:
</p>

<ul>
  <li>Detect faces from a live webcam feed</li>
  <li>Recognize individuals using a face database</li>
  <li>Confirm presence over multiple frames to avoid false positives</li>
  <li>Automatically generate an Excel report with timestamps</li>
</ul>

<p>
Just walk in → the system recognizes you → attendance recorded ✅
</p>

<hr />

<h2>✨ Features</h2>

<ul>
  <li>⚡ Real-time face detection &amp; recognition</li>
  <li>🧾 Automatic Excel attendance report (<code>.xlsx</code>)</li>
  <li>🧠 Uses VGG-Face model via <code>DeepFace</code></li>
  <li>🧍 Works with a <b>single image per person</b> in the database</li>
  <li>🔁 Confirmation mechanism using multiple frames to reduce misclassification</li>
  <li>🎥 Webcam-based (no special hardware required)</li>
</ul>

<hr />

<h2>🛠 Tech Stack</h2>

<table>
  <tr>
    <th align="left">Category</th>
    <th align="left">Technology</th>
  </tr>
  <tr>
    <td>Language</td>
    <td><b>Python</b></td>
  </tr>
  <tr>
    <td>Computer Vision</td>
    <td><b>OpenCV</b>, <b>MediaPipe</b></td>
  </tr>
  <tr>
    <td>Face Recognition</td>
    <td><b>DeepFace</b> (VGG-Face)</td>
  </tr>
  <tr>
    <td>Report Generation</td>
    <td><b>OpenPyXL</b> (Excel export)</td>
  </tr>
</table>

<hr />

<h2>📁 Project Structure</h2>

<details>
  <summary>Click to expand</summary>
  <br />
  <pre>
Face-Recognition-Attendance-System/
│
├── database/                  # One face image per person
│   ├── Ammar.jpg
│   ├── Student1.png
│   └── ...
│
├── main.py                    # Core script (the code you shared)
│
└── attendance_YYYY-MM-DD.xlsx # Auto-generated attendance file
  </pre>
</details>

<hr />

<h2>⚙️ Installation</h2>

<h3>1️⃣ Clone the repository</h3>

<pre><code>git clone https://github.com/AmmarChhipa/Face-Recognition-attendance.git
cd Face-Recognition-attendance
</code></pre>

<h3>2️⃣ Install dependencies</h3>

<pre><code>pip install opencv-python mediapipe deepface openpyxl
</code></pre>

<p>On some systems you may also need:</p>

<pre><code>pip install tensorflow
</code></pre>

<hr />

<h2>📸 Database Setup</h2>

<p>
Place one clear, front-facing image of each person in the <code>database</code> folder.
The <b>file name</b> will be used as the person's name in the attendance report.
</p>

<pre><code>database/
├── Ammar.jpg       → "Ammar"
├── JohnDoe.png     → "JohnDoe"
└── Student01.jpeg  → "Student01"
</code></pre>

<hr />

<h2>▶️ Usage</h2>

<ol>
  <li>Ensure your webcam is connected.</li>
  <li>Place all reference images inside the <code>database/</code> folder.</li>
  <li>Run the script:</li>
</ol>

<pre><code>python main.py
</code></pre>

<ul>
  <li>The system starts reading frames from the webcam.</li>
  <li>Faces are detected using <code>MediaPipe</code>.</li>
  <li>Each detected face is matched against the <code>database/</code> using <code>DeepFace</code>.</li>
  <li>Once a face is recognized for enough continuous frames, the person is marked as <b>Present</b> and timestamp is stored.</li>
</ul>

<p>
Press <b>X</b> at any time to stop the webcam and generate the final attendance Excel file:
</p>

<pre><code>attendance_YYYY-MM-DD.xlsx
</code></pre>

<hr />

<h2>📊 Sample Output (Excel)</h2>

<table>
  <tr>
    <th>Name</th>
    <th>Status</th>
    <th>Time</th>
  </tr>
  <tr>
    <td>Ammar</td>
    <td>Present</td>
    <td>2025-12-06 18:45:15</td>
  </tr>
  <tr>
    <td>Student01</td>
    <td>Absent</td>
    <td>–</td>
  </tr>
</table>

<hr />

<h2>🧪 Future Enhancements</h2>

<ul>
  <li>🔍 Anti-spoof detection (prevent printed photo / mobile screen attacks)</li>
  <li>📊 Real-time analytics dashboard (present/absent stats, graphs)</li>
  <li>☁️ Cloud integration for centralized data storage</li>
  <li>🎭 Mask-aware recognition</li>
  <li>🎥 Multi-camera / multi-classroom support</li>
</ul>

<hr />

<h2>🤝 Contributing</h2>

<p>
Contributions, suggestions, and feature requests are welcome!<br />
Feel free to fork the repo, create a branch, and open a Pull Request.
</p>

<hr />

<h2>⭐ Support</h2>

<p>
If you find this project useful or interesting:
</p>

<ul>
  <li>⭐ Star the repository</li>
  <li>🔁 Share it with others</li>
  <li>👀 Watch the repo for future updates</li>
</ul>

<hr />

<h2>👨‍💻 Developer</h2>

<p>
<b>Ammar Chhipa</b><br />
<!-- Replace the # with your actual LinkedIn / portfolio URL -->
🔗 <a href="https://www.linkedin.com/in/ammar-chhipa" target="_blank">Connect with me on LinkedIn</a>
</p>

<br />

<div align="center">
  <i>“Automation isn’t the future — it’s already here. We just have to build it.”</i>
</div>
