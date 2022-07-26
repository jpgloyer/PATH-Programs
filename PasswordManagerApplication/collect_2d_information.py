from PyQt5 import QtWidgets

# Combine initialize_database_window.py with this class
# Potentially Login.py as well

class collect_2d_information(QtWidgets.QDialog):
    def __init__(self, layout_terms: list = [], parent=None):
        super(collect_2d_information, self).__init__(parent)
        layout = QtWidgets.QGridLayout(self)
        self.data_entry = [QtWidgets.QLineEdit(self) for i in layout_terms]
        self.buttons = [QtWidgets.QPushButton("Cancel", self), QtWidgets.QPushButton("Enter", self)]
        self.buttons[0].clicked.connect(self.cancel)
        self.buttons[1].clicked.connect(self.enter)

        for i in range(len(layout_terms)):
            layout.addWidget(QtWidgets.QLabel(layout_terms[i]),i,0)
            layout.addWidget(self.data_entry[i],i,1)
        for i in self.buttons:
            layout.addWidget(i)

    def enter(self):
        self.accept()

    def cancel(self):
        self.data_entry = []
        self.reject()

    def return_values(self):
        return [i.text() for i in self.data_entry]
        
        
