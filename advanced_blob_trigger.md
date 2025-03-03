
Advanced Blob Trigger
A Python-based interactive application that uses real-time computer vision and OpenGL rendering to create a dynamic "blob" effect triggered by hand movements. Built with cutting-edge techniques as of March 2025, this project runs locally on a MacBook Air M3 and offers advanced features like pose detection, shader-like effects, audio feedback, and customizable parameters.
Inspired by this video, this script elevates the concept with modern libraries and interactivity.
Features
Real-Time Pose Tracking: Uses Mediapipe to track your right hand for precise blob positioning.
Advanced Visual Effects:
Default: Cyan square blob.
Glow: Fading orange trail with smooth scaling.
Particle Burst: Scattered green particles around the blob.
Interactive GUI: Adjust sensitivity, blob size, and trail length with sliders; switch effects via presets.
Audio Feedback: Generates sine wave tones based on blob position.
Optimized for M3: Runs smoothly on Apple Silicon with 60 FPS.
Prerequisites
Python 3.9+
A MacBook with a webcam (tested on M3 Air)
Audio output enabled
Required Libraries
Install dependencies via pip:
bash
pip install opencv-python numpy pyqt5 mediapipe pyopengl pydub scipy
Installation
Clone or download this repository:
bash
git clone <repository-url>
cd <repository-folder>
Install the required libraries (see above).
Ensure your webcam and audio output are functional.
Usage
Save the script as advanced_blob_trigger.py.
Run the script:
bash
python advanced_blob_trigger.py
A window will open with:
Left: Live webcam feed showing your movements.
Middle: Black background with a white vertical line and the blob effect.
Right: Control panel with sliders and a preset dropdown.
Interact:
Move your right hand in front of the webcam to trigger the blob.
Adjust sliders:
Sensitivity (10–100): Detection confidence threshold.
Blob Size (10–200): Size of the blob effect.
Trail Length (1–50): Persistence of the trail effect.
Select a preset (Default, Glow, Particle Burst) from the dropdown.
Listen for audio feedback as the blob moves.
Close the window to exit.
How It Works
Pose Detection: Mediapipe tracks your right hand (landmark 20) using machine learning.
Rendering: PyOpenGL renders shader-like effects in real-time.
Audio: PyDub generates sine waves based on the blob's y-position.
GUI: PyQt5 provides a responsive interface with live parameter updates.
Troubleshooting
Webcam Not Working: Ensure no other apps are using the camera; check permissions in macOS System Settings.
Lag or Low FPS: Reduce timer.start(16) to timer.start(30) in the script for 30 FPS.
No Audio: Verify your audio output is enabled; adjust freq range in audio_feedback for audible tones.
Mediapipe Fails: Ensure good lighting and keep your upper body visible in the frame.
Customization
Colors: Modify RGB values in draw_default, draw_glow, or draw_particles in GLWidget.
Effects: Add new presets by extending apply_preset and corresponding draw_* methods.
Tracking: Change the tracked landmark (e.g., left hand = 19) in update_frame.
Audio: Experiment with freq or add complex waveforms in audio_feedback.
Performance Notes
Tested on a MacBook Air M3 with 60 FPS.
Adjust frame rate in timer.start(16) if needed for different hardware.
License
This project is open-source under the MIT License. Feel free to modify and distribute!
Acknowledgments
Built with xAI's Grok 3 assistance.
Inspired by RavenKwok's video.
