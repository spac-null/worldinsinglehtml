import cv2
import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore
import sys

class BlobTriggerApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blob Trigger Interactive")
        self.setGeometry(100, 100, 1280, 720)

        # Video capture
        self.cap = cv2.VideoCapture(0)  # Use default webcam
        if not self.cap.isOpened():
            raise RuntimeError("Cannot open webcam")

        # Widget setup
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QtWidgets.QHBoxLayout(self.central_widget)

        # Left: Video feed
        self.video_label = QtWidgets.QLabel()
        self.video_label.setFixedSize(640, 480)
        self.layout.addWidget(self.video_label)

        # Right: Blob effect
        self.blob_label = QtWidgets.QLabel()
        self.blob_label.setFixedSize(640, 480)
        self.blob_label.setStyleSheet("background-color: black;")
        self.layout.addWidget(self.blob_label)

        # Controls
        self.controls_widget = QtWidgets.QWidget()
        self.controls_layout = QtWidgets.QVBoxLayout(self.controls_widget)
        self.layout.addWidget(self.controls_widget)

        # Threshold slider
        self.threshold_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.threshold_slider.setRange(10, 255)
        self.threshold_slider.setValue(50)
        self.threshold_slider.valueChanged.connect(self.update_frame)
        self.controls_layout.addWidget(QtWidgets.QLabel("Threshold"))
        self.controls_layout.addWidget(self.threshold_slider)

        # Blur slider
        self.blur_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.blur_slider.setRange(1, 31)
        self.blur_slider.setValue(5)
        self.blur_slider.setSingleStep(2)
        self.blur_slider.valueChanged.connect(self.update_frame)
        self.controls_layout.addWidget(QtWidgets.QLabel("Blur Size"))
        self.controls_layout.addWidget(self.blur_slider)

        # Blob size slider
        self.blob_size_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.blob_size_slider.setRange(5, 100)
        self.blob_size_slider.setValue(20)
        self.blob_size_slider.valueChanged.connect(self.update_frame)
        self.controls_layout.addWidget(QtWidgets.QLabel("Blob Size"))
        self.controls_layout.addWidget(self.blob_size_slider)

        # Background for motion detection
        self.background = None
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Update every ~33ms (~30 FPS)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        # Resize frame to match display
        frame = cv2.resize(frame, (640, 480))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Initialize background
        if self.background is None:
            self.background = gray.astype("float")
            return

        # Parameters from sliders
        threshold = self.threshold_slider.value()
        blur_size = self.blur_slider.value() | 1  # Ensure odd number
        blob_size = self.blob_size_slider.value()

        # Motion detection
        cv2.accumulateWeighted(gray, self.background, 0.5)
        diff = cv2.absdiff(gray, cv2.convertScaleAbs(self.background))
        blur = cv2.GaussianBlur(diff, (blur_size, blur_size), 0)
        _, thresh = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY)

        # Blob detection
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        blob_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.line(blob_frame, (320, 0), (320, 480), (255, 255, 255), 2)  # Vertical line

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest_contour) > 500:  # Minimum area filter
                M = cv2.moments(largest_contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    # Draw blob effect
                    cv2.circle(blob_frame, (cx, cy), blob_size, (0, 255, 255), -1)  # Yellow blob

        # Display video feed
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        qt_image = QtGui.QImage(rgb_frame.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        self.video_label.setPixmap(QtGui.QPixmap.fromImage(qt_image))

        # Display blob effect
        h, w, ch = blob_frame.shape
        bytes_per_line = ch * w
        qt_blob_image = QtGui.QImage(blob_frame.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        self.blob_label.setPixmap(QtGui.QPixmap.fromImage(qt_blob_image))

    def closeEvent(self, event):
        self.cap.release()
        event.accept()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = BlobTriggerApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()