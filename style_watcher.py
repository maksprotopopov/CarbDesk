import sys

from PySide6.QtCore import QFileSystemWatcher

from utils import get_resource_path


class StyleWatcher:
    def __init__(self, app):
        self.app = app
        self.style_path = get_resource_path("style.qss")

        if not getattr(sys, "frozen", False):
            self.watcher = QFileSystemWatcher()
            self.watcher.addPath(str(self.style_path))
            self.watcher.fileChanged.connect(self.reload_style)

        self.reload_style()

    def reload_style(self):
        if not self.style_path.exists():
            return

        with open(self.style_path, "r", encoding="utf-8") as file:
            self.app.setStyleSheet(file.read())
