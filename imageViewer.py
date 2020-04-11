import sys
import os
from PIL import Image
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QPen

class ImageView(QMainWindow):
    currentIndex = 0
    listSize = 0
    imageList = []
    dirName = 'Model/dataset/image'
    imageLabel = QLabel
    def __init__(self):
        super().__init__()
        self.drawing = False
        self.lastPoint = QPoint()
        self.setGeometry(100, 200, 530, 600)
        self.setWindowTitle("ImageViewer")

        leftBtn = QPushButton("left", self)
        leftBtn.setGeometry(170, 550, 100, 30)
        leftBtn.clicked.connect(self.onClickedLeftBtn)

        rigthBtn = QPushButton("right", self)
        rigthBtn.setGeometry(270, 550, 100, 30)
        rigthBtn.clicked.connect(self.onClickedRightBtn)

        fileNames = os.listdir(self.dirName)
        self.listSize = len(fileNames)
        for fileName in fileNames:
            full_fileName = os.path.join(self.dirName, fileName)
            image = QPixmap(full_fileName)
            image = image.scaledToWidth(512)
            image = image.scaledToWidth(512)
            self.imageList.append(image)


        self.imageLabel = QLabel(self)
        pixmap = self.imageList[self.currentIndex]
        self.imageLabel.setPixmap(pixmap)
        self.imageLabel.setGeometry(10, 10, 512, 512)

    def onClickedLeftBtn(self):
        if self.currentIndex != 0:
            self.currentIndex = self.currentIndex - 1
            pixmap = self.imageList[self.currentIndex]
            self.imageLabel.setPixmap(pixmap)
            self.imageLabel.setGeometry(10, 10, 512, 512)

    def onClickedRightBtn(self):
        if self.currentIndex < self.listSize - 1:
            self.currentIndex = self.currentIndex + 1
            pixmap = self.imageList[self.currentIndex]
            self.imageLabel.setPixmap(pixmap)
            self.imageLabel.setGeometry(10, 10, 512, 512)



app = QApplication(sys.argv)
window = ImageView()
window.show()
app.exec_()