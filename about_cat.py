from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QDialogButtonBox, QWidget
from PySide6.QtCore import Qt, QDateTime
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import config

class AboutCatDialog(QDialog):
    def __init__(self, parent):
        super(AboutCatDialog, self).__init__(parent)

        self.resize(470, 360)
        layout = QVBoxLayout(self)
        self.label = QLabel(self)
        self.label.setObjectName("cat")

        self.label.setGeometry(QRect(10, 10, 460, 370))
        aboutPath = config.APPLICATION_DIRNAME + "/icons/about.jpg"
        self.label.setPixmap(QPixmap(aboutPath))
        self.label.setText("")
        layout.addWidget(self.label)
        self.setWindowTitle('About Grading Cat')

        #self.retranslateUi(self)
        #QMetaObject.connectSlotsByName(self)

    # setupUi
    #def retranslateUi(self, Dialog):
        #Dialog.setWindowTitle(QCoreApplication.translate("About_Grading_Cat", "About Grading Cat", None))
        #self.label.setText("")
    # retranslateUi    

   # def showImage(self):        

    @staticmethod
    def show(parent):
        dialog = AboutCatDialog(parent)
        result = dialog.exec_()
        return result == QDialog.Accepted