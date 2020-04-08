import sys, re, socket, traceback, threading, time
from PyQt5.QtWidgets import QApplication, QDialog, QInputDialog, QHBoxLayout, QWidget, QSplitter, QPushButton, QLabel, QMainWindow, QVBoxLayout, QTextEdit, QLineEdit 
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class ListenThread(QThread):
    sig = pyqtSignal(object)

    def __init__(self, socket):
        QThread.__init__(self)
        self.socket = socket

    def run(self):
        with self.socket:
            while(True):
                try:
                    incoming = self.socket.recv(32000).decode()
                except:
                    self.socket.close()
                    return
                if incoming == "<<<END CONNECTION>>>":
                    self.socket.sendall("<<<END CONNECTION>>>".encode())
                    self.socket.close()
                    break
                self.sig.emit(incoming)
        print("Connection Ended")


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
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.q_app = QApplication([])
        """Connection Area"""        

        self.status = QLabel("Host or Connect")
        self.status.setAlignment(Qt.AlignCenter)
        
        #Host Button
        self.host_button = QPushButton("Host")
        self.host_button.clicked.connect(self.host)
        #Connect Button
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect)

        #Connect Button
        self.end_button = QPushButton("End Connection")
        self.end_button.clicked.connect(self.end_connection)

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
        main_layout.addWidget(self.status)
        main_layout.addLayout(connection_layout)
        main_layout.addWidget(split)
        main_layout.addWidget(self.incoming_text)
        main_layout.addLayout(mes_layout)


        self.toggle_buttons()

        #Window
        self.window = QWidget()
        self.window.setLayout(main_layout)
        self.window.setWindowTitle("P2P Chat")
        self.window.show() 

    def host(self):
        port, ok = QInputDialog().getText(self.window, "Host", "Give Port Number\nPort should be between 1024 and 65535", QLineEdit.Normal)
        
        if ok and (not port.isdigit() or not(int(port) >= 1024 and int(port) <= 65535)):
            self.host()
        elif ok and port:
            self.status.setText("Awaiting Connection")
            self.connected = True
            self.toggle_buttons()
            try:
                # Wait for new connection
                self.socket.bind(("0.0.0.0", int(port)))
                self.socket.listen()
                conn, client = self.socket.accept()
                self.socket.close()
                self.socket = conn
                self.status.setText("Connection made with " + str(client))
        
                self.incoming_text.insertHtml("<b> Connection Formed </b>")
                self.incoming_text.insertPlainText("\n")

                # Listening Logic 
                self.listen_thread = ListenThread(conn)
                self.listen_thread.start()
                self.listen_thread.finished.connect(self.connection_closed)
                self.listen_thread.sig.connect(self.new_mes)
            except:
                self.connected = False
                self.toggle_buttons()
                self.status.setText("There was an issue hosting... Please try again")
                traceback.print_exc(file=sys.stdout)


    def connect(self):
        addr, ok = QInputDialog().getText(self.window, "Connect", "IP and Port Format (IP:Port). \nPort should be between 1024 and 65535", QLineEdit.Normal)
        REGEX = r"((\d{1,3})[.](\d{1,3})[.](\d{1,3})[.](\d{1,3})|localhost):\d+"

        addr_l = addr.split(":")

        if ok and (not re.match(REGEX, addr) or not (int(addr_l[1]) >= 1024 and int(addr_l[1]) <= 65535)):
            self.connect()          
        elif ok and addr:
            print(addr)
            self.status.setText("Connecting...")
            try:
                self.socket.connect((addr_l[0], int(addr_l[1])))
                self.status.setText("Connected to "+addr)
                self.incoming_text.insertHtml("<b> Connection Formed </b>")
                self.incoming_text.insertPlainText("\n")
                self.connected = True
                self.toggle_buttons()
                self.listen_thread = ListenThread(self.socket)
                self.listen_thread.start()
                self.listen_thread.finished.connect(self.connection_closed)
                self.listen_thread.sig.connect(self.new_mes)
            except ConnectionRefusedError:
                self.status.setText("Connection Failed. Please try again")
            except Exception:
                self.status.setText("Unknown Error has occured.")
                traceback.print_exc(file=sys.stdout)

    def new_mes(self, mes):
        self.incoming_text.insertHtml(mes)
        self.incoming_text.insertPlainText("\n")

    def end_connection(self):
        self.socket.sendall("<<<END CONNECTION>>>".encode())
        

    def connection_closed(self):
        self.incoming_text.insertHtml("<b> Connection Close </b>")
        self.incoming_text.insertPlainText("\n\n")
        self.socket.close()
        self.connected = False
        self.toggle_buttons()
        self.status.setText("Host or Connect")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def toggle_buttons(self):
        self.host_button.setDisabled(self.connected)
        self.connect_button.setDisabled(self.connected)
        self.end_button.setDisabled(not self.connected)
        self.mes_button.setDisabled(not self.connected)

    def on_submit(self):
        if self.connected:
            self.incoming_text.insertHtml("<b> You: </b>" + self.mes_text.text())
            self.incoming_text.insertPlainText("\n")

            self.socket.sendall(("<b> Friend: </b>" + self.mes_text.text()).encode())

            self.mes_text.setText("")


app = Application()

app.q_app.exec_()

app.socket.close()