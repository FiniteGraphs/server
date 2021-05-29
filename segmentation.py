from image_to_graph import getGraph
import sys
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor
import numpy as np
import networkx as nx
from main import createArrayFromImage
from image_to_graph import getGraph
import math

class Menu(QMainWindow):

    def __init__(self):
        super().__init__()
        self.drawing = False
        self.lastPoint = QPoint()
        self.imagePath="C:\graphs\server\image.jpg"
        self.image = QPixmap(self.imagePath)
        self.bgPoints = np.array([[0, 0]], np.int32)
        self.objPoints = np.array([[0, 0]], np.int32)
        self.sigma = 2
        btnB = QPushButton("Background", self)
        btnB.setStyleSheet("background-color: red")
        btnB.move(0, 0)
        btnO = QPushButton("Object", self)
        btnO.setStyleSheet("background-color: blue")
        btnO.move(120, 0)
        btnS = QPushButton("Submit", self)
        btnS.move(240, 0)
        btnB.clicked.connect(self.onSetBackground)
        btnO.clicked.connect(self.onSetObject)
        btnS.clicked.connect(self.onSegment)
        self.setBgPoints = True
        self.statusBar()
        self.statusBar().setStyleSheet("color: white")
        self.statusBar().showMessage('Background select. Please set more than 10 points')
        self.setGeometry(300, 300, 1000, 1000)
        self.resize(self.image.width(), self.image.height())
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.image)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()
            painter = QPainter(self.image)
            if (self.setBgPoints):
                painter.setPen(QPen(QColor(255 , 0, 0, 100), 5, Qt.SolidLine))
                painter.drawLine(self.lastPoint, event.pos())
                x = int(event.x())
                y = int(event.y())
                pointAlreadyExisted = False
                for i in range(len(self.bgPoints)-1):
                    if self.bgPoints[i][0]==x and self.bgPoints[i][1]==y:
                        pointAlreadyExisted = True
                if pointAlreadyExisted != True:
                    self.bgPoints = np.append(self.bgPoints, [[x, y]], axis=0)
            else:
                painter.setPen(QPen(QColor(0 , 0, 255, 100), 5, Qt.SolidLine))
                painter.drawLine(self.lastPoint, event.pos())
                x = int(event.x())
                y = int(event.y())
                pointAlreadyExisted = False
                for i in range(len(self.objPoints)-1):
                    if self.objPoints[i][0]==x and self.objPoints[i][1]==y:
                        pointAlreadyExisted = True
                if pointAlreadyExisted != True:
                    self.objPoints = np.append(self.objPoints, [[x, y]], axis=0)
            self.update()


    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.drawing = False

    def saveImage(self, fileName, fileFormat):
        self.image.save(fileName, fileFormat)

    def onSetBackground(self):
        self.setBgPoints = True
        self.statusBar().showMessage('Background select. Please set more than 10 points')

    def onSetObject(self):
        self.setBgPoints = False
        self.statusBar().showMessage('Object select. Please set more than 10 points')

    def onSegment(self):
        if len(self.bgPoints) < 10 or (len(self.objPoints) < 10):
            self.statusBar().showMessage('Please set more points')
        else:
            self.bgPoints = np.delete(self.bgPoints, [0, 0], axis=0)
            self.objPoints = np.delete(self.objPoints, [0, 0], axis=0)
            print(self.bgPoints, "|||", self.objPoints)
            imgArray = createArrayFromImage(self.imagePath)
            height, width = imgArray.shape
            print('Height: ', height, '  Width: ', width)
            getGraph(width, height, imgArray, self.bgPoints, self.objPoints)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainMenu = Menu()
    sys.exit(app.exec_())