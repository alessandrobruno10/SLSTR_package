import sys
import rad_to_reflectance
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QDialog

#this GUI code has been tested over a Macbook Pro with MacOS Mojave version 10.14.6
class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'SLSTR Data Processing'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        label = QLabel(self)
        pixmap = QPixmap('satellite.jpg');
        label.setPixmap(pixmap)
        self.resize(pixmap.width(),pixmap.height())
        button = QPushButton('Browse SLSTR product folder...', self)
        button.setToolTip('This is an example button')
        button.resize(240,60)
        button.move(160,180)
        button.clicked.connect(self.on_click)

        self.show()

    @pyqtSlot()
    def on_click(self):
        print('Loading SLSTR product')
        filename = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        rad_to_reflectance.rad_to_reflectance(filename)

#GUI starts by asking users to browse the SLSTR product folder
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
