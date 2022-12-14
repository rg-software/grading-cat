from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QVBoxLayout
from PySide6.QtCore import QRect, Qt
from main_utils import appPath

# Cat picture source:
# http://blogs.reuters.com/oddly-enough/2007/10/11/just-too-obvious-cat-and-mouse/
# Zoe, a domestic shorthair cat, touches the mouse of a computer during a media
# preview for The Cat Fanciers’ Association’s championship in New York October 10, 2007.


class AboutCatDialogUi(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.resize(470, 360)
        layout = QVBoxLayout(self)
        self.label = QLabel(self)
        self.label.setObjectName("cat")

        self.label.setGeometry(QRect(10, 10, 460, 370))
        self.label.setPixmap(QPixmap(f"{appPath()}/icons/about.jpg"))
        self.label.setText("")
        layout.addWidget(self.label)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok, Qt.Horizontal, self)
        buttons.setCenterButtons(True)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)

        self.setWindowTitle("About Grading Cat")


class AboutCatDialog(AboutCatDialogUi):
    def __init__(self, parent):
        super().__init__(parent)

    @staticmethod
    def show(parent):
        dialog = AboutCatDialog(parent)
        result = dialog.exec_()
        return result == QDialog.Accepted
