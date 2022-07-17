from email.charset import QP
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QInputDialog, QMainWindow, QMessageBox
from MultiEncryptionOneClass import MasterDatabase


class App(QtWidgets.QWidget):
    def __init__(self,Database):
        super().__init__()
        self.title='Hello, world!'
        self.left=600
        self.top=400
        self.width=640
        self.height=480
        self.Database = Database
        self.initUI()

    
    def initUI(self):
        #Button dimensions: (x=90,y=25)
        self.setWindowTitle(self.title)
        self.setGeometry(self.left,self.top,self.width,self.height)
        
        
        master_password, m_pw_done = QInputDialog.getText(self, 'Master Password', 'Enter Master Password:')
        self.Database.input_master_password(master_password)
        username, un_done = QInputDialog.getText(self,'Username', 'Enter Username:')
        self.Database.input_username(username)
        personal_password, pp_done = QInputDialog.getText(self, 'Personal Password', 'Enter Personal Password:')
        self.Database.input_personal_password(personal_password)
        self.Database.decrypt('Master',Database.message_list_generator())
        self.Database.split_file_information()
        self.Database.decrypt('Personal',self.Database.file_sections[int(Database.users[Database.username])])
        self.Database.make_personal_info_list()

        #Everything I need for one button
        self.button=QPushButton('Test',self)
        self.button.clicked.connect(self.take_input)
        self.button.move(0,0)

        #Reveal button
        self.reveal=QPushButton('Reveal Password',self)
        self.reveal.clicked.connect(self.reveal_password)
        self.reveal.move(0,100)

        #Add entry button
        self.reveal=QPushButton('Add Entry',self)
        self.reveal.clicked.connect(self.add_entry)
        self.reveal.move(0,150)

        #Change Entry Password
        self.reveal=QPushButton('Change Entry',self)
        self.reveal.clicked.connect(self.change_entry)
        self.reveal.move(0,200)

        #Remove Entry
        self.reveal=QPushButton('Remove Entry',self)
        self.reveal.clicked.connect(self.remove_entry)
        self.reveal.move(0,250)

        #Change personal password
        self.reveal=QPushButton('Change Personal Password',self)
        self.reveal.clicked.connect(self.change_personal_password)
        self.reveal.move(0,300)



        self.show()

    def take_input(self):
        user_input, done = QInputDialog.getText(self,'Test','Enter test info:')
        if done:
            return user_input
        else:
            return 'Canceled'

    def reveal_password(self):
        message_text = ''
        for i in range(len(self.Database.personal_info_list)):
            message_text = message_text + f'{i}: '
            message_text = message_text + self.Database.personal_info_list[i][0]

            message_text = message_text + '\n'
        password_selection, reveal_done = QInputDialog.getText(self, 'Reveal Password:',message_text)
        message = QMessageBox()
        message.setWindowTitle('Password')
        message.setText(('\t\n').join(self.Database.personal_info_list[int(password_selection)]))
        message.exec()

    def add_entry(self):
        website, w_done = QInputDialog.getText(self,'Website:','Which Website is this Entry For?')
        username, u_done = QInputDialog.getText(self,'Username:',f'Enter your Username for {website}:')
        password, p_done = QInputDialog.getText(self, 'Password:',f'Enter Password for {website}:')
        self.Database.personal_info_list.append([website,username,password])
        self

    def change_entry(self):
        self

    def remove_entry(self):
        self

    def change_personal_password(self):
        self




if __name__=='__main__':
    Database = MasterDatabase('OurPasswords.txt')
    app=QApplication(sys.argv)    
    ex=App(Database)
    sys.exit(app.exec_())
