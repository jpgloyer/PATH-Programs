



#---------------------------OUTDATED AND UNUSED-------------------------------







from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QLabel
import sys



# from mainwindow import Ui_MainWindow

class Login(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        #self.setWindowFlag(QtCore.FramelessWindowHint)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setWindowTitle("Login:")
        self.MPWLabel = QLabel("Master Password:")
        self.UNLabel = QLabel("Username:")
        self.PPWLabel = QLabel("Personal Password:")
        self.textMasterPass = QtWidgets.QLineEdit(self)
        self.textName = QtWidgets.QLineEdit(self)
        self.textPass = QtWidgets.QLineEdit(self)
        self.textPass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.textMasterPass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.buttonLogin = QtWidgets.QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        self.close_button = QtWidgets.QPushButton('Cancel',self)
        self.close_button.clicked.connect(self.close_custom)
        layout = QtWidgets.QVBoxLayout(self)
        self.attempts_remaining = 0

        layout.addWidget(self.MPWLabel)
        layout.addWidget(self.textMasterPass)
        layout.addWidget(self.UNLabel)
        layout.addWidget(self.textName)
        layout.addWidget(self.PPWLabel)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)
        layout.addWidget(self.close_button)


    def handleLogin(self):
        self.accept()
        pass
        
    def close_custom(self):
        #Super jank coding, sorry whoever is reading this. Couldn't figure out how to send signals/do subclassing right
        self.attempts_remaining = -1
        self.close()



    def get_mpass(self):
        return self.textMasterPass.text()

    def get_uname(self):
        return self.textName.text()

    def get_ppass(self):
        return self.textPass.text()


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    login = Login()
    temp = login.exec()
    print(temp)

