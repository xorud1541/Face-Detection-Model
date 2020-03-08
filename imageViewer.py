import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 200, 600, 550)
        self.setWindowTitle("ImageViewer")

        leftBtn = QPushButton("left", self)
        leftBtn.setGeometry(200, 500, 100, 30)
        leftBtn.clicked.connect(self.onClickedLeftBtn)

        rigthBtn = QPushButton("right", self)
        rigthBtn.setGeometry(300, 500, 100, 30)
        rigthBtn.clicked.connect(self.onClickedRightBtn)

        label = QLabel(self)
        pixmap = QPixmap("./dataset/test/irene/1.jpg")
        label.setPixmap(pixmap)
        label.setGeometry(100, 100, 300, 300)

    def onClickedLeftBtn(self):
        print("왼쪽 버튼 클릭")

    def onClickedRightBtn(self):
        print("오른쪽 버튼 클릭")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()