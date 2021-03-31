# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'vplag.ui'
##
## Created by: Qt User Interface Compiler version 6.0.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")

        MainWindow.setEnabled(True)
        MainWindow.resize(1040, 660)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(1040, 660))
        font = QFont()
        font.setFamily("Consolas")

        MainWindow.setFont(font)

        MainWindow.setStyleSheet(open("catStyle.qss", "r").read())

        MainWindow.setLocale(QLocale(QLocale.English, QLocale.World))
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        font1 = QFont()
        font1.setFamily("Consolas")
        font1.setPointSize(11)
        self.actionSave.setFont(font1)
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")

        self.actionQuit.setFont(font1)
        self.actionSave_as = QAction(MainWindow)
        self.actionSave_as.setObjectName("actionSave_as")

        self.actionSave_as.setFont(font1)
        self.actionAbout_VPlag = QAction(MainWindow)
        self.actionAbout_VPlag.setObjectName("actionAbout_VPlag")

        self.actionAbout_VPlag.setFont(font1)
        self.actionClose = QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")

        self.actionExport_Template = QAction(MainWindow)
        self.actionExport_Template.setObjectName("actionExport_Template")

        self.actionDetecting_Software = QAction(MainWindow)
        self.actionDetecting_Software.setObjectName("actionDetecting_Software")

        self.actionImport_and_Export_Settings = QAction(MainWindow)
        self.actionImport_and_Export_Settings.setObjectName("actionImport_and_Export_Settings")

        self.actionData_Source = QAction(MainWindow)
        self.actionData_Source.setObjectName("actionData_Source")

        self.actionUpdate_Project_Data = QAction(MainWindow)
        self.actionUpdate_Project_Data.setObjectName("actionUpdate_Project_Data")

        self.actionNew_Project = QAction(MainWindow)
        self.actionNew_Project.setObjectName("actionNew_Project")

        self.actionNew_Detection_Session = QAction(MainWindow)
        self.actionNew_Detection_Session.setObjectName("actionNew_Detection_Session")

        self.actionOpen_Project = QAction(MainWindow)
        self.actionOpen_Project.setObjectName("actionOpen_Project")

        self.actionOpen_Detection_Session = QAction(MainWindow)
        self.actionOpen_Detection_Session.setObjectName("actionOpen_Detection_Session")

        self.VPlagWidget = QWidget(MainWindow)
        self.VPlagWidget.setObjectName("VPlagWidget")

        self.VPlagWidget.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.VPlagWidget.sizePolicy().hasHeightForWidth())
        self.VPlagWidget.setSizePolicy(sizePolicy1)
        self.VPlagWidget.setMinimumSize(QSize(1040, 620))
        self.VPlagWidget.setFont(font)
#if QT_CONFIG(tooltip)
        self.VPlagWidget.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.gridLayout_3 = QGridLayout(self.VPlagWidget)
        self.gridLayout_3.setObjectName("gridLayout_3")

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName("gridLayout")

        self.gridLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout.setHorizontalSpacing(12)
        self.gridLayout.setContentsMargins(12, 6, 12, 6)
        self.tabWidget = QTabWidget(self.VPlagWidget)
        self.tabWidget.setObjectName("tabWidget")

        sizePolicy1.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy1)
        self.tabWidget.setMinimumSize(QSize(720, 600))
        self.tabWidget.setFont(font1)
        self.tabWidget.setStyleSheet("color: #656270;\n""background-color: rgb(234, 229, 226)\n""")

        self.tabChord = QWidget()
        self.tabChord.setObjectName("tabChord")

        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.tabChord.sizePolicy().hasHeightForWidth())
        self.tabChord.setSizePolicy(sizePolicy2)
        self.gridLayout_chord = QGridLayout(self.tabChord)
        self.gridLayout_chord.setObjectName("gridLayout_chord")

        self.gridLayout_chord.setContentsMargins(10, 10, 10, 12)
        self.tabWidget.addTab(self.tabChord, "")
        self.tabChord2 = QWidget()
        self.tabChord2.setObjectName("tabChord2")

        sizePolicy2.setHeightForWidth(self.tabChord2.sizePolicy().hasHeightForWidth())
        self.tabChord2.setSizePolicy(sizePolicy2)
        self.gridLayout_chord2 = QGridLayout(self.tabChord2)
        self.gridLayout_chord2.setObjectName("gridLayout_chord2")

        self.gridLayout_chord2.setHorizontalSpacing(6)
        self.gridLayout_chord2.setContentsMargins(10, 10, 10, 12)
        self.tabWidget.addTab(self.tabChord2, "")

        self.tabNetwork = QWidget()
        self.tabNetwork.setObjectName("tabNetwork")
        sizePolicy2.setHeightForWidth(self.tabNetwork.sizePolicy().hasHeightForWidth())
        self.tabNetwork.setSizePolicy(sizePolicy2)
        self.gridLayout_network = QGridLayout(self.tabNetwork)
        self.gridLayout_network.setObjectName("gridLayout_network")
        self.gridLayout_network.setContentsMargins(10, 10, 10, 12)
        self.tabWidget.addTab(self.tabNetwork, "")

        self.tabBubble = QWidget()
        self.tabBubble.setObjectName("tabBubble")
        sizePolicy2.setHeightForWidth(self.tabBubble.sizePolicy().hasHeightForWidth())
        self.tabBubble.setSizePolicy(sizePolicy2)
        self.gridLayout_bubble = QGridLayout(self.tabBubble)
        self.gridLayout_bubble.setObjectName("gridLayout_bubble")
        self.gridLayout_bubble.setContentsMargins(10, 10, 10, 12)
        self.tabWidget.addTab(self.tabBubble, "")

        self.tabLines = QWidget()
        self.tabLines.setObjectName("tabLines")
        sizePolicy2.setHeightForWidth(self.tabLines.sizePolicy().hasHeightForWidth())
        self.tabLines.setSizePolicy(sizePolicy2)
        self.gridLayout_lines = QGridLayout(self.tabLines)
        self.gridLayout_lines.setObjectName("gridLayout_lines")
        self.gridLayout_lines.setContentsMargins(10, 10, 10, 12)
        self.tabWidget.addTab(self.tabLines, "")


        self.gridLayout.addWidget(self.tabWidget, 0, 1, 1, 1)
        self.verticalLayoutMenu = QVBoxLayout()
        self.verticalLayoutMenu.setSpacing(6)
        self.verticalLayoutMenu.setObjectName("verticalLayoutMenu")

        self.label_Grading_Cat = QLabel(self.VPlagWidget)
        self.label_Grading_Cat.setObjectName("label_Grading_Cat")

        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_Grading_Cat.sizePolicy().hasHeightForWidth())
        self.label_Grading_Cat.setSizePolicy(sizePolicy3)
        font2 = QFont()
        font2.setFamily("Consolas")

        font2.setBold(True)
        font2.setItalic(False)
        self.label_Grading_Cat.setFont(font2)
        self.label_Grading_Cat.setStyleSheet("\n"
"   font-size: 22px;\n"
"	font-weight: bold;\n"
"    color: #fe9f9c; ")

        self.verticalLayoutMenu.addWidget(self.label_Grading_Cat)

        self.line_2 = QFrame(self.VPlagWidget)
        self.line_2.setObjectName("line_2")

        self.line_2.setMinimumSize(QSize(2, 2))
        self.line_2.setBaseSize(QSize(0, 2))
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.line_2.setLineWidth(0)
        self.line_2.setMidLineWidth(3)
        self.line_2.setFrameShape(QFrame.HLine)

        self.verticalLayoutMenu.addWidget(self.line_2)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")

        self.gridLayout_4.setHorizontalSpacing(10)
        self.gridLayout_4.setContentsMargins(-1, -1, -1, 10)
        self.sort = QCheckBox(self.VPlagWidget)
        self.sort.setObjectName("sort")

        self.sort.setTristate(False)

        self.gridLayout_4.addWidget(self.sort, 0, 1, 1, 1)

        self.label_2 = QLabel(self.VPlagWidget)
        self.label_2.setObjectName("label_2")

        font3 = QFont()
        font3.setFamily("Consolas")

        font3.setPointSize(11)
        font3.setBold(True)
        font3.setItalic(False)
        self.label_2.setFont(font3)

        self.gridLayout_4.addWidget(self.label_2, 0, 0, 1, 1)

        self.gridLayout_4.setColumnStretch(0, 3)
        self.gridLayout_4.setColumnStretch(1, 1)
        self.gridLayout_4.setColumnMinimumWidth(0, 2)
        self.gridLayout_4.setColumnMinimumWidth(1, 2)

        self.verticalLayoutMenu.addLayout(self.gridLayout_4)

        self.listStudents = QListWidget(self.VPlagWidget)
        self.listStudents.setObjectName("listStudents")

        self.listStudents.setFocusPolicy(Qt.StrongFocus)

        self.listStudents.setStyleSheet("color: #656270;\n"
"      background-color: #faf1ec")

        self.verticalLayoutMenu.addWidget(self.listStudents)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.horizontalLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.lineEdit = QLineEdit(self.VPlagWidget)
        self.lineEdit.setObjectName("lineEdit")

        self.lineEdit.setMaximumSize(QSize(16777215, 26))
        font4 = QFont()
        font4.setPointSize(11)
        self.lineEdit.setFont(font4)
        self.lineEdit.setStyleSheet("color: #656270;\n"
"background-color: #faf1ec")

        self.horizontalLayout_2.addWidget(self.lineEdit)

        self.toolButton_cancel = QToolButton(self.VPlagWidget)
        self.toolButton_cancel.setObjectName("toolButton_cancel")

        icon = QIcon()
        icon.addFile("icons/cancel.png", QSize(), QIcon.Normal, QIcon.Off)

        self.toolButton_cancel.setIcon(icon)
        self.toolButton_cancel.setIconSize(QSize(16, 16))

        self.horizontalLayout_2.addWidget(self.toolButton_cancel)

        self.toolButton_delete = QToolButton(self.VPlagWidget)
        self.toolButton_delete.setObjectName("toolButton_delete")

        icon1 = QIcon()
        icon1.addFile("icons/delete.png", QSize(), QIcon.Normal, QIcon.Off)

        self.toolButton_delete.setIcon(icon1)
        self.toolButton_delete.setIconSize(QSize(16, 16))

        self.horizontalLayout_2.addWidget(self.toolButton_delete)

        self.toolButton_closeEye = QToolButton(self.VPlagWidget)
        self.toolButton_closeEye.setObjectName("toolButton_closeEye")

        icon2 = QIcon()
        icon2.addFile("icons/closeEye.png", QSize(), QIcon.Normal, QIcon.Off)

        self.toolButton_closeEye.setIcon(icon2)
        self.toolButton_closeEye.setIconSize(QSize(16, 16))

        self.horizontalLayout_2.addWidget(self.toolButton_closeEye)

        self.toolButton_openEye = QToolButton(self.VPlagWidget)
        self.toolButton_openEye.setObjectName("toolButton_openEye")

        icon3 = QIcon()
        icon3.addFile("icons/openEye.png", QSize(), QIcon.Normal, QIcon.Off)

        self.toolButton_openEye.setIcon(icon3)
        self.toolButton_openEye.setIconSize(QSize(16, 16))

        self.horizontalLayout_2.addWidget(self.toolButton_openEye)


        self.verticalLayoutMenu.addLayout(self.horizontalLayout_2)

        self.Show = QCommandLinkButton(self.VPlagWidget)
        self.Show.setObjectName("Show")

        font5 = QFont()
        font5.setFamily("Segoe UI")

        font5.setPointSize(16)
        font5.setBold(True)
        self.Show.setFont(font5)
        self.Show.setStyleSheet("color: #f5eae9;")

        icon4 = QIcon()
        icon4.addFile("icons/Arrow.ico", QSize(), QIcon.Normal, QIcon.Off)

        self.Show.setIcon(icon4)
        self.Show.setIconSize(QSize(30, 30))

        self.verticalLayoutMenu.addWidget(self.Show)

        self.line = QFrame(self.VPlagWidget)
        self.line.setObjectName("line")

        self.line.setMinimumSize(QSize(0, 2))
        self.line.setLineWidth(0)
        self.line.setMidLineWidth(3)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayoutMenu.addWidget(self.line)

        self.label_Range = QLabel(self.VPlagWidget)
        self.label_Range.setObjectName("label_Range")

        self.label_Range.setFont(font3)

        self.verticalLayoutMenu.addWidget(self.label_Range)

        self.rangeSlider = QSlider(self.VPlagWidget)
        self.rangeSlider.setObjectName("rangeSlider")

        self.rangeSlider.setOrientation(Qt.Horizontal)

        self.verticalLayoutMenu.addWidget(self.rangeSlider)

        self.line_3 = QFrame(self.VPlagWidget)
        self.line_3.setObjectName("line_3")

        self.line_3.setMinimumSize(QSize(0, 2))
        self.line_3.setLineWidth(0)
        self.line_3.setMidLineWidth(3)
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayoutMenu.addWidget(self.line_3)

        self.label_3 = QLabel(self.VPlagWidget)
        self.label_3.setObjectName("label_3")

        self.label_3.setFont(font3)

        self.verticalLayoutMenu.addWidget(self.label_3)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.showRate = QCheckBox(self.VPlagWidget)
        self.showRate.setObjectName("showRate")

        font6 = QFont()
        font6.setFamily("Consolas")

        font6.setPointSize(9)
        self.showRate.setFont(font6)

        self.gridLayout_2.addWidget(self.showRate, 1, 0, 1, 1)

        self.showNames = QCheckBox(self.VPlagWidget)
        self.showNames.setObjectName("showNames")

        self.showNames.setEnabled(True)
        self.showNames.setFont(font6)
        self.showNames.setChecked(True)

        self.gridLayout_2.addWidget(self.showNames, 1, 1, 1, 1)

        self.showLinkless = QCheckBox(self.VPlagWidget)
        self.showLinkless.setObjectName("showLinkless")

        self.showLinkless.setFont(font6)
        self.showLinkless.setChecked(True)

        self.gridLayout_2.addWidget(self.showLinkless, 0, 0, 1, 1)

        self.chess = QCheckBox(self.VPlagWidget)
        self.chess.setObjectName("chess")

        self.chess.setFont(font6)

        self.gridLayout_2.addWidget(self.chess, 0, 1, 1, 1)


        self.verticalLayoutMenu.addLayout(self.gridLayout_2)

        self.line_4 = QFrame(self.VPlagWidget)
        self.line_4.setObjectName("line_4")

        self.line_4.setMinimumSize(QSize(0, 2))
        self.line_4.setLineWidth(0)
        self.line_4.setMidLineWidth(2)
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.verticalLayoutMenu.addWidget(self.line_4)

        self.verticalLayoutMenu.setStretch(0, 1)
        self.verticalLayoutMenu.setStretch(3, 5)
        self.verticalLayoutMenu.setStretch(5, 1)
        self.verticalLayoutMenu.setStretch(6, 1)
        self.verticalLayoutMenu.setStretch(12, 2)

        self.gridLayout.addLayout(self.verticalLayoutMenu, 0, 0, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.VPlagWidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")

        self.menubar.setGeometry(QRect(0, 0, 1040, 19))
        font7 = QFont()
        font7.setFamily("Consolas")

        font7.setPointSize(10)
        font7.setBold(True)
        font7.setItalic(False)
        self.menubar.setFont(font7)
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")

        self.menuNew = QMenu(self.menuFile)
        self.menuNew.setObjectName("menuNew")

        self.menuOpen = QMenu(self.menuFile)
        self.menuOpen.setObjectName("menuOpen")

        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")

        self.menuProject = QMenu(self.menubar)
        self.menuProject.setObjectName("menuProject")

        self.menuProject_settings = QMenu(self.menuProject)
        self.menuProject_settings.setObjectName("menuProject_settings")

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuProject.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.menuNew.menuAction())
        self.menuFile.addAction(self.menuOpen.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_as)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuNew.addAction(self.actionNew_Project)
        self.menuNew.addAction(self.actionNew_Detection_Session)
        self.menuOpen.addAction(self.actionOpen_Project)
        self.menuOpen.addAction(self.actionOpen_Detection_Session)
        self.menuHelp.addAction(self.actionAbout_VPlag)
        self.menuProject.addAction(self.menuProject_settings.menuAction())
        self.menuProject.addAction(self.actionUpdate_Project_Data)
        self.menuProject.addAction(self.actionExport_Template)
        self.menuProject_settings.addAction(self.actionDetecting_Software)
        self.menuProject_settings.addAction(self.actionData_Source)
        self.menuProject_settings.addSeparator()
        self.menuProject_settings.addAction(self.actionImport_and_Export_Settings)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "Grading Cat", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", "Save", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", "Quit", None))
        self.actionSave_as.setText(QCoreApplication.translate("MainWindow", "Save as...", None))
        self.actionAbout_VPlag.setText(QCoreApplication.translate("MainWindow", "About Grading Cat", None))
        self.actionClose.setText(QCoreApplication.translate("MainWindow", "Close", None))
        self.actionExport_Template.setText(QCoreApplication.translate("MainWindow", "Export Template", None))
        self.actionDetecting_Software.setText(QCoreApplication.translate("MainWindow", "Detecting Software", None))
        self.actionImport_and_Export_Settings.setText(QCoreApplication.translate("MainWindow", "Import and Export Settings", None))
        self.actionData_Source.setText(QCoreApplication.translate("MainWindow", "Data Source", None))
        self.actionUpdate_Project_Data.setText(QCoreApplication.translate("MainWindow", "Update Project Data", None))
        self.actionNew_Project.setText(QCoreApplication.translate("MainWindow", "New Project", None))
        self.actionNew_Detection_Session.setText(QCoreApplication.translate("MainWindow", "New Detection Session\n"
"", None))
        self.actionOpen_Project.setText(QCoreApplication.translate("MainWindow", "Open Project", None))
        self.actionOpen_Detection_Session.setText(QCoreApplication.translate("MainWindow", "Open Detection Session\n"
"", None))
#if QT_CONFIG(statustip)
        self.VPlagWidget.setStatusTip("")
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.VPlagWidget.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
#if QT_CONFIG(accessibility)
        self.VPlagWidget.setAccessibleName("")
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.VPlagWidget.setAccessibleDescription("")
#endif // QT_CONFIG(accessibility)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabChord), QCoreApplication.translate("MainWindow", "Chord diagram", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabChord2), QCoreApplication.translate("MainWindow", "Chord diagram 2", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabNetwork), QCoreApplication.translate("MainWindow", "Network", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabBubble), QCoreApplication.translate("MainWindow", "Bubble chart", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabLines), QCoreApplication.translate("MainWindow", "Lines", None))
        self.label_Grading_Cat.setText(QCoreApplication.translate("MainWindow", "Grading Cat", None))
        self.sort.setText(QCoreApplication.translate("MainWindow", "Sort", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", "Students", None))
        self.toolButton_cancel.setText(QCoreApplication.translate("MainWindow", "...", None))
        self.toolButton_delete.setText(QCoreApplication.translate("MainWindow", "...", None))
        self.toolButton_closeEye.setText(QCoreApplication.translate("MainWindow", "...", None))
        self.toolButton_openEye.setText(QCoreApplication.translate("MainWindow", "...", None))
        self.Show.setText(QCoreApplication.translate("MainWindow", "Show", None))
        self.label_Range.setText(QCoreApplication.translate("MainWindow", "Range", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", "Settings", None))
        self.showRate.setText(QCoreApplication.translate("MainWindow", "Plagiarism rate", None))
        self.showNames.setText(QCoreApplication.translate("MainWindow", "Student names", None))
        self.showLinkless.setText(QCoreApplication.translate("MainWindow", "Linkless nodes", None))
        self.chess.setText(QCoreApplication.translate("MainWindow", "Chess view", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", "File", None))
        self.menuNew.setTitle(QCoreApplication.translate("MainWindow", "New", None))
        self.menuOpen.setTitle(QCoreApplication.translate("MainWindow", "Open", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", "Help", None))
        self.menuProject.setTitle(QCoreApplication.translate("MainWindow", "Project", None))
        self.menuProject_settings.setTitle(QCoreApplication.translate("MainWindow", "Project Settings", None))
    # retranslateUi

