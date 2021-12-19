from PySide6.QtCore import QMetaObject, QUrl, Qt
from PySide6.QtWidgets import (
    QVBoxLayout,
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QSizePolicy,
)
from PySide6.QtWidgets import QFrame, QGridLayout, QLabel, QTextBrowser
from PySide6.QtWebEngineWidgets import QWebEngineView


class MatchViewerDialog(QDialog):
    def __init__(self, parent, student_1, student_2, html_path):
        super(MatchViewerDialog, self).__init__(parent)

        # sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        # self.setSizePolicy(sizePolicy)
        self.setWindowTitle(f"{student_1} vs {student_2} ({html_path})")

        self.verticalLayout_2 = QVBoxLayout(self)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.textBrowser = QWebEngineView(self)
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setUrl(QUrl.fromLocalFile(html_path))
        # self.textBrowser.setSource(QUrl.fromLocalFile(html_path))

        self.verticalLayout_2.addWidget(self.textBrowser)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout_2.addWidget(self.buttonBox)

        # self.student_1 = student_1
        # self.student_2 = student_2

        # self.gridLayout_Dialog = QGridLayout(self)
        # self.gridLayout_Dialog.setContentsMargins(20, 20, 20, 20)

        # self.gridLayout_Dialog.setObjectName("dialog_frame")

        # self.gridLayoutSettings = QGridLayout()
        # self.gridLayoutSettings.setObjectName("settings_frame")

        # self.textBrowser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # self.gridLayout_Dialog.addWidget(self.textBrowser, 1, 0, 1, 1)

        # self.labelStudentsID = QLabel(self)
        # self.labelStudentsID.setObjectName("ID")
        # students = "Matches for\n" + student_1 + " & " + student_2
        # self.labelStudentsID.setText(students)

        # self.gridLayoutSettings.addWidget(self.labelStudentsID, 0, 0, 1, 1)

        # self.line = QFrame(self)
        # self.line.setObjectName("line")
        # self.line.setFrameShape(QFrame.HLine)
        # self.line.setFrameShadow(QFrame.Sunken)

        # self.gridLayoutSettings.addWidget(self.line, 1, 0, 1, 1)

        # self.label = QLabel(self)
        # self.label.setObjectName("label")
        # self.label.setText("Settings")

        # self.gridLayoutSettings.addWidget(self.label, 2, 0, 1, 1)

        # self.some_settings_1 = QCheckBox(self)
        # self.some_settings_1.setObjectName("checkBox_1")
        # self.some_settings_1.setText("Some settings")

        # self.gridLayoutSettings.addWidget(self.some_settings_1, 3, 0, 1, 1)

        # self.some_settings_2 = QCheckBox(self)
        # self.some_settings_2.setObjectName("checkBox_2")
        # self.some_settings_2.setText("Maybe you need some")

        # self.gridLayoutSettings.addWidget(self.some_settings_2, 4, 0, 1, 1)

        # self.some_settings_3 = QCheckBox(self)
        # self.some_settings_3.setObjectName("checkBox_3")
        # self.some_settings_3.setText("I don't know")

        # self.gridLayoutSettings.addWidget(self.some_settings_3, 5, 0, 1, 1)

        # self.line_2 = QFrame(self)
        # self.line_2.setObjectName("line_2")
        # self.line_2.setFrameShape(QFrame.HLine)
        # self.line_2.setFrameShadow(QFrame.Sunken)

        # self.gridLayoutSettings.addWidget(self.line_2, 6, 0, 1, 1)

        # self.buttonBox = QDialogButtonBox(self)
        # self.buttonBox.setObjectName("buttonBox")
        # self.buttonBox.setOrientation(Qt.Vertical)
        # self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        # self.gridLayoutSettings.addWidget(self.buttonBox, 7, 0, 1, 1)

        # self.line_3 = QFrame(self)
        # self.line_3.setObjectName("line_3")
        # self.line_3.setFrameShape(QFrame.HLine)
        # self.line_3.setFrameShadow(QFrame.Sunken)

        # self.gridLayoutSettings.addWidget(self.line_3, 8, 0, 1, 1)

        # self.gridLayout_Dialog.addLayout(self.gridLayoutSettings, 1, 1, 1, 1)

        self.buttonBox.accepted.connect(self.accept)
        # self.buttonBox.rejected.connect(self.reject)

        QMetaObject.connectSlotsByName(self)

    @staticmethod
    def show(parent, student_1, student_2, html_path):

        dialog = MatchViewerDialog(parent, student_1, student_2, html_path)
        dialog.showMaximized()
        dialog.open()
        # result = dialog.exec()
        # return result == QDialog.Accepted
