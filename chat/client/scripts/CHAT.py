import sys
from PyQt5 import uic
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication, QMainWindow
import socket


class chat(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('forms/чат.ui', self)
    """функция настройки"""
    def arg(self,ip,name):
        self.ip = ip
        self.name = name
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создается сокет
        sock.connect((ip, 5555))  # подключение к серверу
        self.sock = sock
        self.plainTextEdit.setReadOnly(True)
        self.msg = ''
        self.plainTextEdit.insertPlainText('')
        self.LISTEn = Listen(self.sock, self.ip, mainwindow=self.plainTextEdit)  # создается класс прослушка в котрый передаем сокет, ip и self.plainTextEdit
        self.LISTEn.start()  # запускается в отдельном потоке об этом ниже
        self.pushButton.clicked.connect(self.Send)
    """функция за себя говорит"""

    def Send(self):
        if self.lineEdit.text() != '':
            self.sock.send(f'{self.name}:\n{self.lineEdit.text()}\n\n'.encode('utf-8'))
            self.plainTextEdit.insertPlainText(f'{self.name}:\n{self.lineEdit.text()}\n\n')
            self.lineEdit.setText('')
        else:
            pass


class Listen(QThread): # класс который наследуются от класса QThread
    def __init__(self, sock, ip, mainwindow):
        super().__init__()
        self.sock = sock
        self.mainwindow = mainwindow

    def run(self):
        while True:
            res = self.sock.recv(104857600) # ждем сообщение не больше 100мб(в recv пишутся байты)
            self.mainwindow.insertPlainText(res.decode('utf-8'))
