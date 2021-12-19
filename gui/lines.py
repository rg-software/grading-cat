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
import collections
import random
import time
from main_utils import appPath


class LinesView(QGraphicsView):
    def __init__(self, parent):
        super(LinesView, self).__init__()
        self.parent = parent
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setAutoFillBackground(True)
        self.setMinimumSize(700, 550)
        self.setStyleSheet(
            "QGraphicsView {background-color: rgba(54, 64, 80, 255); border-width:2px; border-style:solid;border-top-color: qlineargradient(spread:pad, x1:0.5, y1:0.6, x2:0.5, y2:0.4, stop:0 rgba(54, 64, 80, 120), stop:1 rgba(20, 20, 25,120));border-right-color: qlineargradient(spread:pad, x1:0.4, y1:0.5, x2:0.6, y2:0.5, stop:0 rgba(123, 209, 201, 255), stop:1 rgba(205, 177, 168, 220));border-left-color: qlineargradient(spread:pad, x1:0.4, y1:0.5, x2:0.6, y2:0.5, stop:0 rgba(138, 140, 152, 255), stop:1 rgba(184, 173, 182, 120));border-bottom-color: qlineargradient(spread:pad, x1:0.6, y1:0.5, x2:0.4, y2:0.5, stop:0 rgba(184, 173, 182, 180), stop:1 rgba(212, 199, 205, 180)); border-bottom-width: 3px; border-right-width: 3px;}"
        )
        self.setRenderHints(
            QPainter.Antialiasing
            | QPainter.LosslessImageRendering
            | QPainter.SmoothPixmapTransform
            | QPainter.TextAntialiasing
        )

        self.scene = LinesScene(self)
        self.viewRect = QRectF(
            0.0, 0.0, float(self.width() - 10), float(self.height() - 10)
        )

        self.scene.setSceneRect(self.viewRect)
        self.setScene(self.scene)
        self.scene.drawLines()

    def resizeEvent(self, event):
        self.scene.setSceneRect(0.0, 0.0, self.width() - 10, self.height() - 10)
        self.scene.drawLines()
        super(LinesView, self).resizeEvent(event)

    def sceneUpdate(self):
        self.scene.drawLines()


class LinesScene(QGraphicsScene):
    def __init__(self, parent):
        QGraphicsScene.__init__(self)
        self.parent = parent

        self.GAME = True
        # self.GAME = False
        self.Goal = 5
        self.Score = 0
        self.BestResult = 5000
        self.Prediction = []
        self.newGlobN = 3

        self.scoreColor = QColor(64, 74, 90, 160)
        self.scoreLight = QColor(245, 150, 142, 200)
        self.scoreShadow = QColor(46, 56, 72, 255)
        self.color_cat = (
            QBrush(QColor(254, 154, 154, 245)),
            QPen(QColor(240, 230, 250, 250), 2),
        )
        self.color_cat_pen = QPen(QColor(240, 230, 250, 250), 4)

        self.predictionShadow = QColor(64, 74, 90, 40)

        self.pathColor = QBrush(QColor(130, 157, 151, 70))

        self.linePenLight = QPen(QColor(245, 150, 142, 200), 1)
        self.linePenDark = QPen(QColor(46, 56, 72, 255), 4)
        self.linePenGreen = QPen(QColor(123, 209, 201, 60), 1)
        self.cellColor = QColor(64, 74, 90, 250)

        self.targetPen = QPen(QColor(255, 255, 250, 50), 1)
        self.targetColor = QBrush(QColor(245, 150, 142, 150))
        self.pathColor = QBrush(QColor(130, 157, 151, 60))

        self.quantity = 9

        # self.color_1 = (QBrush(QColor(254, 154, 154, 245)), QPen(QColor(240, 230, 250, 250), 2))
        # self.color_2 = (QBrush(QColor(254, 229, 154, 245)), QPen(QColor(240, 230, 250, 250), 2))
        # self.color_3 = (QBrush(QColor(204, 254, 154, 245)), QPen(QColor(240, 230, 250, 250), 2))
        # self.color_4 = (QBrush(QColor(154, 254, 229, 245)), QPen(QColor(240, 230, 250, 250), 2))
        # self.color_5 = (QBrush(QColor(154, 179, 254, 245)), QPen(QColor(240, 230, 250, 250), 2))
        # self.color_6 = (QBrush(QColor(230, 153, 255, 245)), QPen(QColor(240, 230, 250, 250), 2))

        self.color_1 = (
            QBrush(QColor(253, 28, 28, 255)),
            QPen(QColor(240, 230, 250, 250), 2),
        )
        self.color_2 = (
            QBrush(QColor(253, 253, 28, 255)),
            QPen(QColor(240, 230, 250, 250), 2),
        )
        self.color_3 = (
            QBrush(QColor(84, 253, 28, 255)),
            QPen(QColor(240, 230, 250, 250), 2),
        )
        self.color_4 = (
            QBrush(QColor(28, 253, 253, 255)),
            QPen(QColor(240, 230, 250, 250), 2),
        )
        self.color_5 = (
            QBrush(QColor(28, 28, 253, 255)),
            QPen(QColor(240, 230, 250, 250), 2),
        )
        self.color_6 = (
            QBrush(QColor(253, 28, 253, 255)),
            QPen(QColor(240, 230, 250, 250), 2),
        )
        self.colors = []
        self.colors.extend(
            [
                self.color_1,
                self.color_2,
                self.color_3,
                self.color_4,
                self.color_5,
                self.color_6,
            ]
        )
        self.color_chosen_one = (
            QBrush(QColor(255, 255, 250, 255)),
            QPen(QColor(255, 190, 180, 255), 3),
        )
        self.color_in_line = (
            QBrush(QColor(255, 135, 130, 245)),
            QPen(QColor(255, 160, 155, 245), 4),
        )
        self.color_new_glob = (
            QBrush(QColor(231, 254, 230, 245)),
            QPen(QColor(210, 254, 232, 245), 3),
        )

        self.cell = []
        self.selectedGlob = None
        self.selectedTarget = None

        for i in range(self.quantity):
            line = []
            for j in range(self.quantity):
                spot = (i, j)
                name = "spot_" + str(i) + str(j)
                line.append(Cell(spot, name))
                # print(name)
            self.cell.append(line)

        self.Prediction = self.addNewGlobs(self.newGlobN)
        newGlobs = self.setGlobs()
        # self.drawBubbleChart()

    def mousePressEvent(self, event):
        x = event.scenePos().x()
        y = event.scenePos().y()

        if self.GAME:
            hit = False
            for i in range(len(self.cell)):
                for j in range(len(self.cell)):
                    x1 = self.cell[i][j].x
                    y1 = self.cell[i][j].y
                    x2 = self.cell[i][j].x + self.cell[i][j].w
                    y2 = self.cell[i][j].y + self.cell[i][j].h

                    if x1 < x < x2 and y1 < y < y2:
                        hit = True

                        if self.cell[i][j].occupied:
                            if self.cell[i][j].glob.chosen:
                                self.selectedGlob = None
                            else:
                                self.selectedGlob = self.cell[i][j].glob

                            for a in range(len(self.cell)):
                                for b in range(len(self.cell)):
                                    if self.cell[a][b].occupied:
                                        if self.selectedGlob == self.cell[a][b].glob:
                                            self.cell[a][b].glob.select()
                                        else:
                                            self.cell[a][b].glob.deselect()
                                    else:
                                        self.cell[a][b].untarget()
                                        self.selectedTarget = None
                        else:
                            if self.cell[i][j].target:
                                self.selectedTarget = None
                            else:
                                self.selectedTarget = self.cell[i][j]

                            for a in range(len(self.cell)):
                                for b in range(len(self.cell)):
                                    if self.cell[a][b] == self.selectedTarget:
                                        self.cell[i][j].targetable()
                                    else:
                                        self.cell[a][b].untarget()

            x1 = self.cell[0][0].x
            y1 = self.cell[0][0].y

            x2 = self.cell[-1][-1].x + self.cell[-1][-1].w
            y2 = self.cell[-1][-1].y + self.cell[-1][-1].h

            if not hit:
                for i in range(len(self.cell)):
                    for j in range(len(self.cell)):
                        self.selectedGlob = None
                        self.selectedTarget = None
                        if self.cell[i][j].occupied:
                            self.cell[i][j].glob.deselect()
                        else:
                            self.cell[i][j].untarget()

            for i in range(len(self.cell)):
                for j in range(len(self.cell)):
                    self.cell[i][j].setPath(False)
            if self.selectedTarget != None:
                self.moveGlog()
            else:
                self.drawLines()
        else:
            self.cell = []
            self.selectedGlob = None
            self.selectedTarget = None
            self.Score = 0

            for i in range(self.quantity):
                line = []
                for j in range(self.quantity):
                    spot = (i, j)
                    name = "spot_" + str(i) + str(j)
                    line.append(Cell(spot, name))
                    # print(name)
                self.cell.append(line)

            self.GAME = True
            self.Prediction = self.addNewGlobs(self.newGlobN)
            newGlobs = self.setGlobs()
            self.drawLines()

    def moveGlog(self):
        if self.selectedTarget != None and self.selectedGlob != None:
            self.selectedGlob.deselect()
            self.selectedTarget.untarget()
            self.selectedGlob.parentCell.takeGlob()

            Path = []
            find = findingWay(
                self.selectedGlob.parentCell, self.selectedTarget, self.cell
            )
            Path.extend(find[1])

            if len(Path) > 0:
                for i in range(len(Path)):
                    Path[i].setPath(True)

            if find[0]:
                # print(":)")
                self.selectedTarget.setGlob(self.selectedGlob)

                lines = []
                lines.extend(checkLines(self.cell, self.selectedGlob, self.Goal))

                if len(lines) >= self.Goal:
                    for i in range(len(self.cell)):
                        for j in range(len(self.cell)):
                            if self.cell[i][j].occupied:
                                if self.cell[i][j] in lines:
                                    self.cell[i][j].glob.setInLine()

                    time.sleep(0.1)

                    self.drawLines()
                    self.parent.repaint()

                    time.sleep(0.2)

                    self.Score = self.Score + (
                        (len(lines) * (len(lines) - self.Goal + 1)) * 10
                    )

                    for i in range(len(self.cell)):
                        for j in range(len(self.cell)):
                            self.cell[i][j].setPath(False)
                            if self.cell[i][j].occupied:
                                if self.cell[i][j].glob.inLine:
                                    self.cell[i][j].takeGlob()

                else:
                    self.drawLines()
                    self.parent.repaint()
                    time.sleep(0.2)
                    newGlobs = self.setGlobs()
                    self.drawLines()
                    self.parent.repaint()

                    if self.GAME:
                        time.sleep(0.2)
                        for i in range(len(newGlobs)):
                            selectedGlob = newGlobs[i]
                            lines = []
                            lines.extend(checkLines(self.cell, selectedGlob, self.Goal))
                            if len(lines) >= self.Goal:
                                for i in range(len(self.cell)):
                                    for j in range(len(self.cell)):
                                        if self.cell[i][j].occupied:
                                            if self.cell[i][j] in lines:
                                                self.cell[i][j].glob.setInLine()

                        time.sleep(0.1)
                        self.drawLines()
                        self.parent.repaint()
                        time.sleep(0.2)
                        for i in range(len(self.cell)):
                            for j in range(len(self.cell)):
                                if self.cell[i][j].occupied:
                                    if self.cell[i][j].glob.inLine:
                                        self.cell[i][j].takeGlob()
                        self.drawLines()
                        self.parent.repaint()

                    time.sleep(0.3)
                    freeCells = 0
                    for i in range(len(self.cell)):
                        for j in range(len(self.cell)):
                            if not self.cell[i][j].occupied:
                                freeCells = freeCells + 1
                            self.cell[i][j].setPath(False)

                    if freeCells == 0:
                        self.GAME = False
                        print("Game over")

            if not find[0]:
                self.selectedGlob.parentCell.setGlob(self.selectedGlob)
                # print(":(")

            self.selectedGlob = None
            self.selectedTarget = None

        self.drawLines()
        self.parent.repaint()

    def setGlobs(self):
        newGlobs = self.Prediction
        n = self.newGlobN
        listFreeCells = []
        for i in range(len(self.cell)):
            for j in range(len(self.cell)):
                if not self.cell[i][j].occupied:
                    listFreeCells.append([i, j])

        if len(listFreeCells) >= n:
            spots = random.sample(listFreeCells, k=n)
            # spots = [(0,0)]
            for i in range(n):
                self.cell[spots[i][0]][spots[i][1]].setGlob(newGlobs[i])

        # elif len(listFreeCells) >= 1:
        # spots = random.sample(listFreeCells, k = len(listFreeCells))
        # for i in range(len(listFreeCells)):
        # self.cell[spots[i][0]][spots[i][1]].setGlob(newGlobs[i])
        # elif len(listFreeCells) == 0:
        # self.GAME = False
        # print("Game over")
        else:
            self.GAME = False
            print("Game over")

        self.Prediction = []
        self.Prediction = self.addNewGlobs(n)
        return newGlobs

    def addNewGlobs(self, n):
        globs = []
        for i in range(n):
            color = random.randint(1, 6)
            if color == 1:
                globs.append(Glob(self.color_1, "color_1"))
            if color == 2:
                globs.append(Glob(self.color_2, "color_2"))
            if color == 3:
                globs.append(Glob(self.color_3, "color_3"))
            if color == 4:
                globs.append(Glob(self.color_4, "color_4"))
            if color == 5:
                globs.append(Glob(self.color_5, "color_5"))
            if color == 6:
                globs.append(Glob(self.color_6, "color_6"))

            # if color == 1: globs.append(Glob(self.color_1, "color_1"))
            # if color == 2: globs.append(Glob(self.color_1, "color_1"))
            # if color == 3: globs.append(Glob(self.color_1, "color_1"))
            # if color == 4: globs.append(Glob(self.color_1, "color_1"))
            # if color == 5: globs.append(Glob(self.color_1, "color_1"))
            # if color == 6: globs.append(Glob(self.color_1, "color_1"))

        return globs

    def drawLines(self):
        self.clear()

        scale = self.height() / (self.quantity + 3)
        circleCenterX = self.width() / 2
        circleCenterY = self.height() / 2

        x = circleCenterX - scale * self.quantity / 2
        y = scale * 2
        length = scale * self.quantity

        font = scale - scale / 4
        scoreX, scoreY = (x + scale * 6, scale / 2)

        scoreShadow = self.addText(str(self.Score), QFont("Consolas", font))
        scoreShadow.setPos(scoreX + 2, scoreY + 2)
        scoreShadow.setDefaultTextColor(self.scoreShadow)

        scoreLight = self.addText(str(self.Score), QFont("Consolas", font))
        scoreLight.setPos(scoreX, scoreY)
        scoreLight.setDefaultTextColor(self.scoreLight)

        score = self.addText(str(self.Score), QFont("Consolas", font))
        score.setPos(scoreX + 1, scoreY + 1)
        score.setDefaultTextColor(self.scoreColor)

        if self.GAME:
            catPath = f"{appPath()}/icons/cat_ss.png"
            image = QImage()
            image.load(catPath)
            pixmap = QPixmap.fromImage(image).scaled(
                scale + scale / 3,
                scale + scale / 3,
                Qt.IgnoreAspectRatio,
                Qt.SmoothTransformation,
            )
            pixmapItem = QGraphicsPixmapItem(pixmap)
            # pixmapItem.setScale(pixmapSize, Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
            pixmapItem.setPos(x + scale * 4 - scale / 4, scale / 2)
            self.addItem(pixmapItem)
            for i in range(len(self.Prediction)):
                brushGlob = self.Prediction[i].color[0]
                penGlob = self.Prediction[i].color[1]
                PredictionX, PredictionY = (
                    x + (scale / 10) * (i + 1) + scale * i,
                    scale - scale / 4,
                )
                self.addEllipse(
                    PredictionX + 1,
                    PredictionY + 1,
                    scale - scale / 4,
                    scale - scale / 4,
                    self.linePenDark,
                    self.predictionShadow,
                )
                # self.addEllipse(PredictionX - 1, PredictionY - 1, scale, scale, self.linePenLight , self.cellColor)
                self.addEllipse(
                    PredictionX,
                    PredictionY,
                    scale - scale / 4,
                    scale - scale / 4,
                    penGlob,
                    brushGlob,
                )
                self.addEllipse(
                    PredictionX,
                    PredictionY,
                    scale - scale / 4,
                    scale - scale / 4,
                    self.linePenGreen,
                    self.predictionShadow,
                )
        else:
            gameOverFont = scale / 2
            gameOverX, gameOverY = (x + scale / 20, scale / 2 + scale / 4)

            gameOverShadow = self.addText("GAME OVER", QFont("Consolas", gameOverFont))
            gameOverShadow.setPos(gameOverX + 2, gameOverY + 2)
            gameOverShadow.setDefaultTextColor(self.scoreShadow)

            gameOverLight = self.addText("GAME OVER", QFont("Consolas", gameOverFont))
            gameOverLight.setPos(gameOverX, gameOverY)
            gameOverLight.setDefaultTextColor(self.scoreLight)

            gameOver = self.addText("GAME OVER", QFont("Consolas", gameOverFont))
            gameOver.setPos(gameOverX + 1, gameOverY + 1)
            gameOver.setDefaultTextColor(self.scoreColor)

            goCatPath = f"{appPath()}/icons/cat_ssevl.png"
            pixmap = QPixmap.fromImage(goCatPath).scaled(
                scale + scale / 3,
                scale + scale / 3,
                Qt.IgnoreAspectRatio,
                Qt.SmoothTransformation,
            )
            pixmapItem = QGraphicsPixmapItem(pixmap)
            # pixmapItem.setScale(pixmapSize, Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
            pixmapItem.setPos(x + scale * 4 - scale / 4, scale / 2)
            self.addItem(pixmapItem)

        ####bestResultBox
        # bestResult_font = scale/6
        # bestResultX, bestResultY = (x - scale*2 - scale/2, length + scale/2)
        # bestResult = self.addText(str(self.BestResult), QFont("Consolas", font))
        # bestResult.setPos(bestResultX + 1, bestResultY + 1)
        # bestResult.setDefaultTextColor(self.scoreColor)
        # self.addRect(bestResultX + scale/15, bestResultY + scale + scale/5, scale*2  + scale/5 , scale/4, self.linePenDark, self.cellColor)
        # if self.BestResult > self.Score:
        # BestResult = 100%
        # catY = bestResultY - scale
        # catX = bestResultX + scale/2
        # CatW = scale + scale/2
        # CatH = scale + scale/7
        # n = 5
        # boxX = bestResultX + scale/5
        # boxY = bestResultY - scale
        # for i in range(n):
        # self.addRect(boxX, boxY - (scale + scale/7)*i, scale*2, scale, self.linePenDark, self.cellColor)
        # catY = boxY - (scale + scale/7)*i
        # catY = catY - CatH - scale/2
        # self.addEllipse(catX, catY, CatW, CatW, self.color_cat[1], self.color_cat[0])
        self.addRect(x, y, length, length, self.linePenDark, self.cellColor)

        for i in range(len(self.cell)):
            for j in range(len(self.cell)):
                self.cell[i][j].setCoordinates(scale, x, y)

        for i in range(self.quantity):
            xDLH, yDLH = (x - 1 + scale * (i + 1), y - 1)
            xDLV, yDLV = (x - 1, y + scale * (i + 1) - 1)

            xLLH, yLLH = (x + scale * i, y)
            xLLV, yLLV = (x, y + scale * i)

            self.addLine(xLLH, yLLH, xLLH, yLLH + length, self.linePenLight)
            self.addLine(xLLV, yLLV, xLLV + length, yLLV, self.linePenLight)
            self.addLine(xDLH, yDLH, xDLH, yDLH + length, self.linePenDark)
            self.addLine(xDLV, yDLV, xDLV + length, yDLV, self.linePenDark)
            self.addLine(xDLH, yDLH, xDLH, yDLH + length, self.linePenGreen)
            self.addLine(xDLV, yDLV, xDLV + length, yDLV, self.linePenGreen)

        for i in range(len(self.cell)):
            for j in range(len(self.cell)):
                if self.cell[i][j].occupied:
                    self.cell[i][j].glob.setCoordinates(
                        scale, self.cell[i][j].x, self.cell[i][j].y
                    )

                    x, y = (self.cell[i][j].glob.x, self.cell[i][j].glob.y)
                    w, h = (
                        self.cell[i][j].glob.diameter,
                        self.cell[i][j].glob.diameter,
                    )

                    if self.cell[i][j].glob.chosen:
                        brushGlob = self.color_chosen_one[0]
                        penGlob = self.color_chosen_one[1]
                    elif self.cell[i][j].glob.inLine:
                        brushGlob = self.color_in_line[0]
                        penGlob = self.color_in_line[1]
                        d = self.cell[i][j].glob.diameter
                        x, y = (
                            self.cell[i][j].glob.x + d / 4,
                            self.cell[i][j].glob.y + d / 4,
                        )
                        w, h = (d - d / 2, d - d / 2)
                    elif self.cell[i][j].glob.newGlob:
                        self.cell[i][j].glob.notNewAnymore()
                        brushGlob = self.color_new_glob[0]
                        penGlob = self.color_new_glob[1]
                        d = self.cell[i][j].glob.diameter
                        x, y = (
                            self.cell[i][j].glob.x + d / 8,
                            self.cell[i][j].glob.y + d / 8,
                        )
                        w, h = (d - d / 4, d - d / 4)
                    else:
                        brushGlob = self.cell[i][j].glob.color[0]
                        penGlob = self.cell[i][j].glob.color[1]

                    self.addEllipse(x, y, w, h, penGlob, brushGlob)
                elif self.cell[i][j].target or self.cell[i][j].path:
                    x, y = (self.cell[i][j].x, self.cell[i][j].y)
                    w, h = (self.cell[i][j].w, self.cell[i][j].h)

                    if self.cell[i][j].target:
                        self.addRect(x, y, w, h, self.targetPen, self.targetColor)
                    if self.cell[i][j].path:
                        self.addRect(x, y, w, h, self.targetPen, self.pathColor)


class Cell:
    def __init__(self, spot, name):
        self.name = name
        self.spot = spot
        self.glob = None
        self.occupied = False
        self.target = False
        self.path = False

    def setCoordinates(self, scale, RectX, RectY):
        self.x = RectX + scale * self.spot[0]
        self.y = RectY + scale * self.spot[1]
        self.w = scale
        self.h = scale

    def setPath(self, path):
        self.path = path

    def setGlob(self, glob):
        self.glob = glob
        self.glob.setparentCell(self)
        self.glob.deselect()
        self.occupied = True
        self.target = False

    def takeGlob(self):
        self.glob = None
        self.occupied = False

    def targetable(self):
        self.target = True

    def untarget(self):
        self.target = False


class Glob:
    def __init__(self, color, type):
        self.type = type
        self.color = color
        self.chosen = False
        self.inLine = False
        self.newGlob = True

    def notNewAnymore(self):
        self.newGlob = False

    def setCoordinates(self, scale, x, y):
        self.diameter = scale - scale / 8
        self.x = x + scale / 16
        self.y = y + scale / 16

    def setparentCell(self, parentCell):
        self.parentCell = parentCell

    def select(self):
        self.chosen = True

    def deselect(self):
        self.chosen = False

    def setInLine(self):
        self.inLine = True


def checkLines(field, theGlob, goal):
    length = len(field) - 1
    color = theGlob.type

    lines = []
    line_1 = []
    line_2 = []
    line_3 = []
    line_4 = []

    pos = theGlob.parentCell.spot
    line_1.append(theGlob.parentCell)
    line_2.append(theGlob.parentCell)
    line_3.append(theGlob.parentCell)
    line_4.append(theGlob.parentCell)

    if pos != (0, 0):
        line_1.extend(lineDirection(pos, -1, -1, length, field, color))
    if pos != (length, length):
        line_1.extend(lineDirection(pos, 1, 1, length, field, color))

    if pos[0] != 0 and pos[1] != length:
        line_2.extend(lineDirection(pos, -1, 1, length, field, color))
    if pos[1] != 0 and pos[0] != length:
        line_2.extend(lineDirection(pos, 1, -1, length, field, color))

    if pos[1] != length:
        line_3.extend(lineDirection(pos, 0, 1, length, field, color))
    if pos[1] != 0:
        line_3.extend(lineDirection(pos, 0, -1, length, field, color))

    if pos[0] != length:
        line_4.extend(lineDirection(pos, 1, 0, length, field, color))
    if pos[0] != 0:
        line_4.extend(lineDirection(pos, -1, 0, length, field, color))

    if len(line_1) >= goal:
        lines.extend(line_1)
    if len(line_2) >= goal:
        lines.extend(line_2)
    if len(line_3) >= goal:
        lines.extend(line_3)
    if len(line_4) >= goal:
        lines.extend(line_4)

    ###!!!
    return lines


def lineDirection(pos, di, dj, len, cells, color):
    half_line = []
    a = 0
    while a != 9:
        a = a + 1
        if len >= (pos[0] + di) >= 0 and len >= (pos[1] + dj) >= 0:

            i = pos[0] + di
            j = pos[1] + dj

            if cells[i][j].occupied and cells[i][j].glob.type == color:
                half_line.append(cells[i][j])
                pos = cells[i][j].spot
            else:
                break
        else:
            break

    return half_line


def findingWay(start, finish, field):
    exist = False
    Path = []
    Queue = []
    OpenSpots = []
    Queue.append(start)

    while len(Queue) != 0:
        CurrentSpot = Queue[0]
        Path.append(CurrentSpot)
        Queue = Queue[1:]
        if CurrentSpot == finish:
            exist = True
            break

        else:
            ways = []
            OpenSpots.append(CurrentSpot)

            if (CurrentSpot.spot[0] - 1) >= 0:
                i = CurrentSpot.spot[0] - 1
                j = CurrentSpot.spot[1]
                if (not field[i][j].occupied) and (field[i][j] not in OpenSpots):
                    ways.append(field[i][j])

            if (CurrentSpot.spot[0] + 1) < len(field):
                i = CurrentSpot.spot[0] + 1
                j = CurrentSpot.spot[1]
                if (not field[i][j].occupied) and (field[i][j] not in OpenSpots):
                    ways.append(field[i][j])

            if (CurrentSpot.spot[1] - 1) >= 0:
                i = CurrentSpot.spot[0]
                j = CurrentSpot.spot[1] - 1
                if (not field[i][j].occupied) and (field[i][j] not in OpenSpots):
                    ways.append(field[i][j])

            if (CurrentSpot.spot[1] + 1) < len(field):
                i = CurrentSpot.spot[0]
                j = CurrentSpot.spot[1] + 1
                if (not field[i][j].occupied) and (field[i][j] not in OpenSpots):
                    ways.append(field[i][j])

            # if len(ways) > 0:
            # for i in range(len(ways)):
            # if ways[i] not in Queue: Queue.append(ways[i])

            if len(ways) > 1:
                direction = []
                for i in range(len(ways)):
                    diff = abs(ways[i].spot[0] - finish.spot[0]) + abs(
                        ways[i].spot[1] - finish.spot[1]
                    )
                    direction.append([diff, ways[i]])
                direction = sorted(direction, key=itemgetter(0), reverse=True)
                for i in range(len(ways)):
                    if direction[i][1] not in Queue:
                        Queue.insert(0, direction[i][1])

            elif len(ways) == 1:
                if ways[0] not in Queue:
                    Queue.insert(0, ways[0])

            else:
                Path = Path[:-1]

    if not exist:
        Path = []
    else:
        hm = optimizePath(Path)
        if 0 < len(hm) < len(Path):
            Path = hm
    return exist, Path


def optimizePath(Path):
    optPath = []
    optPath.extend(Path)
    for i in range(len(Path)):
        cellA = Path[i]
        for j in range(len(Path)):
            cellB = Path[j]
            if (
                i < j
                and (j - i > 1)
                and (
                    (
                        abs(cellA.spot[0] - cellB.spot[0]) <= 1
                        and (cellA.spot[1] - cellB.spot[1]) == 0
                    )
                    or (
                        abs(cellA.spot[1] - cellB.spot[1]) <= 1
                        and (cellA.spot[0] - cellB.spot[0]) == 0
                    )
                )
            ):

                if cellA in optPath and cellB in optPath:
                    indexA = optPath.index(cellA)
                    indexB = optPath.index(cellB)
                    del optPath[indexA + 1 : indexB]

    return optPath
