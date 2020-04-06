import sys
import os
from PIL import Image
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap

class ImageView(QMainWindow):
    currentIndex = 0
    imageList = []
    dirName = 'dataset/image'
    imageLabel = QLabel
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 200, 530, 600)
        self.setWindowTitle("ImageViewer")

        leftBtn = QPushButton("left", self)
        leftBtn.setGeometry(170, 550, 100, 30)
        leftBtn.clicked.connect(self.onClickedLeftBtn)

        rigthBtn = QPushButton("right", self)
        rigthBtn.setGeometry(270, 550, 100, 30)
        rigthBtn.clicked.connect(self.onClickedRightBtn)

        fileNames = os.listdir(self.dirName)
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
        self.currentIndex = self.currentIndex - 1
        pixmap = self.imageList[self.currentIndex]
        self.imageLabel.setPixmap(pixmap)
        self.imageLabel.setGeometry(10, 10, 512, 512)

    def onClickedRightBtn(self):
        self.currentIndex = self.currentIndex + 1
        pixmap = self.imageList[self.currentIndex]
        self.imageLabel.setPixmap(pixmap)
        self.imageLabel.setGeometry(10, 10, 512, 512)



app = QApplication(sys.argv)
window = ImageView()
window.show()
app.exec_()