# tray_launcher.py
import fcntl
import os
import subprocess
import sys
from pathlib import Path

from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QMenu, QSystemTrayIcon


class TodoTray:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.tray = QSystemTrayIcon()

        # Icon path relative to this file
        icon_path = Path(__file__).parent / "assets" / "checkbox.png"
        self.tray.setIcon(QIcon(str(icon_path)))

        menu = QMenu()
        open_action = QAction("Open Todo List")
        open_action.triggered.connect(self.open_todo)
        menu.addAction(open_action)

        quit_action = QAction("Quit")
        quit_action.triggered.connect(self.quit_app)
        menu.addAction(quit_action)

        self.tray.setContextMenu(menu)
        self.tray.show()
        self.tray.activated.connect(self.on_tray_click)

        self.lock_file = Path.home() / ".cache" / "hyprtodo-tray.lock"
        self.lock_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            self.lock_fd = open(self.lock_file, "w")
            fcntl.flock(self.lock_fd.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except IOError:
            print("Hyprtodo tray is already running!")
            sys.exit(1)

    def open_todo(self):
        # Get terminal from environment variable or use fallback
        terminal = os.environ.get("TERMINAL", "kitty")

        subprocess.Popen(
            [
                terminal,
                "-e",
                "--class",
                "hyprtodo",
                "python",
                "-m",
                "hyprtodo.hyprtodo",
            ]
        )

    def on_tray_click(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.open_todo()

    def run(self):
        sys.exit(self.app.exec())

    def quit_app(self):
        fcntl.flock(self.lock_fd.fileno(), fcntl.LOCK_UN)
        self.lock_fd.close()
        self.lock_file.unlink(missing_ok=True)
        self.app.quit()


def main():
    tray = TodoTray()
    tray.run()


if __name__ == "__main__":
    main()
