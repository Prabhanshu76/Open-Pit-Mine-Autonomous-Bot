from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication, QLabel, QSizePolicy, QVBoxLayout, QAction, QPushButton, \
    QDesktopWidget, QApplication, QGridLayout, QHBoxLayout
import menuform2 as cw


class MenuForm(QtWidgets.QDialog):
    def __init__(self):
        super(MenuForm, self).__init__()
        self.btn = []
        self.hLaout = []
        vLayout = QVBoxLayout(self)
        maxrow = 4
        maxcol = 8
        bn = 0
        im = 1
        self.setStyleSheet("background-color: rgb(30, 30, 30);")
        """
        Initializing and assigning ID to each of 32 buttons
        Assigning tag images to 32 buttons
        4 sets of 8 buttons on horizontal layout
        Then these 4 horizontal layouts are assigned to a vertical layout, forming 8x4 butoon setup
        """
        for i in range(maxrow):
            self.hLaout.append(i)
            self.hLaout[i] = QHBoxLayout()
            for x in range(maxcol):
                self.btn.append(bn)
                self.btn[bn] = QtWidgets.QPushButton()
                self.btn[bn].setObjectName(str(bn))
                self.btn[bn].setIcon(QtGui.QIcon('tagsImg//' + str(im) + '.jpg'))
                self.btn[bn].setIconSize(QtCore.QSize(85, 110))
                self.btn[bn].setStyleSheet("color: rgb(85, 170, 255);")
                self.btn[bn].clicked.connect(self.tag_button)
                self.hLaout[i].addWidget(self.btn[bn])
                bn = bn + 1
                im = im + 1
            vLayout.addLayout(self.hLaout[i])

    def tag_button(self):
        """
        On selecting a button, button ID is stored as a string and sending it to call_form for April tag to detect a specified tag ID
        Then call_form() is called to call menuform2.py
        """
        sending_button = self.sender()
        bn = str(sending_button.objectName())
        # print(bn)
        self.call_form(bn)

    def call_form(self, tagId):
        """
        Call menuform2.py
        """
        form3 = cw.CvTag()
        form3.set_parmeter(tagId)
        form3.resize(800, 500)
        form3.exec_()
        # self.hide()
