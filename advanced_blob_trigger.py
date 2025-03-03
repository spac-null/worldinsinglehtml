import cv2
import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore, QtOpenGL
import sys
import mediapipe as mp
from OpenGL.GL import *
from OpenGL.GLU import *
from pydub import AudioSegment
from pydub.playback import play
import scipy.interpolate as interp
import threading

class AdvancedBlobTriggerApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Blob Trigger")
        self.setGeometry(100, 100, 1280, 720)

        # Video capture
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("Cannot open webcam")

        # Mediapipe setup
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

        # Widget setup
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QtWidgets.QHBoxLayout(self.central_widget)

        # Left: Video feed
        self.video_label = QtWidgets.QLabel()
        self.video_label.setFixedSize(640, 480)
        self.layout.addWidget(self.video_label)

        # Right: OpenGL blob effect
        self.gl_widget = GLWidget()
        self.gl_widget.setFixedSize(640, 480)
        self.layout.addWidget(self.gl_widget)

        # Controls
        self.controls_widget = QtWidgets.QWidget()
        self.controls_layout = QtWidgets.QVBoxLayout(self.controls_widget)
        self.layout.addWidget(self.controls_widget)

        # Sensitivity slider
        self.sensitivity_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.sensitivity_slider.setRange(10, 100)
        self.sensitivity_slider.setValue(50)
        self.sensitivity_slider.valueChanged.connect(self.update_params)
        self.controls_layout.addWidget(QtWidgets.QLabel("Sensitivity"))
        self.controls_layout.addWidget(self.sensitivity_slider)

        # Blob size slider
        self.blob_size_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.blob_size_slider.setRange(10, 200)
        self.blob_size_slider.setValue(50)
        self.blob_size_slider.valueChanged.connect(self.update_params)
        self.controls_layout.addWidget(QtWidgets.QLabel("Blob Size"))
        self.controls_layout.addWidget(self.blob_size_slider)

        # Trail length slider
        self.trail_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.trail_slider.setRange(1, 50)
        self.trail_slider.setValue(10)
        self.trail_slider.valueChanged.connect(self.update_params)
        self.controls_layout.addWidget(QtWidgets.QLabel("Trail Length"))
        self.controls_layout.addWidget(self.trail_slider)

        # Preset dropdown
        self.preset_combo = QtWidgets.QComboBox()
        self.preset_combo.addItems(["Default", "Glow", "Particle Burst"])
        self.preset_combo.currentIndexChanged.connect(self.apply_preset)
        self.controls_layout.addWidget(QtWidgets.QLabel("Effect Preset"))
        self.controls_layout.addWidget(self.preset_combo)

        # State variables
        self.blob_pos = None
        self.prev_pos = []
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(16)  # ~60 FPS

        # Audio setup
        self.audio_thread = threading.Thread(target=self.audio_feedback, daemon=True)
        self.audio_thread.start()

    def update_params(self):
        self.gl_widget.blob_size = self.blob_size_slider.value()
        self.gl_widget.trail_length = self.trail_slider.value()

    def apply_preset(self):
        preset = self.preset_combo.currentText()
        if preset == "Glow":
            self.gl_widget.effect_type = "glow"
            self.blob_size_slider.setValue(80)
            self.trail_slider.setValue(20)
        elif preset == "Particle Burst":
            self.gl_widget.effect_type = "particles"
            self.blob_size_slider.setValue(30)
            self.trail_slider.setValue(5)
        else:
            self.gl_widget.effect_type = "default"
            self.blob_size_slider.setValue(50)
            self.trail_slider.setValue(10)
        self.update_params()

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        frame = cv2.resize(frame, (640, 480))
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_frame)

        if results.pose_landmarks:
            # Track right hand (landmark 20)
            hand_x = int(results.pose_landmarks.landmark[20].x * 640)
            hand_y = int(results.pose_landmarks.landmark[20].y * 480)
            self.blob_pos = (hand_x, hand_y)
            self.prev_pos.append(self.blob_pos)
            if len(self.prev_pos) > self.trail_slider.value():
                self.prev_pos.pop(0)
        else:
            self.blob_pos = None

        # Update video feed
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        qt_image = QtGui.QImage(rgb_frame.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        self.video_label.setPixmap(QtGui.QPixmap.fromImage(qt_image))

        # Update GL widget
        self.gl_widget.blob_pos = self.blob_pos
        self.gl_widget.prev_pos = self.prev_pos
        self.gl_widget.update()

    def audio_feedback(self):
        while True:
            if self.blob_pos:
                # Simple sine wave tone based on y-position
                freq = 200 + (self.blob_pos[1] / 480) * 800
                audio = AudioSegment.sine(duration=100, freq=freq).fade_out(50)
                play(audio)
            QtCore.QThread.msleep(100)

    def closeEvent(self, event):
        self.cap.release()
        self.pose.close()
        event.accept()

class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.blob_pos = None
        self.prev_pos = []
        self.blob_size = 50
        self.trail_length = 10
        self.effect_type = "default"

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, w, h, 0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

        # Draw vertical line
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_LINES)
        glVertex2f(320, 0)
        glVertex2f(320, 480)
        glEnd()

        if self.blob_pos:
            x, y = self.blob_pos
            if self.effect_type == "glow":
                self.draw_glow(x, y)
            elif self.effect_type == "particles":
                self.draw_particles(x, y)
            else:
                self.draw_default(x, y)

    def draw_default(self, x, y):
        glColor3f(0.0, 1.0, 1.0)  # Cyan
        glBegin(GL_QUADS)
        r = self.blob_size / 2
        glVertex2f(x - r, y - r)
        glVertex2f(x + r, y - r)
        glVertex2f(x + r, y + r)
        glVertex2f(x - r, y + r)
        glEnd()

    def draw_glow(self, x, y):
        for i, pos in enumerate(self.prev_pos):
            alpha = 1.0 - (i / len(self.prev_pos))
            glColor4f(1.0, 0.5, 0.0, alpha)  # Orange with fading alpha
            glBegin(GL_QUADS)
            r = self.blob_size * (1 - i / len(self.prev_pos))
            px, py = pos
            glVertex2f(px - r, py - r)
            glVertex2f(px + r, py - r)
            glVertex2f(px + r, py + r)
            glVertex2f(px - r, py + r)
            glEnd()

    def draw_particles(self, x, y):
        np.random.seed(42)
        for i in range(20):
            offset_x = np.random.uniform(-self.blob_size, self.blob_size)
            offset_y = np.random.uniform(-self.blob_size, self.blob_size)
            alpha = np.random.uniform(0.5, 1.0)
            glColor4f(0.0, 1.0, 0.0, alpha)  # Green particles
            glBegin(GL_POINTS)
            glPointSize(5)
            glVertex2f(x + offset_x, y + offset_y)
            glEnd()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = AdvancedBlobTriggerApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()