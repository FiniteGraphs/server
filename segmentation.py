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
        self.bgPoints = None
        self.objPoints = None
        self.sigma = 2
        btnB = QPushButton("Background", self)
        btnB.setStyleSheet("background-color: red")
        btnB.move(0, 0)
        btnO = QPushButton("Object", self)
        btnO.setStyleSheet("background-color: blue")
        btnO.move(120, 0)
        btnS = QPushButton("Submit", self)
        btnS.move(240, 0)
        btnS.clicked.connect(self.onSegment)
        
        self.statusBar()
        self.statusBar().setStyleSheet("color: white")
        self.statusBar().showMessage('Background select')
        self.setGeometry(100, 100, 500, 300)
        self.resize(self.image.width(), self.image.height())
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.image)

    def mousePressEvent(self, event):
        needPoints = False
        if self.bgPoints is None or self.objPoints is None:
                needPoints = True
        if event.button() == Qt.LeftButton and event.buttons() and needPoints:
            drawBg = True
            if self.bgPoints is not None:
                drawBg = False
            self.drawing = True
            self.lastPoint = event.pos()
            painter = QPainter(self.image)
            if drawBg:
                painter.setPen(QPen(QColor(255 ,0, 0, 100), 5, Qt.SolidLine))
                painter.drawLine(self.lastPoint, event.pos())
                self.lastPoint = event.pos()
                self.bgPoints = np.array([event.x(), event.y()])
                self.statusBar().showMessage('Obect select')
            else:
                painter.setPen(QPen(QColor(0 , 0, 255, 100), 5, Qt.SolidLine))
                painter.drawLine(self.lastPoint, event.pos())
                self.lastPoint = event.pos()
                self.objPoints = np.array([event.x(), event.y()])
                self.statusBar().showMessage('Press submit')
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.drawing = False

    def saveImage(self, fileName, fileFormat):
        self.image.save(fileName, fileFormat)

    def onSegment(self):
        print(self.bgPoints, "|||", self.objPoints)
        imgArray = createArrayFromImage(self.imagePath)
        height, width = imgArray.shape
        print('Height: ', height, '  Width: ', width)
        getGraph(width, height, imgArray)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainMenu = Menu()
    sys.exit(app.exec_())