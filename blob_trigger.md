Blob Trigger Interactive
A Python application that replicates an interactive blob trigger mechanism, inspired by a video demonstration (link to X post). This project uses computer vision to detect motion from a webcam feed and triggers a visual "blob" effect on a split-screen display. Built with OpenCV, NumPy, and PyQt5, it runs locally on a MacBook Air M3 and includes interactive sliders to adjust detection parameters in real-time.
Features
Real-time Motion Detection: Captures your silhouette via webcam and tracks movement.

Blob Effect: Displays a responsive yellow blob on a black background with a white vertical line, triggered by motion.

Interactive GUI: Adjust threshold, blur size, and blob size with sliders for a customizable experience.

Optimized for M3: Lightweight and efficient for smooth performance on Apple Silicon.
Prerequisites
Python 3.9+: Ensure Python is installed (comes pre-installed on macOS).

MacBook with Webcam: Tested on a MacBook Air M3; should work on other macOS devices with a camera.
Required Libraries
opencv-python: For video capture and computer vision.

numpy: For numerical operations and image processing.

pyqt5: For the graphical user interface.
Install them via pip:
bash
pip install opencv-python numpy pyqt5

Installation
Clone or download this repository to your local machine:
bash
git clone <repository-url>
cd blob-trigger-interactive

Alternatively, copy the blob_trigger.py script and this README.md into a folder.

Install the dependencies:
bash
pip install -r requirements.txt

(If you create a requirements.txt with opencv-python, numpy, and pyqt5, or install them manually as shown above.)

Ensure your webcam is accessible and not in use by another application.
Usage
Run the script:
bash
python blob_trigger.py
A window will open with:
Left Panel: Live video feed from your webcam.

Middle Panel: Black background with a white vertical line and a yellow blob that responds to your movement.

Right Panel: Sliders to tweak:
Threshold: Motion detection sensitivity (10–255).

Blur Size: Smoothing of the motion map (1–31, odd numbers only).

Blob Size: Size of the triggered blob (5–100).
Move in front of the webcam to trigger the blob effect. Adjust sliders to fine-tune the detection and appearance.

Close the window to exit the application.
How It Works
Video Capture: Uses OpenCV to grab frames from your webcam.

Motion Detection: Applies background subtraction, Gaussian blur, and thresholding to detect your silhouette.

Blob Rendering: Identifies the largest contour (your movement) and draws a yellow blob at its centroid.

GUI: PyQt5 provides a responsive split-screen interface with real-time updates.
Customization
Blob Color: Change the RGB value in cv2.circle(blob_frame, (cx, cy), blob_size, (0, 255, 255), -1) (e.g., (255, 0, 0) for red).

Frame Rate: Adjust self.timer.start(30) to a lower value (e.g., 15) for higher FPS, if your M3 can handle it.

Effects: Add more visual effects by modifying the blob_frame rendering logic (e.g., gradients, multiple blobs).
Notes
Lighting: Best results with consistent lighting and a plain background.

Performance: Optimized for efficiency on the M3; may lag slightly under poor lighting or heavy system load.

Troubleshooting: If the webcam fails to open, ensure no other app is using it and check permissions in macOS System Settings > Security & Privacy.
License
This project is open-source and available under the MIT License (LICENSE). Feel free to modify and share!
Acknowledgments
Inspired by RavenKwok's X post.

Built with love by [xAI's Grok]