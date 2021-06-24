from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout
from PySide6.QtCore import QRect
import config


class AboutCatDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.resize(470, 360)
        layout = QVBoxLayout(self)
        self.label = QLabel(self)
        self.label.setObjectName("cat")

        self.label.setGeometry(QRect(10, 10, 460, 370))
        aboutPath = config.APPLICATION_DIRNAME + "/icons/about.jpg"
        self.label.setPixmap(QPixmap(aboutPath))
        self.label.setText("")
        layout.addWidget(self.label)
        self.setWindowTitle("About Grading Cat")

    @staticmethod
    def show(parent):
        dialog = AboutCatDialog(parent)
        result = dialog.exec_()
        return result == QDialog.Accepted
