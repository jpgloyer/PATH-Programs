from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QInputDialog, QFileDialog


class admin(QtWidgets.QDialog):
    #Add option to remove user
    #Add option to modify file location
    #Add option to transfer or add admin rights (admins have negative user ID #'s?)
        #^^^Maybe encrypt local DataBase_Location.txt file?
    def __init__(self, parent: None):
        super(admin,self).__init__(parent)
        self.layout = QtWidgets.QVBoxLayout(self)

        self.change_master_password_button = QtWidgets.QPushButton('Change Master Password',self)
        self.change_master_password_button.clicked.connect(self.change_master_password)
        self.layout.addWidget(self.change_master_password_button)

        # self.format_database_button = QtWidgets.QPushButton('Format Database',self)
        # self.format_database_button.clicked.connect(self.format_database)
        # self.layout.addWidget(self.format_database_button)

        # self.change_database_location_button = QtWidgets.QPushButton('Change Database Location',self)
        # self.change_database_location_button.clicked.connect(self.change_database_location)
        # self.layout.addWidget(self.change_database_location_button)

        self.new_pass = ''
        self.format = False

    def change_master_password(self):
        '''Takes input to to self.new_pass. self.new_pass can be accessed after self.exec() to set a new password.'''


        #-------------------------------------------Modify to add secondary confirm password line and QLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)


        self.new_pass = QInputDialog.getText(self,'New Master Password', 'Enter new organization master password: ')[0]


    # def format_database(self):
    #     '''Confirms user's choice to format the database, then sets self.format to True.
    #     self.format can be accessed after self.exec() to trigger database_initialization'''
    #     confirmation, c_done = QInputDialog.getText(self,'CONFIRM',f'Please ensure every member has exported their password database. \n\n***CONTINUING WITH THIS ACTION WILL ERASE THE ENTIRE DATABASE*** \n\nType "CONFIRM" to procede:')
    #     self.how_many_users = QInputDialog.getInt(self, "How Many Users?", "How Many Users?", 1, 1, 30)[0]
    #     #print(self.how_many_users)
    #     if confirmation == 'CONFIRM' and c_done:
    #         self.format = True
    #         self.close()


    # def change_database_location(self):
    #     File = QFileDialog()
    #     File.setFileMode(QFileDialog.ExistingFile)
    #     File.setNameFilter("*.txt")
    #     if File.exec():
    #         with open("DataBase_location.txt",'w') as Location:
    #             Location.write(File.selectedFiles()[0])