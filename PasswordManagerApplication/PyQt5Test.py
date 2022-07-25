import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QPushButton, QFileDialog, QInputDialog, QMessageBox, QListWidget, QListWidgetItem
from MultiEncryptionOneClass import MasterDatabase
import pyperclip
from Login import Login
from admin import admin
from initialize_database_window import initialize_database_window
import csv



class App(QtWidgets.QWidget):
    def __init__(self,Database):
        super().__init__()
        self.title='Password Manager'
        self.left=600
        self.top=400
        self.width=400
        self.height=400
        self.Database = Database
        self.format = False
        

        self.login_screen()
        #Add specific inputs that will trigger database_initialization <-- maybe?

        self.Database.make_personal_info_list()
        self.Database.make_group_info_list()
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

#---------------------------------------------  Add system here to check for "Group Name: Individual" in preamble and automatically log in to the only user saved...
#---------------------------------------------  using the master password as the personal password

#---------------------------------------------  Add system to use User 1 as a group password storage, being encrypted with the master password
#---------------------------------------------  Move admin to User 2 slot and allow Admin sole control over altering group passwords


            #Username Validation
            valid_user = False
            if correct_master:
                self.Database.split_file_information()
                try:
                    self.Database.input_username(uname)
                    self.Database.users[self.Database.username]
                    valid_user = True
                except:
                    if uname == '':
                        valid_user = True
                        for username, value in self.Database.users.items():
                            if value == '1':
                                self.Database.input_username(username)
                                #print(username)
                    pass

            #User Password Validation
            correct_personal = False
            if valid_user:
                if ppass == '':
                    ppass = m_pass
                self.Database.input_personal_password(ppass)
                self.Database.decrypt('Personal',self.Database.file_sections[int(self.Database.users[self.Database.username])])
                #
                self.Database.decrypt('Group',self.Database.file_sections[1])
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
        layout = QtWidgets.QGridLayout(self)

        #Reveal button
        self.reveal=QPushButton('Reveal Password',self)
        self.reveal.clicked.connect(self.reveal_password)

        #Add entry button
        self.add=QPushButton('Add Entry',self)
        self.add.clicked.connect(self.add_entry)

        #Change Entry Password
        self.change_entry_password=QPushButton('Change Entry',self)
        self.change_entry_password.clicked.connect(self.change_entry)

        #Remove Entry
        self.remove=QPushButton('Remove Entry',self)
        self.remove.clicked.connect(self.remove_entry)

        #Change personal password
        self.change_personal_password_button=QPushButton('Change Personal Password',self)
        self.change_personal_password_button.clicked.connect(self.change_personal_password)

        #Import passwords
        self.import_passwords_button = QPushButton("Import Passwords",self)
        self.import_passwords_button.clicked.connect(self.import_passwords)

        #Credits button
        self.credits = QPushButton('Credits',self)
        self.credits.clicked.connect(self.credits_message)
        #self.credits.move(540,455)
        #self.credits.resize(100,25)

        self.list_widget = QListWidget(self)
        self.list_widget.setGeometry(250,100,200,200)
        for i in self.Database.personal_info_list[1:]:
            self.list_widget.addItem(QListWidgetItem(f'{i[0]}'))
        
        #print(self.Database.users)

        if self.Database.users[self.Database.username] == '2' or len(self.Database.users) == 1:
            self.admin_button = QPushButton('Admin options',self)
            self.admin_button.clicked.connect(self.admin_options)
            layout.addWidget(self.admin_button, 3, 2)

        layout.addWidget(self.reveal,0,0)
        layout.addWidget(self.add,1,0)
        layout.addWidget(self.change_entry_password,2,0)
        layout.addWidget(self.remove,3,0)
        layout.addWidget(self.change_personal_password_button,4,0)
        layout.addWidget(self.list_widget,0,1,4,1)
        layout.addWidget(self.credits, 4, 2)
        layout.addWidget(self.import_passwords_button, 5,0)
        #---------------------------------------------------------------------------------------Add button to generate a temporary random password

        self.show()

    def reveal_password(self):
        if self.list_widget.selectedItems():
            for i in self.Database.personal_info_list:
                if self.list_widget.selectedItems()[0].text() == i[0]:
                    copy_to_clipboard = QMessageBox.question(self,'Copy password to clipboard?', f"Website: {i[0]}\nUsername: {i[1]}\nPassword: {i[2]}\n\nCopy password to clipboard?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if copy_to_clipboard == QMessageBox.Yes:
                        pyperclip.copy(i[2])
        pass

    def add_entry(self, website: str = '', username: str = '', password: str = ''):
        #---------------------------------------------------------Add randomize password option
        
        if not (website and username and password):
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
        else:
            self.Database.personal_info_list.append([website,username,password])
            self.list_widget.addItem(QListWidgetItem(website))
        pass
        

    def change_entry(self):
        #---------------------------------------------------------Add randomize password option
        entry_to_change = self.list_widget.selectedItems()[0].text()
        for i in range(len(self.Database.personal_info_list)):
            if entry_to_change == self.Database.personal_info_list[i][0]:
                new_password, np_done = QInputDialog.getText(self,'New Password',f'Enter {self.Database.personal_info_list[i][1]}\'s new password for {self.Database.personal_info_list[i][0]}:')
                if np_done and new_password:
                    self.Database.personal_info_list[i][2] = new_password
        self

    def remove_entry(self):
        try:
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
        except IndexError:
            message = QMessageBox()
            message.setText("Error: Please select an entry to remove:")
            message.exec()
        pass

    def change_personal_password(self):
        personal_password, pp_done = QInputDialog.getText(self, 'Personal Password', 'Enter Personal Password:')
        self.Database.input_personal_password(personal_password)
        pass

    def import_passwords(self):
        File = QFileDialog()
        File.setFileMode(QFileDialog.ExistingFile)
        File.setNameFilter("*.csv")
        
        if File.exec_():
            with open(File.selectedFiles()[0]) as NewPasswords:
                passwords = csv.reader(NewPasswords)
                entries = []
                for row in passwords:
                    entries.append(row)
                del passwords
                for i in entries[1:]:
                    self.add_entry(i[0],i[1],i[2])
        


    def credits_message(self):
        message = QMessageBox()
        message.setText('Written by Pierce Gloyer')
        message.exec()
        pass


    def admin_options(self):
        admin_options = admin(self)
        admin_options.exec()
        if admin_options.new_pass:
            self.Database.master_password = admin_options.new_pass
        if admin_options.format == True:
            self.format = True
            self.close()
            pass
        pass

        

if __name__=='__main__':


    Database = MasterDatabase('Database_location.txt')
    #Database.initialize_database()
    app=QApplication(sys.argv)    
    ex=App(Database)

    app.exec_()


    if ex.format == True:
        initialize = initialize_database_window()
        initialize.exec()
        new_db_vals = initialize.return_values()
        Database.initialize_database(new_db_vals)
    else:
        Database.save_changes()
        Database.reencrypt()
