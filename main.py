import sys
import os
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
from about_cat import AboutCatDialog
from new_diagram_dialog import NewDiagramDialog
from number_of_nodes import NumberOfNodesDialog


def openNewSession():
    text = project.detect()    
    if text != "":   
        students, matrix = newDiagramFromJPlag(text)
        if len(students) > 1 and len(matrix) == len(students):
            saveMatrix(students, matrix)
            if len(config.STUDENTS_LIST) > 1 and len(config.STUDENTS_LIST) == len(config.RESULT_MATRIX) and len(config.RESULT_MATRIX) == len(config.RESULT_MATRIX[0]):
                window.updateDiagram()
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
def aboutGradingCat():
    isOk = AboutCatDialog.show(window)
    #url = "https://memegenerator.net/img/instances/70259669/patience-as-i-catch-up-on-grading.jpg"
    #webbrowser.open(url, new=0, autoraise=True)

#### test menu ####

def newDiagram(): 
    isOk, n = NumberOfNodesDialog.show(window)
    if isOk:
        isOk, matrix, names = NewDiagramDialog.show(window, n)
        if isOk:
            if len(matrix) > 0:
                config.STUDENTS_LIST = names
                config.RESULT_MATRIX = matrix 
              
                if len(config.STUDENTS_LIST) > 1 and len(config.STUDENTS_LIST) == len(config.RESULT_MATRIX) and len(config.RESULT_MATRIX) == len(config.RESULT_MATRIX[0]):
                    config.SELECTED_STUDENT = ""
                    config.SELECTED_STUDENTS = []
                    config.HIDED_STUDENTS = []
                    window.updateDiagram()
                    window.ui.actionSave.setEnabled(True)
                    window.ui.actionSave_as.setEnabled(True)
                    window.ui.actionClose.setEnabled(True)
def openDiagram(): 
    config.FILE_NAME = QFileDialog.getOpenFileName(None,"Load File","","Text (*.txt);;All Files (*)")[0]
    if config.FILE_NAME != "":
        file = open(config.FILE_NAME)
        try:
            results = file.read().replace('\n','').split(';') 
            window.ui.lineEdit.clear            
            nodes, matrix = expandMatrix(results)
            if len(nodes) > 1 and len(matrix) == len(nodes):
                saveMatrix(nodes, matrix)
        finally:
            file.close()      
    
        if len(config.STUDENTS_LIST) > 1 and len(config.STUDENTS_LIST) == len(config.RESULT_MATRIX) and len(config.RESULT_MATRIX) == len(config.RESULT_MATRIX[0]):
            config.SELECTED_STUDENT = ""
            config.SELECTED_STUDENTS = []
            config.HIDED_STUDENTS = []
            window.updateDiagram()
            window.ui.actionSave.setEnabled(True)
            window.ui.actionSave_as.setEnabled(True)
            window.ui.actionClose.setEnabled(True)
    pass
def saveDiagram():
    if len(config.STUDENTS_LIST) > 0:       
        if config.FILE_NAME != "": 
            string = ','.join(config.STUDENTS_LIST) 
            for i in range(len(config.STUDENTS_LIST)):
                string_ints = [str(int) for int in config.RESULT_MATRIX[i]]      
                line = ",".join(string_ints)
                #line = ','.join(config.RESULT_MATRIX[i])
                string = string + ";\n" + line
            
            file = open(config.FILE_NAME, 'w+')
            try:
                file.write(string)
            finally:
                file.close()  
        else: saveAsDiagram() 
def save_asDiagram():
    if len(config.STUDENTS_LIST) > 0:
        config.FILE_NAME = QFileDialog.getSaveFileName(None,"Load File","","Text (*.txt);;All Files (*)")[0]
        #print(config.FILE_NAME)
        if config.FILE_NAME != "": saveDiagram()
def closeDiagram():
    config.FILE_NAME = ""
    config.STUDENTS_LIST.clear()
    config.RESULT_MATRIX.clear()
    config.HIDED_STUDENTS.clear()
    config.SELECTED_STUDENT = ""
    config.SELECTED_STUDENTS.clear()

    window.ui.actionSave.setEnabled(False)
    window.ui.actionSave_as.setEnabled(False)
    window.ui.actionClose.setEnabled(False)

    window.ui.lineEdit.clear()
    window.updateList("")
    window.ui.listStudents.clear()
    window.drawDiagrams()
    pass

#### -------- ####    

if __name__ == "__main__":
    app = QApplication(sys.argv)

    config.APPLICATION_DIRNAME = os.path.dirname(__file__)

    window = MainWindow()
    #window.ui.setToolTip('This is a tooltip message.') 

    window.ui.actionNew_Project_2.triggered.connect(project.newProject)
    window.ui.actionOpen_Project_2.triggered.connect(project.openProject)
    window.ui.actionSettings.triggered.connect(project.setSettings)
    window.ui.actionSync_with_Data_Source.triggered.connect(project.syncWithDataSource)
    window.ui.actionDetect.triggered.connect(openNewSession)

    window.ui.actionQuit.triggered.connect(window.close)  
    window.ui.actionAbout_Grading_Cat.triggered.connect(aboutGradingCat)  
    
    window.ui.showNames.stateChanged.connect(window.updateDiagram)
    window.ui.showLinkless.stateChanged.connect(window.updateDiagram)
    window.ui.showRate.stateChanged.connect(window.updateDiagram)
    window.ui.chess.stateChanged.connect(window.updateDiagram)
    window.ui.sort.stateChanged.connect(window.updateDiagram)

    window.ui.listStudents.itemClicked.connect(window.selectedStudent)
    window.ui.lineEdit.setToolTip('Enter student ID to select') 
    window.ui.ShowButton.clicked.connect(window.findStudent)
    window.ui.ShowButton.setToolTip('No one selected')
    window.ui.toolButton_cancel.clicked.connect(window.clearLine)
    window.ui.toolButton_cancel.setToolTip('Cancel') 
    window.ui.toolButton_delete.clicked.connect(window.deleteStudent)
    window.ui.toolButton_delete.setToolTip('Delete')

    window.ui.toolButton_openEye.clicked.connect(window.exposeStudent)
    window.ui.toolButton_openEye.setToolTip('Expose')
    openEyePath = config.APPLICATION_DIRNAME + "/icons/openEye.png"
    window.ui.toolButton_openEye.setIcon(QIcon(openEyePath))

    window.ui.toolButton_closeEye.clicked.connect(window.hideStudent)
    window.ui.toolButton_closeEye.setToolTip('Hide')
    closeEyePath = config.APPLICATION_DIRNAME + "/icons/closeEye.png"
    window.ui.toolButton_closeEye.setIcon(QIcon(closeEyePath))

    window.ui.resetButton.clicked.connect(window.resetSettings)
    window.ui.resetButton.setToolTip('Reset settings')

    window.ui.rangeSlider.valueChanged.connect(window.updateDiagram)
    rangeLabel = "Range:  > " + str(window.ui.rangeSlider.value()) + "%"
    window.ui.label_Range.setText(rangeLabel)


    #### test menu ####

    window.ui.actionNew.triggered.connect(newDiagram) 
    window.ui.actionOpen.triggered.connect(openDiagram) 
    window.ui.actionSave.triggered.connect(saveDiagram)
    window.ui.actionSave_as.triggered.connect(save_asDiagram) 
    window.ui.actionClose.triggered.connect(closeDiagram)

    #### --------- ####

    window.chordDiagramScene.signal.update.connect(window.updateDiagram)
    window.chordDiagramScene.signal.clear.connect(window.clearLine)

    window.chordDiagram2Scene.signal.update.connect(window.updateDiagram)
    window.chordDiagram2Scene.signal.clear.connect(window.clearLine)

    window.networkScene.signal.update.connect(window.updateDiagram)
    window.networkScene.signal.clear.connect(window.clearLine)

    window.show() 
    project.updateMainWinTitle()
    sys.exit(app.exec_())