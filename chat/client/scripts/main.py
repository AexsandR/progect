from client import ENTER, REG
from CHAT import chat
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
app = QApplication(sys.argv)
enter = ENTER()
enter.show()
reg = REG()
reg.hide()
Chat = chat()
Chat.hide()
sys.exit(app.exec_())
