from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import *
from PySide6 import QtCore, QtGui
from PySide6.QtCore import *
from PySide6 import QtGui
from PySide6.QtGui import *
from operator import *
from ui_mainwindow import Ui_MainWindow
from diagrams import *
from lines import LinesView

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        
        self.ui.setupUi(self)    

        self.ui.actionSettings.setEnabled(True)
        self.ui.actionSettings.setEnabled(True)
        self.ui.actionSave_2.setEnabled(False)

        self.ui.actionSettings.setEnabled(False)
        self.ui.actionSync_with_Data_Source.setEnabled(False)
        self.ui.actionDetect.setEnabled(False)
                
        self.ui.actionQuit.setEnabled(True)
        
        #self.ui.actionSave.triggered.connect(saveDiagram)
        #self.ui.actionNew_Project.triggered.connect(project.newProject)
        #self.ui.actionNew_Detection_Session.triggered.connect(openNewSession)
        #self.ui.actionOpen_Project.triggered.connect(project.openProject)
        #self.ui.actionUpdate_Project_Data.triggered.connect(project.updateProjectData)
        #self.ui.actionExport_Template.triggered.connect(project.exportTemplate)
        #self.ui.actionDetecting_Software.triggered.connect(project.detectingSoftware)
        #self.ui.actionData_Source.triggered.connect(project.dataSource)
        #self.ui.actionImport_and_Export_Settings.triggered.connect(project.importExportSettings)
        #self.ui.actionOpen_Detection_Session.triggered.connect(openDiagram)            
        #self.ui.actionSave_as.triggered.connect(saveAsDiagram)
        #self.ui.actionClose.triggered.connect(closeDiagram)
        #width = 600 height = 700

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
        self.ui.tabWidget.addTab(self.tabChord, "")

        self.tabChord2 = QWidget()
        self.tabChord2.setObjectName("tabChord2")
        sizePolicy2.setHeightForWidth(self.tabChord2.sizePolicy().hasHeightForWidth())
        self.tabChord2.setSizePolicy(sizePolicy2)
        self.gridLayout_chord2 = QGridLayout(self.tabChord2)
        self.gridLayout_chord2.setObjectName("gridLayout_chord2")
        self.gridLayout_chord2.setContentsMargins(10, 10, 10, 12)
        self.ui.tabWidget.addTab(self.tabChord2, "")

        self.tabNetwork = QWidget()
        self.tabNetwork.setObjectName("tabNetwork")
        sizePolicy2.setHeightForWidth(self.tabNetwork.sizePolicy().hasHeightForWidth())
        self.tabNetwork.setSizePolicy(sizePolicy2)
        self.gridLayout_network = QGridLayout(self.tabNetwork)
        self.gridLayout_network.setObjectName("gridLayout_network")
        self.gridLayout_network.setContentsMargins(10, 10, 10, 12)
        self.ui.tabWidget.addTab(self.tabNetwork, "")

        self.tabBubble = QWidget()
        self.tabBubble.setObjectName("tabBubble")
        sizePolicy2.setHeightForWidth(self.tabBubble.sizePolicy().hasHeightForWidth())
        self.tabBubble.setSizePolicy(sizePolicy2)
        self.gridLayout_bubble = QGridLayout(self.tabBubble)
        self.gridLayout_bubble.setObjectName("gridLayout_bubble")
        self.gridLayout_bubble.setContentsMargins(10, 10, 10, 12)
        self.ui.tabWidget.addTab(self.tabBubble, "")

        self.tabLines = QWidget()
        self.tabLines.setObjectName("tabLines")
        sizePolicy2.setHeightForWidth(self.tabLines.sizePolicy().hasHeightForWidth())
        self.tabLines.setSizePolicy(sizePolicy2)
        self.gridLayout_lines = QGridLayout(self.tabLines)
        self.gridLayout_lines.setObjectName("gridLayout_lines")
        self.gridLayout_lines.setContentsMargins(10, 10, 10, 12)
        self.ui.tabWidget.addTab(self.tabLines, "")

        self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(self.tabChord), QCoreApplication.translate("MainWindow", "Chord diagram", None))
        self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(self.tabChord2), QCoreApplication.translate("MainWindow", "Chord diagram 2", None))
        self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(self.tabNetwork), QCoreApplication.translate("MainWindow", "Network", None))
        self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(self.tabBubble), QCoreApplication.translate("MainWindow", "Bubble chart", None))
        self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(self.tabLines), QCoreApplication.translate("MainWindow", "Lines", None))

        self.chordDiagramScene = GraphicsSceneChordDiagram()
        self.chordDiagram2Scene = GraphicsSceneChordDiagram2()
        self.networkScene = GraphicsSceneNetwork()
        self.bubbleChartScene = GraphicsSceneBubbleChart()
                
        self.ChordDiagramView = GraphicsView(self, self.chordDiagramScene)        
        self.ChordDiagram2View = GraphicsView(self, self.chordDiagram2Scene)        
        self.NetworkDiagramView = GraphicsView(self, self.networkScene)        
        self.BubbleDiagramView = GraphicsView(self, self.bubbleChartScene)

        self.gridLayout_chord.addWidget(self.ChordDiagramView, 10, 10)
        self.gridLayout_chord2.addWidget(self.ChordDiagram2View, 10, 10)
        self.gridLayout_network.addWidget(self.NetworkDiagramView, 10, 10)
        self.gridLayout_bubble.addWidget(self.BubbleDiagramView, 10, 10)

        self.linesView = LinesView(self)
        self.gridLayout_lines.addWidget(self.linesView, 10, 10)


