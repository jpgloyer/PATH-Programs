from PyQt5.QtWidgets import QFileDialog, QGridLayout, QLineEdit, QDialog, QPushButton, QLabel


# Combine initialize_database_window.py with this class
# Potentially Login.py as well

class collect_information(QDialog):

    '''
    Pass a list of arguments you would like to collect information for
    ex. collect_information(["Username:","Password:"]) -> .return_values() will return user inputs for a username and password after a window is displayed and completed
    Passing an argument in the input list that starts with '*' (ex "*Password:") will cause user input to be hidden as they type it
    '''


    def __init__(self, layout_terms: list = [], flags: list = [], parent=None):


        #------------------If "file_select" flag is present, add button that opens a QFileDialog window and assigns the selection to self.new_file_location


        super(collect_information, self).__init__(parent)
        self.win_layout = QGridLayout(self)
        self.data_entry = [QLineEdit(self) for i in layout_terms]
        self.file_choice = ''
        self.file_label = ''


        #Buttons
        self.buttons = [QPushButton("Cancel", self), QPushButton("Enter", self)]
        self.buttons[0].clicked.connect(self.cancel)
        self.buttons[1].clicked.connect(self.enter)
        self.buttons[0].setAutoDefault(False)
        self.buttons[1].setAutoDefault(True)
        
        for i in flags:
            if i == 'file':
                self.buttons.append(QPushButton("Choose Database:", self))
                self.buttons[-1].clicked.connect(self.choose_database)
                self.buttons[-1].setAutoDefault(False)
        
        
        self.use_this_data = False
        self.attempts_remaining = 3


        for i in range(len(layout_terms)):
            if layout_terms[i][0] == '*':
                self.data_entry[i].setEchoMode(QLineEdit.Password)

        for i in range(len(layout_terms)):
            self.win_layout.addWidget(QLabel(layout_terms[i].strip("*")),i,0)
            self.win_layout.addWidget(self.data_entry[i],i,1)
        row_counter = len(layout_terms)
        
        for i in self.buttons[2:]:
            self.win_layout.addWidget(i, row_counter,0)
            row_counter += 1
        


        self.win_layout.addWidget(self.buttons[0],100, 0)
        self.win_layout.addWidget(self.buttons[1],100, 1)

    def enter(self):
        self.use_this_data = True
        self.accept()

    def cancel(self):
        self.reject()
        #self.close()

    def choose_database(self):
        file_select = QFileDialog()
        file_select.setFileMode(QFileDialog.ExistingFile)
        file_select.setNameFilter("*.txt")
        

        if self.file_label:
            self.file_label.deleteLater()

        if file_select.exec():
            self.file_choice = file_select.selectedFiles()[0]
            self.file_label = QLabel(file_select.selectedFiles()[0])
        
        self.win_layout.addWidget(self.file_label,3,1)
        


    def return_values(self):
        return [i.text() for i in self.data_entry]
        

# if __name__=='__main__':
#     Application = QtWidgets.QApplication(sys.argv)
#     App = QtWidgets.QWidget()
#     Collect = collect_information(["Test1", "Test2"])
#     Collect.exec()
#     print(Collect.return_values())