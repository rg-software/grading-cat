import types
import sys
import os
from operator import itemgetter

from PySide6.QtGui import QColor, QIcon
from PySide6.QtWidgets import QFileDialog, QGridLayout, QInputDialog
from PySide6.QtWidgets import QMainWindow, QProgressDialog, QSizePolicy, QWidget
from PySide6 import QtCore
from PySide6.QtCore import QCoreApplication

from gui.diagrams import GraphicsSceneChordDiagram, GraphicsSceneChordDiagram2
from gui.diagrams import GraphicsSceneNetwork, GraphicsView, findMaxPlag
from gui.project_config_editor import ProjectConfigDialog
from gui.new_diagram_dialog import NewDiagramDialog
from gui.number_of_nodes import NumberOfNodesDialog
from gui.ui_mainwindow import Ui_MainWindow
from gui.about_cat import AboutCatDialog
from gui.lines import LinesView
from main_utils import newSessionDiagram, expandMatrix, saveMatrix, appPath
from .match_viewer import MatchViewerDialog
import config
import project


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)
        self.setWindowIcon(QIcon("icons/cat.png"))

        self.ui.actionSettings.setEnabled(True)
        self.ui.actionSettings.setEnabled(True)

        self.ui.actionSettings.setEnabled(False)
        self.ui.actionSync_with_Data_Source.setEnabled(False)
        self.ui.actionDetect.setEnabled(False)

        self.ui.actionQuit.setEnabled(True)

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

        self.ui.tabWidget.setTabText(
            self.ui.tabWidget.indexOf(self.tabChord),
            QCoreApplication.translate("MainWindow", "Chord diagram", None),
        )
        self.ui.tabWidget.setTabText(
            self.ui.tabWidget.indexOf(self.tabChord2),
            QCoreApplication.translate("MainWindow", "Chord diagram 2", None),
        )
        self.ui.tabWidget.setTabText(
            self.ui.tabWidget.indexOf(self.tabNetwork),
            QCoreApplication.translate("MainWindow", "Network", None),
        )

        self.chordDiagramScene = GraphicsSceneChordDiagram()
        self.chordDiagram2Scene = GraphicsSceneChordDiagram2()
        self.networkScene = GraphicsSceneNetwork()

        self.ChordDiagramView = GraphicsView(self, self.chordDiagramScene)
        self.ChordDiagram2View = GraphicsView(self, self.chordDiagram2Scene)
        self.NetworkDiagramView = GraphicsView(self, self.networkScene)

        self.gridLayout_chord.addWidget(self.ChordDiagramView, 10, 10)
        self.gridLayout_chord2.addWidget(self.ChordDiagram2View, 10, 10)
        self.gridLayout_network.addWidget(self.NetworkDiagramView, 10, 10)

        #### LINES ####

        self.tabLines = QWidget()
        self.tabLines.setObjectName("tabLines")
        sizePolicy2.setHeightForWidth(self.tabLines.sizePolicy().hasHeightForWidth())
        self.tabLines.setSizePolicy(sizePolicy2)
        self.gridLayout_lines = QGridLayout(self.tabLines)
        self.gridLayout_lines.setObjectName("gridLayout_lines")
        self.gridLayout_lines.setContentsMargins(10, 10, 10, 12)
        self.ui.tabWidget.addTab(self.tabLines, "")

        self.ui.tabWidget.setTabText(
            self.ui.tabWidget.indexOf(self.tabLines),
            QCoreApplication.translate("MainWindow", "Lines", None),
        )

        self.linesView = LinesView(self)
        self.gridLayout_lines.addWidget(self.linesView, 10, 10)

        self._PROJECT_OPENED_ITEMS = [
            ("actionSettings", True),
            ("actionSync_with_Data_Source", True),
            ("actionDetect", True),
        ]
        #### CONNECTORS
        self.ui.actionNew_Project_2.triggered.connect(self.newProject)
        # self.ui.actionOpen_Project_2.triggered.connect(self.openProject)
        self.ui.actionSettings.triggered.connect(self.editSettings)
        self.ui.actionSync_with_Data_Source.triggered.connect(self.syncWithDataSource)
        self.ui.actionDetect.triggered.connect(self.openNewSession)
        self.ui.actionQuit.triggered.connect(self.close)

        # self.ui.actionAbout_Grading_Cat.triggered.connect(self.aboutGradingCat)

        self.ui.showNames.stateChanged.connect(self.updateDiagram)
        self.ui.showLinkless.stateChanged.connect(self.updateDiagram)
        self.ui.showRate.stateChanged.connect(self.updateDiagram)
        self.ui.chess.stateChanged.connect(self.updateDiagram)
        self.ui.sort.stateChanged.connect(self.updateDiagram)

        self.ui.listStudents.itemClicked.connect(self.selectedStudent)
        self.ui.lineEdit.setToolTip("Enter student ID to select")
        self.ui.ShowButton.clicked.connect(self.findStudent)
        self.ui.ShowButton.setToolTip("No one selected")
        self.ui.toolButton_cancel.clicked.connect(self.clearLine)
        self.ui.toolButton_cancel.setToolTip("Cancel")
        self.ui.toolButton_delete.clicked.connect(self.deleteStudent)
        self.ui.toolButton_delete.setToolTip("Delete")

        self.ui.toolButton_openEye.clicked.connect(self.exposeStudent)
        self.ui.toolButton_openEye.setToolTip("Expose")

        openEyePath = f"{appPath()}/icons/openEye.png"
        self.ui.toolButton_openEye.setIcon(QIcon(openEyePath))

        self.ui.toolButton_closeEye.clicked.connect(self.hideStudent)
        self.ui.toolButton_closeEye.setToolTip("Hide")
        closeEyePath = f"{appPath()}/icons/closeEye.png"
        self.ui.toolButton_closeEye.setIcon(QIcon(closeEyePath))

        self.ui.resetButton.clicked.connect(self.resetSettings)
        self.ui.resetButton.setToolTip("Reset settings")

        self.ui.rangeSlider.valueChanged.connect(self.updateDiagram)
        rangeLabel = f"Range:  > {self.ui.rangeSlider.value()}%"
        self.ui.label_Range.setText(rangeLabel)

        self.chordDiagramScene.signal.update.connect(self.updateDiagram)
        self.chordDiagramScene.signal.clear.connect(self.clearLine)

        self.chordDiagram2Scene.signal.update.connect(self.updateDiagram)
        self.chordDiagram2Scene.signal.clear.connect(self.clearLine)

        self.networkScene.signal.update.connect(self.updateDiagram)
        self.networkScene.signal.clear.connect(self.clearLine)

        self.ui.actionNew.triggered.connect(self.newDiagram)
        self.ui.actionOpen.triggered.connect(self.openDiagram)
        self.ui.actionSave.triggered.connect(self.saveDiagram)
        self.ui.actionSave_as.triggered.connect(self.save_asDiagram)
        self.ui.actionClose.triggered.connect(self.closeDiagram)

        self._updateTitle(None)  # no project loaded

    def newDiagram(self):
        isOk, n = NumberOfNodesDialog.show(self)
        if isOk:
            isOk, matrix, names = NewDiagramDialog.show(self, n)
            if isOk:
                if len(matrix) > 0:
                    config.STUDENTS_LIST = names
                    config.RESULT_MATRIX = matrix

                    if (
                        len(config.STUDENTS_LIST) > 1
                        and len(config.STUDENTS_LIST) == len(config.RESULT_MATRIX)
                        and len(config.RESULT_MATRIX) == len(config.RESULT_MATRIX[0])
                    ):
                        config.SELECTED_STUDENT = ""
                        config.SELECTED_STUDENTS = []
                        config.HIDED_STUDENTS = []
                        self.updateDiagram()
                        self.ui.actionSave.setEnabled(True)
                        self.ui.actionSave_as.setEnabled(True)
                        self.ui.actionClose.setEnabled(True)

    def openDiagram(self):
        config.FILE_NAME = QFileDialog.getOpenFileName(
            None, "Load File", "", "Text (*.txt);;All Files (*)"
        )[0]
        if config.FILE_NAME != "":
            file = open(config.FILE_NAME)
            try:
                results = file.read().replace("\n", "").split(";")
                self.ui.lineEdit.clear
                nodes, matrix = expandMatrix(results)
                if len(nodes) > 1 and len(matrix) == len(nodes):
                    saveMatrix(nodes, matrix)
            finally:
                file.close()

            if (
                len(config.STUDENTS_LIST) > 1
                and len(config.STUDENTS_LIST) == len(config.RESULT_MATRIX)
                and len(config.RESULT_MATRIX) == len(config.RESULT_MATRIX[0])
            ):
                config.SELECTED_STUDENT = ""
                config.SELECTED_STUDENTS = []
                config.HIDED_STUDENTS = []
                self.updateDiagram()
                self.ui.actionSave.setEnabled(True)
                self.ui.actionSave_as.setEnabled(True)
                self.ui.actionClose.setEnabled(True)

    def saveDiagram(self):
        if len(config.STUDENTS_LIST) > 0:
            if config.FILE_NAME != "":
                string = ",".join(config.STUDENTS_LIST)
                for i in range(len(config.STUDENTS_LIST)):
                    string_ints = [str(int) for int in config.RESULT_MATRIX[i]]
                    line = ",".join(string_ints)
                    # line = ','.join(config.RESULT_MATRIX[i])
                    string = string + ";\n" + line

                file = open(config.FILE_NAME, "w+")
                try:
                    file.write(string)
                finally:
                    file.close()
            else:
                self.saveAsDiagram()

    def save_asDiagram(self):
        if len(config.STUDENTS_LIST) > 0:
            config.FILE_NAME = QFileDialog.getSaveFileName(
                None, "Load File", "", "Text (*.txt);;All Files (*)"
            )[0]
            # print(config.FILE_NAME)
            if config.FILE_NAME != "":
                self.saveDiagram()

    def closeDiagram(self):
        config.FILE_NAME = ""
        config.STUDENTS_LIST.clear()
        config.RESULT_MATRIX.clear()
        config.HIDED_STUDENTS.clear()
        config.SELECTED_STUDENT = ""
        config.SELECTED_STUDENTS.clear()

        self.ui.actionSave.setEnabled(False)
        self.ui.actionSave_as.setEnabled(False)
        self.ui.actionClose.setEnabled(False)

        self.ui.lineEdit.clear()
        self.updateList("")
        self.ui.listStudents.clear()
        self.drawDiagrams()

    @QtCore.Slot()
    def on_actionAbout_Grading_Cat_triggered(self):
        AboutCatDialog.show(self)

    def updateList(self, student):
        # rate = findMaxPlag()
        # if config.SORT: rate = sorted(rate, key=itemgetter(1), reverse=True)
        if student in config.STUDENTS_LIST:
            currentIndex = config.STUDENTS_LIST.index(student)
            config.SELECTED_STUDENT = config.STUDENTS_LIST[currentIndex]
            maxPlag = max(config.RESULT_MATRIX[currentIndex])
            students = []
            for i in range(len(config.STUDENTS_LIST)):
                if currentIndex != i:
                    students.append([config.RESULT_MATRIX[currentIndex][i], i])
                else:
                    students.append([maxPlag, i])

            if config.SORT:
                del students[currentIndex]
                students = sorted(students, key=itemgetter(0), reverse=True)
                students.insert(0, [maxPlag, currentIndex])
                currentIndex = 0

            for i in range(len(config.STUDENTS_LIST)):
                self.ui.listStudents.item(i).setBackground(QColor(250, 247, 247))  #!
                if i == currentIndex:
                    # window.listStudents.item(i).setBackground(QColor(248, 155, 141))
                    self.ui.listStudents.item(i).setSelected(True)
                    newRow = student + "\t- " + str(maxPlag) + "%"
                    self.ui.listStudents.item(i).setText(newRow)
                else:
                    if int(students[i][0]) >= config.RANGE_PLAG:
                        if students[i][0] == maxPlag:
                            self.ui.listStudents.item(i).setForeground(
                                QColor(235, 50, 50)
                            )
                        else:
                            self.ui.listStudents.item(i).setForeground(
                                QColor(250, 130, 130)
                            )
                        self.ui.listStudents.item(i).setBackground(
                            QColor(231, 214, 212)
                        )
                    else:
                        self.ui.listStudents.item(i).setForeground(
                            QColor(119, 110, 107)
                        )
                    text = (
                        config.STUDENTS_LIST[students[i][1]]
                        + "\t- "
                        + str(students[i][0])
                        + "%"
                    )
                    self.ui.listStudents.item(i).setText(text)

    def drawDiagrams(self):
        self.ChordDiagramView.scene.drawDiagram()
        self.ChordDiagram2View.scene.drawDiagram()
        self.NetworkDiagramView.scene.drawDiagram()

    def viewMatchReport(self, studentID_1, studentID_2):
        html_path = project.htmlReportPath(studentID_1, studentID_2)
        isOk = MatchViewerDialog.show(self, studentID_1, studentID_2, html_path)
        # if isOk:
        #     print("Yay!")

    def updateDiagram(self):
        config.SHOW_NAMES = self.ui.showNames.isChecked()
        config.SHOW_LINKLESS = self.ui.showLinkless.isChecked()
        config.SHOW_RARE = self.ui.showRate.isChecked()
        config.CHESS = self.ui.chess.isChecked()
        config.SORT = self.ui.sort.isChecked()

        config.RANGE_PLAG = self.ui.rangeSlider.value()
        rangeLabel = "Range:  > " + str(config.RANGE_PLAG) + "%"
        self.ui.label_Range.setText(rangeLabel)

        if config.COUPLE != "":
            project.viewMatchReport(config.WAITING_FOR_, config.COUPLE)
            config.SELECTED_STUDENT = config.WAITING_FOR_
            # config.WAITING_FOR_ = ""
            config.COUPLE = ""

        if config.SELECTED_STUDENT != "":
            self.ui.lineEdit.clear
            self.ui.lineEdit.setText(str(config.SELECTED_STUDENT))
            self.ui.lineEdit.setToolTip("Selected student")
            self.ui.ShowButton.setToolTip("Show selected student")

            # if config.SELECTED_STUDENT not in config.HIDED_STUDENTS:
            # self.ui.toolButton_openEye.clicked.connect(self.hideStudent)
            # self.ui.toolButton_openEye.setToolTip('Hide')
            # iconPath = config.APPLICATION_DIRNAME + "/icons/closeEye.png"
            # self.ui.toolButton_openEye.setIcon(QIcon(iconPath))
            # else:
            # self.ui.toolButton_openEye.clicked.connect(self.exposeStudent)
            # self.ui.toolButton_openEye.setToolTip('Expose')
            # iconPath = config.APPLICATION_DIRNAME + "/icons/openEye.png"
            # self.ui.toolButton_openEye.setIcon(QIcon(iconPath))

        if len(config.STUDENTS_LIST) > 0:
            self.studentList()
            self.updateLinkedStudents(config.SELECTED_STUDENT)
            self.drawDiagrams()
            if len(config.SELECTED_STUDENT) > 0:
                self.updateList(config.SELECTED_STUDENT)

    def studentList(self):
        self.ui.listStudents.clear()
        # window.listRate.clear()
        rate = findMaxPlag()
        for i in range(len(config.STUDENTS_LIST)):
            if config.SORT:
                rate = sorted(rate, key=itemgetter(1), reverse=True)

            text = config.STUDENTS_LIST[rate[i][2]] + "\t- " + str(rate[i][1]) + "%"
            self.ui.listStudents.addItem(text)
            # window.listStudents.addItem(config.STUDENTS_LIST[i])
            # text = str(rate[i][1]) + "%"
            # window.listRate.addItem(text)
        pass

    def selectedStudent(self, item):
        node = item.text().split()[0]

        if node != "" and node in config.STUDENTS_LIST:
            if config.SELECTED_STUDENT == node and config.WAITING_FOR_ == "":
                config.WAITING_FOR_ = node
            elif config.SELECTED_STUDENT == node and config.WAITING_FOR_ == node:
                config.WAITING_FOR_ = ""
            elif config.SELECTED_STUDENT != "" and config.WAITING_FOR_ != "":
                if node in config.SELECTED_STUDENTS:
                    config.COUPLE = node
                else:
                    config.WAITING_FOR_ = ""

            config.SELECTED_STUDENT = node

            self.ui.lineEdit.setText(node)
            self.ui.lineEdit.setToolTip("Selected student")
            self.ui.ShowButton.setToolTip("Show selected student")
            self.updateDiagram()

    def updateLinkedStudents(self, student):
        config.SELECTED_STUDENTS.clear()
        if student in config.STUDENTS_LIST:
            currentIndex = config.STUDENTS_LIST.index(student)
            for i in range(len(config.STUDENTS_LIST)):
                if (
                    currentIndex != i
                    and int(config.RESULT_MATRIX[currentIndex][i]) >= config.RANGE_PLAG
                ):
                    config.SELECTED_STUDENTS.append(config.STUDENTS_LIST[i])

    def clearLine(self):
        config.WAITING_FOR_ = ""
        config.COUPLE = ""
        config.SELECTED_STUDENT = ""
        config.SELECTED_STUDENTS.clear()
        self.ui.lineEdit.clear()
        self.ui.lineEdit.setToolTip("Enter student ID to select")
        self.ui.ShowButton.setToolTip("No one selected")
        self.updateList("")
        self.updateDiagram()

    def resetSettings(self):
        self.ui.showNames.setChecked(True)
        self.ui.showLinkless.setChecked(True)
        self.ui.showRate.setChecked(False)
        self.ui.chess.setChecked(False)
        self.ui.sort.setChecked(False)
        self.ui.rangeSlider.setValue(25)
        config.SHOW_NAMES = True
        config.SHOW_LINKLESS = True
        config.SHOW_RARE = False
        config.CHESS = False
        config.SORT = False
        config.RANGE_PLAG = 25

    def deleteStudent(self):
        if (
            config.SELECTED_STUDENT != ""
            and config.SELECTED_STUDENT in config.STUDENTS_LIST
        ):
            index = config.STUDENTS_LIST.index(config.SELECTED_STUDENT)
            config.STUDENTS_LIST.remove(config.SELECTED_STUDENT)

            del config.RESULT_MATRIX[index]
            for i in range(len(config.RESULT_MATRIX)):
                del config.RESULT_MATRIX[i][index]

            if config.SELECTED_STUDENT in config.HIDED_STUDENTS:
                config.HIDED_STUDENTS.remove(config.SELECTED_STUDENT)

            config.SELECTED_STUDENT = ""
            config.SELECTED_STUDENTS.clear()
            self.ui.lineEdit.clear()
            self.updateList("")
            self.updateDiagram()
        pass

    def hideStudent(self):
        if (
            config.SELECTED_STUDENT != ""
            and config.SELECTED_STUDENT in config.STUDENTS_LIST
        ):
            if config.SELECTED_STUDENT not in config.HIDED_STUDENTS:
                config.HIDED_STUDENTS.append(config.SELECTED_STUDENT)

            config.WAITING_FOR_ = ""
            config.COUPLE = ""
            config.SELECTED_STUDENT = ""
            config.SELECTED_STUDENTS.clear()
            self.ui.lineEdit.clear()
            self.updateList("")
            self.updateDiagram()
        pass

    def exposeStudent(self):
        if (
            config.SELECTED_STUDENT != ""
            and config.SELECTED_STUDENT in config.STUDENTS_LIST
            and config.SELECTED_STUDENT in config.HIDED_STUDENTS
        ):
            config.HIDED_STUDENTS.remove(config.SELECTED_STUDENT)

            self.updateList(config.SELECTED_STUDENT)
            self.updateDiagram()

    def findStudent(self):
        student = self.ui.lineEdit.text()
        if student != "":
            student = student.split()[0]
            config.SELECTED_STUDENT = student
            self.updateDiagram()

    def _updateTitle(self, project_path):
        self.setWindowTitle(f"{config.APPLICATION_TITLE}: {project_path}")

    def _updateMenuStatus(self, items):
        for item, status in items:
            getattr(self.ui, item).setEnabled(status)

    def editSettings(self):
        isOk, config = ProjectConfigDialog.show(self, project.settings())
        if isOk:
            project.saveSettings(config)

    def newProject(self):
        if r := QFileDialog.getExistingDirectory(
            self,
            "Choose project folder",
            sys.path[0],  # starting folder may be revised
            QFileDialog.ShowDirsOnly,
        ):
            project.newProject(r)
            self._updateTitle(r)
            self._updateMenuStatus(self._PROJECT_OPENED_ITEMS)
            self.editSettings()

    @QtCore.Slot()
    def on_actionOpen_Project_2_triggered(self):
        if r := QFileDialog.getExistingDirectory(
            self,
            "Choose project folder",
            sys.path[0],  # starting folder may be revised
            QFileDialog.ShowDirsOnly,
        ):
            project.openProject(r)
            self._updateTitle(r)
            self._updateMenuStatus(self._PROJECT_OPENED_ITEMS)

    def syncWithDataSource(self):
        progress = QProgressDialog("Downloading files...", "Cancel", 0, 1, self)
        progress.setMinimumDuration(0)
        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.processAppEvents = types.MethodType(
            lambda x: QtCore.QCoreApplication.instance().processEvents(), progress
        )
        project.syncWithDataSource(progress)

    def openNewSession(self):
        item, isOk = QInputDialog.getItem(
            self,
            config.APPLICATION_TITLE,
            "Choose assignment",
            project.assignments(),
            editable=False,
        )
        if isOk and newSessionDiagram(project.detect(item)):
            self.updateDiagram()
