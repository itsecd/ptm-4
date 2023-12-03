import sys
from time import time
import logging, logging.config
import my_logger

from PyQt5 import QtWidgets
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QFont, QRegExpValidator
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QProgressBar

import alg_luhn
import gen_num
import graph
import read_settings


class Window(QMainWindow):
    """Основной класс нашей програмы"""

    def create_graph(self):
        """Создаем и передаем данные для  """
        self.cores = [1, 2, 3, 4, 5, 6, 7, 8]
        self.times = []
        for i in self.cores:
            self.start = time()
            self.result = gen_num.num_selection(self.data, i)
            self.end = time()
            self.times.append(self.end - self.start)
            print(self.end - self.start)
            second = self.end - self.start
            if int(second) > 80: # такая проверка для вида работы логера, цифра условная, условие выполняется на 1 варианте
                logger.warning("The calculation is long. Check the input data")
            self.pbar.setValue(12 * i)
        self.pbar.setValue(100)
        logger.debug("The hash calculation for option %s has begun", str(self.variant_label.text()))
        self.main_function()

    def main_function(self):
        """Предлагаем пользователю что нужно выполнить"""
        self.check_by_alg_moon.show()
        self.button_restart.show()
        self.button_show_graph.show()
        self.pbar.hide()
        self.first_text.setText(
            "Вуаля, процесс закончен!\n   Что желаете сделать?")
        self.first_text.adjustSize()

    def progress(self, variant):
        """Работа прогресс бара"""
        self.data = read_settings.read_json(variant)
        self.pbar.setValue(0)
        self.create_graph()

    def button_start_click(self):
        """Начало работы программы, предлагает выбрать вариант, после корректного
        ввода передает данные в функцию progress, для дальнейших вычислений."""
        if self.variant_label.text() != '':
            if int(self.variant_label.text()) > 20:
                logger.warning("The user entered a non-existent option. Repeat the request")
                QMessageBox.about(self, "Ошибка", "Нет такого варианта")

                self.variant_label.clear()
            else:

                self.button_start.hide()
                self.first_text.setText("Подождите, идет загрузка!\n")
                self.first_text.adjustSize()
                self.variant_label.hide()
                self.pbar.show()
                self.progress(self.variant_label.text())
        else:
            QMessageBox.about(self, "Ошибка", "Пустое поле недопустимо")
            logger.warning("The user did not select an option. Repeat the request")

    def button_restart_click(self):
        """Возвращает стартовый экран"""
        self.first_text.setText("Введите номер варианта")
        self.first_text.adjustSize()
        self.button_restart.hide()
        self.check_by_alg_moon.hide()
        self.button_show_graph.hide()
        self.variant_label.clear()
        self.variant_label.show()
        self.button_start.show()
        logger.debug("Return to the home page, completed")


    def button_show_graph_click(self):
        """Вызываем функцию создания графика"""
        graph.show_plt(self.cores, self.times)
        logger.debug("The graph is shown successfully")


    def check_by_alg_moon_click(self):
        """Вызываем алгоритм луна"""
        if alg_luhn.alg_luhn(self.result):
            QMessageBox.about(
                self, "Успех", "Последовательность прошла алгоритм луна")
        else:
            QMessageBox.about(
                self,
                "Провал",
                "Последовательность провалила алгоритм луна")

    def set_position(self):
        """Устанавливаем позицию для каждого элемента, кнопки, текст и тд"""
        self.first_text.move(390, 200)
        self.variant_label.move(465, 250)
        self.button_start.move(445, 310)
        self.button_show_graph.move(445, 310)
        self.button_restart.move(330, 310)
        self.check_by_alg_moon.move(560, 310)
        self.pbar.move(375, 310)

    def set_size(self):
        """Устанавливаем размер для каждого элемента, кнопки, текст и тд"""
        self.variant_label.setFixedSize(60, 40)
        self.first_text.adjustSize()
        self.button_start.setFixedSize(100, 30)
        self.check_by_alg_moon.setFixedSize(100, 30)
        self.button_show_graph.setFixedSize(100, 30)
        self.button_restart.setFixedSize(100, 30)
        self.pbar.setFixedSize(300, 30)

    def set_value(self):
        """Устанавливаем текст для обектов"""
        self.first_text.setFont(QFont('Times', 14))
        self.first_text.setText("Введите номер варианта")
        self.button_start.setText("Продолжить")
        self.button_show_graph.setText("График")
        self.check_by_alg_moon.setText("Алгоритм Луна")
        self.button_restart.setText("Перезапустить")

    def __init__(self) -> None:
        """конструктор, инициализируем все, и даже больше"""
        super(Window, self).__init__()
        self.cores = None
        self.end = None
        self.start = None
        self.arguments_for_check_hash = None
        self.times = None
        self.result = None
        self.data = None
        self.first_text = QtWidgets.QLabel(self)
        self.variant_label = QtWidgets.QLineEdit(self)
        self.button_start = QtWidgets.QPushButton(self)
        self.button_restart = QtWidgets.QPushButton(self)
        self.button_show_graph = QtWidgets.QPushButton(self)
        self.check_by_alg_moon = QtWidgets.QPushButton(self)
        reg_variant = QRegExp("[1-9][0-9]")
        input_validator = QRegExpValidator(reg_variant, self.variant_label)
        self.variant_label.setValidator(input_validator)
        self.button_start.clicked.connect(self.button_start_click)
        self.button_restart.clicked.connect(self.button_restart_click)
        self.button_show_graph.clicked.connect(self.button_show_graph_click)
        self.check_by_alg_moon.clicked.connect(self.check_by_alg_moon_click)
        self.pbar = QProgressBar(self)
        self.pbar.hide()
        self.button_show_graph.hide()
        self.button_restart.hide()
        self.check_by_alg_moon.hide()
        self.set_value()
        self.set_position()
        self.set_size()
        logger.debug("The program was built successfully")

def application() -> None:
    """"Start aplication mainwindow"""
    app = QApplication(sys.argv)
    window = Window()
    window.setObjectName("MainWindow")
    window.setMinimumSize(1000, 800)
    window.setMaximumSize(1024, 720)
    window.setStyleSheet("#MainWindow{border-image:url(phon.png)}")
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    """Начало начал, запускаем основную функцию application()"""
    # logger = logging.getLogger(__file__)
    # logger.setLevel(logging.DEBUG)
    # formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s')
    # console_handler = logging.StreamHandler()
    # file_handler = logging.FileHandler("example.log")
    # console_handler.setLevel(logging.DEBUG)
    # file_handler.setLevel(logging.WARNING)
    # console_handler.setFormatter(formatter)
    # file_handler.setFormatter(formatter)
    # logger.addHandler(console_handler)
    # logger.addHandler(file_handler)
    logger = my_logger.My_log(__file__).get_logger()
    application()

