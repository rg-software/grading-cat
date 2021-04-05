import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import *
from PySide6 import QtCore, QtGui
from PySide6.QtCore import *
from PySide6 import QtGui
from PySide6.QtGui import *
from operator import *
import config
import webbrowser
from ui_mainwindow import Ui_MainWindow
from diagrams import *
from lines import LinesView
import project

def expandMatrix(text):
    students = []
    rate = []
    students.extend(text[0].split(','))
    
    matrix = text[1:]
    for i in range(len(matrix)):
        line = matrix[i].split(',')
        rate.append(line) 
        for j in range(len(rate[i])):
            rate[i][j] = int(rate[i][j])

    return students, rate
def saveMatrix(students, rate):
        
        #window.ui.lineEdit.clear
        config.STUDENTS_LIST.clear()
        config.RESULT_MATRIX.clear()
        config.HIDED_STUDENTS.clear()
        config.SELECTED_STUDENTS.clear()
        config.SELECTED_STUDENT = ""

        config.STUDENTS_LIST.extend(students)
        config.RESULT_MATRIX.extend(rate)

def CSVtoSomething(content):   
    result = []
    fileStrings = []
    studentNames = []
    for i in range(len(content)):
        fileStrings.append(content[i].split(';'))
        #print(fileStrings[i])
        for j in range(len(fileStrings[i])):
            if fileStrings[i][j] not in studentNames and len(fileStrings[i][j]) > 5: #ну а что делать?!
                studentNames.append(fileStrings[i][j])
    ### мать
    matrix = []
    for i in range(len(studentNames)):
        line = []
        for j in range(len(studentNames)):
            line.append(0)
        matrix.append(line)

    for i in range(len(fileStrings)):
        if fileStrings[i][0] in studentNames:
            indexA = studentNames.index(fileStrings[i][0])
            for j in range(len(fileStrings[i])):
                if fileStrings[i][j] in studentNames:
                    indexB = studentNames.index(fileStrings[i][j])
                    if indexA != indexB:
                        matrix[indexA][indexB] = matrix[indexB][indexA] = fileStrings[i][j+1].split('.')[0] ###...

    names = ','.join(studentNames)
    result.append(names)
    for i in range(len(studentNames)):
        line = ','.join(matrix[i])
        result.append(line)
    return result

def newDiagramFromJPlag(text):
    #text = "s1252001-s1260009: 32.753624\ns1252001-s1260017: 21.987314\ns1252001-s1260027: 41.365463"
    resultsList = text.split('\n')
    studentA = []
    studentB = []
    rate = []
    students = []    
    matrix = []
    for i in range(len(resultsList)):
        resultsList[i].replace(' ','')
        if len(resultsList[i]) > 0 and '-' in resultsList[i] and ':' in resultsList[i]:
            part1 = resultsList[i].split('-')
            part2 = part1[1].split(':')
            studentA.append(part1[0])
            studentB.append(part2[0])
            rate.append(part2[1])

            if studentA[i] not in students: students.append(studentA[i])
            if studentB[i] not in students: students.append(studentB[i])
        
    for i in range(len(students)):
        line = []
        for j in range(len(students)):
            line.append(0)
        matrix.append(line)

    for i in range(len(studentA)):
        indexA = students.index(studentA[i])
        indexB = students.index(studentB[i])
        matrix[indexA][indexB] = int(float(rate[i]))
        matrix[indexB][indexA] = int(float(rate[i]))

    
    return students, matrix
def openNewSession():
    text = project.newDetectionSession()
    if len(text) > 0:        
        #if 'JPlag'
        students, matrix = newDiagramFromJPlag(text)
        if len(students) > 1 and len(matrix) == len(students):
            saveMatrix(students, matrix)
            if len(config.STUDENTS_LIST) > 1 and len(config.STUDENTS_LIST) == len(config.RESULT_MATRIX) and len(config.RESULT_MATRIX) == len(config.RESULT_MATRIX[0]):
                updateDiagram()

def updateDiagram():

    config.SHOW_NAMES = window.ui.showNames.isChecked()
    config.SHOW_LINKLESS = window.ui.showLinkless.isChecked()
    config.SHOW_RARE = window.ui.showRate.isChecked()
    config.CHESS = window.ui.chess.isChecked()
    config.SORT = window.ui.sort.isChecked()

    config.RANGE_PLAG = window.ui.rangeSlider.value()
    rangeLabel = "Range:  > " + str(config.RANGE_PLAG) + "%"
    window.ui.label_Range.setText(rangeLabel)

    if config.SELECTED_STUDENT != "":
        window.ui.lineEdit.clear
        window.ui.lineEdit.setText(str(config.SELECTED_STUDENT))

    if len(config.STUDENTS_LIST) > 0:
        studentList()
        updateLinkedStudents(config.SELECTED_STUDENT)
        drawDiagrams()
        if len(config.SELECTED_STUDENT) > 0:
            updateList(config.SELECTED_STUDENT)
        #config.SELECTED_STUDENTS.clear()

    # TODO-BE-DO-BE-DO    
    pass
def studentList():
    window.ui.listStudents.clear()
    #window.listRate.clear()
    rate = findMaxPlag()
    for i in range(len(config.STUDENTS_LIST)):
        if config.SORT: rate = sorted(rate, key=itemgetter(1), reverse=True) 

        text = config.STUDENTS_LIST[rate[i][2]] + "\t- " + str(rate[i][1]) + "%"
        window.ui.listStudents.addItem(text)
        #window.listStudents.addItem(config.STUDENTS_LIST[i])
        #text = str(rate[i][1]) + "%"
        #window.listRate.addItem(text)
    pass
def selectedStudent(item):
    
    student = item.text().split()[0]
    config.SELECTED_STUDENT = student
    #updateList(student)
    window.ui.lineEdit.setText(student)
    updateDiagram()
    pass
def updateLinkedStudents(student):
    config.SELECTED_STUDENTS.clear()
    if student in config.STUDENTS_LIST:
        currentIndex = config.STUDENTS_LIST.index(student)
        for i in range(len(config.STUDENTS_LIST)):
            if currentIndex != i and int(config.RESULT_MATRIX[currentIndex][i]) >= config.RANGE_PLAG:
                config.SELECTED_STUDENTS.append(config.STUDENTS_LIST[i])
def updateList(student):   
    #rate = findMaxPlag()
    #if config.SORT: rate = sorted(rate, key=itemgetter(1), reverse=True)
    if student in config.STUDENTS_LIST:
        currentIndex = config.STUDENTS_LIST.index(student)
        config.SELECTED_STUDENT = config.STUDENTS_LIST[currentIndex]       
        maxPlag = max(config.RESULT_MATRIX[currentIndex])
        students = []
        for i in range(len(config.STUDENTS_LIST)):
            if currentIndex != i:
                students.append([config.RESULT_MATRIX[currentIndex][i], i])
            else: students.append([maxPlag, i])
        
        if config.SORT: 
            del students[currentIndex]
            students = sorted(students, key=itemgetter(0), reverse=True)            
            students.insert(0,[maxPlag, currentIndex])            
            currentIndex = 0

        for i in range(len(config.STUDENTS_LIST)):
            window.ui.listStudents.item(i).setBackground(QColor(250, 247, 247)) #!   
            if i == currentIndex:
                #window.listStudents.item(i).setBackground(QColor(248, 155, 141))
                window.ui.listStudents.item(i).setSelected(True)
                newRow = student + "\t- " + str(maxPlag) + "%"
                window.ui.listStudents.item(i).setText(newRow)   
            else:
                if int(students[i][0]) >= config.RANGE_PLAG:
                    if students[i][0] == maxPlag:
                        window.ui.listStudents.item(i).setForeground(QColor(235, 50, 50))
                    else: window.ui.listStudents.item(i).setForeground(QColor(250, 130, 130))
                    window.ui.listStudents.item(i).setBackground(QColor(231, 214, 212))   
                else: window.ui.listStudents.item(i).setForeground(QColor(119, 110, 107))                     
                text = config.STUDENTS_LIST[students[i][1]] + "\t- " + str(students[i][0]) + "%"
                window.ui.listStudents.item(i).setText(text)             

### file menu

def openDiagram():    
    config.FILE_NAME = QFileDialog.getOpenFileName(None,"Load File","","Text (*.txt);;All Files (*)")[0]
    if config.FILE_NAME != "":
        file = open(config.FILE_NAME)
        try:
            results = file.read().replace('\n','').split(';') 
            window.ui.lineEdit.clear            
            students, matrix = expandMatrix(results)
            if len(students) > 1 and len(matrix) == len(students):
                saveMatrix(students, matrix)
        finally:
            file.close()      
    
        if len(config.STUDENTS_LIST) > 1 and len(config.STUDENTS_LIST) == len(config.RESULT_MATRIX) and len(config.RESULT_MATRIX) == len(config.RESULT_MATRIX[0]):
            updateDiagram()
    pass
def saveAsDiagram():    
    if len(config.STUDENTS_LIST) > 0:
        config.FILE_NAME = QFileDialog.getSaveFileName(None,"Load File","","Text (*.txt);;All Files (*)")[0]
        print(config.FILE_NAME)
        if config.FILE_NAME != "": saveDiagram()
    # TODO
    pass
def saveDiagram():
    #if config.FILE_NAME != "":
        #with open(config.FILE_NAME, "w") as text_file: 
            #print(f"Purchase Amount:", file=text_file)
    
    if len(config.STUDENTS_LIST) > 0:       
        if config.FILE_NAME != "": 
            string = ','.join(config.STUDENTS_LIST) 
            for i in range(len(config.STUDENTS_LIST)):
                line = ','.join(config.RESULT_MATRIX[i])
                string = string + ";\n" + line

            
            file = open(config.FILE_NAME, 'w+')
            try:
                file.write(string)
            finally:
                file.close()  
        else: saveAsDiagram() 
    # TODO
    pass
def closeDiagram():
    config.FILE_NAME = ""
    config.STUDENTS_LIST.clear()
    config.RESULT_MATRIX.clear()
    config.HIDED_STUDENTS.clear()
    config.SELECTED_STUDENT = ""
    config.SELECTED_STUDENTS.clear()

    window.ui.lineEdit.clear()
    updateList("")
    window.ui.listStudents.clear()
    drawDiagrams()
    #clearDiagram()
    pass
def clearDiagram():
    blankScene = QGraphicsScene()
    window.ChordDiagramView.setScene(blankScene)
    window.ChordDiagram2View.setScene(blankScene)
    window.NetworkDiagramView.setScene(blankScene)
    window.BubbleDiagramView.setScene(blankScene)
    pass
def aboutCat():
    url = "https://memegenerator.net/img/instances/70259669/patience-as-i-catch-up-on-grading.jpg"
    webbrowser.open(url, new=0, autoraise=True)
    pass

def drawDiagrams(): 
    
    window.ChordDiagramView.scene.drawDiagram()
    window.ChordDiagram2View.scene.drawDiagram()
    window.NetworkDiagramView.scene.drawDiagram()
    window.BubbleDiagramView.scene.drawDiagram()

    #window.ChordDiagramView.sceneUpdate()
    #window.ChordDiagram2View.sceneUpdate()
    #window.NetworkDiagramView.sceneUpdate()
    #window.BubbleDiagramView.sceneUpdate()

    ######################
    #width = window.ChordDiagramView.width() - 10
    #height = window.ChordDiagramView.height() - 10
    #chordDiagramScene = GraphicsSceneChordDiagram(0, 0, width, height, window.ChordDiagramView)
    #window.ChordDiagramView.setScene(chordDiagramScene)
    #chordDiagramScene.signal.update.connect(updateDiagram)
    #chordDiagramScene.signal.clear.connect(clearLine)

    #width = window.ChordDiagram2View.width() - 10
    #height = window.ChordDiagram2View.height() - 10
    #chordDiagram2Scene = GraphicsSceneChordDiagram2(0, 0, width, height, window.ChordDiagram2View)
    #window.ChordDiagram2View.setScene(chordDiagram2Scene)
    #chordDiagram2Scene.signal.update.connect(updateDiagram)
    #chordDiagram2Scene.signal.clear.connect(clearLine)

    #width = window.NetworkDiagramView.width() - 10
    #height = window.NetworkDiagramView.height() - 10
    #networkScene = GraphicsSceneNetwork(0, 0, width, height, window.NetworkDiagramView)
    #window.NetworkDiagramView.setScene(networkScene)
    #networkScene.signal.update.connect(updateDiagram)
    #networkScene.signal.clear.connect(clearLine)

    #width = window.BubbleDiagramView.width() - 10
    #height = window.BubbleDiagramView.height() - 10
    #bubbleChartScene = GraphicsSceneBubbleChart(0, 0, width, height, window.BubbleDiagramView)
    #window.BubbleDiagramView.setScene(bubbleChartScene)
    #bubbleChartScene.signal.update.connect(updateDiagram)
    #bubbleChartScene.signal.clear.connect(clearLine)
    pass
def clearLine():
    config.SELECTED_STUDENT = ""
    config.SELECTED_STUDENTS.clear()
    window.ui.lineEdit.clear()
    updateList("")
    updateDiagram()
    pass
def showLinks():
    student = window.ui.lineEdit.text()
    if len(student) > 0:
        student = student.split()[0]
        config.SELECTED_STUDENT = student
        updateDiagram()        
    pass
def deleteStudent():
    if  config.SELECTED_STUDENT != "" and config.SELECTED_STUDENT in config.STUDENTS_LIST:
        index = config.STUDENTS_LIST.index(config.SELECTED_STUDENT)        
        config.STUDENTS_LIST.remove(config.SELECTED_STUDENT)
        
        del config.RESULT_MATRIX[index]
        for i in range(len(config.RESULT_MATRIX)):
            del config.RESULT_MATRIX[i][index]
      
        if config.SELECTED_STUDENT in config.HIDED_STUDENTS:
            config.HIDED_STUDENTS.remove(config.SELECTED_STUDENT)

        config.SELECTED_STUDENT = ""
        config.SELECTED_STUDENTS.clear()
        window.ui.lineEdit.clear()
        updateList("")
        updateDiagram()
    pass
def hideStudent():
    if  config.SELECTED_STUDENT != "" and config.SELECTED_STUDENT in config.STUDENTS_LIST:
        if config.SELECTED_STUDENT not in config.HIDED_STUDENTS:
            config.HIDED_STUDENTS.append(config.SELECTED_STUDENT)

        config.SELECTED_STUDENT = ""
        config.SELECTED_STUDENTS.clear()
        window.ui.lineEdit.clear()
        updateList("")
        updateDiagram()
    pass
def exposeStudent():
    if  config.SELECTED_STUDENT != "" and config.SELECTED_STUDENT in config.STUDENTS_LIST and config.SELECTED_STUDENT in config.HIDED_STUDENTS:
        config.HIDED_STUDENTS.remove(config.SELECTED_STUDENT)
        updateList(config.SELECTED_STUDENT)
        updateDiagram()
    pass

class Communicate(QObject):
    update = Signal()
    clear =  Signal()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        
        self.ui.setupUi(self)    

        self.ui.actionNew_Project_2.triggered.connect(project.newProject)
        self.ui.actionSettings.setEnabled(True)
        self.ui.actionOpen_Project_2.triggered.connect(project.openProject)
        self.ui.actionSettings.setEnabled(True)

        self.ui.actionSettings.triggered.connect(project.setSettings)
        self.ui.actionSettings.setEnabled(False)
        self.ui.actionSync_with_Data_Source.triggered.connect(project.syncWithDataSource)
        self.ui.actionSync_with_Data_Source.setEnabled(False)
        self.ui.actionDetect.triggered.connect(project.detect)
        self.ui.actionDetect.setEnabled(False)
        

        #self.ui.actionNew_Project.triggered.connect(project.newProject)
        #self.ui.actionNew_Detection_Session.triggered.connect(openNewSession)
        #self.ui.actionOpen_Project.triggered.connect(project.openProject)
        #self.ui.actionUpdate_Project_Data.triggered.connect(project.updateProjectData)
        #self.ui.actionExport_Template.triggered.connect(project.exportTemplate)
        #self.ui.actionDetecting_Software.triggered.connect(project.detectingSoftware)
        #self.ui.actionData_Source.triggered.connect(project.dataSource)
        #self.ui.actionImport_and_Export_Settings.triggered.connect(project.importExportSettings)


        #self.ui.actionOpen_Detection_Session.triggered.connect(openDiagram)
        #self.ui.actionSave.triggered.connect(saveDiagram)    
        #self.ui.actionSave_as.triggered.connect(saveAsDiagram)
        #self.ui.actionClose.triggered.connect(closeDiagram)
        self.ui.actionQuit.triggered.connect(self.close)
        self.ui.actionQuit.setEnabled(True)

        self.ui.actionAbout_VPlag.triggered.connect(aboutCat)   
        
        self.ui.rangeSlider.valueChanged.connect(updateDiagram)
        rangeLabel = "Range:  > " + str(self.ui.rangeSlider.value()) + "%"
        self.ui.label_Range.setText(rangeLabel)
      
        self.ui.showNames.stateChanged.connect(updateDiagram)
        self.ui.showLinkless.stateChanged.connect(updateDiagram)
        self.ui.showRate.stateChanged.connect(updateDiagram)
        self.ui.chess.stateChanged.connect(updateDiagram)
        self.ui.sort.stateChanged.connect(updateDiagram)

        self.ui.listStudents.itemClicked.connect(selectedStudent)
        self.ui.Show.clicked.connect(showLinks)
        self.ui.toolButton_cancel.clicked.connect(clearLine)
        self.ui.toolButton_delete.clicked.connect(deleteStudent)
        self.ui.toolButton_closeEye.clicked.connect(hideStudent)
        self.ui.toolButton_openEye.clicked.connect(exposeStudent)

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
        self.chordDiagramScene.signal.update.connect(updateDiagram)
        self.chordDiagramScene.signal.clear.connect(clearLine)

        self.chordDiagram2Scene = GraphicsSceneChordDiagram2()
        self.chordDiagram2Scene.signal.update.connect(updateDiagram)
        self.chordDiagram2Scene.signal.clear.connect(clearLine)

        self.networkScene = GraphicsSceneNetwork()
        self.networkScene.signal.update.connect(updateDiagram)
        self.networkScene.signal.clear.connect(clearLine)

        self.bubbleChartScene = GraphicsSceneBubbleChart()
        self.bubbleChartScene.signal.update.connect(updateDiagram)
        self.bubbleChartScene.signal.clear.connect(clearLine)
                
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


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    project.updateMainWinTitle()

    sys.exit(app.exec_())