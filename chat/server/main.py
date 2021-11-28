from server_enter import Chat_Enter
from server_chat import Chat
import threading
import socket

name = socket.gethostname()
ip = socket.gethostbyname(name)  # получаем ip
print(name, ip)
"""передаем ip в классы"""
enter = Chat_Enter(ip)
online = Chat(ip)
"""дальше запуск"""
r2 = threading.Thread(target=enter.Start)
r1 = threading.Thread(target=online.run)
r1.start()
r2.start()
r1.join()
r2.join()
