import sys
import os
import cv2
import numpy as np
from PIL import Image
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QPen, QImage, QColor

face_cascade = cv2.CascadeClassifier('./Model/OpenCV-Python-Series/src/cascades/data/haarcascade_frontalface_default.xml')
class ImageView(QMainWindow):
    currentIndex = 0
    listSize = 0
    windowWidth = 530
    windowHeight = 600
    imageInfoList = []
    dirName = 'Model/dataset/image'
    imageLabel = QLabel

    def __init__(self):
        super().__init__()
        self.setGeometry(100, 200, self.windowWidth, self.windowHeight)
        self.setWindowTitle("ImageViewer")
        self.setMouseTracking(True)

        leftBtn = QPushButton("left", self)
        leftBtn.setGeometry(170, 550, 100, 30)
        leftBtn.clicked.connect(self.onClickedLeftBtn)

        rigthBtn = QPushButton("right", self)
        rigthBtn.setGeometry(270, 550, 100, 30)
        rigthBtn.clicked.connect(self.onClickedRightBtn)

        fileNames = os.listdir(self.dirName)
        self.listSize = len(fileNames)
        for fileName in fileNames:
            imageInfo = {'image' : None, 'faceRects' : None}
            full_fileName = os.path.join(self.dirName, fileName)
            image = QPixmap(full_fileName)
            image = image.scaled(512, 512, Qt.KeepAspectRatio)
            imageInfo['image'] = image

            self.imageInfoList.append(imageInfo)

        for imageInfo in self.imageInfoList:
            faceRect = self.getFaceRectangle(imageInfo['image'])
            imageInfo['faceRects'] = faceRect
            self.drawRectangle(imageInfo['faceRects'], imageInfo['image'])

        self.imageLabel = QLabel(self)
        pixmap = self.imageInfoList[self.currentIndex]['image']
        self.imageLabel.setPixmap(pixmap)
        x = (self.windowWidth - pixmap.width()) / 2
        self.imageLabel.setGeometry(x, 10, 512, 512)

    def onClickedLeftBtn(self):
        if self.currentIndex != 0:
            self.currentIndex = self.currentIndex - 1
            pixmap = self.imageInfoList[self.currentIndex]['image']
            self.imageLabel.setPixmap(pixmap)
            x = (self.windowWidth - pixmap.width()) / 2
            self.imageLabel.setGeometry(x, 10, 512, 512)

    def onClickedRightBtn(self):
        if self.currentIndex < self.listSize - 1:
            self.currentIndex = self.currentIndex + 1
            pixmap = self.imageInfoList[self.currentIndex]['image']
            self.imageLabel.setPixmap(pixmap)
            x = (self.windowWidth - pixmap.width()) / 2
            self.imageLabel.setGeometry(x, 10, 512, 512)

    def drawRectangle(self, faceRects, pixmap):
        self.painterInstance = QPainter(pixmap)
        self.painterInstance.setPen(QColor(255, 0, 0))

        for (x, y, width, height) in faceRects:
            self.painterInstance.drawRect(x, y, width, height)

        return pixmap

    def getFaceRectangle(self, pixmap):
        img = pixmap.toImage()
        img = img.convertToFormat(4)

        width = img.width()
        height = img.height()

        ptr = img.bits()
        ptr.setsize(img.byteCount())
        arr = np.array(ptr).reshape(height, width, 4)
        faceRect = face_cascade.detectMultiScale(arr, scaleFactor=1.1, minNeighbors=5)

        return faceRect

    def mouseMoveEvent(self, event):
        posx = event.x()
        posy = event.y()

        faceRects = self.imageInfoList[self.currentIndex]['faceRects']

        for (x1, y1, w, h) in faceRects:
            x2 = x1 + w
            y2 = y1 + h

            if x1 <= posx and posx <= x2 and y1 <= posy and posy <= y2:
                print('in')
                break


app = QApplication(sys.argv)
window = ImageView()
window.show()
app.exec_()