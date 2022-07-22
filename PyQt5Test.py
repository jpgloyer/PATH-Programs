#Add system to save a local unencrypted text file containing the file location for the passwords document, allowing the user to import a network based file


#from email.charset import QP
#from pickle import TRUE
#from re import U
import sys
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QInputDialog, QMainWindow, QMessageBox, QListWidget, QListWidgetItem, QLabel, QLineEdit
from MultiEncryptionOneClass import MasterDatabase
import pyperclip
from Login import Login
from MultiEncryptionOneClass import MasterDatabase



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
        self.format = False
        
        self.login_screen()

        self.Database.make_personal_info_list()
        self.initUI()
    


    def login_screen(self):
        correct_credentials = False
        screen = Login()
        screen.attempts_remaining = 3
        
        while not correct_credentials and screen.attempts_remaining > 0:
            
            screen.exec()
            
            m_pass = screen.get_mpass()
            uname = screen.get_uname()
            ppass = screen.get_ppass()

            #Master Password Validation
            correct_master = False
            self.Database.input_master_password(m_pass)
            self.Database.decrypt('Master',self.Database.message_list_generator())
            if self.Database.decrypted_master_message.find('Preamble:') != -1:
                correct_master = True

            #Username Validation
            valid_user = False
            if correct_master:
                self.Database.split_file_information()
                try:
                    self.Database.input_username(uname)
                    self.Database.users[self.Database.username]
                    valid_user = True
                except:
                    pass

            #User Password Validation
            correct_personal = False
            if valid_user:
                self.Database.input_personal_password(ppass)
                self.Database.decrypt('Personal',self.Database.file_sections[int(self.Database.users[self.Database.username])])
                if self.Database.decrypted_personal_message.find('Website: Username: Password:') != -1:
                    correct_personal = True
            

            #Results
            if correct_master and valid_user and correct_personal:
                correct_credentials = True
                screen.accept()
            elif not correct_master and screen.attempts_remaining >= 0:
                screen.attempts_remaining -= 1
                message = QMessageBox()
                message.setText(f"INVALID MASTER PASSWORD\n{screen.attempts_remaining} attempts remaining")
                message.exec()
            elif not valid_user and screen.attempts_remaining >= 0:
                screen.attempts_remaining -= 1
                message = QMessageBox()
                message.setText(f"INVALID USERNAME\n{screen.attempts_remaining} attempts remaining")
                message.exec()
            elif not correct_personal and screen.attempts_remaining >= 0:
                screen.attempts_remaining -= 1
                message = QMessageBox()
                message.setText(f"INVALID PERSONAL PASSWORD\n{screen.attempts_remaining} attempts remaining")
                message.exec()

        
        if screen.attempts_remaining <= 0:
            exit()


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
                new_password, np_done = QInputDialog.getText(self,'New Password',f'Enter {self.Database.personal_info_list[i][1]}\'s new password for {self.Database.personal_info_list[i][0]}:')
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


    def admin_options(self):
        admin_options = admin(self)
        admin_options.exec()
        if admin_options.new_pass:
            self.Database.master_password = admin_options.new_pass
        if admin_options.format == True:
            self.format = True
            self.close()
            pass
            #self.Database.initialize_database()
        pass



class admin(QtWidgets.QDialog):
    #Add option to remove user
    def __init__(self, parent: None):
        super(admin,self).__init__(parent)
        self.layout = QtWidgets.QVBoxLayout(self)

        self.change_master_password_button = QtWidgets.QPushButton('Change Master Password',self)
        self.change_master_password_button.clicked.connect(self.change_master_password)
        self.layout.addWidget(self.change_master_password_button)

        self.format_database_button = QtWidgets.QPushButton('Format Database',self)
        self.format_database_button.clicked.connect(self.format_database)
        self.layout.addWidget(self.format_database_button)

        self.new_pass = ''
        self.format = False

    def change_master_password(self):
        self.new_pass = QInputDialog.getText(self,'New Master Password', 'Enter new organization master password: ')[0]


    def format_database(self):
        confirmation, c_done = QInputDialog.getText(self,'CONFIRM',f'Type "CONFIRM" to erase your organizations password database and create a new one:')
        if confirmation == 'CONFIRM' and c_done:
            self.format = True
            self.close()

class initialize_database_window(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(initialize_database_window, self).__init__(parent)
        self.labels = []
        self.data_entry = []
        self.enter_button = QPushButton("Enter",self)
        self.enter_button.clicked.connect(self.enter)
        self.cancel_button = QPushButton("Cancel",self)
        self.cancel_button.clicked.connect(self.cancel)
        self.number_of_users = (0,0)
        
        while self.number_of_users[0] == 0:
            self.number_of_users = QInputDialog.getInt(self, "How Many Users?", "How Many Users?", 0, 0, 30)

        for i in range(self.number_of_users[0]):
            self.labels.append(QLabel(f"User{i+1}'s name:"))
            self.data_entry.append(QLineEdit(self))        

        layout = QtWidgets.QGridLayout(self)

        self.group_name = QLineEdit(self)
        layout.addWidget(QLabel("Group name: "),0,0)
        layout.addWidget(self.group_name,0,1)

        for i in range(len(self.labels)):
            layout.addWidget(self.labels[i],i+1,0)
            layout.addWidget(self.data_entry[i],i+1,1)
            if self.labels[i] == self.labels[-1]:
                layout.addWidget(self.enter_button,100,1)
                layout.addWidget(self.cancel_button,100,0)
        

    def enter(self):
        self.accept()

    def cancel(self):
        self.labels = []
        self.data_entry = []
        self.reject()

    def return_values(self):
        users = []
        for i in self.data_entry:
            users.append(i.text())
        return users, self.group_name.text()
        

if __name__=='__main__':
    Database = MasterDatabase('Database_location.txt')
    app=QApplication(sys.argv)    
    ex=App(Database)
    #sys.exit(app.exec_())
    app.exec_()

    Database.save_changes()
    Database.reencrypt()


    if ex.format == True:
        initialize = initialize_database_window()
        initialize.exec()
        new_db_vals = initialize.return_values()
        Database.initialize_database(new_db_vals[0],new_db_vals[1])
