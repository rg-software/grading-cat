from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QDialogButtonBox, QWidget
from PySide6.QtCore import Qt, QDateTime
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class NumberOfNodesDialog(QDialog):
    def __init__(self, parent):
        super(NumberOfNodesDialog, self).__init__(parent)        
        self.number = 4

        #layout = QVBoxLayout(self)
        self.gridLayout_Dialog = QGridLayout(self)
        self.gridLayout = QGridLayout()
        font = QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)

        labelPlease = QLabel(self)
        labelName = "Please_"
        labelPlease.setObjectName(labelName)
        labelPlease.setMinimumSize(QSize(200, 50)) #?
        labelPlease.setMaximumSize(QSize(200, 50))
        self.gridLayout.addWidget(labelPlease, 0, 0, 1, 1)
        labelPlease.setFont(font)
        labelPlease.setText(QCoreApplication.translate("Dialog", "Please enter the expected\nnumber of nodes", None))
                           
        self.horizontalSpacer = QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(self.horizontalSpacer, 0, 1, 1, 1)
        
        
        font.setPointSize(14)
        
        self.spinBox = QSpinBox(self)
        self.spinBox.setFont(font)
        self.spinBox.setObjectName("spinBox")
        self.spinBox.setMinimum(2)
        self.spinBox.setMaximum(24)
        self.spinBox.setValue(5)
        self.spinBox.setMinimumSize(QSize(60, 40)) #?
        self.spinBox.setMaximumSize(QSize(60, 40))
        self.gridLayout.addWidget(self.spinBox, 0, 2, 1, 1)

        self.gridLayout_Dialog.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.verticalSpacer = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout_Dialog.addItem(self.verticalSpacer, 1, 0, 1, 1)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.gridLayout_Dialog.addWidget(self.buttonBox, 2, 0, 1, 1)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.setWindowTitle('Number of nodes')


    def _saveValues(self):
        self.number = self.spinBox.value()


    @staticmethod
    def show(parent):
        dialog = NumberOfNodesDialog(parent)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            dialog._saveValues()
        return result == QDialog.Accepted, dialog.number
