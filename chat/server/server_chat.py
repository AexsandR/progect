import socket
import threading


class Chat:
    def __init__(self, ip):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создаем сокет
        self.user = []
        self.sock.bind((ip, 5555))  # даем сокету ip и порт
        self.sock.listen()  # запускаем режим прослушивания

    """функция прослушки и отправки, но сначало посмотрите следущию функцию"""

    def Listen_and_otpravka(self):
        while True:
            disconent = [] # список отключившихся
            if len(self.user) != 0:
                for client in self.user: # пробегаем по списоку сокетов клиентоа
                    try:
                        res = client.recv(104857600) # если никто ничего не отпровляет то выдаст ошибку, но если
                        # кто то отправил то все будет норм
                    except socket.error:
                        pass
                    else:
                        """дальше записываем в сообщение в истории и отпрвка других сообщений"""
                        file1 = open('кэш.txt', mode='a')
                        res = res.decode('utf-8')
                        print(res)
                        try:
                            file1.write(res)
                        except Exception:
                            file1.close()
                        else:
                            file1.close()
                            for user in self.user:
                                if user != client:
                                    print('отправил')
                                    try:
                                        if res != '':
                                            user.send(res.encode('utf-8')) # если бпользователь отключился то выдаст ошибку
                                    except Exception:
                                        print('удален')
                                        disconent.append(user) # добовляем в список отключившихся
            for i in disconent:
                self.user.remove(i) # удаляем пользователь из списка

    def Connect(self):
        self.sock.setblocking(False) # ставим не блокирущий режим он нужен для того чтобы он не блокировался
        while True:
            try:
                client, addr = self.sock.accept() # ожидаем подключение но нам выдаст ошибку потому что у нас
                # неблокирущий сокет, но если кто то подключится то все будет норм
                """отправка истории"""
                file = open('кэш.txt', mode='r')
                f = file.readlines()
                stroka = ''
                print(client)
                for i in f:
                    stroka += i
                file.close()
                if len(stroka) != 0:
                    client.send(stroka.encode('utf-8'))
                    print('отправил')
            except socket.error:
                pass
            else:
                """добовляем сокет клиента в список"""
                self.user.append(client)

    def run(self): # запуск сервера
        print('online on')
        r1 = threading.Thread(target=self.Connect)
        r2 = threading.Thread(target=self.Listen_and_otpravka)
        r1.start()
        r2.start()
        r1.join()
        r2.join()
