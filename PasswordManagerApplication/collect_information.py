from PyQt5 import QtWidgets
import sys


# Combine initialize_database_window.py with this class
# Potentially Login.py as well

class collect_information(QtWidgets.QDialog):

    '''
    Pass a list of arguments you would like to collect information for
    ex. collect_information(["Username:","Password:"]) -> .return_values() will return user inputs for a username and password after a window is displayed and completed
    Passing an argument in the input list that starts with '*' (ex "*Password:") will cause user input to be hidden as they type it
    '''



    def __init__(self, layout_terms: list = [], flags: list = [], parent=None):


        #------------------If "file_select" flag is present, add button that opens a QFileDialog window and assigns the selection to self.new_file_location


        super(collect_information, self).__init__(parent)
        layout = QtWidgets.QGridLayout(self)
        self.data_entry = [QtWidgets.QLineEdit(self) for i in layout_terms]
        self.buttons = [QtWidgets.QPushButton("Cancel", self), QtWidgets.QPushButton("Enter", self)]
        self.buttons[0].clicked.connect(self.cancel)
        self.buttons[1].clicked.connect(self.enter)
        self.buttons[0].setAutoDefault(False)
        self.buttons[1].setAutoDefault(True)
        self.use_this_data = False
        self.attempts_remaining = 3
        for i in range(len(layout_terms)):
            if layout_terms[i][0] == '*':
                self.data_entry[i].setEchoMode(QtWidgets.QLineEdit.Password)

        for i in range(len(layout_terms)):
            layout.addWidget(QtWidgets.QLabel(layout_terms[i].strip("*")),i,0)
            layout.addWidget(self.data_entry[i],i,1)
        for i in self.buttons:
            layout.addWidget(i)

    def enter(self):
        self.use_this_data = True
        self.accept()

    def cancel(self):
        self.reject()
        #self.close()

    def return_values(self):
        return [i.text() for i in self.data_entry]
        

if __name__=='__main__':
    Application = QtWidgets.QApplication(sys.argv)
    App = QtWidgets.QWidget()
    Collect = collect_information(["Test1", "Test2"])
    Collect.exec()
    print(Collect.return_values())