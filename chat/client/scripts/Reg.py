import sys
import threading
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import socket
from proverka import check_password
from PyQt5.QtCore import QThread

class REG(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('forms/reg.ui', self)  # Загружаем дизайн
        self.code_server = ''
        self.pb_code.clicked.connect(self.get_the_code)
        self.pb_reg.clicked.connect(self.registrations)
        self.email_proverka = ''
        self.ip = ''
        self.CLass = ''

    """метод для регистрации"""

    def registrations(self):
        ip = self.ip
        Chat = self.CLass
        if len(self.emai_userl.text()) < 5:  #  проверка на непустое ли полк для ввода
            self.error.setText("Ошибка в первом поле")
        elif len(self.name_user.text()) < 5:  #проверка на непустое ли полк для ввода
            self.error.setText("Ошибка во втором поле")
        else:
            """проверка паролей"""
            try:
                if check_password(self.password.text()):
                    pass
            except Exception as error:
                self.error.setText(str(error))
            else:
                if self.password.text() != self.password1.text():
                    self.error.setText("пароли не совпадают")
                    """проверка кода"""
                elif len(self.code.text()) == 0:
                    self.error.setText("Ведите код")
                elif self.code_server != self.code.text():
                    self.error.setText("код не верный")
                    self.code_server = ''
                elif self.email_proverka != self.emai_userl.text():  # проверка на почту если пользователь сменит поч
                    # ту кагда получил код
                    self.email_proverka = ''
                    self.code_server = ''
                    self.error.setText("Не та почта")
                else:
                    """отправка данных для проверки и продолжения"""
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создаем сокет
                    try:
                        sock.connect((ip, 4444))  # подключаемся
                    except Exception:
                        self.error.setText("Проверьте подключение")  # ну тут понятно
                    else:
                        """после того как подключились отпровляем строку с данными"""
                        stroka = 'reg ' + self.emai_userl.text() + ' ' + self.password.text() + ' ' + \
                                 self.name_user.text()
                        sock.send(stroka.encode('utf-8'))  # вот тут мы и отпровляем данные
                        res = sock.recv(1024)  # тут приходит ответ  от проверки
                        msg = res.decode('utf-8')  # переводим сообщени в строку
                        """дальше по условиям понятно"""
                        if msg == 'ok':
                            client = self.name_user.text()
                            print('ura')
                            sock.close()
                            self.hide()
                            Chat.arg(ip, client)
                            Chat.show()
                        elif msg == 'email занят':
                            self.error.setText(msg)
                        elif msg == 'имя занято':
                            self.error.setText(msg)
                        sock.close()
    """метод для настройки"""
    def Arg(self,ip,name):
        self.CLass = name
        self.ip = ip
    """метод для получения кода для проверки"""

    def get_the_code(self):
        ip = self.ip
        self.error.setText("")
        """я уже писал об этом"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((ip, 4444))
        except Exception:
            self.error.setText("Проверьте подключение")
        else:
            """тут мы отпровляем наш email"""
            if len(self.emai_userl.text()) > 0:
                self.email_proverka = self.emai_userl.text()
                stroka = 'код ' + self.emai_userl.text()
                sock.send(stroka.encode('utf-8'))
                """получаем код"""
                res = sock.recv(1024)
                self.code_server = res.decode('utf-8')
            sock.close()
            print(self.code_server)