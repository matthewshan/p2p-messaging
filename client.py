import sys
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QSplitter, QPushButton, QLabel, QMainWindow, QVBoxLayout, QTextEdit, QLineEdit 
from PyQt5.QtCore import Qt

class LineText(QLineEdit):
    def __init__(self, callback):
        self.enter_callback = callback
        super().__init__()

    def keyPressEvent(self, event):
        key = event.key()
        if key == 16777220:
            self.enter_callback()
        else:
            super().keyPressEvent(event)
    
class Application():
    def __init__(self):
        # Non-GUI Members
        self.connected = False;

        app = QApplication([])
        """Connection Area"""

        def toggleConn():
            print(self)
            self.connected = not self.connected
            self.toggle_buttons()
        
        
        #Host Button
        self.host_button = QPushButton("Host")
        self.host_button.clicked.connect(toggleConn)

        #Connect Button
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(toggleConn)

        #Connect Button
        self.end_button = QPushButton("End Connection")
        self.end_button.clicked.connect(toggleConn)

        #Layout
        connection_layout = QHBoxLayout()
        connection_layout.addWidget(self.host_button)
        connection_layout.addWidget(self.connect_button)
        connection_layout.addWidget(self.end_button)

        split = QSplitter(Qt.Vertical)

        """Message Layout"""
        #Text Area
        self.incoming_text = QTextEdit()
        self.incoming_text.setReadOnly(True)
        self.incoming_text.insertHtml("<b>Welcome to P2P Chat<b/>")
        self.incoming_text.insertPlainText("\n")

        #Message Area
        self.mes_text = LineText(self.on_submit)

        #Message Button
        self.mes_button = QPushButton("Submit")
        self.mes_button.clicked.connect(self.on_submit)

        # Message area Layout
        mes_layout = QHBoxLayout()
        mes_layout.addWidget(self.mes_text)
        mes_layout.addWidget(self.mes_button)
        
        """Main Layout"""
        main_layout = QVBoxLayout()
        main_layout.addLayout(connection_layout)
        main_layout.addWidget(split)
        main_layout.addWidget(self.incoming_text)
        main_layout.addLayout(mes_layout)


        self.toggle_buttons()

        #Window
        window = QWidget()
        window.setLayout(main_layout)
        window.setWindowTitle("P2P Chat")
        window.show()

        app.exec_()   

    def toggle_buttons(self):
        self.host_button.setDisabled(self.connected)
        self.connect_button.setDisabled(self.connected)
        self.end_button.setDisabled(not self.connected)
        self.mes_button.setDisabled(not self.connected)

    def on_submit(self):
        if self.connected:
            self.incoming_text.insertHtml("<b> You: </b>" + self.mes_text.text())
            self.incoming_text.insertPlainText("\n")

            self.mes_text.setText("")


# window = MainWindow()
# window.show()

Application()