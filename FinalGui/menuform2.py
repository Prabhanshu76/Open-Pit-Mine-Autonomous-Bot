from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QByteArray, QSettings, QTimer, pyqtSlot
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication, QLabel, QSizePolicy, QVBoxLayout, QAction, QPushButton, \
    QDesktopWidget, QApplication, QGridLayout, QHBoxLayout
import aprCv as cv
import socket
import autotest as at
import time
import pandas as pd
import csv
import csvsort as cs


class CvTag(QtWidgets.QDialog):
    def __init__(self):
        """
        Initializing Buttons and Labels
        """
        super(CvTag, self).__init__()
        self.start_time = time.time()
        self.currentAngle = 90
        self.label = QtWidgets.QLabel()
        self.label4 = QtWidgets.QLabel(self.label)
        self.label2 = QtWidgets.QLabel()
        self.label3 = QtWidgets.QLabel(self.label2)
        self.aut = at.Autonomous()
        self.css=cs.csv_sort()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.flag = 0
        self.dfname = 0
        self.tagId = ""
        self.entry1 = []
        self.saveData = []
        self.receiveddata=''
        self.fg = 77
        self.b1 = QtWidgets.QPushButton(self.label2)
        self.b2 = QtWidgets.QPushButton(self.label2)
        self.b3 = QtWidgets.QPushButton(self.label2)
        self.b4 = QtWidgets.QPushButton(self.label2)
        self.b5 = QtWidgets.QPushButton(self.label2)
        self.b6 = QtWidgets.QPushButton(self.label2)
        self.b7 = QtWidgets.QPushButton(self.label2)
        self.b8 = QtWidgets.QPushButton(self.label2)
        self.b9 = QtWidgets.QPushButton(self.label2)
        self.b10 = QtWidgets.QPushButton(self.label2)
        self.b11 = QtWidgets.QPushButton(self.label2)
        self.b12 = QtWidgets.QPushButton(self.label2)
        self.setup()

    def setup(self):
        """
        Setting Color and GEometry of Labels and putting them in Horizontal Layout
        Horizontal Layout is put in Vertical Layout
        """
        self.label4.setStyleSheet("background-color: rgb(132, 123, 123);")
        self.label4.setText("")
        self.label4.setObjectName("label4")
        self.label.setGeometry(QtCore.QRect(10, 10, 640, 480))
        self.setStyleSheet("background-color: rgb(30, 30, 30);")
        self.label.setText("")

        self.label2.setGeometry(QtCore.QRect(10, 5, 640, 480))
        self.label2.setStyleSheet("background-color: rgb(132, 123, 123);")
        self.label2.setText("")

        self.label3.setGeometry(QtCore.QRect(10, 0, 100, 50))
        self.label3.setStyleSheet("background-color: rgb(132, 123, 123);")
        self.label3.setText("Tag:" + self.tagId)

        hLayouta1 = QHBoxLayout()
        vLayout = QVBoxLayout(self)
        hLayouta1.addWidget(self.label)
        hLayouta1.addWidget(self.label2)
        vLayout.addLayout(hLayouta1)

        self.set_window()

    def set_window(self):
        """
        Button setup for Training and Autonomous mode Window
        Rest buttons are set invisible
        """
        self.b1.setGeometry(QtCore.QRect(10, 50, 113, 150))
        self.b1.setObjectName("Train")
        self.b1.setText("Train")

        self.b1.clicked.connect(lambda: self.train())

        self.b2.setGeometry(QtCore.QRect(10, 230, 113, 150))
        self.b2.setObjectName("Autonomous")
        self.b2.setText("Autonomous")
        self.b2.clicked.connect(lambda: self.auto())

        self.b3.setGeometry(QtCore.QRect(10, 400, 113, 50))
        self.b3.setObjectName("Back")
        self.b3.setText("Back")
        self.b3.clicked.connect(self.close_1)

        self.b4.setVisible(False)
        self.b5.setVisible(False)
        self.b6.setVisible(False)
        self.b7.setVisible(False)
        self.b8.setVisible(False)
        self.b9.setVisible(False)
        self.b10.setVisible(False)
        self.b11.setVisible(False)
        self.b12.setVisible(False)

    def set_parmeter(self, tagId):
        """
        Function called in menuform.py
        """
        self.tagId = tagId
        self.label3.setText("Tag:" + tagId)
        """
        Sending Label(to show AprilTag detection window) and tagId to aprCv.py
        CvCap() is class(QThread) from aprCv.py to start Video Streaming to detect AprilTag
        """
        self.ncv = cv.CvCap()
        self.ncv.set_objects(self.label, self.tagId)
        self.start_video()

    def start_video(self):
        """
        Start QThread in aprCv.py to start camera streaming to detect AprilTag
        """
        print('Start')
        self.ncv.start_cv_thread()

    def close_1(self):
        """
        Stop QThread in aprCv.py
        """
        self.ncv.stop_cv()
        self.hide()
        # self.send_server(str(4).encode())
        print("Program Terminated")

    def close_2(self):
        """
        Close Train window
        csvsort.py is called on clicking back button to sort dataset in Z axis in descending order
        """
        print("D2")
        self.b1.setEnabled(True)
        self.b2.setEnabled(True)
        self.b2.setVisible(True)
        self.b3.setVisible(True)
        self.css.sort_val()
        # self.send_server(str(4).encode())
        self.set_window()

    def train(self):
        """
        Run's when Train button is selected
        Button setup for Train Window
        Buttons are disabled till start button is clicked(start_train())
        First end_train() is called then start_train()
        """
        self.b4.setVisible(True)
        self.b5.setVisible(True)
        self.b6.setVisible(True)
        self.b7.setVisible(True)
        self.b8.setVisible(True)
        self.b9.setVisible(True)
        self.b10.setVisible(True)

        self.b1.setGeometry(QtCore.QRect(45, 115, 40, 60))
        self.b1.setObjectName("Up")
        self.b1.setText(u"\u2191")

        self.b2.setGeometry(QtCore.QRect(45, 185, 40, 60))
        self.b2.setObjectName("Down")
        self.b2.setText(u"\u2193")

        self.b4.setGeometry(QtCore.QRect(5, 105, 30, 150))
        self.b4.setObjectName("Left")
        self.b4.setText(u"\u2190")

        self.b5.setGeometry(QtCore.QRect(95, 105, 30, 150))
        self.b5.setObjectName("Right")
        self.b5.setText(u"\u2192")

        self.b6.setGeometry(QtCore.QRect(10, 265, 113, 30))
        self.b6.setObjectName("Stop")
        self.b6.setText("Stop(Space)")

        self.b7.setGeometry(QtCore.QRect(27, 320, 80, 60))
        self.b7.setObjectName("R")
        self.b7.setText("Reset(R)")

        self.b8.setGeometry(QtCore.QRect(10, 70, 113, 30))
        self.b8.setObjectName("Save")
        self.b8.setText("Save")

        self.b9.setGeometry(QtCore.QRect(10, 40, 113, 30))
        self.b9.setObjectName("Start")
        self.b9.setText("Start")
        self.b3.setVisible(False)
        self.b10.setGeometry(QtCore.QRect(10, 400, 113, 50))
        self.b10.setObjectName("Back")
        self.b10.setText("Back")
        self.b10.clicked.connect(self.close_2)
        self.end_train()

    def start_train(self):
        """
        Training mode starts. Keyboard keys are used to control bot(keyPressEvent and keyReleaseEvent ane called)
        """
        print("startT")

        self.b1.setEnabled(True)
        self.b2.setEnabled(True)
        self.b4.setEnabled(True)
        self.b5.setEnabled(True)
        self.b6.setEnabled(True)
        self.b7.setEnabled(True)
        self.b8.setEnabled(True)
        self.b1.keyPressEvent = self.keyPressEvent
        self.b1.keyReleaseEvent = self.keyReleaseEvent
        self.b8.clicked.connect(lambda: self.save_data())
        self.b10.clicked.connect(self.close_2)

    def save_data(self):
        """
        Saves live Coordinate data that is being appended in keyPressEvent stored in a CSV File
        """
        with open('trainData.csv', 'a') as csvFile:
            for i in self.saveData:
                writer = csv.writer(csvFile)
                writer.writerow(i)
            csvFile.close()
            self.saveData = []
        if self.dfname == 0:
            data = pd.read_csv('trainData.csv', names=["Time", "X", "Y", "Z", "Roll", "Yaw", "Pitch", "angle"])
            data.to_csv('trainData2.csv')
            dfname = 1
        else:
            data = pd.read_csv('trainData.csv')
            data[1:].to_csv('trainData2.csv')
        self.end_train()

    def end_train(self):
        """
        Function used to disable key press event till driver start training by clicking "Start"
        """
        print("endT")
        self.b10.clicked.connect(self.close_2)
        self.b1.setEnabled(False)
        self.b2.setEnabled(False)
        self.b4.setEnabled(False)
        self.b5.setEnabled(False)
        self.b6.setEnabled(False)
        self.b7.setEnabled(False)
        self.b8.setEnabled(False)
        self.b9.clicked.connect(lambda: self.start_train())

    def left_move(self):
        """
        Function to decrement steer angle by 20 degrees

        """
        # self.steerAngle

        if self.steerAngle >= 30:
            self.steerAngle = self.steerAngle - 20
        else:
            self.steerAngle = 10
        print(self.steerAngle)
        # print(self.fg)

    def right_move(self):
        """
        Function to increment steer angle by 20 degrees

        """
        # self.steerAngle

        if self.steerAngle <= 150:
            self.steerAngle = self.steerAngle + 20
        else:
            self.steerAngle = 170
        print(self.steerAngle)
        # print(self.fg)

    def send_server(self, encodedKey):
        """
        Sends data to Pi using socket
        """
        host = '192.168.137.96'
        port = 1040
        buffer_size = 1024

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(3)
        # print("hi1")
        try:
            self.s.connect((host, port))
            # print("bye1")
        except socket.error as e:
            print("Caught exception: " + str(e))
            # aptag.logger.critical("Unable to connect with the server !")
            # aptag.logger.warning("Exiting training mode \n")
        self.s.send(encodedKey)
        self.receiveddata = self.s.recv(buffer_size)
        # print("hi11234")
        #value = data.decode()
        #print("received data:", value)
        self.s.close()

    def keyPressEvent(self, e):
        """
        Called when Keyboard keys are pressed, AprilTag live coordinates are extracted from a CSV file which is being
        constantly being updated from aprCv.py. These live coordinates are being saved in a List, updating on each
        keypress and when save button is clicked, given list is being saved in a CSV File.
        """
        print("event", e)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            df = pd.read_csv('data.csv', names=["Time", "X", "Y", "Z", "Roll", "Yaw", "Pitch"])
        except pandas.io.common.EmptyDataError:
            print("File Empty")

        # print(df['Time'][0])
        try:
            self.entry1 = [df['Time'][0], df['X'][0], df['Y'][0], df['Z'][0], df['Roll'][0], df['Yaw'][0],
                           df['Pitch'][0]]

            if e.key() == Qt.Key_Up:
                self.b1.setStyleSheet("background-color: red")
                self.b2.setStyleSheet("background-color: grey")
                self.steerAngle = 0
                print("forward")

            if e.key() == Qt.Key_Down:
                self.b2.setStyleSheet("background-color: red")
                self.b1.setStyleSheet("background-color: grey")
                self.steerAngle = 1
                print("backward")

            if e.key() == Qt.Key_Left:
                self.b4.setStyleSheet("background-color: red")
                self.steerAngle = self.currentAngle
                self.left_move()
                self.currentAngle = self.steerAngle
                print("leftMove")

            if e.key() == Qt.Key_Right:
                self.b5.setStyleSheet("background-color: red")
                self.steerAngle = self.currentAngle
                self.right_move()
                self.currentAngle = self.steerAngle
                print("rightMove")

            if e.key() == Qt.Key_Space:
                self.b6.setStyleSheet("background-color: red")
                self.b1.setStyleSheet("background-color: grey")
                self.b2.setStyleSheet("background-color: grey")
                self.steerAngle = 3
                print("Stop")

            if e.key() == Qt.Key_R:
                self.b7.setStyleSheet("background-color: red")
                self.steerAngle = 2
                print("reset")

            if len(self.entry1) == 0:
                self.steerAngle = 3
                print("Stop!")

            print(time.time())

            if (time.time() - self.start_time) > 0.08:
                self.send_server(str(self.steerAngle).encode())
                print(time.time() - self.start_time)
                self.start_time = time.time()
            #self.updata=ud.Up_Data()
            print(self.receiveddata)
            #dataPi = ((self.receiveddata.decode()).split(':'))
            #distance1 , distance2, speed ,ipAddr=str(dataPi[0]) , str(dataPi[1]) , str(dataPi[2]) , '192.168.137.96'
            #variableSensor='Ultrasonic1 : '+distance1+' Ultrasonic2 : '+distance2+' Motor Speed : '+speed
            #liveCoord = {'assetState': 'ON' ,  'assetSpeed':speed,   'variableSensor':variableSensor, 'assetIpAddress':ipAddr ,  'assetRelativePostion':str(str(self.entry1[1])+' , '+str(self.entry1[2])+' , '+str(self.entry1[3])),'locationX':format(float(self.entry1[1]), '.4f'),'locationY':format(float(self.entry1[2]), '.4f'),'locationZ':format(float(self.entry1[3]), '.4f'),'angleX':format(float(self.entry1[4]), '.4f'),'angleY':format(float(self.entry1[5]), '.4f'),'angleZ':format(float(self.entry1[6]), '.4f'),'sensorsWorkingCondtion':'ON', 'lastUpdatedOn':str(time.ctime(int(time.time())))}
            #print(self.updata.mine_post_data(self.updata.get_authtoken(),liveCoord))
            #data from send_server  yaha chahiye       
            row = self.entry1
            row.append(self.steerAngle)
            self.saveData.append(row)
            print(time.time())
        except:
            print("No data From Live Cord")

    def keyReleaseEvent(self, e):
        # print("event", e)

        if e.key() == Qt.Key_Left:
            # print(' Up')
            self.b4.setStyleSheet("background-color: grey")

        if e.key() == Qt.Key_Right:
            # print(' Up')
            self.b5.setStyleSheet("background-color: grey")

        if e.key() == Qt.Key_Space:
            # print(' Up')
            self.b6.setStyleSheet("background-color: grey")

        if e.key() == Qt.Key_R:
            # print(' Up')
            self.b7.setStyleSheet("background-color: grey")

    def close_3(self):
        """
        Close Autonomous mode window
        """
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print("D2")
        self.b1.setVisible(True)
        self.b10.setVisible(True)
        self.b12.setVisible(False)
        self.b11.setVisible(False)
        self.b2.setEnabled(True)
        self.b2.setVisible(True)
        self.b3.setVisible(True)
        # self.aut=at.Autonomous()
        self.aut.StopAuc()
        self.send_server(str(4).encode())
        self.close_2

    def close_4(self):
        """
        Close Autonomous mode window
        """
        print("CLOSe4")
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.b11.setGeometry(QtCore.QRect(10, 200, 113, 60))
        self.b11.setText("Start")
       
        self.aut.StopAuc()
        self.send_server(str(3).encode())
        self.b11.clicked.connect(self.auto)
        
    

    def auto(self):
        """
        Function called for Autonomous movement of Bot, autotest.py is called
        """
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.b12.setVisible(True)
        self.b11.setVisible(True)
        self.b11.setGeometry(QtCore.QRect(10, 200, 113, 60))
        self.b11.setObjectName("pushButton")
        self.b11.setText("Stop")
        self.b11.clicked.connect( self.close_4)
        self.b1.setVisible(False)
        self.b2.setVisible(False)
        self.b3.setVisible(False)
        self.b10.setVisible(False)
        self.b12.setGeometry(QtCore.QRect(10, 400, 113, 50))
        self.b12.setObjectName("pushButton")
        self.b12.setText("Back")
        self.b12.clicked.connect(self.close_3)
        self.aut.StartAuc()
