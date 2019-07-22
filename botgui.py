# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gif.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QByteArray, QSettings, QTimer, pyqtSlot
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QSizePolicy, QVBoxLayout, QAction, QPushButton, QDesktopWidget, QApplication,QGridLayout,QHBoxLayout
from PyQt5.QtGui import QMovie
import time
#import cvcap as cv
import aprCv as cv
import socket
import autotest as at
import pyxhook
import time
import pandas as pd
import csv
import shutil



class Ui_Form(QWidget):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(491, 280)
        #Align at center of Screen
        qr = Form.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        Form.move(qr.topLeft())
        #Color
        Form.setAutoFillBackground(True)
        p = Form.palette()
        p.setColor(Form.backgroundRole(), Qt.white)
        Form.setPalette(p)
        #Label
        self.label = QtWidgets.QLabel(Form) 
        self.label.setGeometry(QtCore.QRect(0, 0, 491, 280))
        self.label.setObjectName("label")


        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "TextLabel"))
        #self.Gif()
        #self.conn(Form)
        self.CallNewForm(Form)

        

        #button = QPushButton('Next', self.label)
        #button.setToolTip('This is an example button')
        #button.move(10,10)
        #button.clicked.connect(lambda:self.CallNewForm(Form))
        #self.CallNewForm(Form)
    def conn(self,form):
        
        host = '192.168.43.187'
        port = 1040
        buffer_size = 1024
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.QTimer.singleShot(5000, lambda:self.connecting())
        s.settimeout(5) 
        try:
           #QTimer.singleShot(5000, lambda:self.on_connect())
            s.connect((host, port))
            s.send('2'.encode())
            data=s.recv(buffer_size)
            s.close()
            print("Connected")
            self.movie = QMovie("giphy.gif", QByteArray(), self.label)
            size = self.movie.scaledSize()
            #self.setStyleSheet("background-color: red")
            self.setGeometry(200, 200, size.width()-10, size.height())
            self.movie.setCacheMode(QMovie.CacheAll)
            self.label.setMovie(self.movie)
            self.movie.start()
            self.movie.loopCount()
            QTimer.singleShot(3430, lambda:self.movie.stop())
            self.label2 = QtWidgets.QLabel(Form)
            self.label2.setGeometry(QtCore.QRect(155,230, 200, 10))
            self.label2.setObjectName("label2")
            self.label2.setText("Connecting To Server....")
            QTimer.singleShot(3300, lambda:self.CallNewForm(form))
            
            #self.on_click()
        except socket.timeout:
            print("No conntime")
            
            self.label.setGeometry(QtCore.QRect(155,150, 220, 20))
            #self.label.setObjectName("label2")
            self.label.setText("Connection Timeout")
            #QTimer.singleShot(3000, lambda:self.on_noconnect())
            
            #QTimer.singleShot(5000, lambda:self.on_connect())
            #sys.exit()
        except socket.error:
            print("No conn") 
            self.label.setGeometry(QtCore.QRect(155,150, 220, 20))
            #self.label.setObjectName("label2")
            self.label.setText("Connection Error")

            #QTimer.singleShot(3000, lambda:self.on_noconnect())
                            
                                

    def CallNewForm(self,Form):
        #self.CloseDialog()
        form2 = MenuForm()
        form2.resize(800,500)
        form2.exec_()
        self.hide()

    def CloseDialog(self):
        self.close()     


 
class MenuForm(QtWidgets.QDialog):


    def __init__(self):
        super(MenuForm, self).__init__()
        str1=""
        listButton1=['pushButton_1','pushButton_2','pushButton_3','pushButton_4','pushButton_5','pushButton_6','pushButton_7','pushButton_8','pushButton_9','pushButton_10','pushButton_11','pushButton_12','pushButton_13','pushButton_14','pushButton_15','pushButton_16','pushButton_17','pushButton_18','pushButton_19','pushButton_20','pushButton_21','pushButton_22','pushButton_23','pushButton_24','pushButton_25','pushButton_26','pushButton_27','pushButton_28','pushButton_29','pushButton_30','pushButton_31','pushButton_32']
        img1=['1.jpg','2.jpg','3.jpg','4.jpg','5.jpg','6.jpg','7.jpg','8.jpg','9.jpg','10.jpg','11.jpg','12.jpg','13.jpg','14.jpg','15.jpg','16.jpg','17.jpg','18.jpg','19.jpg','20.jpg','21.jpg','22.jpg','23.jpg','24.jpg','25.jpg','26.jpg','27.jpg','28.jpg','29.jpg','30.jpg','31.jpg','32.jpg']
       
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: rgb(30, 30, 30);")
        #self.setWindowOpacity(1 - 50 / 100)


        self.btn=[]
        self.hLaout=[]
        vLayout = QVBoxLayout(self)
        maxrow=4
        maxcol=8
        bn=0
        im=1
        for i in range(maxrow):
            self.hLaout.append(i)
            self.hLaout[i]=QHBoxLayout()
            for x in range(maxcol) :
                self.btn.append(bn)
                self.btn[bn]= QtWidgets.QPushButton()
                #self.btn[bn].setText('BTN-' +str(bn))
                self.btn[bn].setObjectName(str(bn))
                self.btn[bn].setIcon(QtGui.QIcon('tagsImg//'+str(im)+'.jpg'))
                self.btn[bn].setIconSize(QtCore.QSize(85,110))
                self.btn[bn].setStyleSheet("color: rgb(85, 170, 255);")
                #self.btn[x].setGeometry(qc.QRect(0,100+(x*20), 100,20))
                self.btn[bn].clicked.connect(self.tagButton)
                self.hLaout[i].addWidget(self.btn[bn])
                bn=bn+1
                im=im+1
            vLayout.addLayout(self.hLaout[i])    
            
    
            
        
        

    def tagButton(self):
        sending_button = self.sender()
        bn=str(sending_button.objectName())
        #print(bn)
        self.CallNewForm(bn) 
        #self.hide()   


    
    def CallNewForm(self,tagId):
        #self.CloseDialog()
        #print(str)
        form3 = CvTag()
        form3.setParmeter(tagId)
        form3.resize(800,500)
        form3.exec_()


           

class CvTag(QtWidgets.QDialog):

    ntag=12
    def __init__(self):
        super(CvTag, self).__init__()
        print("8765r4w3q2wertfgyujhkikl;./likjuyhtrseazxcvbghjuy76treds")
        self.flag=0
        self.tagId=""
        self.entry1=[]
        self.fg=77
        self.start_time=time.time()
        self.currentAngle=90
        self.label = QtWidgets.QLabel()
        self.label.setGeometry(QtCore.QRect(10, 10, 640, 480))
        self.setStyleSheet("background-color: rgb(30, 30, 30);")
        self.label.setText("")
        self.label2 = QtWidgets.QLabel()
        self.label2.setGeometry(QtCore.QRect(10, 5, 640, 480))
        self.label2.setStyleSheet("background-color: rgb(132, 123, 123);")
        self.label2.setText("")
        self.label3 = QtWidgets.QLabel(self.label2)
        self.label3.setGeometry(QtCore.QRect(10, 0, 100, 50))
        self.label3.setStyleSheet("background-color: rgb(132, 123, 123);")
        self.label3.setText("Tag:"+self.tagId)
        self.b1= QtWidgets.QPushButton(self.label2)
        self.b2= QtWidgets.QPushButton(self.label2)
        self.b3= QtWidgets.QPushButton(self.label2)
        self.b4= QtWidgets.QPushButton(self.label2)
        self.b5= QtWidgets.QPushButton(self.label2)
        self.b6= QtWidgets.QPushButton(self.label2)
        self.b7= QtWidgets.QPushButton(self.label2)
        self.b8= QtWidgets.QPushButton(self.label2)
        self.b9= QtWidgets.QPushButton(self.label2)
        self.b1.setGeometry(QtCore.QRect(10, 50, 113, 150))
        self.b1.setObjectName("pushButton")
        self.b1.setText("Train")
        #self.label2.setVisible(False)

        self.b1.clicked.connect(lambda:self.train())

        
        self.b2.setGeometry(QtCore.QRect(10, 230, 113, 150))
        self.b2.setObjectName("pushButton")
        self.b2.setText("Autonomous")
        self.b2.clicked.connect(lambda:self.auto())
        
        self.b3.setGeometry(QtCore.QRect(10, 400, 113, 50))
        self.b3.setObjectName("pushButton")
        self.b3.setText("Back")
        self.b3.clicked.connect(self.CloseDialog)
        
        self.b4.setGeometry(QtCore.QRect(0, 0, 1, 1))
        self.b5.setGeometry(QtCore.QRect(0, 0, 1, 1))
        self.b6.setGeometry(QtCore.QRect(0, 0, 1, 1))
        self.b7.setGeometry(QtCore.QRect(0, 0, 1, 1))
        self.b8.setGeometry(QtCore.QRect(0, 0, 1, 1))
        self.b9.setGeometry(QtCore.QRect(0, 0, 1, 1))



        hLayouta1 = QHBoxLayout()
        vLayout = QVBoxLayout(self)
        hLayouta1.addWidget(self.label)
        hLayouta1.addWidget(self.label2)
        vLayout.addLayout(hLayouta1)
        #try:
        #    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #    print("connected")
        #except socket.error:
        #    print("Socket Creation Failed")    

          
        '''self.ncv=cv.CvCap()
        self.ncv.setObjects(self.label,self.tagId)
        self.StartVideo()'''
    def setParmeter(self,tagId):
        self.tagId=tagId
        self.label3.setText("Tag:"+tagId)
        self.ncv=cv.CvCap()
        self.ncv.setObjects(self.label,self.tagId)
        self.StartVideo()
    def StartVideo(self):
        print('Start')
        self.ncv.StartCvThread()

    def CloseDialog(self):
        #print('Stop')
        self.ncv.StopCv()   
        self.hide()
        self.sendToServer(str(4).encode())
        print("Program Terminated")
        self.hm.stop()
        #aptag.logger.warning("Exiting training mode \n")
        

    

    def eve(self,event1):
        entry=event1 
        #print(self.entry) 

    def flg(self,flag1):
        #print(flag1)
        self.ntag=flag1 

        #print('a: '+str(self.ntag))
        if flag1==1:
        	self.fg=1

        else:
            self.fg=0	


    #def returnFlg(self):
    #    return self.tag       
              
    



    def train(self):
        print("Trainqwef")
        
        self.b1.setGeometry(QtCore.QRect(45, 115,40, 60))
        self.b1.setObjectName("pushButton")
        self.b1.setText(u"\u2191")
        #self.b1.setEnabled(False)

        self.b2.setGeometry(QtCore.QRect(45, 185,40, 60))
        self.b2.setObjectName("pushButton")
        self.b2.setText(u"\u2193")
        #self.b2.setEnabled(False)
        
        self.b4.setGeometry(QtCore.QRect(5, 105, 30, 150))
        self.b4.setObjectName("pushButton")
        self.b4.setText(u"\u2190")
        #self.b4.setEnabled(False)
        
        self.b5.setGeometry(QtCore.QRect(95, 105, 30, 150))
        self.b5.setObjectName("pushButton")
        self.b5.setText(u"\u2192")
        #self.b5.setEnabled(False)

        self.b6.setGeometry(QtCore.QRect(10, 265,113, 30))
        self.b6.setObjectName("pushButton")
        self.b6.setText("Stop(Space)")
        #self.b6.setEnabled(False)

        self.b7.setGeometry(QtCore.QRect(27, 320,80, 60))
        self.b7.setObjectName("pushButton")
        self.b7.setText("Reset(R)")
        #self.b7.setEnabled(False)

        self.b8.setGeometry(QtCore.QRect(10, 70,113, 30))
        self.b8.setObjectName("pushButton")
        self.b8.setText("Save")
        self.b9.setGeometry(QtCore.QRect(10, 40,113, 30))
        self.b9.setObjectName("pushButton")
        self.b9.setText("Start")
        self.b8.clicked.connect(lambda: shutil.copyfile('spider.csv', 'trainData.csv'))

       


        self.b1.keyPressEvent = self.keyPressEvent
        self.b1.keyReleaseEvent = self.keyReleaseEvent
        #self.b2.keyPressEvent = self.keyPressEvent
        #self.b2.keyReleaseEvent = self.keyReleaseEvent

        #QtWidgets.QShortcut(QtCore.Qt.Key_Up, self, self.fooUp)

    def leftMove(self):
        """
        Function to decrement steer angle by 20 degrees

        """
        self.steerAngle

        if self.steerAngle >= 30:
            self.steerAngle = self.steerAngle - 20
        else:
            self.steerAngle = 10
        print(self.steerAngle)
        #print(self.fg)


    def rightMove(self):
        """
        Function to increment steer angle by 20 degrees

        """
        self.steerAngle

        if self.steerAngle <= 150:
            self.steerAngle = self.steerAngle + 20
        else:
            self.steerAngle = 170
        print(self.steerAngle)
        #print(self.fg)


    def sendToServer(self,encodedKey):
        """
        Sends data to Pi using socket
        :param encodedKey:
        """
        host = '192.168.43.187'
        port = 1040
        buffer_size = 1024

        #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.s.settimeout(3)
        #print("hi1")
        try:
            self.s.connect((host, port))
            #print("bye1")
        except socket.error as e:
            print("Caught exception: " + str(e))
            #aptag.logger.critical("Unable to connect with the server !")
            #aptag.logger.warning("Exiting training mode \n")
        self.s.send(encodedKey)
        data = self.s.recv(buffer_size)
        #print("hi11234")
        value=data.decode()
        print("received data:",value)
        self.s.close()


    '''def keyEvt(self):
        print("m :"+str(self.ntag))'''

    def keyPressEvent(self, e):
        print("event", e)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
        	df = pd.read_csv('data.csv', names=["Time", "X", "Y", "Z", "Roll", "Yaw", "Pitch"])
        except pandas.io.common.EmptyDataError:
        	print("File Empty")
			
        	
        #print(df['Time'][0])
        self.entry1=[df['Time'][0],df['X'][0],df['Y'][0],df['Z'][0],df['Roll'][0],df['Yaw'][0],df['Pitch'][0]]
        
        if e.key()  == Qt.Key_Up and len(self.entry1)!=0:
            
            self.b1.setStyleSheet("background-color: red")
            self.b2.setStyleSheet("background-color: grey")
            #self.sendToServer(str(0).encode())
            self.steerAngle = 0
            print("forward")

        if e.key()  == Qt.Key_Down and len(self.entry1)!=0:
            
            self.b2.setStyleSheet("background-color: red")
            self.b1.setStyleSheet("background-color: grey")
            #self.sendToServer(str(1).encode())
            self.steerAngle = 1
            print("backward")

        if e.key()  == Qt.Key_Left and len(self.entry1)!=0:
            
            self.b4.setStyleSheet("background-color: red")
            self.steerAngle = self.currentAngle
            self.leftMove()
            self.currentAngle = self.steerAngle
            #self.sendToServer(str(self.steerAngle).encode())
            print("leftMove")
            
        if e.key()  == Qt.Key_Right and len(self.entry1)!=0: 
            
            self.b5.setStyleSheet("background-color: red")
            self.steerAngle = self.currentAngle
            self.rightMove()
            self.currentAngle = self.steerAngle
            #self.sendToServer(str(self.steerAngle).encode())
            print("rightMove")

        if e.key()  == Qt.Key_Space :
            
            self.b6.setStyleSheet("background-color: red")
            self.b1.setStyleSheet("background-color: grey")
            self.b2.setStyleSheet("background-color: grey")
            #self.sendToServer(str(3).encode())
            self.steerAngle = 3
            print("Stop")
            
        if e.key()  == Qt.Key_R and len(self.entry1)!=0:
            
            self.b7.setStyleSheet("background-color: red") 
            #self.sendToServer(str(2).encode())
            self.steerAngle = 2
            print("reset") 

        if  len(self.entry1)==0:
        	self.steerAngle = 3
        	print("Stop!")
            
        	    
        
        if((time.time()-self.start_time)>0.25):    
            self.sendToServer(str(self.steerAngle).encode())
            print(time.time()-self.start_time)     
            self.start_time=time.time()
            
        with open('spider.csv', 'a') as csvFile:
            row = self.entry1
            #row.append(keyPressed)
            row.append(self.steerAngle)
            #print(row)
            writer = csv.writer(csvFile)
            writer.writerow(row)
            csvFile.close()  


    def keyReleaseEvent(self, e):
        print("event", e)
        if e.key()  == Qt.Key_Up :
            print(' Up')
            #self.b1.setStyleSheet("background-color: grey")
            #self.sendToServer(str(3).encode())
            #self.steerAngle = 3
            #print("reset")

        if e.key()  == Qt.Key_Down :
            print(' Up')
            #self.b2.setStyleSheet("background-color: grey")
            #self.sendToServer(str(3).encode())
            #self.steerAngle = 3
            #print("reset")
            
        if e.key()  == Qt.Key_Left :
            print(' Up')
            self.b4.setStyleSheet("background-color: grey")
            
        if e.key()  == Qt.Key_Right :
            print(' Up')
            self.b5.setStyleSheet("background-color: grey")

        if e.key()  == Qt.Key_Space :
            print(' Up')
            self.b6.setStyleSheet("background-color: grey")
            
        if e.key()  == Qt.Key_R :
            print(' Up')
            self.b7.setStyleSheet("background-color: grey")    


   




    def auto(self):
        print("Trainqwef")
        
        self.b1.setGeometry(QtCore.QRect(10, 200,113, 60))
        self.b1.setObjectName("pushButton")
        self.b1.setText("Stop")   
        self.b2.clicked.connect(lambda:self.sendToServer(str(3).encode()))
        
        self.b2.setVisible(False) 
        self.aut=at.Autonomous()
        self.aut.autoControl()
        #self.aut.compareCoordinates(self.entry)'''       
      
        


   



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

