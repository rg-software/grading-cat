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
        #Злой человек осуждает такой разбор :( 
        #Что ж, он всегда может показать "как надо", в рамках этой функции, например.
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
def saveDiagram_2():    
    if len(config.STUDENTS_LIST) > 0:       
        #Нужно имя файла, я забыла, где его брать. 
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
    # Очевидно, еще заставит менять формат сохранения. 
    # Но, я лучше подожду -- инициатива тут наказывается хуже промедления.  
    pass

def openDiagram_2():    
    # Это функция скорей всего вернется тоже, но каким извращёнными способом, лучше пока даже не гадать.
    pass

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

def aboutCat():
    # Ссылка нормально работает, но поменять это может и надо… Но как-нибудь потом. 
    # Если уж мы серьезные вещи откладываем на потом, то это уж точно подождет. 
    url = "https://memegenerator.net/img/instances/70259669/patience-as-i-catch-up-on-grading.jpg"
    webbrowser.open(url, new=0, autoraise=True)

### file menu
## Злой человек считает, что вы работаете неправильно :(             ##
## Пока посидите тут, я вас воскрешу в своей программе, чуть позже.  ##
def clearDiagram():
    blankScene = QGraphicsScene()
    window.ChordDiagramView.setScene(blankScene)
    window.ChordDiagram2View.setScene(blankScene)
    window.NetworkDiagramView.setScene(blankScene)
    window.BubbleDiagramView.setScene(blankScene)
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
## ----------------------------------------------------------------- ##


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

def drawDiagrams(): 
    
    window.ChordDiagramView.scene.drawDiagram()
    window.ChordDiagram2View.scene.drawDiagram()
    window.NetworkDiagramView.scene.drawDiagram()
    window.BubbleDiagramView.scene.drawDiagram()

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


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()

    window.ui.actionNew_Project_2.triggered.connect(project.newProject)
    window.ui.actionOpen_Project_2.triggered.connect(project.openProject)
    window.ui.actionSave_2.triggered.connect(saveDiagram_2)

    window.ui.actionSettings.triggered.connect(project.setSettings)
    window.ui.actionSync_with_Data_Source.triggered.connect(project.syncWithDataSource)
    window.ui.actionDetect.triggered.connect(openNewSession)

    window.ui.actionQuit.triggered.connect(window.close)    
    window.ui.actionAbout_VPlag.triggered.connect(aboutCat)   
        
    window.ui.rangeSlider.valueChanged.connect(updateDiagram)
    rangeLabel = "Range:  > " + str(window.ui.rangeSlider.value()) + "%"
    window.ui.label_Range.setText(rangeLabel)
      
    window.ui.showNames.stateChanged.connect(updateDiagram)
    window.ui.showLinkless.stateChanged.connect(updateDiagram)
    window.ui.showRate.stateChanged.connect(updateDiagram)
    window.ui.chess.stateChanged.connect(updateDiagram)
    window.ui.sort.stateChanged.connect(updateDiagram)

    window.ui.listStudents.itemClicked.connect(selectedStudent)
    window.ui.Show.clicked.connect(showLinks)
    window.ui.toolButton_cancel.clicked.connect(clearLine)
    window.ui.toolButton_delete.clicked.connect(deleteStudent)
    window.ui.toolButton_closeEye.clicked.connect(hideStudent)
    window.ui.toolButton_openEye.clicked.connect(exposeStudent)

    window.chordDiagramScene.signal.update.connect(updateDiagram)
    window.chordDiagramScene.signal.clear.connect(clearLine)

    window.chordDiagram2Scene.signal.update.connect(updateDiagram)
    window.chordDiagram2Scene.signal.clear.connect(clearLine)

    window.networkScene.signal.update.connect(updateDiagram)
    window.networkScene.signal.clear.connect(clearLine)

    window.bubbleChartScene.signal.update.connect(updateDiagram)
    window.bubbleChartScene.signal.clear.connect(clearLine)


    window.show()
    project.updateMainWinTitle()

    sys.exit(app.exec_())