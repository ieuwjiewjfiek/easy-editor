from PIL import Image
from PIL import ImageFilter
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import  QFileDialog, QLineEdit, QListWidget, QTextEdit, QApplication, QGroupBox, QMessageBox, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QRadioButton
import os
from PIL import Image
from PIL import ImageFilter
from PyQt5.QtGui import QPixmap
app = QApplication([])
widget = QWidget()

btn_folder = QPushButton('Папка')
btn_left = QPushButton('Лево')
btn_right = QPushButton('Право')
btn_mirrow = QPushButton('Зеркало')
btn_sharpness = QPushButton('Резкость')
btn_black = QPushButton('Ч/Б')
list_widget = QListWidget()
text  = QLabel('Картинка')

widget.resize(1200,700)


horizontal_1 = QHBoxLayout()
horizontal_2 = QHBoxLayout()
column_1 = QVBoxLayout()
column_2 = QVBoxLayout()


column_1.addWidget(btn_folder)
column_1.addWidget(list_widget)
column_2.addWidget(text, 95)
horizontal_2.addWidget(btn_left,  stretch = 10)
horizontal_2.addWidget(btn_right,  stretch = 10)
horizontal_2.addWidget(btn_mirrow,  stretch = 10)
horizontal_2.addWidget(btn_sharpness,  stretch = 10)
horizontal_2.addWidget(btn_black,  stretch = 10)


horizontal_1.addLayout(column_1,20)
horizontal_1.addLayout(column_2, 80)
column_2.addLayout(horizontal_2)
widget.setLayout(horizontal_1)

workdir = ''
def choseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()   
def filter(files, extensions):
    result = []
    for filename in files:
        for extension in extensions:
            if filename.endswith(extension):
                result.append(filename)
    return result
def showFilenameerList():
    choseWorkdir()
    extensions = ['.jpg', '.gif', '.jpeg', '.png', '.bmp']
    filenames = filter(os.listdir(workdir), extensions)
    list_widget.clear()
    for filename in filenames:
        list_widget.addItem(filename)
class ImageProcessor():
    def __init__(self):
        self.image = None
        self.filename = None
        self.save_dir = 'Modified/'
    def loadImage(self, filename):
        self.filename = filename
        image_path = os.path.join(workdir, filename)
        self.image = Image.open(image_path)
    def showImage(self, path):
        text.hide()
        pixmapimage = QPixmap(path)
        w, h = text.width(), text.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        text.setPixmap(pixmapimage)
        text.show()
    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not (os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)
    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def left_rotate(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path1 = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path1)
    def right_rotate(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path2 = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path2)
    def mirrow_rotate(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path3 = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path3)
    def sharpness(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.saveImage()
        image_path4 = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path4)

workimage = ImageProcessor()

def showChosenImage():

    if list_widget.currentRow() >= 0:
        filename = list_widget.currentItem().text()
        workimage.loadImage(filename)
        image_path = os.path.join(workdir, workimage.filename)
        workimage.showImage(image_path)


list_widget.currentRowChanged.connect(showChosenImage)
btn_black.clicked.connect(workimage.do_bw) 
btn_left.clicked.connect(workimage.left_rotate) 
btn_right.clicked.connect(workimage.right_rotate) 
btn_mirrow.clicked.connect(workimage.mirrow_rotate)
#btn_sharpness.clicked.connect(workimage.sharpness)
btn_folder.clicked.connect(showFilenameerList)   

widget.show()
app.exec_()
