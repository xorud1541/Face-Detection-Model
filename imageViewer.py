import sys
import os
import cv2
import numpy as np
from PIL import Image
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QPen, QImage

face_cascade = cv2.CascadeClassifier('./Model/OpenCV-Python-Series/src/cascades/data/haarcascade_frontalface_default.xml')
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

    def getFaceRectangle(self, pixmap):
        img = pixmap.toImage()
        img = img.convertToFormat(4)

        width = img.width()
        height = img.height()

        ptr = img.bits()
        ptr.setsize(img.byteCount())
        arr = np.array(ptr).reshape(height, width, 4)  # Copies the data
        faceRect = face_cascade.detectMultiScale(arr, scaleFactor=1.1, minNeighbors=5)

        return faceRect

app = QApplication(sys.argv)
window = ImageView()
window.show()
app.exec_()