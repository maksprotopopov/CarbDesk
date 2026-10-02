from PySide6.QtWidgets import QApplication
import sys
from pathlib import Path

from main_window import MainWindow
from style_watcher import StyleWatcher

app = QApplication(sys.argv)

style_watcher = StyleWatcher(app)

window = MainWindow()
window.show()

sys.exit(app.exec())
