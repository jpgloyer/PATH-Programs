import sys
import os
from PyQt5.QtWidgets import QApplication, QPushButton, QFileDialog, QInputDialog, QMessageBox, QListWidget, QListWidgetItem, QGridLayout, QWidget
from MasterDatabase import MasterDatabase
import pyperclip
from csv import reader
from collect_information import collect_information



"""SingleUser"""

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title='Password Manager'
        self.left=600
        self.top=400
        self.width=400
        self.height=400
        self.database_location = ''
        self.make_new_database = False

        self.login_screen()

        self.initUI()
    
    def login_screen(self):
        correct_credentials = False

        self.screen = collect_information(["*Master Password:"],['file','format'], "Password Manager")
        
        
        while not correct_credentials and self.screen.attempts_remaining > 0:
            
            self.screen.exec()

            if self.screen.result() == self.screen.Rejected:
                exit()

            if self.screen.new_database:
                self.make_new_database = True



            credentials = self.screen.return_values()
            m_pass = credentials[0]



            #First, check if user explicitly chose file location during login
            if self.screen.file_choice:
                self.database_location = self.screen.file_choice
                self.Database = MasterDatabase(self.database_location)
                
                
            else:
                #Second, try to open file recorded by local file DataBase_location.txt
                try:
                    with open("DataBase_location.txt") as File:
                        for line in File:
                            self.database_location = line
                    self.Database = MasterDatabase(self.database_location)
                #Lastly, create new database and database_location files locally
                except:
                    self.make_new_database = True

            if self.make_new_database:
                dialog = QFileDialog()
                dir_path = dialog.getExistingDirectory(self, 'Select directory to store your database:')
                
                with open("DataBase_location.txt",'w') as File:
                    File.write("New_Database.txt")
                    self.database_location = dir_path+"\\Database.txt"
                self.Database = MasterDatabase(self.database_location, ['Initialize'])
                message = QMessageBox()
                message.setText(f"New database created in {self.database_location}\n\n\nPassword: Password")
                message.exec()
                m_pass = 'Password'
                


            #Master Password Validation
            correct_master = False
            self.Database.input_master_password(m_pass)
            self.Database.decrypt('Master',self.Database.message_list_generator())
            if self.Database.decrypted_personal_message[0:28] == 'Website: Username: Password:':
                correct_master = True
            
            self.Database.make_personal_info_list()

            
            #Results
            if correct_master:# and valid_user and correct_personal:
                with open("DataBase_location.txt",'w') as File:
                    File.write(self.database_location)
                correct_credentials = True
            elif not correct_master and self.screen.attempts_remaining >= 0:
                self.screen.attempts_remaining -= 1
                message = QMessageBox()
                message.setText(f"INVALID MASTER PASSWORD\n{self.screen.attempts_remaining} attempts remaining")
                message.exec()

        
        if self.screen.attempts_remaining <= 0:
            exit()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left,self.top,self.width,self.height)
        layout = QGridLayout(self)

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


        #Import passwords
        self.import_passwords_button = QPushButton("Import Passwords",self)
        self.import_passwords_button.clicked.connect(self.import_passwords)

        #Credits button
        self.credits = QPushButton('Credits',self)
        self.credits.clicked.connect(self.credits_message)

        #Export button
        self.export = QPushButton('Export',self)
        self.export.clicked.connect(self.export_passwords)

        self.list_widget = QListWidget(self)
        self.list_widget.setGeometry(250,100,200,200)
        for i in self.Database.personal_info_list[1:]:
            self.list_widget.addItem(QListWidgetItem(f'{i[0]}'))
        


        self.change_master_pw_button = QPushButton("Change Master Password",self)
        self.change_master_pw_button.clicked.connect(self.change_master_pw)
        
        layout.addWidget(self.change_master_pw_button, 4, 0)

        layout.addWidget(self.reveal,0,0)
        layout.addWidget(self.add,1,0)
        layout.addWidget(self.change_entry_password,2,0)
        layout.addWidget(self.remove,3,0)

        layout.addWidget(self.list_widget,0,1,4,4)
        layout.addWidget(self.credits, 4,3)
        layout.addWidget(self.export, 4,2)
        layout.addWidget(self.import_passwords_button, 4,1)
        #---------------------------------------------------------------------------------------Add button to generate a temporary random password

        self.show()

    def export_passwords(self):
        confirmation, c_done = QInputDialog.getText(self,'CONFIRM',f'Typing "CONFIRM" will export an UNENCRYPTED list of passwords as "ExportedPasswords.txt." This text file can then be uploaded into a new database.')
        if confirmation:
            self.Database.export_passwords('ExportedPasswords.csv')


    def reveal_password(self):
        if self.list_widget.selectedItems():
            for i in self.Database.personal_info_list:
                if self.list_widget.selectedItems()[0].text() == i[0]:
                    copy_to_clipboard = QMessageBox.question(self,'Copy password to clipboard?', f"Website: {i[0]}\nUsername: {i[1]}\nPassword: {i[2]}\n\nCopy password to clipboard?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if copy_to_clipboard == QMessageBox.Yes:
                        pyperclip.copy(i[2])
        pass

    def add_entry(self, website: str = '', username: str = '', password: str = ''):
        is_duplicate = False
        if not (website and username and password):
            layout_list = ["Website: ","Username: ","Password: "]
            window = collect_information(layout_list)

            while not (window.data_entry[0].text() and window.data_entry[1].text() and window.data_entry[2].text()):
                is_duplicate = False
                window.exec()
                for i in self.Database.personal_info_list:
                    if i[0] == window.data_entry[0].text():
                        is_duplicate = True
                        
                if window.result() == window.Rejected:
                    break
                elif is_duplicate:
                    message = QMessageBox()
                    message.setText(f'Entry for {window.data_entry[0].text()} already present in personal database.\nUse "username@website" to store multiple accounts\' information.')
                    message.exec()
                
                elif not (window.data_entry[0].text() and window.data_entry[1].text() and window.data_entry[2].text()):
                    message = QMessageBox()
                    message.setText("Complete All Fields or Cancel to Continue")
                    message.exec()

            if window.result() == window.Accepted:
                website = window.data_entry[0].text()
                username = window.data_entry[1].text()
                password = window.data_entry[2].text()
                if password == 'random' or password == 'Random':
                    password = self.Database.randomize_password(QInputDialog.getInt(self,"Random Password Length:", "Random Password Length:", 10, 10, 30)[0])
                    new_password = QMessageBox()
                    new_password.setWindowTitle("New Password:")
                    new_password.setText(password)
                    new_password.exec()
                self.Database.personal_info_list.append([website,username,password])
                self.list_widget.addItem(QListWidgetItem(website))
        else:
            self.Database.personal_info_list.append([website,username,password])
            self.list_widget.addItem(QListWidgetItem(website))
            
        pass
        

    def change_entry(self):
        error: bool = False
        try:
            entry_to_change = self.list_widget.selectedItems()[0].text()
        except IndexError:
            message = QMessageBox()
            message.setText("Error: Please select an entry to remove:")
            message.exec()
            error = True

        if not error:
            for i in range(len(self.Database.personal_info_list)):
                if entry_to_change == self.Database.personal_info_list[i][0]:
                    new_password, np_done = QInputDialog.getText(self,'New Password',f'Enter {self.Database.personal_info_list[i][1]}\'s new password for {self.Database.personal_info_list[i][0]}:\nEnter "Random" to randomize password:')
                    if np_done and new_password:
                        if new_password.lower() != "random":
                            self.Database.personal_info_list[i][2] = new_password
                        else:
                            password_length = QInputDialog.getInt(self, "Password Length:", "Password Length:", 10, 10, 30)[0]
                            self.Database.personal_info_list[i][2] = self.Database.randomize_password(password_length)
                            new_password = QMessageBox()
                            new_password.setWindowTitle("New Password:")
                            new_password.setText(self.Database.personal_info_list[i][2])
                            new_password.exec()

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



    def import_passwords(self):
        File = QFileDialog()
        File.setFileMode(QFileDialog.ExistingFile)
        File.setNameFilter("*.csv")
        message = 'Entries for:\n\n'
        show_message = False
        redundant_entry = False
        
        if File.exec_():
            with open(File.selectedFiles()[0]) as NewPasswords:
                passwords = reader(NewPasswords)
                entries = []
                for row in passwords:
                    entries.append(row)
                del passwords
                for i in entries[1:]:
                    redundant_entry = False
                    for j in self.Database.personal_info_list:
                        if i[0] == j[0]:
                            redundant_entry = True
                            show_message = True
                    if not redundant_entry:
                        self.add_entry(i[0],i[1],i[2])
                    else:
                        message = message + f'{i[0]}\n'

        message = message + '\nalready present\t\t\t\t'
        if show_message == True:
            message_box = QMessageBox()
            message_box.setText(message)
            message_box.exec()
        


    def credits_message(self):
        message = QMessageBox()
        message.setWindowTitle("Credits")
        message.setText('Developed by Pierce Gloyer\njpgloyer@gmail.com')
        message.exec()
        pass

    def change_master_pw(self):
        new_pass = QInputDialog.getText(self,'New Master Password', 'Enter new master password: ')[0]
        self.Database.input_master_password(new_pass)

    
    def get_database(self):
        return self.Database
        

if __name__=='__main__':
    #Database = MasterDatabase('Database_location.txt')
    app=QApplication(sys.argv)    
    #ex=App(Database)
    ex = App()

    app.exec_()

    Database = ex.get_database()


    Database.save_changes()
        #Database.reencrypt()
