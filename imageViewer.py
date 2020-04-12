import sys
import os
import cv2
import numpy as np
from PIL import Image
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QPen, QImage, QColor
import RedvelvetClassifier as Classifier

face_cascade = cv2.CascadeClassifier('./Model/OpenCV-Python-Series/src/cascades/data/haarcascade_frontalface_default.xml')
model = Classifier.Classifier()
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
        model.loadModel()

        leftBtn = QPushButton("left", self)
        leftBtn.setGeometry(170, 550, 100, 30)
        leftBtn.clicked.connect(self.onClickedLeftBtn)

        rigthBtn = QPushButton("right", self)
        rigthBtn.setGeometry(270, 550, 100, 30)
        rigthBtn.clicked.connect(self.onClickedRightBtn)

        fileNames = os.listdir(self.dirName)
        self.listSize = len(fileNames)
        for fileName in fileNames:
            imageInfo = {'origin' : None, 'image' : None, 'faceRects' : None}
            full_fileName = os.path.join(self.dirName, fileName)
            image = QPixmap(full_fileName)
            image = image.scaled(512, 512, Qt.KeepAspectRatio)
            imageInfo['origin'] = image

            self.imageInfoList.append(imageInfo)

        for imageInfo in self.imageInfoList:
            faceRect = self.getFaceRectangle(imageInfo['origin'])
            imageInfo['faceRects'] = faceRect
            imageInfo['image'] = self.drawRectangle(imageInfo['faceRects'], imageInfo['origin'])

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
        pix = pixmap.copy()
        self.painterInstance = QPainter(pix)
        self.painterInstance.setPen(QColor(255, 0, 0))

        for (x, y, width, height) in faceRects:
            self.painterInstance.drawRect(x, y, width, height)

        return pix

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

    def mousePressEvent(self, event):
        posx = event.x()
        posy = event.y()
        pixmap = self.imageInfoList[self.currentIndex]['image']
        x = (self.windowWidth - pixmap.width()) / 2
        posx = posx - x
        posy = posy - 10
        faceRects = self.imageInfoList[self.currentIndex]['faceRects']

        for (x1, y1, w, h) in faceRects:
            x2 = x1 + w
            y2 = y1 + h

            if x1 <= posx and posx <= x2 and y1 <= posy and posy <= y2:
                inputImage = self.imageInfoList[self.currentIndex]['origin'].copy(x1, y1, w, h)
                inputImage = inputImage.scaled(96, 96)
                img = inputImage.toImage()
                img = img.convertToFormat(QImage.Format_Grayscale8)
                width = img.width()
                height = img.height()

                ptr = img.bits()
                ptr.setsize(img.byteCount())
                arr = np.array(ptr).reshape(height, width, 1)
                model.predictImage(arr)
                break


app = QApplication(sys.argv)
window = ImageView()
window.show()
app.exec_()