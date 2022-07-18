from email.charset import QP
from pickle import TRUE
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QInputDialog, QMainWindow, QMessageBox, QListWidget, QListWidgetItem
from MultiEncryptionOneClass import MasterDatabase
import pyperclip


class App(QtWidgets.QWidget):
    def __init__(self,Database):
        super().__init__()
        self.title='Hello, world!'
        self.left=600
        self.top=400
        self.width=640
        self.height=480
        self.Database = Database
        m_pw_done = False
        un_done = False
        p_pw_done = False

        #Validate Master Password
        while not m_pw_done:
            master_password, m_pw_done = QInputDialog.getText(self, 'Master Password', 'Enter Master Password:')
            self.Database.input_master_password(master_password)
            self.Database.decrypt('Master',self.Database.message_list_generator())
            if self.Database.decrypted_master_message.find('Preamble:') == -1:
                m_pw_done = False

        self.Database.split_file_information()

        #Validate Username
        while not un_done:
            try:
                username, un_done = QInputDialog.getText(self,'Username', 'Enter Username:')
                self.Database.input_username(username)
                self.Database.users[self.Database.username]
            except:
                un_done = False
        
        #Validate Personal Password
        while not p_pw_done:
            personal_password, p_pw_done = QInputDialog.getText(self, 'Personal Password', 'Enter Personal Password:')
            self.Database.input_personal_password(personal_password)
            self.Database.decrypt('Personal',self.Database.file_sections[int(self.Database.users[self.Database.username])])
            if self.Database.decrypted_personal_message.find('Website: Username: Password:') == -1:
                p_pw_done = False

        self.Database.make_personal_info_list()
    
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left,self.top,self.width,self.height)
        
        #Reveal button
        self.reveal=QPushButton('Reveal Password',self)
        self.reveal.clicked.connect(self.reveal_password)
        self.reveal.move(0,100)
        self.reveal.resize(200,25)

        #Add entry button
        self.add=QPushButton('Add Entry',self)
        self.add.clicked.connect(self.add_entry)
        self.add.move(0,150)
        self.add.resize(200,25)

        #Change Entry Password
        self.change_entry_password=QPushButton('Change Entry',self)
        self.change_entry_password.clicked.connect(self.change_entry)
        self.change_entry_password.move(0,200)
        self.change_entry_password.resize(200,25)

        #Remove Entry
        self.remove=QPushButton('Remove Entry',self)
        self.remove.clicked.connect(self.remove_entry)
        self.remove.move(0,250)
        self.remove.resize(200,25)

        #Change personal password
        self.change_personal_password_button=QPushButton('Change Personal Password',self)
        self.change_personal_password_button.clicked.connect(self.change_personal_password)
        self.change_personal_password_button.move(0,300)
        self.change_personal_password_button.resize(200,25)

        self.list_widget = QListWidget(self)
        self.list_widget.setGeometry(250,100,200,200)
        for i in self.Database.personal_info_list[1:]:
            self.list_widget.addItem(QListWidgetItem(f'{i[0]}'))

        self.show()

    def take_input(self):
        user_input, done = QInputDialog.getText(self,'Test','Enter test info:')
        if done:
            return user_input
        else:
            return 'Canceled'

    def reveal_password(self):
        message = QMessageBox()
        for i in self.Database.personal_info_list:
            #print(i)
            if self.list_widget.selectedItems()[0].text() == i[0]:
                message.setText(f"Website: {i[0]}\nUsername: {i[1]}\nPassword: {i[2]}")
        message.exec()
        pyperclip.copy(i[2])
        pass

    def add_entry(self):
        #ADD INPUT VALIDATION
        website_used = True
        while website_used == True:
            website, w_done = QInputDialog.getText(self,'Website:','Which Website is this Entry For?')
            website_in_list = False
            for i in self.Database.personal_info_list:
                if i[0] == website:
                    website_in_list = True
                    alert = QMessageBox()
                    alert.setText(f'Entry for {website} already present in personal database.\nUse "username@website" to store multiple accounts\' information.')
                    alert.exec()
            if website_in_list == False:
                website_used = False
        username, u_done = QInputDialog.getText(self,'Username:',f'Enter your Username for {website}:')
        password, p_done = QInputDialog.getText(self, 'Password:',f'Enter Password for {website}:')
        self.Database.personal_info_list.append([website,username,password])
        self.list_widget.addItem(QListWidgetItem(website))
        pass
        

    def change_entry(self):
        entry_to_change = self.list_widget.selectedItems()[0].text()
        for i in range(len(self.Database.personal_info_list)):
            if entry_to_change == self.Database.personal_info_list[i][0]:
                new_password, np_done = QInputDialog.getText(self,'New Password',f'Enter {self.Database.personal_info_list[i][1]}\' new password for {self.Database.personal_info_list[i][0]}:')
                if np_done and new_password:
                    self.Database.personal_info_list[i][2] = new_password
        self

    def remove_entry(self):
        entry_to_remove = self.list_widget.selectedItems()[0].text()
        for i in self.Database.personal_info_list:
            if entry_to_remove == i[0]:
                confirmation, c_done = QInputDialog.getText(self,'CONFIRM',f'Type "CONFIRM" to delete {i[1]}\'s {i[0]} password entry:')
                if confirmation == 'CONFIRM':
                    personal_info_list = []
                    for j in self.Database.personal_info_list:
                        if j != i:
                            personal_info_list.append(j)
                    self.Database.personal_info_list = personal_info_list
                    self.list_widget.takeItem(self.list_widget.row(self.list_widget.selectedItems()[0]))
                    #self.list_widget.item(self.list_widget.row(self.list_widget.selectedItems()[0])).setSelected(False)
        pass

    def change_personal_password(self):
        personal_password, pp_done = QInputDialog.getText(self, 'Personal Password', 'Enter Personal Password:')
        self.Database.input_personal_password(personal_password)
        pass




if __name__=='__main__':
    Database = MasterDatabase('OurPasswords.txt')
    app=QApplication(sys.argv)    
    ex=App(Database)
    #sys.exit(app.exec_())
    app.exec_()
    Database.save_changes()
    Database.reencrypt()
