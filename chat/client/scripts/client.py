import sys
import threading
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import socket
from proverka import check_password
from CHAT import chat
from PyQt5.QtCore import QThread
from Reg import REG
from PyQt5.QtWidgets import QInputDialog

file = open('Ip.txt', mode='r')
file = file.readlines()
if len(file):
    ip = file[0]
else:
    ip = ''  # ip принтуется в сервере!!!!!!!!!!!!!!!!!!!!!!


class ENTER(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('forms/заход для клиента.ui', self)
        self.enter.clicked.connect(self.Enter)
        self.registration.clicked.connect(self.Reg)
        self.setting_up_ip.clicked.connect(self.setting)

    """функция для входа"""

    def Enter(self):
        global ip
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.email.text() != '' and self.password.text() != '':  # проверка на непустые ли поля ввода
            try:
                sock.connect((ip, 4444))  # подключение к сокету сервера
            except Exception:
                self.label_3.setText('проверьте подключение')
            else:
                stroka = 'вход ' + self.email.text() + ' ' + self.password.text()  # собираем строку где первое слово команнда для мервера 2 наш email 3 пароль
                sock.send(stroka.encode('utf-8'))  # отпровляем эту строку
                res = sock.recv(1024)  # принимаем ответ
                res = res.decode('utf-8')
                if res == 'нет такого пользователя':
                    self.label_3.setText(res)
                else:
                    """меняем форму"""
                    sock.close()
                    self.hide()
                    Chat.arg(ip, res)
                    Chat.show()
        sock.close()

    """функция для начало работы класса REG"""

    def Reg(self):  # запускаем форму регистрации
        global ip
        self.hide()
        reg.Arg(ip,Chat)
        reg.show()
    """функция для замены ip"""
    def setting(self):
        global ip
        Ip, ok_pressed = QInputDialog.getText(self, "Введите ip", f'{ip}')
        if ok_pressed:
            with open('Ip.txt', mode="w") as file:
                file.write(f'{Ip}')
            ip = Ip






app = QApplication(sys.argv)
enter = ENTER()
enter.show()
reg = REG()
reg.hide()
Chat = chat()
Chat.hide()
sys.exit(app.exec_())
