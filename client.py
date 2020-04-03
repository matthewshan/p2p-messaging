import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QMainWindow, QVBoxLayout, QTextEdit, QLineEdit 
from PyQt5.QtCore import Qt
class Application():
    def __init__(self):
        app = QApplication([])


        #Text Area
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.insertHtml("<b>Welcome to P2P Chat<b/>")
        self.text_area.insertPlainText("\n")

        #Message Area
        self.mes_area = QLineEdit()

        #Message Button
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.on_submit)

        #Layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text_area)
        self.layout.addWidget(self.mes_area)
        self.layout.addWidget(self.submit_button)

        #Window
        self.window = QWidget()
        self.window.setLayout(self.layout)
        self.window.setWindowTitle("P2P Chat")
        self.window.show()

        app.exec_()

    def on_submit(self):
        mes = self.mes_area.text()
        self.text_area.insertHtml("<b> You: </b>" + mes)
        self.text_area.insertPlainText("\n")


# window = MainWindow()
# window.show()

Application()