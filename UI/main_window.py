from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QStyle
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QImage, QIcon
import cv2
import time

from posture.detector import PostureDetector

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Posture Monitor")
        self.setFixedSize(480, 400)
        
        # Set Window Icon
        self.setWindowIcon(QIcon("ui/images/app_icon.png"))

        # ---- UI ELEMENTS ----
        self.title = QLabel("Posture Monitor")
        self.title.setObjectName("title")

        self.timer_label = QLabel("00:00")
        self.timer_label.setObjectName("timer")

        self.status_label = QLabel("Good posture")
        self.status_label.setObjectName("statusGood")
        self.status_label.setAlignment(Qt.AlignCenter)

        self.camera = QLabel()
        self.camera.setObjectName("camera_display")
        self.camera.setFixedSize(280, 210)
        self.camera.setAlignment(Qt.AlignCenter)

        self.avatar = QLabel()
        self.avatar.setFixedSize(100, 140)
        self.update_avatar(True)

        # ---- LAYOUTS ----
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Top Bar (Title and Timer)
        top = QHBoxLayout()
        top.addWidget(self.title)
        top.addStretch()
        top.addWidget(self.timer_label)

        # Middle Section (Camera and Avatar)
        middle = QHBoxLayout()
        middle.setSpacing(15)
        middle.addWidget(self.camera)
        middle.addWidget(self.avatar)

        main_layout.addLayout(top)
        main_layout.addLayout(middle)
        main_layout.addWidget(self.status_label)

        # ---- LOGIC ----
        self.cap = cv2.VideoCapture(0)
        self.detector = PostureDetector()
        self.start_time = time.time()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_avatar(self, good: bool):
        path = "ui/images/good_posture.png" if good else "ui/images/bad_posture.png"
        pixmap = QPixmap(path)
        if not pixmap.isNull():
            self.avatar.setPixmap(pixmap.scaled(100, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret: return

        posture = self.detector.process(frame)

        # Update Visual State and trigger QSS refresh
        new_id = "statusBad" if posture == "bad" else "statusGood"
        if self.status_label.objectName() != new_id:
            self.status_label.setObjectName(new_id)
            self.status_label.setText("Bad posture" if posture == "bad" else "Good posture")
            self.update_avatar(posture == "good")
            
            # Force CSS update
            self.status_label.style().unpolish(self.status_label)
            self.status_label.style().polish(self.status_label)

        # Timer Update
        elapsed = int(time.time() - self.start_time)
        self.timer_label.setText(f"{elapsed//60:02d}:{elapsed%60:02d}")

        # Camera Display
        frame = cv2.resize(frame, (280, 210))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        img = QImage(frame.data, w, h, ch * w, QImage.Format_RGB888)
        self.camera.setPixmap(QPixmap.fromImage(img))