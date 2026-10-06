import sys
from pathlib import Path


def get_app_data_path():
    if sys.platform == "win32":
        return Path.home() / "AppData" / "Local" / "LocalMind"

    elif sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "LocalMind"

    else:
        return Path.home() / ".local" / "share" / "LocalMind"


def get_resource_path(filename):
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS) / filename

    return Path(__file__).parent / filename
