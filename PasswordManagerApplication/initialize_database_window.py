from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton, QInputDialog, QLabel, QLineEdit


class initialize_database_window(QtWidgets.QDialog):
    def __init__(self, parent=None):
        #-----------------------------------------------------------------------------------------------------------------------------
        #Add system to validate usernames and check for duplicates
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

        if self.number_of_users[0] > 1:
            for i in range(self.number_of_users[0]+1):
                if i == 0:
                    self.labels.append(QLabel(f"Group/User 1's name:"))
                    self.data_entry.append(QLineEdit(self))
                else:
                    self.labels.append(QLabel(f"User{i+1}'s name:"))
                    self.data_entry.append(QLineEdit(self))        
        else:
            self.labels.append(QLabel("User's Name:"))
            self.data_entry.append(QLineEdit(self))

        layout = QtWidgets.QGridLayout(self)
        for i in range(len(self.labels)):
            layout.addWidget(self.labels[i],i,0)
            layout.addWidget(self.data_entry[i],i,1)
        layout.addWidget(self.enter_button,100,1)
        layout.addWidget(self.cancel_button,100,0)


    def enter(self):
        self.accept()

    def cancel(self):
        self.labels = []
        self.data_entry = []
        self.reject()

    def return_values(self):
        users = [i.text() for i in self.data_entry]
        
        return users