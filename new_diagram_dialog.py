from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QDialogButtonBox, QWidget
from PySide6.QtCore import Qt, QDateTime
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class NewDiagramDialog(QDialog):
    def __init__(self, parent, n):
        super(NewDiagramDialog, self).__init__(parent)        
        self.n = n
        self.matrix = []
        self.names = []
        for i in range(n):
            name = "node_" + str(i) 
            self.names.append(name)
            line = []
            for j in range(n): 
                line.append(int(0))
            self.matrix.append(line)

        #layout = QVBoxLayout(self)
        self.gridLayout_Dialog = QGridLayout(self)
        self.gridLayout_Dialog.setContentsMargins(20, 20, 20, 20);
        self.gridLayout = QGridLayout()
        self.matrix_lines = []
        self.name_lines_text = []
        self.name_lines_edit = []
        label = QLabel(self)
        label.setObjectName("Nodes")
        self.gridLayout.addWidget(label, 0, 0, 1, 1)
        label.setText(QCoreApplication.translate("Dialog", "Nodes", None))

        w, h = (50, 50)
        if n > 16: h = 20

        font = QFont()
        font.setFamily("Consolas")
        

        for i in range(n):  
            font.setPointSize(9)
            labelNodeName = QLabel(self)
            labelName = "NodeName_" + str(i)
            labelNodeName.setObjectName(labelName)
            labelNodeName.setMinimumSize(QSize(w, h)) #?
            labelNodeName.setMaximumSize(QSize(w, h))
            labelNodeName.setFont(font)
            self.name_lines_text.append(labelNodeName)
            self.gridLayout.addWidget(labelNodeName, 0, i + 2, 1, 1)
            labelNodeName.setText(QCoreApplication.translate("Dialog", self.names[i], None))


            lineEdit_NodeName = QLineEdit(self)
            lineEdit_NodeName.setMinimumSize(QSize(w*2, h)) #?
            lineEdit_NodeName.setMaximumSize(QSize(w*2, h))
            lineEdit_NodeName.setMaxLength(12)
            lineEdit_NodeName.textChanged.connect(self.changeName)
            nodeName = "NodeName_" + str(i)
            lineEdit_NodeName.setObjectName(nodeName)
            lineEdit_NodeName.setFont(font)
            self.name_lines_edit.append(lineEdit_NodeName)
            self.gridLayout.addWidget(self.name_lines_edit[i], i + 1, 0, 1, 1) 
            
            self.name_lines_edit[i].setText(QCoreApplication.translate("Dialog", self.names[i], None))

            self.horizontalSpacer = QSpacerItem(15, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
            self.gridLayout.addItem(self.horizontalSpacer, i + 1, 1, 1, 1)

            for j in range(n):
                #hm...
                if j < i:                  
                    font.setPointSize(12)
                    lineEdit = QLineEdit(self)
                    self.onlyInt = QIntValidator()
                    lineEdit.setValidator(self.onlyInt)
                    lineEdit.setFont(font)
                    lineEdit.setMinimumSize(QSize(w, h))
                    lineEdit.setMaximumSize(QSize(w, h))
                    lineEdit.setMaxLength(3)
                    lineName = "lineEdit_" + str(i) + str(j)
                    lineEdit.setObjectName(lineName)
                    self.matrix_lines.append([lineEdit, (i, j)])
                    self.gridLayout.addWidget(self.matrix_lines[-1][0], i + 1, j + 2, 1, 1)

                    self.matrix_lines[-1][0].setText(QCoreApplication.translate("Dialog", str(self.matrix[i][j]), None))


        self.gridLayout_Dialog.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.verticalSpacer = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout_Dialog.addItem(self.verticalSpacer, 1, 0, 1, 1)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.gridLayout_Dialog.addWidget(self.buttonBox, 2, 0, 1, 1)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.setWindowTitle('Weights matrix')


    def changeName(self, text):           
        for i in range(len(self.name_lines_edit)):
            if self.name_lines_edit[i].text() == text:
                if len(text) > 6: text = text[:6] + '\n' + text[6:]
                self.name_lines_text[i].setText(text)

        pass

    def _addLineEditWithLabel(self, layout, label, line_edit_name):
        new_layout = QHBoxLayout()
        new_layout.addWidget(QLabel(label))
        new_layout.addWidget(QLineEdit(self, objectName = line_edit_name))
        e = QWidget(self)
        e.setLayout(new_layout)
        layout.addWidget(e)


    def _saveValues(self):
        for x in range(len(self.matrix_lines)):
            i, j = self.matrix_lines[x][1]
            value = int(self.matrix_lines[x][0].text())

            self.matrix[i][j] = self.matrix[j][i] = value

        for i in range(len(self.name_lines_edit)):
            self.names[i] = self.name_lines_edit[i].text()

        pass

    @staticmethod
    def show(parent, n):
        dialog = NewDiagramDialog(parent, n)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            dialog._saveValues()
        return result == QDialog.Accepted, dialog.matrix, dialog.names
