import sys
import math
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtGui
from PySide6.QtGui import *
from operator import *
import config
import webbrowser

def saveMatrix(results):
    window.lineEdit.clear
    config.STUDENTS_LIST.clear()
    config.RESULT_MATRIX.clear()
    config.HIDED_STUDENTS.clear()
    config.SELECTED_STUDENTS.clear()
    config.SELECTED_STUDENT = ""

    config.STUDENTS_LIST.extend(results[0].split(','))

    matrix = results[1:]
    for i in range(len(matrix)):
        line = matrix[i].split(',')
        config.RESULT_MATRIX.append(line)     

    pass

def updateDiagram():

    config.SHOW_NAMES = window.showNames.isChecked()
    config.SHOW_LINKLESS = window.showLinkless.isChecked()
    config.SHOW_RARE = window.showRate.isChecked()
    config.CHESS = window.chess.isChecked()

    config.RANGE_PLAG = window.rangeSlider.value()
    rangeLabel = "Range:  > " + str(config.RANGE_PLAG) + "%"
    window.label_Range.setText(rangeLabel)

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
    window.listStudents.clear()
    #window.listRate.clear()
    rate = findMaxPlag()
    for i in range(len(config.STUDENTS_LIST)):
        text = config.STUDENTS_LIST[i] + "\t- " + str(rate[i][1]) + "%"
        window.listStudents.addItem(text)
        #window.listStudents.addItem(config.STUDENTS_LIST[i])
        #text = str(rate[i][1]) + "%"
        #window.listRate.addItem(text)
    pass

def selectedStudent(item):
    
    student = item.text().split()[0]
    config.SELECTED_STUDENT = student
    #updateList(student)
    window.lineEdit.setText(student)
    updateDiagram()
    pass

def updateLinkedStudents(student):
    config.SELECTED_STUDENTS.clear()
    if student in config.STUDENTS_LIST:
        currentIndex = config.STUDENTS_LIST.index(student)
        for i in range(len(config.STUDENTS_LIST)):
            if currentIndex != i and int(config.RESULT_MATRIX[currentIndex][i]) > config.RANGE_PLAG:
                config.SELECTED_STUDENTS.append(config.STUDENTS_LIST[i])

def updateList(student):   
    #rate = findMaxPlag()
    for i in range(len(config.STUDENTS_LIST)):
        window.listStudents.item(i).setBackground(QColor(250, 247, 247)) #!        
        #text = config.STUDENTS_LIST[i] + "\t- " + str(rate[i][1]) + "%"
        window.listStudents.item(i).setText(config.STUDENTS_LIST[i])
        window.listStudents.item(i).setForeground(QColor(62, 48, 51))
        

    if student in config.STUDENTS_LIST:          

        currentIndex = config.STUDENTS_LIST.index(student)
        window.listStudents.item(currentIndex).setBackground(QColor(248, 155, 141))
        maxPlag = max(config.RESULT_MATRIX[currentIndex])
        newRow = student + "\t- " + str(maxPlag) + "%"
        window.listStudents.item(currentIndex).setText(newRow)
        for i in range(len(config.STUDENTS_LIST)):
            if currentIndex != i and int(config.RESULT_MATRIX[currentIndex][i]) >= config.RANGE_PLAG:
                if config.RESULT_MATRIX[currentIndex][i] == maxPlag:
                    window.listStudents.item(i).setForeground(QColor(235, 50, 50))
                    #else: window.listStudents.item(i).setForeground(QColor(250, 130, 130))
                window.listStudents.item(i).setBackground(QColor(231, 214, 212))
                #config.SELECTED_STUDENT = config.STUDENTS_LIST[i]              

                newRow2 = config.STUDENTS_LIST[i] + "\t- " + str(config.RESULT_MATRIX[currentIndex][i]) + "%"
                window.listStudents.item(i).setText(newRow2)                

### file menu
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
            line.append('0')
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

def newDiagram():
    config.FILE_NAME = ""
    filename = QFileDialog.getOpenFileName(None,"Load File","","Text (*.csv);;All Files (*)")[0]
    if filename != '':
        file = open(filename)
        try:
            content = file.read().split('\n') 
            #results = fukingCSVtoSomething(content).split(';') 
            #saveMatrix(results)            
            saveMatrix(CSVtoSomething(content))
        finally:
            file.close()      
    
    #print()
    if len(config.STUDENTS_LIST) > 1 and len(config.STUDENTS_LIST) == len(config.RESULT_MATRIX) and len(config.RESULT_MATRIX) == len(config.RESULT_MATRIX[0]):
        updateDiagram()
    pass
def openDiagram():    
    config.FILE_NAME = QFileDialog.getOpenFileName(None,"Load File","","Text (*.txt);;All Files (*)")[0]
    if config.FILE_NAME != "":
        file = open(config.FILE_NAME)
        try:
            results = file.read().replace('\n','').split(';') 
            saveMatrix(results)
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
def changeColor(red, green, blue):
    if red + 20 > 255: red = 100
    else: red = red + 20
    if blue - 10 < 170: blue = 240
    else: blue = blue - 10
    if green + 20 > 255: green = 120
    else: green = green + 20
    return red, green, blue
def findMaxPlag():    
    listRate = []
    for i in range(len(config.STUDENTS_LIST)):        
        listRate.append([config.STUDENTS_LIST[i], int(max(config.RESULT_MATRIX[i])), i]) 
    return listRate
def checkText(studentName, x, y):
    for i in range(len(studentName)):
        student = studentName[i][1]
        xt1 = studentName[i][0].x()
        xt2 = studentName[i][0].x() + len(student)*10
        yt1 = studentName[i][0].y() + 5
        yt2 = yt1 + 25 #24?            

        if xt1 < x < xt2 and yt1 < y < yt2:
            return student
    return ""
def selectNode(name): 
    if name != "" and name in config.STUDENTS_LIST:
        config.SELECTED_STUDENT = name
        window.lineEdit.clear
        window.lineEdit.setText(name)
        updateDiagram() 
    
# # #
#
#
# Diagrams...
#
#
# # #


class GraphicsSceneBubbleChart(QGraphicsScene):
    def __init__(self, x, y, width, height, parent=None):
        QGraphicsScene.__init__(self, x, y, width, height, parent)   
        self.Nodes = []
        self.studentName = []
        self.srudentsInRange = []
        self.drawBubbleChart()

    def mousePressEvent(self, event):
        x = event.scenePos().x()
        y = event.scenePos().y()
        clearLine()
        selectNode(checkText(self.studentName, x, y))
       
        for i in range(len(self.Nodes)):
            if self.Nodes[i].name in self.srudentsInRange:
                xn1 = self.Nodes[i].x 
                xn2 = self.Nodes[i].x + self.Nodes[i].width 
                yn1 = self.Nodes[i].y 
                yn2 = self.Nodes[i].y + self.Nodes[i].height   
                if xn1 < x < xn2 and yn1 < y < yn2:                
                    selectNode(self.Nodes[i].name)

    def drawBubbleChart(self):
        if len(config.STUDENTS_LIST) > 1:
            pen=QPen(Qt.white)
            #brush=QBrush((QColor(160, 205, 225, 40)))

            if self.width() > self.height(): minNodeRadius = self.height()/(len(config.STUDENTS_LIST)+2)
            else: minNodeRadius = self.width()/(len(config.STUDENTS_LIST) + 2)
   
            circleCenterX = self.width()/2
            circleCenterY = self.height()/2  

        
            maxPlagList = findMaxPlag()    
            MrPlagiarism = sorted(maxPlagList, key=itemgetter(1), reverse=True)  
    
            stage = MrPlagiarism[0][1]        
            group = 1 #?
            for i in range(len(config.STUDENTS_LIST)):
                n = 0
                for j in range(len(config.STUDENTS_LIST)):
                    if MrPlagiarism[i][1] == MrPlagiarism[j][1]:
                        n = n + 1
                if n > group : group = n

            step = 0
            if MrPlagiarism[-1][1] >= config.RANGE_PLAG and MrPlagiarism[0][1] >= MrPlagiarism[-1][1]:
                step = int((MrPlagiarism[0][1] - MrPlagiarism[-1][1])/10) + 1
            elif MrPlagiarism[-1][1] <= config.RANGE_PLAG and MrPlagiarism[0][1] >= config.RANGE_PLAG:
                step = int((MrPlagiarism[0][1] - config.RANGE_PLAG)/10) + 1   
    
            for i in range(len(config.STUDENTS_LIST)):        
                if MrPlagiarism[i][1] > 0:
                    nodeWidth = nodeHeight = minNodeRadius*MrPlagiarism[i][1]/18 #20?
                    if step < len(config.STUDENTS_LIST)/2: nodeWidth = nodeHeight = minNodeRadius*MrPlagiarism[i][1]/14
                    if step < len(config.STUDENTS_LIST)/4: nodeWidth = nodeHeight = minNodeRadius*MrPlagiarism[i][1]/12
                else:nodeWidth = nodeHeight = minNodeRadius        
                self.Nodes.append(Node(MrPlagiarism[i][0], nodeWidth, nodeHeight))


            pW = self.width()/12
            pH = self.height()/12
            scale = (self.width() - pW)/(step + 1)
            self.addLine(scale/3, self.height() - pH, self.width() - scale/3 - pW, self.height() - pH, pen)
    
            for i in range(step):        
                self.addLine(scale*(i + 1), self.height() - pH - 5, scale*(i + 1), self.height() - pH + 5, pen)
    
            red, green, blue = (100, 215, 255)
            theta = 2*math.pi / (group)
            groupCount = 0
            nodeBias = step
            self.srudentsInRange.clear        

            for i in range(len(config.STUDENTS_LIST)):
                dx, dy = (0, 0)
                level = self.height()/len(config.STUDENTS_LIST)
                redp, greenp, bluep, ap = (242, 244, 255, 180)
                a = 180
                widthp = 1
                if config.CHESS:
                    if i% 2 == 0: red, green, blue, a = (95, 160, 200, 220) 
                    else: red, green, blue, a = (245, 145, 130, 220)

                if config.SELECTED_STUDENT != "":

                    if config.SELECTED_STUDENT == self.Nodes[i].name:
                        red, green, blue, a = (254, 113, 105, 200)
                    else: red, green, blue, a = (102, 151, 180, 150) 
            
                    if config.STUDENTS_LIST[MrPlagiarism[i][2]] in config.SELECTED_STUDENTS:
                        redp, greenp, bluep, ap = (254, 132, 121, 255)
                        widthp = 3
                    elif config.STUDENTS_LIST[MrPlagiarism[i][2]] == config.SELECTED_STUDENT:
                        redp, greenp, bluep, ap = (255, 184, 171, 255)
                        widthp = 4
                    else: 
                        redp, greenp, bluep, ap = (120, 170, 200, 255)
                        widthp = 1              

                if len(config.HIDED_STUDENTS) > 0:
                    if self.Nodes[i].name in config.HIDED_STUDENTS: 
                        a, ap = (10, 10)

                colorBrush = QColor(red, green, blue, a)
                nodePen = QPen(QColor(redp, greenp, bluep, ap), widthp)

                if MrPlagiarism[i][1] >= config.RANGE_PLAG and (MrPlagiarism[i][1] > 0 or config.SHOW_LINKLESS):
                    if MrPlagiarism[i][1] < stage: 
                        nodeBias = step - (int(MrPlagiarism[0][1]/10) - int(MrPlagiarism[i][1]/10))
                        stage = MrPlagiarism[i][1]
                        groupCount = 0            
                    else: 
                        groupCount = groupCount + 1
                        radius =  self.Nodes[i].width/5
                        angle = groupCount * theta
                        dx = int(radius* math.cos(angle))
                        dy = int(radius* math.sin(angle))

                    if step > 0:
                        nodeY = self.height() - pH*2 - level*(int(MrPlagiarism[i][1]/10))/2 - self.Nodes[i].height/2 - dy
                        nodeX = scale*nodeBias - self.Nodes[i].width/2 - dx
                        if int(MrPlagiarism[i][1]%10) > 0:
                            nodeX = nodeX + scale*int(MrPlagiarism[i][1]%10)/10
                
                        self.Nodes[i].setX(nodeX)
                        self.Nodes[i].setY(nodeY)

                        self.addEllipse(self.Nodes[i].x, self.Nodes[i].y, self.Nodes[i].width, self.Nodes[i].height, nodePen, QBrush(colorBrush))
                        self.srudentsInRange.append(self.Nodes[i].name)
                        red, green, blue = changeColor(red, green, blue)
         
            textLevel = []
            for i in range(len(self.Nodes)):
                redt, greent, bluet, at = (250, 240, 240, 255)
                redts, greents, bluets, ats = (75, 100, 125, 150)
                if MrPlagiarism[i][1] >= config.RANGE_PLAG and step > 0 and (MrPlagiarism[i][1] > 0 or config.SHOW_LINKLESS):
              
                    if config.SELECTED_STUDENT != "":
                        if  self.Nodes[i].name == config.SELECTED_STUDENT:
                            redt, greent, bluet, at = (255, 233, 224, 255)
                        elif self.Nodes[i].name in config.SELECTED_STUDENTS: 
                            redt, greent, bluet, at = (254, 113, 105, 255)
                        else: redt, greent, bluet, at = (102, 151, 180, 255)
                    else: redt, greent, bluet, at = (250, 240, 240, 255)

                    if len(config.HIDED_STUDENTS) > 0:
                        if self.Nodes[i].name in config.HIDED_STUDENTS: 
                            at = 20
                            ats = 20
                            if self.Nodes[i].name == config.SELECTED_STUDENT:
                                redt, greent, bluet, at = (215, 115, 105, 50)
                    
                    textColor = QColor(redt, greent, bluet, at)
                    textShadowColor = QColor(redts, greents, bluets, ats)
                    if config.SHOW_NAMES:
                        student = self.Nodes[i].name
                        if len(student) > 12:
                            student = student[0:12] + "..."
                        font = 12
                        if config.SHOW_RARE:
                            if len(student) + 6 > 12:
                                student = student[0:10] + "..."
                            font = 10
                            student = student + ' - ' +  str(MrPlagiarism[i][1]) + '%'                
                
                        textX = self.Nodes[i].x + self.Nodes[i].width/5
                        textY = self.Nodes[i].y

                        textLevel = sorted(textLevel, key=itemgetter(0))
                        for j in range(len(textLevel)):
                            if abs(textX - textLevel[j][1]) < self.Nodes[i].width and abs(textY - textLevel[j][0]) < font: textY = textY + font*2                
                
                        indent = 10
                        if textX < indent: textX = indent
                        if textX + len(student)*(font-3) > self.width(): textX = self.width() - len(student)*(font-3) - indent

                        if textY < indent: textY = indent
                        if textY + font > self.height(): textY = self.height() - font - indent

                        textLevel.append([textY, textX])

                        textShadow = self.addText(student, QFont("Times", font))
                        textShadow.setPos(textX+1, textY+1)          
                        textShadow.setDefaultTextColor(textShadowColor)

                        text = self.addText(student, QFont("Times", font))
                        text.setPos(textX, textY)          
                        text.setDefaultTextColor(textColor)
                        self.studentName.append([text, self.Nodes[i].name])
        pass
class GraphicsSceneNetwork(QGraphicsScene):
    def __init__(self, x, y, width, height, parent=None):
        QGraphicsScene.__init__(self, x, y, width, height, parent) 
        self.Nodes = []
        self.studentName = []
        self.drawNetwork()

    def mousePressEvent(self, event):
        x = event.scenePos().x()
        y = event.scenePos().y()
        print(x, y)

    def drawNetwork(self):
        #if len(config.STUDENTS_LIST) > 1:
        pass
class GraphicsSceneChordDiagram2(QGraphicsScene):
    def __init__(self, x, y, width, height, parent=None):
        QGraphicsScene.__init__(self, x, y, width, height, parent)    
        self.listNodes = []
        self.studentName = []
        self.drawChordDiagram2()

    def mousePressEvent(self, event):
        x = event.scenePos().x()
        y = event.scenePos().y()
        #print(self.Nodes[0].width, self.Nodes[0].width)
        clearLine()
        selectNode(checkText(self.studentName, x, y))
        
        for i in range(len(self.listNodes)):
            if self.listNodes[i][0].x > self.listNodes[i][9].x:
                xn1 = self.listNodes[i][9].x
                xn2 = self.listNodes[i][0].x
            else:
                xn1 = self.listNodes[i][0].x
                xn2 = self.listNodes[i][9].x
            
            if self.listNodes[i][0].y > self.listNodes[i][9].y:
                yn1 = self.listNodes[i][9].y
                yn2 = self.listNodes[i][0].y
            else:
                yn1 = self.listNodes[i][0].y
                yn2 = self.listNodes[i][9].y            

            if xn1 < x < xn2 and yn1 < y < yn2:
                selectNode(self.listNodes[i][0].name) 
                

    def drawChordDiagram2(self):
        maxPlagList = findMaxPlag()
       
        pen=QPen(Qt.white)
        brush=QBrush((QColor(170, 212, 142)))

        circleCenterX = self.width()/2
        circleCenterY = self.height()/2

        #self.addEllipse(circleCenterX,  circleCenterY,  20,  20, QPen(QColor(254, 234, 230)), QBrush(QColor(255, 255, 255)))

        radius = findRadius(self.width(), self.height()) + 40 #...40?
        perimeter = findPerimeter(radius)

        #########################
    
        nodeWidth = perimeter / len(config.STUDENTS_LIST) / 12
        nodeHeight = perimeter / len(config.STUDENTS_LIST) / 12
    
        #chordDiagram2Scene.addEllipse(circleCenterX, circleCenterY, nodeWidth, nodeHeight, pen, brush)
    
        theta = 2*math.pi / len(config.STUDENTS_LIST)/12        
        step = 0

        for i in range(len(config.STUDENTS_LIST)):
            Nodes = []    
        
            for j in range(12):
                Nodes.append(Node(config.STUDENTS_LIST[i], nodeWidth, nodeHeight))
                angle =  step* theta
                dx = int(radius * math.cos(angle))
                dy = int(radius * math.sin(angle))

                Nodes[j].setX(circleCenterX + dx)
                Nodes[j].setY(circleCenterY + dy) 

                step = step + 1
        
            self.listNodes.append(Nodes)

            red, green, blue, a = redl, greenl, bluel, al = (140, 140, 160, 255)               
            notedList = [] 
        if len(config.STUDENTS_LIST) > 1:
            redp, greenp, bluep, ap = (255, 250, 250, 255)
            for i in range(len(self.listNodes)):            
                notedList.append(config.STUDENTS_LIST[i])                  
                for t in range(10):
                                   
                    x1 = self.listNodes[i][t].x + self.listNodes[i][t].width/2
                    y1 = self.listNodes[i][t].y + self.listNodes[i][t].width/2
           
                    if config.RANGE_PLAG <= maxPlagList[i][1] or config.SHOW_LINKLESS:
                        for j in range(len(self.listNodes)):
                            if i != j and float(config.RESULT_MATRIX[i][j]) > 0 and t < float(config.RESULT_MATRIX[i][j])/10 and config.STUDENTS_LIST[j] not in notedList:

                                penWidth = self.listNodes[i][t].width/3                    

                                x2 = self.listNodes[j][t].x + self.listNodes[i][t].width/2
                                y2 = self.listNodes[j][t].y + self.listNodes[i][t].width/2
                    
                                path1 = QPainterPath()
                                path2 = QPainterPath()
                                path1.clear  
                                path2.clear
                                al, a = (255, 255)

                                if float(config.RESULT_MATRIX[i][j]) <= config.RANGE_PLAG: 
                                    al = al - int(config.RANGE_PLAG)*2 - 40
                                                        
                                if config.CHESS:
                                    if i% 2 == 0: redl, greenl, bluel, al = (95, 160, 200, al) 
                                    else: redl, greenl, bluel, al = (245, 145, 130, al)

                                if config.SELECTED_STUDENT != "":
                                    if (config.SELECTED_STUDENT == self.listNodes[i][t].name and self.listNodes[j][t].name in config.SELECTED_STUDENTS) or (config.SELECTED_STUDENT== self.listNodes[j][t].name and self.listNodes[i][t].name in config.SELECTED_STUDENTS):
                                        redl, greenl, bluel, al = (226, 113, 105, al)
                                    else: redl, greenl, bluel, al = (102, 151, 180, al - 200)                                   

                                if len(config.HIDED_STUDENTS) > 0:
                                    if self.listNodes[i][t].name in config.HIDED_STUDENTS or self.listNodes[j][t].name in config.HIDED_STUDENTS: al = 5

                                if config.RANGE_PLAG >= maxPlagList[j][1] and not config.SHOW_LINKLESS: al = 0


                                colorLine = QColor(redl, greenl, bluel, al)

                                path1.moveTo(x1 + self.listNodes[i][t].width/4, y1 + self.listNodes[i][t].width/4)
                                path2.moveTo(x1, y1)

                                x1a = x1 + (circleCenterX - x1)/6
                                y1a = y1 + (circleCenterY - y1)/6

                                path1.lineTo(x1a, y1a)
                                path2.lineTo(x1a, y1a)

                                x2a = x2 + (circleCenterX - x2)/6
                                y2a = y2 + (circleCenterY - y2)/6

                                ctrlX1 = x1a + (circleCenterX - x1a)/2
                                ctrlY1 = y1a + (circleCenterY - y1a)/2
                                ctrlX2 = x2a + (circleCenterX - x2a)/2
                                ctrlY2 = y2a + (circleCenterY - y2a)/2

                                path1.cubicTo(ctrlX1, ctrlY1,  ctrlX2, ctrlY2,  x2a, y2a)
                                path1.lineTo(x2, y2)

                                path2.moveTo(x2a, y2a)
                                path2.lineTo(x2 + self.listNodes[i][t].width/4, y2 + self.listNodes[i][t].width/4)

                                self.addPath(path1, QPen(colorLine, penWidth))
                                self.addPath(path2, QPen(colorLine, penWidth))
                                #chordDiagram2Scene.addLine(x1, y1, x2, y2, QPen(color, penWidth))

                            if 140 + j*5 > 255: 
                                greenl = 140 + j*2
                                if 140 + j*2 > 255: greenl = 140 + j
                                #???
                            else: greenl = 140 + j*5 
                        #red, green, blue, a = (red, green, blue, 255)
                        
                        if config.CHESS:
                             if i% 2 == 0: red, green, blue, a = (95, 160, 200, a) 
                             else: red, green, blue, a = (245, 145, 130, a)
                
                        if config.SELECTED_STUDENT != "":
                            if config.SELECTED_STUDENT== self.listNodes[i][t].name:
                                red, green, blue, a = (254, 113, 105, a)
                            elif self.listNodes[i][t].name in config.SELECTED_STUDENTS: 
                                red, green, blue, a = (205, 140, 134, a)
                            else: red, green, blue, a = (102, 151, 180, a)
               
                        
                        if len(config.HIDED_STUDENTS) > 0:
                            if self.listNodes[i][t].name in config.HIDED_STUDENTS:
                                red, green, blue, a = (65, 75, 90, 255)
                                ap = 50
                                if config.SELECTED_STUDENT != "":
                                    if config.SELECTED_STUDENT ==  self.listNodes[i][t].name:                               
                                        red, green, blue, a = (95, 65, 70, 255) 
                            else: ap = 255

                        #if config.RANGE_PLAG <= maxPlagList[i][1] or config.SHOW_LINKLESS:
                        colorBrush = QColor(red, green, blue, a)
                        colorPen = QColor(redp, greenp, bluep, ap)
                        self.addEllipse(self.listNodes[i][t].x, self.listNodes[i][t].y, self.listNodes[i][t].width, self.listNodes[i][t].height, QPen(colorPen), QBrush(colorBrush))
         
                if redl + 20 > 255: redl = 90
                else: redl = redl + 20   
                red, green, blue = (redl, greenl, bluel)
            
            for i in range(len(self.listNodes)): 
                redt, greent, bluet, at = (250, 200, 190, 255)
                if config.SELECTED_STUDENT != "":
                    if config.SELECTED_STUDENT== self.listNodes[i][t].name:
                        redt, greent, bluet, at = (254, 113, 105, 255)
                    elif self.listNodes[i][t].name in config.SELECTED_STUDENTS: 
                        redt, greent, bluet, at = (205, 140, 134, 255)
                    else: redt, greent, bluet, at = (102, 151, 180, 255)
          

                if len(config.HIDED_STUDENTS) > 0:
                    if self.listNodes[i][t].name in config.HIDED_STUDENTS: 
                        at = 50
                        if config.SELECTED_STUDENT != "":
                            if config.SELECTED_STUDENT ==  self.listNodes[i][t].name: at = 50  
                        
                
                textColor = QColor(redt, greent, bluet, at)
                if config.SHOW_NAMES and (config.RANGE_PLAG <= maxPlagList[i][1] or config.SHOW_LINKLESS):
                    student = self.listNodes[i][0].name
                    font = 12
                    if len(student) > 12:
                        student = student[0:12] + "..."                
                    if config.SHOW_RARE:
                        if len(student) + 6 > 12:
                            student = student[0:10] + "..."
                            font = 9
                            student = student + ' - ' +  str(maxPlagList[i][1]) + '%'
                
                    textWidth = len(student)*(font - 3)
                    textX = self.listNodes[i][3].x
                    textY = self.listNodes[i][3].y
                
                    if circleCenterX - textX >= 0 and circleCenterY - textY >= 0:
                        textX = textX - textWidth
                        textY = textY - self.listNodes[i][4].width*3 - font*2
                    elif circleCenterX - textX >= 0 and circleCenterY - textY <= 0:
                        textX = textX - textWidth
                        textY = textY + self.listNodes[i][4].width*3 - font*2

                    elif circleCenterX - textX <= 0 and circleCenterY - textY <= 0:
                        textX = textX + textWidth/5
                        textY = textY + self.listNodes[i][4].width*3 - font*2
                    elif circleCenterX - textX <= 0 and circleCenterY - textY >= 0:
                        textX = textX + textWidth/5
                        textY = textY - self.listNodes[i][4].width*3 - font*2

                    indent = 10
                    if textX < indent: textX = indent
                    if textX + len(student)*(font-3) > self.width(): textX = self.width() - len(student)*(font-3) - indent

                    if textY < indent: textY = indent
                    if textY + font > self.height(): textY = self.height() - font - indent

                    textShadowColor = QColor(75, 85, 95, 70)
                    textShadow = self.addText(student, QFont("Times", font))
                    textShadow.setPos(textX+1, textY+1)          
                    textShadow.setDefaultTextColor(textShadowColor)

                    text = self.addText(student, QFont("Times", font))
                    text.setPos(textX, textY)
                    text.setDefaultTextColor(textColor)
                    self.studentName.append([text, self.listNodes[i][0].name]) 
                    
class GraphicsSceneChordDiagram(QGraphicsScene):   

    def __init__(self, x, y, width, height, parent): 
        QGraphicsScene.__init__(self, x, y, width, height, parent)   

        self.Nodes = []
        self.studentName = []
        self.drawChordDiagram()    

    def mousePressEvent(self, event):
        x = event.scenePos().x()
        y = event.scenePos().y()
        #print(self.Nodes[0].width, self.Nodes[0].width)
        clearLine()
        selectNode(checkText(self.studentName, x, y))

        for i in range(len(self.Nodes)):
            xn1 = self.Nodes[i].x - self.Nodes[i].width/2
            xn2 = self.Nodes[i].x + self.Nodes[i].width - self.Nodes[i].width/2
            yn1 = self.Nodes[i].y - self.Nodes[i].height/2
            yn2 = self.Nodes[i].y + self.Nodes[i].height - self.Nodes[i].height/2

            #self.addRect(xt1, yt1, xt2 -  xt1,  20, QPen(Qt.white), QBrush((QColor(160, 205, 225, 70))))

            if xn1 < x < xn2 and yn1 < y < yn2:
                selectNode(self.Nodes[i].name)            

    def drawChordDiagram(self):
        maxPlagList = findMaxPlag()       
        #self.width
        #TODO
        #imgWidth, imgHeight = window.chordDiagramView.size()
        #print(window.chordDiagramView.width())                

        circleCenterX = self.width()/2
        circleCenterY = self.height()/2

        #self.addEllipse(circleCenterX,  circleCenterY,  20,  20, QPen(QColor(254, 234, 230)), QBrush(QColor(255, 255, 255)))
        #self.addEllipse(self.width() - 10,  circleCenterY,  20,  20, QPen(QColor(254, 234, 230)), QBrush(QColor(255, 255, 255)))
        #self.addEllipse(10,  circleCenterY,  20,  20, QPen(QColor(254, 234, 230)), QBrush(QColor(255, 255, 255)))
        #self.addEllipse(circleCenterX,  10,  20,  20, QPen(QColor(254, 234, 230)), QBrush(QColor(255, 255, 255)))
        #self.addEllipse(circleCenterX,  self.height() - 10,  20,  20, QPen(QColor(254, 234, 230)), QBrush(QColor(255, 255, 255)))
        
        radius = findRadius(self.width(), self.height())
        perimeter = findPerimeter(radius)

        #config.STUDENTS_LIST
        #config.RESULT_MATRIX
                
        nodeWidth = perimeter / len(config.STUDENTS_LIST) / 3
        nodeHeight = perimeter / len(config.STUDENTS_LIST) / 3

        theta = 2*math.pi / len(config.STUDENTS_LIST)

        #transforms = []
        if len(config.STUDENTS_LIST) > 1:
            for i in range(len(config.STUDENTS_LIST)):
                self.Nodes.append(Node(config.STUDENTS_LIST[i], nodeWidth, nodeHeight))

                angle = i * theta
                dx = int(radius * math.cos(angle))
                dy = int(radius * math.sin(angle))

                #self.Nodes[i].setX(circleCenterX + dx - self.Nodes[i].width/2)
                #self.Nodes[i].setY(circleCenterY + dy - self.Nodes[i].height/2)       
                
                self.Nodes[i].setX(circleCenterX + dx)
                self.Nodes[i].setY(circleCenterY + dy)  
        
            for i in range(len(self.Nodes)):

                x1 =  self.Nodes[i].x
                y1 =  self.Nodes[i].y

                for j in range(len( self.Nodes)):
                    if i != j and float(config.RESULT_MATRIX[i][j]) > 0 and (config.RANGE_PLAG <= maxPlagList[i][1] or config.SHOW_LINKLESS):
                
                        penWidth = float(config.RESULT_MATRIX[i][j])/10
                        x2 =  self.Nodes[j].x
                        y2 =  self.Nodes[j].y
                        red, green, blue, a = (238, 151, 142, 240)

                        if penWidth >= config.RANGE_PLAG/10:
                            red, green, blue, a = (238, 151, 142, 240)
                        else:
                            red, green, blue, a = (131, 118, 122, 50)

                        if config.CHESS:
                            if i% 2 == 0: red, green, blue = (95, 160, 200) 
                            else: red, green, blue = (245, 145, 130) 

                        if config.SELECTED_STUDENT != "":
                            if (config.SELECTED_STUDENT ==  self.Nodes[i].name and self.Nodes[j].name in config.SELECTED_STUDENTS) or (config.SELECTED_STUDENT==  self.Nodes[j].name and  self.Nodes[i].name in config.SELECTED_STUDENTS):
                                red, green, blue, a = (226, 113, 105, 255)  
                            else: red, green, blue, a = (102, 151, 180, 50) 
                        #scene.addLine(x1, y1, x2, y2, QPen(color, penWidth))
                        if len(config.HIDED_STUDENTS) > 0:
                            if self.Nodes[i].name in config.HIDED_STUDENTS or self.Nodes[j].name in config.HIDED_STUDENTS: a = 5

                        color = QColor(red, green, blue, a)
                        path = QPainterPath()
                        path.clear                
                        path.moveTo(x1, y1)
                        #TODO Nodes[j].getWidth()?
                        ctrlX1 = x1 + (circleCenterX -  self.Nodes[j].width - x1)/3
                        ctrlY1 = y1 + (circleCenterY -  self.Nodes[j].width - y1)/3
                        ctrlX2 = x2 + (circleCenterX -  self.Nodes[j].width - x2)/3
                        ctrlY2 = y2 + (circleCenterY -  self.Nodes[j].width - y2)/3
                        path.cubicTo(ctrlX1, ctrlY1,  ctrlX2, ctrlY2,  x2, y2)

                        if config.RANGE_PLAG <= maxPlagList[j][1] or config.SHOW_LINKLESS:
                            self.addPath(path, QPen(color, penWidth))     
  
            for i in range(len(self.Nodes)):
                redt, greent, bluet, at = (254, 234, 230, 255)
                red, green, blue, a = (160, 205, 225, 255)
                
                if config.RANGE_PLAG <= maxPlagList[i][1] or config.SHOW_LINKLESS:
                    if config.CHESS:
                        if i% 2 == 0: red, green, blue = (95, 160, 200) 
                        else: red, green, blue = (245, 145, 130)
            
                    if config.SELECTED_STUDENT != "":
                        if config.SELECTED_STUDENT ==  self.Nodes[i].name:
                            red, green, blue = redt, greent, bluet = (254, 113, 105)                        
                        elif self.Nodes[i].name in config.SELECTED_STUDENTS: 
                            red, green, blue = redt, greent, bluet = (205, 140, 134)                         
                        else: red, green, blue = redt, greent, bluet = (102, 151, 180)
                        
                    if len(config.HIDED_STUDENTS) > 0:
                            if self.Nodes[i].name in config.HIDED_STUDENTS:
                                red, green, blue, a = (65, 75, 90, 255)
                                if config.SELECTED_STUDENT != "":
                                    if config.SELECTED_STUDENT ==  self.Nodes[i].name:                               
                                        red, green, blue, a = (95, 65, 70, 255)                                
                                at = 50

                    brush=QBrush(QColor(red, green, blue, a))
                    textColor = QColor(redt, greent, bluet, at)   
                    pen=QPen(QColor(254, 234, 230, at))
                    
                    self.addEllipse( self.Nodes[i].x -  self.Nodes[i].width/2,  self.Nodes[i].y -  self.Nodes[i].height/2,  self.Nodes[i].width,  self.Nodes[i].height, pen, brush)
        
                    if config.SHOW_NAMES:
                        font = 12
                        student =  self.Nodes[i].name
                        if len(student) > 12:
                            student = student[0:12] + "..."

                        if config.SHOW_RARE:
                            if len(student) + 6 > 12:
                                student = student[0:10] + "..."
                            font = 10
                            student = student + ' - ' +  str(maxPlagList[i][1]) + '%'    
                                
                        textWidth = len(student)*(font-3)
                        textX =  self.Nodes[i].x
                        textY =  self.Nodes[i].y
                #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        if circleCenterX - textX - self.Nodes[i].width >= 0:
                            textX = textX - textWidth
                        else: textX = textX + self.Nodes[i].width/2
                        
                        if circleCenterY - textY >= 0:
                            textY = textY -  self.Nodes[i].width -  self.Nodes[i].width/3
                        else: textY = textY +  self.Nodes[i].width/3  
                        
                        indent = 10
                        if textX < indent: textX = indent
                        if textX + len(student)*(font-3) > self.width(): textX = self.width() - len(student)*(font-3) - indent

                        if textY < indent: textY = indent
                        if textY + font > self.height(): textY = self.height() - font - indent

                        textShadowColor = QColor(75, 85, 95, 70)
                        textShadow = self.addText(student, QFont("Times", font))
                        textShadow.setPos(textX+1, textY+1)          
                        textShadow.setDefaultTextColor(textShadowColor)

                        text = self.addText(student, QFont("Times", font))                    
                        text.setPos(textX, textY)                 
                        text.setDefaultTextColor(textColor)   
                        self.studentName.append([text, self.Nodes[i].name])

class GraphicsView(QGraphicsView):
    def __init__(self):
        super(GraphicsView, self).__init__()

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding )
        self.setAutoFillBackground(True)
        self.setMinimumSize(700, 550)
        self.setStyleSheet('QGraphicsView {background-color: rgba(54, 64, 80, 255); border-width:2px; border-style:solid;border-top-color: qlineargradient(spread:pad, x1:0.5, y1:0.6, x2:0.5, y2:0.4, stop:0 rgba(54, 64, 80, 120), stop:1 rgba(20, 20, 25,120));border-right-color: qlineargradient(spread:pad, x1:0.4, y1:0.5, x2:0.6, y2:0.5, stop:0 rgba(123, 209, 201, 255), stop:1 rgba(205, 177, 168, 220));border-left-color: qlineargradient(spread:pad, x1:0.4, y1:0.5, x2:0.6, y2:0.5, stop:0 rgba(138, 140, 152, 255), stop:1 rgba(184, 173, 182, 120));border-bottom-color: qlineargradient(spread:pad, x1:0.6, y1:0.5, x2:0.4, y2:0.5, stop:0 rgba(184, 173, 182, 180), stop:1 rgba(212, 199, 205, 180)); border-bottom-width: 3px; border-right-width: 3px;}')
        self.setRenderHints(QPainter.Antialiasing | QPainter.LosslessImageRendering | QPainter.SmoothPixmapTransform | QPainter.TextAntialiasing);
        #self.property()
        #QColor(54, 64, 80, 255)


    def resizeEvent(self, event):
        updateDiagram()
        super(GraphicsView, self).resizeEvent(event)

def drawDiagrams(): 
    #chordDiagramView = GraphicsView()
    #window.gridLayout_chord.addWidget(chordDiagramView, 10, 10)

    width = ChordDiagram2View.width() - 10
    height = ChordDiagramView.height() - 10
    chordDiagramScene = GraphicsSceneChordDiagram(0, 0, width, height, ChordDiagramView)
    ChordDiagramView.setScene(chordDiagramScene)

    width = ChordDiagram2View.width() - 10
    height = ChordDiagram2View.height() - 10
    chordDiagram2Scene = GraphicsSceneChordDiagram2(0, 0, width, height, ChordDiagram2View)
    ChordDiagram2View.setScene(chordDiagram2Scene)

    width = NetworkDiagramView.width() - 10
    height = NetworkDiagramView.height() - 10
    networkScene = GraphicsSceneNetwork(0, 0, width, height, NetworkDiagramView)
    NetworkDiagramView.setScene(networkScene)

    width = BubbleDiagramView.width() - 10
    height = BubbleDiagramView.height() - 10
    bubbleChartScene = GraphicsSceneBubbleChart(0, 0, width, height, BubbleDiagramView)
    BubbleDiagramView.setScene(bubbleChartScene)

    #chordDiagram2Scene = GraphicsSceneChordDiagram2(0, 0, imgWidth, imgHeight, window.chordDiagram2View)
    #networkScene = GraphicsSceneNetwork(0, 0, imgWidth, imgHeight, window.networkView)
    #bubbleChartScene = GraphicsSceneBubbleChart(0, 0, imgWidth, imgHeight, window.bubbleChartView)

    #imgWidth = window.chordDiagramView.width() - 10
    #imgHeight = window.chordDiagramView.height() - 10

    #chordDiagramScene = GraphicsSceneChordDiagram(0, 0,   window.chordDiagramView)
    #chordDiagram2Scene = GraphicsSceneChordDiagram2(0, 0, imgWidth, imgHeight, window.chordDiagram2View)
    #networkScene = GraphicsSceneNetwork(0, 0, imgWidth, imgHeight, window.networkView)
    #bubbleChartScene = GraphicsSceneBubbleChart(0, 0, imgWidth, imgHeight, window.bubbleChartView)

    #chordDiagramScene.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


    #chordDiagramScene.update
    #chordDiagramView = GraphicsView(window.chordDiagramView, window.chordDiagramView.parent)

    #chordDiagramView.setScene(chordDiagramScene)
    #window.chordDiagramView.setScene(chordDiagramScene)
    #window.chordDiagram2View.setScene(chordDiagram2Scene)
    #window.networkView.setScene(networkScene)
    #window.bubbleChartView.setScene(bubbleChartScene)
    pass

class Node():
    def __init__(self, name, imgWidth, imgHeight):
        self.name = name
        self.width = imgWidth/5*4
        self.height = imgHeight/5*4

    def setX(self, x):
        self.x = x
    def setY(self, y):
        self.y = y

def findRadius(imgWidth, imgHeight):    
    if imgWidth > imgHeight:
        radius = imgHeight
    else: radius = imgWidth

    return radius/3

def findPerimeter(radius):
        return 2 * math.pi * radius
def clearLine():
    #window.lineEdit.setText(student)
    config.SELECTED_STUDENT = ""
    config.SELECTED_STUDENTS.clear()
    window.lineEdit.clear()
    updateList("")
    updateDiagram()
    pass
def showLinks():
    student = window.lineEdit.text()
    if len(student) > 0:
        student = student.split()[0]
        config.SELECTED_STUDENT = student
        updateDiagram()        
    pass
def aboutCat():
    url = "https://memegenerator.net/img/instances/70259669/patience-as-i-catch-up-on-grading.jpg"
    webbrowser.open(url, new=0, autoraise=True)
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
        window.lineEdit.clear()
        updateList("")
        updateDiagram()
    pass
def hideStudent():
    if  config.SELECTED_STUDENT != "" and config.SELECTED_STUDENT in config.STUDENTS_LIST:
        if config.SELECTED_STUDENT not in config.HIDED_STUDENTS:
            config.HIDED_STUDENTS.append(config.SELECTED_STUDENT)

        config.SELECTED_STUDENT = ""
        config.SELECTED_STUDENTS.clear()
        window.lineEdit.clear()
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

    ui_file_name = "vplag.ui"
    ui_file = QFile(ui_file_name)
    if not ui_file.open(QIODevice.ReadOnly):
        print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
        sys.exit(-1)
    loader = QUiLoader()
    window = loader.load(ui_file)
    ui_file.close()
    if not window:
        print(loader.errorString())
        sys.exit(-1)    
    
  
    window.show()   

    window.actionNew.triggered.connect(newDiagram)
    window.actionOpen.triggered.connect(openDiagram)
    window.actionSave.triggered.connect(saveDiagram)    
    window.actionSave_as.triggered.connect(saveAsDiagram)
    window.actionQuit.triggered.connect(window.close)

    window.actionAbout_VPlag.triggered.connect(aboutCat)   
        
    window.rangeSlider.valueChanged.connect(updateDiagram)
    rangeLabel = "Range:  > " + str(window.rangeSlider.value()) + "%"
    window.label_Range.setText(rangeLabel)
      
    window.showNames.stateChanged.connect(updateDiagram)
    window.showLinkless.stateChanged.connect(updateDiagram)
    window.showRate.stateChanged.connect(updateDiagram)
    window.chess.stateChanged.connect(updateDiagram)
    

    window.listStudents.itemClicked.connect(selectedStudent)
    window.Show.clicked.connect(showLinks)
    window.toolButton_cancel.clicked.connect(clearLine)
    window.toolButton_delete.clicked.connect(deleteStudent)
    window.toolButton_closeEye.clicked.connect(hideStudent)
    window.toolButton_openEye.clicked.connect(exposeStudent)

    global ChordDiagramView
    ChordDiagramView = GraphicsView()
    global ChordDiagram2View
    ChordDiagram2View = GraphicsView()
    global NetworkDiagramView
    NetworkDiagramView = GraphicsView()
    global BubbleDiagramView
    BubbleDiagramView = GraphicsView()
   
    window.gridLayout_chord.addWidget(ChordDiagramView, 10, 10)
    window.gridLayout_chord2.addWidget(ChordDiagram2View, 10, 10)
    window.gridLayout_network.addWidget(NetworkDiagramView, 10, 10)
    window.gridLayout_bubble.addWidget(BubbleDiagramView, 10, 10)

    sys.exit(app.exec_())