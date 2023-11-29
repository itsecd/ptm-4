import os
import sys
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import csv
import make_firstCSV
import porting_newDataset
import random_name


class Ui_Image(object):
    def setupUi(self, Image):
        Image.setObjectName("Image")
        Image.resize(832, 734)
        self.centralwidget = QtWidgets.QWidget(Image)
        self.centralwidget.setStyleSheet(
            "    background-color: #f5f0e1;border-radius: 30")
        self.centralwidget.setObjectName("centralwidget")
        self.next_dog = QtWidgets.QPushButton(self.centralwidget)
        self.next_dog.setGeometry(QtCore.QRect(20, 570, 301, 81))
        self.next_dog.setStyleSheet("QPushButton{\n"
                                    "    background-color: #f5f0e1;\n"
                                    "    border: 4px solid #1e3d59;\n"
                                    "    border-radius: 30;\n"
                                    "    color:#1e3d59\n"
                                    "}\n"
                                    "QPushButton:pressed{\n"
                                    "    background-color: #f5f0ef;\n"
                                    "}\n"
                                    "")
        self.next_dog.setObjectName("next_dog")
        self.next_cat = QtWidgets.QPushButton(self.centralwidget)
        self.next_cat.setGeometry(QtCore.QRect(500, 570, 301, 81))
        self.next_cat.setStyleSheet("QPushButton{\n"
                                    "    background-color: #f5f0e1;\n"
                                    "    border: 4px solid #1e3d59;\n"
                                    "    border-radius: 30;\n"
                                    "    color:#1e3d59\n"
                                    "}\n"
                                    "QPushButton:pressed{\n"
                                    "    background-color: #f5f0ef;\n"
                                    "}\n"
                                    "")
        self.next_cat.setObjectName("next_cat")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(-490, 0, 2031, 161))
        self.frame.setStyleSheet("background-color:#1e3d59")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.NAME = QtWidgets.QLabel(self.frame)
        self.NAME.setGeometry(QtCore.QRect(690, 10, 381, 51))
        font = QtGui.QFont()
        font.setFamily("ROG Fonts")
        font.setPointSize(10)
        self.NAME.setFont(font)
        self.NAME.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.NAME.setMouseTracking(False)
        self.NAME.setStyleSheet("color:#f5f0e1")
        self.NAME.setAlignment(QtCore.Qt.AlignCenter)
        self.NAME.setObjectName("NAME")
        self.go_back = QtWidgets.QPushButton(self.frame)
        self.go_back.setGeometry(QtCore.QRect(500, 10, 61, 61))
        self.go_back.setStyleSheet("QPushButton{\n"
                                   "    background-color: #f5f0e1;\n"
                                   "    border: 4px solid #1e3d59;\n"
                                   "    border-radius: 30;\n"
                                   "    color:#1e3d59\n"
                                   "}\n"
                                   "QPushButton:pressed{\n"
                                   "    background-color: #f5f0ef;\n"
                                   "}\n"
                                   "")
        self.go_back.setObjectName("go_back")
        self.Dogimg = QtWidgets.QLabel(self.centralwidget)
        self.Dogimg.setGeometry(QtCore.QRect(30, 170, 361, 351))
        self.Dogimg.setObjectName("Dogimg")
        self.Catimg = QtWidgets.QLabel(self.centralwidget)
        self.Catimg.setGeometry(QtCore.QRect(420, 170, 381, 351))
        self.Catimg.setObjectName("Catimg")
        Image.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Image)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 832, 26))
        self.menubar.setObjectName("menubar")
        Image.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Image)
        self.statusbar.setObjectName("statusbar")
        Image.setStatusBar(self.statusbar)

        self.retranslateUi(Image)
        QtCore.QMetaObject.connectSlotsByName(Image)

    def retranslateUi(self, Image):

        _translate = QtCore.QCoreApplication.translate
        Image.setWindowTitle(_translate("Image", "MainWindow"))
        self.next_dog.setText(_translate("Image", "NEXT DOG"))
        self.next_cat.setText(_translate("Image", "NEXT CAT"))
        self.NAME.setText(_translate(
            "Image", "The  coolest  app  in  the  world"))
        self.go_back.setText(_translate("Image", "BACK"))


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(499, 749)
        font = QtGui.QFont()
        font.setFamily("ROG Fonts")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet(
            "background-color: #f5f0e1;border-radius: 30")
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(-630, 0, 2031, 211))
        self.frame.setStyleSheet("background-color:#1e3d59;border-radius: 30")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.NAME = QtWidgets.QLabel(self.frame)
        self.NAME.setGeometry(QtCore.QRect(690, 10, 381, 51))
        font = QtGui.QFont()
        font.setFamily("ROG Fonts")
        font.setPointSize(10)
        self.NAME.setFont(font)
        self.NAME.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.NAME.setMouseTracking(False)
        self.NAME.setStyleSheet("color:#f5f0e1")
        self.NAME.setAlignment(QtCore.Qt.AlignCenter)
        self.NAME.setObjectName("NAME")
        self.logo = QtWidgets.QLabel(self.frame)
        self.logo.setGeometry(QtCore.QRect(630, 100, 111, 141))
        self.logo.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap(
            f"{os.getcwd()}/img/imgonline-com-ua-Resize-eaZg8IxsenvxUV.png"))
        self.logo.setObjectName("logo")
        self.logo_2 = QtWidgets.QLabel(self.frame)
        self.logo_2.setGeometry(QtCore.QRect(730, 120, 101, 101))
        self.logo_2.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.logo_2.setText("")
        self.logo_2.setPixmap(QtGui.QPixmap(
            f"{os.getcwd()}/img/imgonline-com-ua-Resize-eaZg8IxsenvxUV.png"))
        self.logo_2.setObjectName("logo_2")
        self.logo_3 = QtWidgets.QLabel(self.frame)
        self.logo_3.setGeometry(QtCore.QRect(830, 120, 101, 101))
        self.logo_3.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.logo_3.setText("")
        self.logo_3.setPixmap(QtGui.QPixmap(
            f"{os.getcwd()}/img/imgonline-com-ua-Resize-eaZg8IxsenvxUV.png"))
        self.logo_3.setObjectName("logo_3")
        self.logo_5 = QtWidgets.QLabel(self.frame)
        self.logo_5.setGeometry(QtCore.QRect(930, 120, 101, 101))
        self.logo_5.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.logo_5.setText("")
        self.logo_5.setPixmap(QtGui.QPixmap(
            f"{os.getcwd()}/img/imgonline-com-ua-Resize-eaZg8IxsenvxUV.png"))
        self.logo_5.setObjectName("logo_5")
        self.logo_4 = QtWidgets.QLabel(self.frame)
        self.logo_4.setGeometry(QtCore.QRect(1030, 120, 101, 101))
        self.logo_4.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.logo_4.setText("")
        self.logo_4.setPixmap(QtGui.QPixmap(
            f"{os.getcwd()}/img/imgonline-com-ua-Resize-eaZg8IxsenvxUV.png"))
        self.logo_4.setObjectName("logo_4")
        self.fullWay = QtWidgets.QLineEdit(self.centralwidget)
        self.fullWay.setGeometry(QtCore.QRect(50, 220, 380, 60))
        font = QtGui.QFont()
        font.setFamily("Algerian")
        font.setPointSize(14)
        self.fullWay.setFont(font)
        self.fullWay.setStyleSheet("background-color:#f5f0e1;\n"
                                   "border: 4px solid #1e3d59;\n"
                                   "border-radius: 30;\n"
                                   "color:#1e3d59\n"
                                   "")
        self.fullWay.setAlignment(QtCore.Qt.AlignCenter)
        self.fullWay.setObjectName("fullWay")
        self.CreateFirstCSV = QtWidgets.QPushButton(self.centralwidget)
        self.CreateFirstCSV.setGeometry(QtCore.QRect(270, 400, 211, 61))
        font = QtGui.QFont()
        font.setFamily("Algerian")
        self.CreateFirstCSV.setFont(font)
        self.CreateFirstCSV.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.CreateFirstCSV.setStyleSheet("QPushButton{\n"
                                          "    background-color: #f5f0e1;\n"
                                          "    border: 4px solid #1e3d59;\n"
                                          "    border-radius: 30;\n"
                                          "    color:#1e3d59\n"
                                          "}\n"
                                          "QPushButton:pressed{\n"
                                          "    background-color: #f5f0ef;\n"
                                          "}\n"
                                          "")
        self.CreateFirstCSV.setObjectName("CreateFirstCSV")
        self.IMPORTdataset = QtWidgets.QPushButton(self.centralwidget)
        self.IMPORTdataset.setGeometry(QtCore.QRect(20, 400, 211, 61))
        font = QtGui.QFont()
        font.setFamily("Algerian")
        self.IMPORTdataset.setFont(font)
        self.IMPORTdataset.setStyleSheet("QPushButton{\n"
                                         "    background-color: #f5f0e1;\n"
                                         "    border: 4px solid #1e3d59;\n"
                                         "    border-radius: 30;\n"
                                         "    color:#1e3d59\n"
                                         "}\n"
                                         "QPushButton:pressed{\n"
                                         "    background-color: #f5f0ef;\n"
                                         "}\n"
                                         "")
        self.IMPORTdataset.setObjectName("IMPORTdataset")
        self.RANDOM = QtWidgets.QPushButton(self.centralwidget)
        self.RANDOM.setGeometry(QtCore.QRect(270, 500, 211, 61))
        font = QtGui.QFont()
        font.setFamily("Algerian")
        self.RANDOM.setFont(font)
        self.RANDOM.setStyleSheet(
            "QPushButton{\n"
            "    background-color: #f5f0e1;\n"
            "    border: 4px solid #1e3d59;\n"
            "    border-radius: 30;\n"
            "    color:#1e3d59\n"
            "}\n"
            "QPushButton:pressed{\n"
            "    background-color: #f5f0ef;\n"
            "}\n"
            "")
        self.RANDOM.setObjectName("RANDOM")
        self.NEXTimg = QtWidgets.QPushButton(self.centralwidget)
        self.NEXTimg.setGeometry(QtCore.QRect(20, 500, 211, 61))
        font = QtGui.QFont()
        font.setFamily("Algerian")
        self.NEXTimg.setFont(font)
        self.NEXTimg.setStyleSheet("QPushButton{\n"
                                   "    background-color: #f5f0e1;\n"
                                   "    border: 4px solid #1e3d59;\n"
                                   "    border-radius: 30;\n"
                                   "    color:#1e3d59\n"
                                   "}\n"
                                   "QPushButton:pressed{\n"
                                   "    background-color: #f5f0ef;\n"
                                   "}\n"
                                   "")
        self.NEXTimg.setObjectName("NEXTimg")
        self.take = QtWidgets.QPushButton(self.centralwidget)
        self.take.setGeometry(QtCore.QRect(130, 290, 211, 51))
        font = QtGui.QFont()
        font.setFamily("Algerian")
        self.take.setFont(font)
        self.take.setStyleSheet("QPushButton{\n"
                                "    background-color: #f5f0e1;\n"
                                "    border: 4px solid #1e3d59;\n"
                                "    border-radius: 25;\n"
                                "    color:#1e3d59\n"
                                "}\n"
                                "QPushButton:pressed{\n"
                                "    background-color: #f5f0ef;\n"
                                "}\n"
                                "")
        self.take.setObjectName("take")
        self.EXIT = QtWidgets.QPushButton(self.centralwidget)
        self.EXIT.setGeometry(QtCore.QRect(140, 610, 211, 61))
        font = QtGui.QFont()
        font.setFamily("Algerian")
        font.setPointSize(20)
        self.EXIT.setFont(font)
        self.EXIT.setStyleSheet("QPushButton{\n"
                                "    background-color: #f5f0e1;\n"
                                "    border: 4px solid #1e3d59;\n"
                                "    border-radius: 30;\n"
                                "    color:#1e3d59\n"
                                "}\n"
                                "QPushButton:pressed{\n"
                                "    background-color: #f5f0ef;\n"
                                "}\n"
                                "")
        self.EXIT.setObjectName("EXIT")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 499, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.NAME.setText(_translate(
            "MainWindow", "The  coolest  app  in  the  world"))
        self.fullWay.setText(_translate("MainWindow", "INPUT FULL WAY"))
        self.CreateFirstCSV.setText(_translate(
            "MainWindow", "1.Create the first csv file"))
        self.IMPORTdataset.setText(_translate(
            "MainWindow", "2.Import in thr new dataset"))
        self.RANDOM.setText(_translate("MainWindow", "3.random dataset"))
        self.NEXTimg.setText(_translate("MainWindow", "output next img"))
        self.take.setText(_translate("MainWindow", "take the path"))
        self.EXIT.setText(_translate("MainWindow", "EXIT"))


class IteratorM:
    def __init__(self, file_name: str, class_name: str) -> None:
        self.limit = -1
        self.counter = -1
        self.file_name = file_name
        self.class_name = class_name
        self.rows = []
        with open(f"{file_name}.csv") as file:
            reader = csv.reader(file, delimiter=";")
            for row in reader:
                if row[2] == class_name:
                    self.rows.append(row[0] + ";" + row[2])
                    self.limit += 1

    def __iter__(self):
        return self

    def __next__(self) -> str:
        if self.counter < self.limit:
            self.counter += 1
            return (self.rows[self.counter])[:-6]
        else:
            print("None")
            raise StopIteration


def push_exit():
    sys.exit(app.exec_())


def push_takepath():
    global check_way
    global full_way
    full_way = ui.fullWay.text()+"/"
    if (os.path.exists(ui.fullWay.text()+"/CatIT") == False):
        msg = QMessageBox()
        msg.setWindowTitle("Ошибка")
        msg.setText("файлы не найдены!\nВведите путь еще раз")
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()
        check_way = False
    else:
        check_way = True
        print(full_way)


def make_iter():
    global li_cat
    global li_dog
    global ro
    class_dog = "DogIT"
    li_dog = IteratorM("Dataset_firstCSV", class_dog)
    class_cat = "CatIT"
    li_cat = IteratorM("Dataset_firstCSV", class_cat)


def script_1():
    global check_way
    global first_csv
    global check_firstCSV
    global check_file
    if (check_way == True):
        first_csv = "Dataset_firstCSV"
        make_firstCSV.make_csv(first_csv)
        make_firstCSV.make_file_abstract("DogIT", full_way, first_csv)
        make_firstCSV.make_file_abstract("CatIT", full_way, first_csv)
        check_firstCSV = True
        check_file = True
        if (ro == False):
            make_iter()
    else:
        msg = QMessageBox()
        msg.setWindowTitle("Ошибка!!!")
        msg.setText("Установлен неверный путь!!!\nВведите путь еще раз!!!")
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()


def script_2():
    global first_csv
    global check_way
    global check_firstCSV
    if (check_firstCSV == True):
        class_csv = "dataset_class"
        make_firstCSV.make_csv(class_csv)
        porting_newDataset.porting(first_csv, class_csv)
    else:
        msg = QMessageBox()
        msg.setWindowTitle("Ошибка!!!")
        msg.setText("Пожалуйста создайте первый CSV файл, чтобы продолжить")
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()


def script_3():
    global check_way
    global first_csv
    if (check_file == True):
        random_csv = "dataset_random"
        make_firstCSV.make_csv(random_csv)
        random_name.random_name(first_csv, random_csv)
    else:
        msg = QMessageBox()
        msg.setWindowTitle("Ошибка!!!")
        msg.setText("Установлен неверный путь!!!\nВведите путь еще раз!!!")
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()


def open_window_two():

    if (check_file):
        Image = QtWidgets.QMainWindow()
        Image.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        Image.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        ui = Ui_Image()
        ui.setupUi(Image)
        Application.close()
        Image.show()

        def button_dog():
            a = next(li_dog)
            ui.Dogimg.setPixmap(QtGui.QPixmap(a))
            print(a)

        def button_cat():
            b = next(li_cat)
            ui.Catimg.setPixmap(QtGui.QPixmap(b))
            print(b)

        def returnHub():
            Image.close()
            Application.show()

        ui.go_back.clicked.connect(returnHub)
        ui.next_dog.clicked.connect(button_dog)
        ui.next_cat.clicked.connect(button_cat)
    else:
        msg = QMessageBox()
        msg.setWindowTitle("Ошибка!!!")
        msg.setText(
            "Вы еще не создали первый CSV файл\nПожалуйста, нажмите на кнопку 'Create the first csv file' и повторите попытку ")
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()


if __name__ == "__main__":
    full_way = ''
    check_way = False
    check_dataset = False
    first_csv = ""
    check_firstCSV = False
    import sys
    ro = False
    check_file = os.path.exists("Dataset_firstCSV.csv")
    if (check_file == True):
        first_csv = "Dataset_firstCSV"
        make_iter()
        ro = True
    app = QtWidgets.QApplication(sys.argv)
    Application = QtWidgets.QMainWindow()
    Application.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    Application.setAttribute(QtCore.Qt.WA_TranslucentBackground)
    ui = Ui_MainWindow()
    ui.setupUi(Application)
    Application .show()
    app.setWindowIcon(
        QIcon('C:/Users/79093/Desktop/Application progra/laba3/GUI_lab/img/icon.ico'))
    ui.EXIT.clicked.connect(push_exit)
    ui.take.clicked.connect(push_takepath)
    ui.CreateFirstCSV.clicked.connect(script_1)
    ui.IMPORTdataset.clicked.connect(script_2)
    ui.RANDOM.clicked.connect(script_3)
    ui.NEXTimg.clicked.connect(open_window_two)
    sys.exit(app.exec_())