import socket
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3

import random


class Chat_Enter:
    def __init__(self, ip):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создаем сокет

        sock.bind((ip, 4444))  # даем сокету ip и порт
        sock.listen()  # запускаем режим прослушивания

        self.socket = sock
        self.code = ''
        self.RES = ''

    def Start(self):
        print('enter on')
        while True:
            try:
                client, addr = self.socket.accept()  # ожидаем подключение
            except socket.error:
                pass
            else:
                res = client.recv(1024)  # ожидае сообщения
                res = res.decode("utf-8")  # переводим сообщение в строку
                res = res.split()
                if res[0] == 'код':
                    self.Send_kod(res[1])  # функция для отправки кода на почту
                    if self.RES != '':
                        print(self.RES)
                    client.send(self.code.encode('utf-8'))  # отправка пользователю код для проверки
                elif res[0] == 'вход':
                    email = res[1]
                    password = res[2]
                    con = sqlite3.connect("DATA_USER.SQL")
                    cur = con.cursor()
                    res_sql = cur.execute(f"""SELECT name FROM user_info \
                                                          WHERE email='{email}' and password='{password}'""").fetchall()
                    if len(res_sql) == 1:  # если пользователь есть то отпровляем имя иначе ошибку
                        client.send(res_sql[0][0].encode('utf-8'))
                    else:
                        client.send('нет такого пользователя'.encode('utf-8'))
                elif res[0] == 'reg': # если пользователь хочет зарегистрироваться там все понятно по отпровляемых сообщений
                    con = sqlite3.connect("DATA_USER.SQL")
                    cur = con.cursor()
                    res_sql = cur.execute(f"""SELECT email FROM user_info \
                                       WHERE email='{res[1]}'""").fetchall()
                    print(res_sql)
                    if len(res_sql) == 0:
                        res_sql = con.execute(f"""SELECT * FROM user_info \
                                                               WHERE name ='{res[3]}'""").fetchall()
                        if len(res_sql) != 0:
                            client.send('имя занято'.encode('utf-8'))
                            con.close()
                        else:
                            """если все ок то добовляем в бд данные пользователя"""
                            con.execute(
                                f"""INSERT INTO user_info (email, password, name) VALUES ('{res[1]}', '{res[2]}', '{res[3]}') """)
                            con.commit()
                            client.send('ok'.encode('utf-8'))
                            con.close()
                    else:
                        client.send('email занят'.encode('utf-8'))
                client.close

    def Send_kod(self, email1):
        self.RES = ''

        msg = MIMEMultipart()
        email = 'chat_yandex@mail.ru'
        password = 'F5qbmzLQf05MMWcNywMA'
        to_email = email1
        self.code = str(random.randint(0, 9999))
        try:
            """настрока почты сервера"""
            msg.attach(MIMEText(self.code, 'plain'))
            server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
            server.login(email, password)
            """отправка сообщения"""
            server.sendmail(email, to_email, msg.as_string())
            server.quit()
        except Exception as er:
            print(er)

            self.RES = 'error'
        else:
            self.RES = 'ok'
