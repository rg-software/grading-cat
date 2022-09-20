import sys, pathlib, subprocess
from PySide6.QtWidgets import QApplication

if not (pathlib.Path("gui") / "ui_mainwindow.py").exists():
    subprocess.run(["pyside6-uic", "vplag.ui", "-o", "gui/ui_mainwindow.py"])

from gui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
