from PySide6.QtCore import QFileSystemWatcher
from pathlib import Path


class StyleWatcher:
    def __init__(self, app):
        self.app = app

        self.style_path = Path(__file__).resolve().parent / "style.qss"

        self.watcher = QFileSystemWatcher()
        self.watcher.addPath(str(self.style_path))

        self.watcher.fileChanged.connect(self.reload_style)

        self.reload_style()

    def reload_style(self):
        with open(self.style_path, "r", encoding="utf-8") as file:
            self.app.setStyleSheet(file.read())
