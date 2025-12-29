import sys
import ctypes
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from UI.main_window import MainWindow

# Fix for Windows Taskbar Icon
try:
    myappid = 'posture.monitor.v1'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass

app = QApplication(sys.argv)

# Application-wide Icon
app.setWindowIcon(QIcon("ui/images/app_icon.png"))

# Load Stylesheet
qss_path = Path(__file__).parent / "UI" / "styles.qss"
with open(qss_path, "r") as f:
    app.setStyleSheet(f.read())
    
window = MainWindow()
window.show()

sys.exit(app.exec())