import sys
import math
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import *
from PySide6 import QtCore, QtGui
from PySide6.QtCore import *
from PySide6 import QtGui
from PySide6.QtGui import *
from operator import *
import config

class Communicate(QObject):
    update = Signal()
    clear =  Signal()

class GraphicsSceneBubbleChart(QGraphicsScene):
    def __init__(self):
        QGraphicsScene.__init__(self)  
        self.signal = Communicate()
        self.Nodes = []
        self.studentName = []
        self.srudentsInRange = []
        #self.drawBubbleChart()

    def mouseDoubleClickEvent(self, event):
        x = event.scenePos().x()
        y = event.scenePos().y()
        self.positionCheck(x, y, True)

    def mousePressEvent(self, event):
        x = event.scenePos().x()
        y = event.scenePos().y()
        self.positionCheck(x, y, False)

    def positionCheck(self, x, y, double):
        hit = False
        name = ""
        #clearLine()
        if len(config.STUDENTS_LIST) > 1 and len(config.RESULT_MATRIX) == len(config.STUDENTS_LIST):
            #self.signal.clear.emit()          
       
            for i in range(len(self.Nodes)):
                if self.Nodes[i].name in self.srudentsInRange:
                    xn1 = self.Nodes[i].x 
                    xn2 = self.Nodes[i].x + self.Nodes[i].width 
                    yn1 = self.Nodes[i].y 
                    yn2 = self.Nodes[i].y + self.Nodes[i].height   
                    if xn1 < x < xn2 and yn1 < y < yn2:                        
                        name = self.Nodes[i].name 

            if name != "": hit = selectNode(name, double)
            else: 
                name = checkText(self.studentName, x, y)
                if name != "": hit = selectNode(name, double)            
                
            if hit: self.signal.update.emit()
            else: self.signal.clear.emit()

    def drawDiagram(self):
        self.clear()
        hint_text = ""

        if len(config.STUDENTS_LIST) <= 1:
            hint_text = "Hint: start a new investigation"
        else:
            if config.SELECTED_STUDENT == "":
                hint_text = "Hint: select one of the nodes - one click to highlight, two clicks to select"
            else:
                if config.WAITING_FOR_ == "":
                    hint_text = "Hint: click on the highlighting node one more time or select another one"
                else:
                    if config.COUPLE == "":
                        hint_text = "Hint: select one more node to start the comparison"


        hintX, hintY = (5, 3)
        hintShadowColor = QColor(75, 85, 95, 70)
        hintShadow = self.addText(hint_text, QFont("Times", 9))
        hintShadow.setPos(hintX  + 1, hintY + 1)          
        hintShadow.setDefaultTextColor(hintShadowColor)

        hintColor = QColor(234, 255, 239, 180)
        hint = self.addText(hint_text, QFont("Times", 9))                    
        hint.setPos(hintX, hintY)                 
        hint.setDefaultTextColor(hintColor)  
        if len(config.STUDENTS_LIST) > 1 and len(config.RESULT_MATRIX) == len(config.STUDENTS_LIST):
            
            self.Nodes = []
            self.studentName = []
            self.srudentsInRange = []
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
            elif MrPlagiarism[-1][1] < config.RANGE_PLAG and MrPlagiarism[0][1] >= config.RANGE_PLAG:
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
                    if config.WAITING_FOR_ == self.Nodes[i].name:
                        red, green, blue, a = (234, 255, 239, a)
                    elif config.SELECTED_STUDENT == self.Nodes[i].name:
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
                        if config.WAITING_FOR_ ==  self.Nodes[i].name:
                            red, green, blue = redt, greent, bluet = (234, 255, 239)
                        elif  self.Nodes[i].name == config.SELECTED_STUDENT:
                            redt, greent, bluet, at = (255, 233, 224, 255)
                        elif self.Nodes[i].name in config.SELECTED_STUDENTS: 
                            redt, greent, bluet, at = (254, 113, 105, 255)
                        else: redt, greent, bluet, at = (102, 151, 180, 255)
                    else: redt, greent, bluet, at = (250, 240, 240, 255)

                    if len(config.HIDED_STUDENTS) > 0:
                        if self.Nodes[i].name in config.HIDED_STUDENTS: 
                            at = 20
                            ats = 20
                            if self.Nodes[i].name == config.SELECTED_STUDENTT:
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
    def __init__(self):
        QGraphicsScene.__init__(self) 
        self.signal = Communicate()
        self.Nodes = []
        self.studentName = []
        #self.drawNetwork()
    def mouseDoubleClickEvent(self, event):
        x = event.scenePos().x()
        y = event.scenePos().y()
        self.positionCheck(x, y, True)

    def mousePressEvent(self, event):
        x = event.scenePos().x()
        y = event.scenePos().y()
        self.positionCheck(x, y, False)

    def positionCheck(self, x, y, double):
        hit = False
        name = ""
        #if len(config.STUDENTS_LIST) > 1 and len(config.RESULT_MATRIX) == len(config.STUDENTS_LIST):
            #self.signal.update.emit()

    def drawDiagram(self):
        self.clear()
        hint_text = ""

        if len(config.STUDENTS_LIST) <= 1:
            hint_text = "Hint: start a new investigation"
        else:
            if config.SELECTED_STUDENT == "":
                hint_text = "Hint: select one of the nodes - one click to highlight, two clicks to select"
            else:
                if config.WAITING_FOR_ == "":
                    hint_text = "Hint: click on the highlighting node one more time or select another one"
                else:
                    if config.COUPLE == "":
                        hint_text = "Hint: select one more node to start the comparison"


        hintX, hintY = (5, 3)
        hintShadowColor = QColor(75, 85, 95, 70)
        hintShadow = self.addText(hint_text, QFont("Times", 9))
        hintShadow.setPos(hintX  + 1, hintY + 1)          
        hintShadow.setDefaultTextColor(hintShadowColor)

        hintColor = QColor(234, 255, 239, 180)
        hint = self.addText(hint_text, QFont("Times", 9))                    
        hint.setPos(hintX, hintY)                 
        hint.setDefaultTextColor(hintColor)  
        #if len(config.STUDENTS_LIST) > 1 and len(config.RESULT_MATRIX) == len(config.STUDENTS_LIST):
            #self.Nodes = []
            #self.studentName = []
        #if len(config.STUDENTS_LIST) > 1:
        pass
class GraphicsSceneChordDiagram2(QGraphicsScene):
    def __init__(self):
        QGraphicsScene.__init__(self) 
        self.signal = Communicate()
        self.listNodes = []
        self.studentName = []
        #self.drawChordDiagram2()

    def mouseDoubleClickEvent(self, event):
        x = event.scenePos().x()
        y = event.scenePos().y()
        self.positionCheck(x, y, True)

    def mousePressEvent(self, event):
        x = event.scenePos().x()
        y = event.scenePos().y()
        self.positionCheck(x, y, False)

    def positionCheck(self, x, y, double):
        hit = False
        name = ""

        if len(config.STUDENTS_LIST) > 1 and len(config.RESULT_MATRIX) == len(config.STUDENTS_LIST):
        
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
                    name = self.listNodes[i][0].name 

            if name != "": hit = selectNode(name, double)
            else: 
                name = checkText(self.studentName, x, y)
                if name != "": hit = selectNode(name, double)            
                
            if hit: self.signal.update.emit()
            else: self.signal.clear.emit()

    def drawDiagram(self):
        self.clear()
        hint_text = ""

        if len(config.STUDENTS_LIST) <= 1:
            hint_text = "Hint: start a new investigation"
        else:
            if config.SELECTED_STUDENT == "":
                hint_text = "Hint: select one of the nodes - one click to highlight, two clicks to select"
            else:
                if config.WAITING_FOR_ == "":
                    hint_text = "Hint: click on the highlighting node one more time or select another one"
                else:
                    if config.COUPLE == "":
                        hint_text = "Hint: select one more node to start the comparison"


        hintX, hintY = (5, 3)
        hintShadowColor = QColor(75, 85, 95, 70)
        hintShadow = self.addText(hint_text, QFont("Times", 9))
        hintShadow.setPos(hintX  + 1, hintY + 1)          
        hintShadow.setDefaultTextColor(hintShadowColor)

        hintColor = QColor(234, 255, 239, 180)
        hint = self.addText(hint_text, QFont("Times", 9))                    
        hint.setPos(hintX, hintY)                 
        hint.setDefaultTextColor(hintColor)  
        if len(config.STUDENTS_LIST) > 1 and len(config.RESULT_MATRIX) == len(config.STUDENTS_LIST):
            
            self.listNodes = []
            self.studentName = []
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
           
                        if config.RANGE_PLAG < maxPlagList[i][1] or config.SHOW_LINKLESS or config.SELECTED_STUDENT == self.listNodes[i][t].name:
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

                                    if float(config.RESULT_MATRIX[i][j]) < config.RANGE_PLAG: 
                                        al = al - int(config.RANGE_PLAG)*2 - 40
                                                     
                                    if config.CHESS:
                                        if i% 2 == 0: redl, greenl, bluel, al = (95, 160, 200, al) 
                                        else: redl, greenl, bluel, al = (245, 145, 130, al)

                                    if config.SELECTED_STUDENT != "":
                                        if (config.SELECTED_STUDENT == self.listNodes[i][t].name and self.listNodes[j][t].name in config.SELECTED_STUDENTS) or (config.SELECTED_STUDENT == self.listNodes[j][t].name and self.listNodes[i][t].name in config.SELECTED_STUDENTS):                                       
                                           redl, greenl, bluel, al = (226, 113, 105, al)
                                        else: redl, greenl, bluel, al = (102, 151, 180, 10)                                     

                                    if len(config.HIDED_STUDENTS) > 0:
                                        if self.listNodes[i][t].name in config.HIDED_STUDENTS or self.listNodes[j][t].name in config.HIDED_STUDENTS: al = 5

                                    if config.RANGE_PLAG > maxPlagList[j][1]: al = 5
                                    if config.RANGE_PLAG > maxPlagList[j][1] and not config.SHOW_LINKLESS: al = 0
                                    if config.RANGE_PLAG > maxPlagList[j][1] and not config.SHOW_LINKLESS and config.SELECTED_STUDENT == self.listNodes[j][t].name: al = 15 
                                   

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
                                if config.WAITING_FOR_ == self.listNodes[i][t].name:
                                    red, green, blue, a = (234, 255, 239, a)
                                elif config.SELECTED_STUDENT== self.listNodes[i][t].name:
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

                            colorBrush = QColor(red, green, blue, a)
                            colorPen = QColor(redp, greenp, bluep, ap)
                            self.addEllipse(self.listNodes[i][t].x, self.listNodes[i][t].y, self.listNodes[i][t].width, self.listNodes[i][t].height, QPen(colorPen), QBrush(colorBrush))
         
                    if redl + 20 > 255: redl = 90
                    else: redl = redl + 20   
                    red, green, blue = (redl, greenl, bluel)
            
                for i in range(len(self.listNodes)): 
                    redt, greent, bluet, at = (250, 200, 190, 255)
                    if config.SELECTED_STUDENT != "":
                        if config.WAITING_FOR_ == self.listNodes[i][t].name:
                                    red, green, blue, a = (234, 255, 239, a)                               
                        elif config.SELECTED_STUDENT== self.listNodes[i][t].name:
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
                    if config.SHOW_NAMES and (config.RANGE_PLAG < maxPlagList[i][1] or config.SHOW_LINKLESS or config.SELECTED_STUDENT == self.listNodes[i][0].name):
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
    def __init__(self): 
        QGraphicsScene.__init__(self)   
        self.signal = Communicate()
        self.Nodes = []
        self.studentName = []
        #self.drawDiagram()          

    def mouseDoubleClickEvent(self, event):
        x = event.scenePos().x()
        y = event.scenePos().y()
        self.positionCheck(x, y, True)

    def mousePressEvent(self, event):
        x = event.scenePos().x()
        y = event.scenePos().y()
        self.positionCheck(x, y, False)

    def positionCheck(self, x, y, double):
        hit = False
        name = ""
        if len(config.STUDENTS_LIST) > 1 and len(config.RESULT_MATRIX) == len(config.STUDENTS_LIST):

            for i in range(len(self.Nodes)):
                xn1 = self.Nodes[i].x - self.Nodes[i].width/2
                xn2 = self.Nodes[i].x + self.Nodes[i].width - self.Nodes[i].width/2
                yn1 = self.Nodes[i].y - self.Nodes[i].height/2
                yn2 = self.Nodes[i].y + self.Nodes[i].height - self.Nodes[i].height/2
               
                if xn1 < x < xn2 and yn1 < y < yn2:
                    name = self.Nodes[i].name 

            if name != "": hit = selectNode(name, double)
            else: 
                name = checkText(self.studentName, x, y)
                if name != "": hit = selectNode(name, double)            
                
            if hit: self.signal.update.emit()
            else: self.signal.clear.emit()

    def drawDiagram(self):
        self.clear()
        hint_text = ""

        if len(config.STUDENTS_LIST) <= 1:
            hint_text = "Hint: start a new investigation"
        else:
            if config.SELECTED_STUDENT == "":
                hint_text = "Hint: select one of the nodes - one click to highlight, two clicks to select"
            else:
                if config.WAITING_FOR_ == "":
                    hint_text = "Hint: click on the highlighting node one more time or select another one"
                else:
                    if config.COUPLE == "":
                        hint_text = "Hint: select one more node to start the comparison"


        hintX, hintY = (5, 3)
        hintShadowColor = QColor(75, 85, 95, 70)
        hintShadow = self.addText(hint_text, QFont("Times", 9))
        hintShadow.setPos(hintX  + 1, hintY + 1)          
        hintShadow.setDefaultTextColor(hintShadowColor)

        hintColor = QColor(234, 255, 239, 180)
        hint = self.addText(hint_text, QFont("Times", 9))                    
        hint.setPos(hintX, hintY)                 
        hint.setDefaultTextColor(hintColor)  

        if len(config.STUDENTS_LIST) > 1 and len(config.RESULT_MATRIX) == len(config.STUDENTS_LIST):
            
            self.Nodes = []
            self.studentName = []
            maxPlagList = findMaxPlag()                       

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
                        if i != j and float(config.RESULT_MATRIX[i][j]) > 0 and (config.RANGE_PLAG < maxPlagList[i][1] or config.SHOW_LINKLESS):
                
                            penWidth = float(config.RESULT_MATRIX[i][j])/10
                            x2 =  self.Nodes[j].x
                            y2 =  self.Nodes[j].y
                            red, green, blue, a = (238, 151, 142, 240)

                            if penWidth >= config.RANGE_PLAG/10:
                                red, green, blue, a = (238, 151, 142, 240)
                            else:
                                red, green, blue, a = (131, 118, 122, 30)

                            if config.CHESS:
                                if i% 2 == 0: red, green, blue = (95, 160, 200) 
                                else: red, green, blue = (245, 145, 130) 

                            if config.SELECTED_STUDENT != "":
                                if (config.SELECTED_STUDENT ==  self.Nodes[i].name and self.Nodes[j].name in config.SELECTED_STUDENTS) or (config.SELECTED_STUDENT ==  self.Nodes[j].name and  self.Nodes[i].name in config.SELECTED_STUDENTS):
                                    red, green, blue, a = (226, 113, 105, 255)  
                                else: red, green, blue, a = (102, 151, 180, 20) 

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

                            if config.RANGE_PLAG < maxPlagList[j][1] or config.SHOW_LINKLESS:
                                self.addPath(path, QPen(color, penWidth))     
  
                for i in range(len(self.Nodes)):
                    redt, greent, bluet, at = (254, 234, 230, 255)
                    red, green, blue, a = (160, 205, 225, 255)
                
                    if config.RANGE_PLAG < maxPlagList[i][1] or config.SHOW_LINKLESS or config.SELECTED_STUDENT == self.Nodes[i].name:
                        if config.CHESS:
                            if i% 2 == 0: red, green, blue = (95, 160, 200) 
                            else: red, green, blue = (245, 145, 130)
            
                        if config.SELECTED_STUDENT != "":
                            if config.WAITING_FOR_ ==  self.Nodes[i].name:
                                red, green, blue = redt, greent, bluet = (234, 255, 239)                                
                            elif config.SELECTED_STUDENT ==  self.Nodes[i].name:
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
    def __init__(self, parent, scene):
        super(GraphicsView, self).__init__()        
        self.parent = parent
        self.signal = Communicate()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding )
        self.setAutoFillBackground(True)
        self.setMinimumSize(700, 550)
        self.setStyleSheet('QGraphicsView {background-color: rgba(54, 64, 80, 255); border-width:2px; border-style:solid;border-top-color: qlineargradient(spread:pad, x1:0.5, y1:0.6, x2:0.5, y2:0.4, stop:0 rgba(54, 64, 80, 120), stop:1 rgba(20, 20, 25,120));border-right-color: qlineargradient(spread:pad, x1:0.4, y1:0.5, x2:0.6, y2:0.5, stop:0 rgba(123, 209, 201, 255), stop:1 rgba(205, 177, 168, 220));border-left-color: qlineargradient(spread:pad, x1:0.4, y1:0.5, x2:0.6, y2:0.5, stop:0 rgba(138, 140, 152, 255), stop:1 rgba(184, 173, 182, 120));border-bottom-color: qlineargradient(spread:pad, x1:0.6, y1:0.5, x2:0.4, y2:0.5, stop:0 rgba(184, 173, 182, 180), stop:1 rgba(212, 199, 205, 180)); border-bottom-width: 3px; border-right-width: 3px;}')
        self.setRenderHints(QPainter.Antialiasing | QPainter.LosslessImageRendering | QPainter.SmoothPixmapTransform | QPainter.TextAntialiasing);
        
        self.scene = scene 
        self.scene.setSceneRect(0.0, 0.0, self.width() - 10, self.height() - 10)
        self.setScene(self.scene)

        #self.property()
        #QColor(54, 64, 80, 255)
        

    def resizeEvent(self, event):      
        self.scene.setSceneRect(0.0, 0.0, self.width() - 10, self.height() - 10)   
        self.scene.drawDiagram()
        super(GraphicsView, self).resizeEvent(event)

    #def paintEvent(self, event):
        #QGraphicsView.paintEvent(self, event)#########   
        #self.scene.drawDiagram()     
        #print('view paint event')

    def sceneUpdate(self):
        self.scene.drawDiagram()

class Node():
    def __init__(self, name, imgWidth, imgHeight):
        self.name = name
        self.width = imgWidth/5*4
        self.height = imgHeight/5*4
        self.x = imgWidth/2
        self.н = imgHeight/2

    def setX(self, x):
        self.x = x
    def setY(self, y):
        self.y = y

def findRadius(imgWidth, imgHeight):    
    if imgWidth > imgHeight:
        radius = imgHeight
    else: radius = imgWidth

    return radius/3
def findPerimeter(radius): return 2 * math.pi * radius

def selectNode(name, double): 

    if name != "" and name in config.STUDENTS_LIST:

        if double:
            if config.SELECTED_STUDENT == name: 
                config.WAITING_FOR_ = name
                config.SELECTED_STUDENT = name
        else:
            if config.SELECTED_STUDENT == name and config.WAITING_FOR_ == "":
                config.WAITING_FOR_ = name

            elif config.SELECTED_STUDENT == name and config.WAITING_FOR_ == name:
                config.WAITING_FOR_ = ""

            elif config.SELECTED_STUDENT != "" and config.WAITING_FOR_ != "":
                if name in config.SELECTED_STUDENTS: 
                    config.COUPLE = name
                else: 
                    config.WAITING_FOR_ = ""
        
            config.SELECTED_STUDENT = name
        return True
    return False


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