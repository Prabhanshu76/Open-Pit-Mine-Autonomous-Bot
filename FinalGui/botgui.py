from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QByteArray, QSettings, QTimer, pyqtSlot
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication, QLabel, QSizePolicy, QVBoxLayout, QAction, QPushButton, \
    QDesktopWidget, QApplication, QGridLayout, QHBoxLayout
from PyQt5.QtGui import QMovie, QPixmap
import socket
import menuform as mf


class Ui_Form(QWidget):
    def setupUi(self, Form):
        """
        Setup for Connection Screen
        491x280 px Frameless window with Label on it
        The LAble shows GIF on successful connection  to Socket Server
        conn() function is called to check connection

        """
        Form.setObjectName("Form")
        Form.resize(491, 280)
        # Align at center of Screen
        qr = Form.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        Form.move(qr.topLeft())
        # Color
        Form.setAutoFillBackground(True)
        p = Form.palette()
        p.setColor(Form.backgroundRole(), Qt.white)
        Form.setPalette(p)
        Form.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # Label
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(0, 0, 491, 280))
        self.label.setObjectName("label")
        print("Working")
        self.conn_gif()
        #self.conn()
        QtCore.QMetaObject.connectSlotsByName(Form)

    def conn(self):
        """
        Establishing initial Socket Connection
        On successful connection conn_gif() is called to display GIF on Label
        If there is socket error then Label will show the error and window will close after seconds
        """
        host = '192.168.137.96'
        port = 1040
        buffer_size = 1024

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        try:
            s.connect((host, port))
            s.send('2'.encode())
            data = s.recv(buffer_size)
            s.close()
            print("Connected")
            self.conn_gif()

        except socket.timeout as e:
            print("No conntime",str(e))
            self.label.setGeometry(QtCore.QRect(155, 150, 220, 20))
            self.label.setText("Connection Timeout")
            QTimer.singleShot(3000, lambda: sys.exit())

        except socket.error:
            print("No conn")
            self.label.setGeometry(QtCore.QRect(155, 150, 220, 20))
            self.label.setText("Connection Error")
            QTimer.singleShot(3000, lambda: sys.exit())

    def conn_gif(self):
        """
        Play GIF File for 3.3 seconds if Connection is Established and calls call_form() after 3.3 seconds
        """
        self.movie = QMovie("giphy.gif", QByteArray(), self.label)
        size = self.movie.scaledSize()
        # self.setStyleSheet("background-color: red")
        self.setGeometry(200, 200, size.width() - 10, size.height())
        self.movie.setCacheMode(QMovie.CacheAll)
        self.label.setMovie(self.movie)
        self.movie.start()
        self.movie.loopCount()
        QTimer.singleShot(3430, lambda: self.movie.stop())
        self.label2 = QtWidgets.QLabel(Form)
        self.label2.setGeometry(QtCore.QRect(155, 230, 200, 10))
        self.label2.setObjectName("label2")
        self.label2.setText("Connecting To Server....")
        QTimer.singleShot(3300, lambda: self.call_form())

    def call_form(self):
        """
        Call menuform.py in a 800x500 px window
        """
        form2 = mf.MenuForm()
        form2.resize(800, 500)
        form2.exec_()
        sys.exit()
        # self.hide()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
