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
import project
from diagrams import *
from main_window import MainWindow
from diagrams import findMaxPlag

def openNewSession():
    text = project.detect()    
    if text != "":   
        students, matrix = newDiagramFromJPlag(text)
        if len(students) > 1 and len(matrix) == len(students):
            saveMatrix(students, matrix)
            if len(config.STUDENTS_LIST) > 1 and len(config.STUDENTS_LIST) == len(config.RESULT_MATRIX) and len(config.RESULT_MATRIX) == len(config.RESULT_MATRIX[0]):
                updateDiagram()
                window.ui.actionSave_2.setEnabled(True)

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


def updateDiagram():
    config.SHOW_NAMES = window.ui.showNames.isChecked()
    config.SHOW_LINKLESS = window.ui.showLinkless.isChecked()
    config.SHOW_RARE = window.ui.showRate.isChecked()
    config.CHESS = window.ui.chess.isChecked()
    config.SORT = window.ui.sort.isChecked()

    config.RANGE_PLAG = window.ui.rangeSlider.value()
    rangeLabel = "Range:  > " + str(config.RANGE_PLAG) + "%"
    window.ui.label_Range.setText(rangeLabel)

    if config.COUPLE != "":
        project.сall_me_whatever_you_like(config.WAITING_FOR_, config.COUPLE)
        config.SELECTED_STUDENT = config.WAITING_FOR_
        config.WAITING_FOR_ = ""
        config.COUPLE = ""

    if config.SELECTED_STUDENT != "":
        window.ui.lineEdit.clear
        window.ui.lineEdit.setText(str(config.SELECTED_STUDENT))
        window.ui.lineEdit.setToolTip('Selected student') 

    if len(config.STUDENTS_LIST) > 0:
        studentList()
        updateLinkedStudents(config.SELECTED_STUDENT)
        drawDiagrams()
        if len(config.SELECTED_STUDENT) > 0:
            updateList(config.SELECTED_STUDENT)

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
    node = item.text().split()[0]

    if node != "" and node in config.STUDENTS_LIST:
       
        if config.SELECTED_STUDENT == node and config.WAITING_FOR_ == "":
            config.WAITING_FOR_ = node
        elif config.SELECTED_STUDENT == node and config.WAITING_FOR_ == node:
            config.WAITING_FOR_ = ""
        elif config.SELECTED_STUDENT != "" and config.WAITING_FOR_ != "":
            if node in config.SELECTED_NODES: 
                config.COUPLE = node
            else: 
                config.WAITING_FOR_ = ""
        
        config.SELECTED_STUDENT = node   

        window.ui.lineEdit.setText(node)
        window.ui.lineEdit.setToolTip('Selected student') 
        updateDiagram()

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

def drawDiagrams(): 
    
    window.ChordDiagramView.scene.drawDiagram()
    window.ChordDiagram2View.scene.drawDiagram()
    window.NetworkDiagramView.scene.drawDiagram()

    pass
def clearLine():
    config.WAITING_FOR_ = ""
    config.COUPLE = ""
    config.SELECTED_STUDENT = ""
    config.SELECTED_STUDENTS.clear()
    window.ui.lineEdit.clear()        
    window.ui.lineEdit.setToolTip('No one selected')
    updateList("")
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
def resetSettings():

    window.ui.showNames.setChecked(True)
    window.ui.showLinkless.setChecked(True)
    window.ui.showRate.setChecked(False)
    window.ui.chess.setChecked(False)
    window.ui.sort.setChecked(False)
    window.ui.rangeSlider.setValue(0)
    config.SHOW_NAMES = True
    config.SHOW_LINKLESS = True
    config.SHOW_RARE = False
    config.CHESS = False
    config.SORT = False
    config.RANGE_PLAG = 0
    

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    #window.ui.setToolTip('This is a tooltip message.') 

    window.ui.actionNew_Project_2.triggered.connect(project.newProject)
    window.ui.actionOpen_Project_2.triggered.connect(project.openProject)
    window.ui.actionSettings.triggered.connect(project.setSettings)
    window.ui.actionSync_with_Data_Source.triggered.connect(project.syncWithDataSource)
    window.ui.actionDetect.triggered.connect(openNewSession)

    window.ui.actionQuit.triggered.connect(window.close)     
        
    window.ui.rangeSlider.valueChanged.connect(updateDiagram)
    rangeLabel = "Range:  > " + str(window.ui.rangeSlider.value()) + "%"
    window.ui.label_Range.setText(rangeLabel)
      
    window.ui.showNames.stateChanged.connect(updateDiagram)
    window.ui.showLinkless.stateChanged.connect(updateDiagram)
    window.ui.showRate.stateChanged.connect(updateDiagram)
    window.ui.chess.stateChanged.connect(updateDiagram)
    window.ui.sort.stateChanged.connect(updateDiagram)

    window.ui.listStudents.itemClicked.connect(selectedStudent)

    window.ui.lineEdit.setToolTip('No one selected') 
    #window.ui.lineEdit.setToolTip('Enter student ID to select') Больше не работает, потому что нет кнопки show
    window.ui.toolButton_cancel.clicked.connect(clearLine)
    window.ui.toolButton_cancel.setToolTip('Cancel') 
    window.ui.toolButton_delete.clicked.connect(deleteStudent)
    window.ui.toolButton_delete.setToolTip('Delete')
    window.ui.toolButton_closeEye.clicked.connect(hideStudent)
    window.ui.toolButton_closeEye.setToolTip('Hide')
    window.ui.toolButton_openEye.clicked.connect(exposeStudent)
    window.ui.toolButton_openEye.setToolTip('Expose')
    window.ui.resetButton.clicked.connect(resetSettings)
    window.ui.resetButton.setToolTip('Reset settings')

    window.chordDiagramScene.signal.update.connect(updateDiagram)
    window.chordDiagramScene.signal.clear.connect(clearLine)

    window.chordDiagram2Scene.signal.update.connect(updateDiagram)
    window.chordDiagram2Scene.signal.clear.connect(clearLine)

    window.networkScene.signal.update.connect(updateDiagram)
    window.networkScene.signal.clear.connect(clearLine)

    window.show()
    project.updateMainWinTitle()

    sys.exit(app.exec_())