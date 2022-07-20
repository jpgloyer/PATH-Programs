#Add system to save a local unencrypted text file containing the file location for the passwords document, allowing the user to import a network based file


#from email.charset import QP
#from pickle import TRUE
#from re import U
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QInputDialog, QMainWindow, QMessageBox, QListWidget, QListWidgetItem
from MultiEncryptionOneClass import MasterDatabase
import pyperclip



class App(QtWidgets.QWidget):
    def __init__(self,Database):
        super().__init__()
        self.title='Password Manager'
        self.left=600
        self.top=400
        self.width=640
        self.height=480
        self.Database = Database
        m_pw_done = False
        un_done = False
        p_pw_done = False
        

        # self.ps = QtWidgets.QLineEdit(self)
        # self.ps.setWindowTitle("Enter Password")
        # self.ps.setEchoMode(QtWidgets.QLineEdit.Password)
        # self.ps.resize(200,200)
        # self.ps.show()
        # print(self.ps.text())



        #Validate Master Password
        attempts_remaining = 3
        while not m_pw_done:
            master_password, m_pw_done = QInputDialog.getText(self, 'Master Password', 'Enter Master Password:')
            if not m_pw_done:
                exit()
            self.Database.input_master_password(master_password)
            self.Database.decrypt('Master',self.Database.message_list_generator())
            if self.Database.decrypted_master_message.find('Preamble:') == -1:
                message = QMessageBox()
                attempts_remaining -= 1
                message.setText(f"INCORRECT PASSWORD\n{attempts_remaining} attempts remaining")
                message.exec()
                if attempts_remaining == 0:
                    exit()
                m_pw_done = False

        self.Database.split_file_information()

        
        #Validate Username
        attempts_remaining = 3
        while not un_done:
            username, un_done = QInputDialog.getText(self,'Username', 'Enter Username:')
            if not un_done:
                exit()
            try:
                self.Database.input_username(username)
                self.Database.users[self.Database.username]
            except:
                message = QMessageBox()
                attempts_remaining -= 1
                message.setText(f"INVALID USERNAME\n{attempts_remaining} attempts remaining")
                message.exec()
                if attempts_remaining == 0:
                    exit()
                un_done = False
        

        #Validate Personal Password
        attempts_remaining = 3
        while not p_pw_done:
            personal_password, p_pw_done = QInputDialog.getText(self, 'Personal Password', 'Enter Personal Password:')
            if not p_pw_done:
                exit()
            self.Database.input_personal_password(personal_password)
            self.Database.decrypt('Personal',self.Database.file_sections[int(self.Database.users[self.Database.username])])
            if self.Database.decrypted_personal_message.find('Website: Username: Password:') == -1:
                message = QMessageBox()
                attempts_remaining -= 1
                message.setText(f'INCORRECT PASSWORD\n{attempts_remaining} attempts remaining')
                message.exec()
                if attempts_remaining == 0:
                    exit()
                p_pw_done = False

        self.Database.make_personal_info_list()

        self.title = f"{self.Database.users['Preamble']} Password Manager"
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

        #Credits button
        self.credits = QPushButton('Credits',self)
        self.credits.clicked.connect(self.credits_message)
        self.credits.move(540,455)
        self.credits.resize(100,25)

        self.list_widget = QListWidget(self)
        self.list_widget.setGeometry(250,100,200,200)
        for i in self.Database.personal_info_list[1:]:
            self.list_widget.addItem(QListWidgetItem(f'{i[0]}'))

        if self.Database.users[self.Database.username] == '1':
            self.admin_button = QPushButton('Admin options',self)
            self.admin_button.clicked.connect(self.admin_options)
            self.admin_button.move(540,430)
            self.admin_button.resize(100,25)

        self.show()

    def reveal_password(self):
        if self.list_widget.selectedItems():
            for i in self.Database.personal_info_list:
                #print(i)
                if self.list_widget.selectedItems()[0].text() == i[0]:
                    copy_to_clipboard = QMessageBox.question(self,'Copy password to clipboard?', f"Website: {i[0]}\nUsername: {i[1]}\nPassword: {i[2]}\n\nCopy password to clipboard?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if copy_to_clipboard == QMessageBox.Yes:
                        pyperclip.copy(i[2])
        pass

    def add_entry(self):
        website_used = True
        w_done = True
        u_done = True
        p_done = True
        website = ''
        username = ''
        password = ''
        while website_used == True:
            while website == '' and w_done:
                website, w_done = QInputDialog.getText(self,'Website:','Which Website is this Entry For?')
                website_in_list = False
                for i in self.Database.personal_info_list:
                    if i[0] == website:
                        website_in_list = True
                        alert = QMessageBox()
                        alert.setText(f'Entry for {website} already present in personal database.\nUse "username@website" to store multiple accounts\' information.')
                        alert.exec()
                        website = ''
                if website_in_list == False:
                    website_used = False
        if w_done:
            while username == '' and u_done:
                username, u_done = QInputDialog.getText(self,'Username:',f'Enter your Username for {website}:')
            if u_done:
                while password == '' and p_done:
                    password, p_done = QInputDialog.getText(self, 'Password:',f'Enter Password for {website}:')
                if p_done:
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

    def credits_message(self):
        message = QMessageBox()
        message.setText('Written by Pierce Gloyer')
        message.exec()
        self.Database.test_master_decryption('Passwor')

    def admin_options(self):
        pass




if __name__=='__main__':
    Database = MasterDatabase('OurPasswords.txt')
    app=QApplication(sys.argv)    
    ex=App(Database)
    #sys.exit(app.exec_())
    app.exec_()
    Database.save_changes()
    Database.reencrypt()

