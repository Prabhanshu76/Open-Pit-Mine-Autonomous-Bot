'''
This Program has another QThread for running PiCamera
Pass label4 in set_objects method in menuform2
Give label4 dimension of(430,330,200,140)
'''
import numpy as np
import cv2
from PyQt5 import QtCore,QtWidgets
from PyQt5.QtCore import (QCoreApplication, QObject, QRunnable, QThread,
                          QThreadPool, pyqtSignal,pyqtSlot,Qt)
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtWidgets import QWidget,QLabel
import math
from argparse import ArgumentParser
import time
import cv2
import numpy
import csv
#import rospy
#import gif2 as gi
import botgui as gi

import apriltag
camera_params = (834.65688267, 832.75807601, 244.3682,318.55439201)
size = 18
#32
position = {'tag0': None, 'roll': None ,'time':None}



class CvThread(QThread):
    changePixmap = pyqtSignal(QImage)
    
    tagId=""
    startvideo=True
    entry=[]
    

    def Stop(self):
        self.startvideo=False
    
    def run(self):

        parser = ArgumentParser(
             description='test apriltag Python bindings')

        parser.add_argument('device_or_movie', metavar='INPUT', nargs='?', default=0,
                        help='Movie to load or integer ID of camera device')

        apriltag.add_arguments(parser)

        options = parser.parse_args()
        
        cap = cv2.VideoCapture(-1)
        

    

        start_time=time.time()
        #entry=[]
        detector = apriltag.Detector(options,
                                  searchpath=apriltag._get_demo_searchpath())
        #print(self.tagId)       
        while (self.startvideo):
            ret, frame = cap.read()
            #ret2, frame2 = cap2.read()
            #self.bu.label2.setVisible(False) 
           
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                detections, dimg ,tag_id= detector.detect(gray, return_image=True)
                index=33
                flag=0
                if(int(self.tagId) in tag_id):
                    index=tag_id.index(int(self.tagId))
                    flag=1
                #print(len(detections))
                #num_detections = len(detections)
                overlay = frame // 2 
                for i, detection in enumerate(detections):
                    if(i!=index):
                        continue
                    #print("ind "+str(i))
                    #print(tag_id)
                    #print(dimg.size)
                    #overlay = frame // 2 + dimg[:, :, None] // 2
                    pose, e0, e1 = detector.detection_pose(detection,
                                                   camera_params,
                                                   size)

                    apriltag._draw_pose(overlay,
                                 camera_params,
                                 size,
                                 pose)
                    b = numpy.matrix([[0], [0], [0], [1]])
                    coordinate = numpy.matmul(pose, b)
                    new_coord=coordinate
                    position['tag0'] = new_coord
                    roll = math.degrees(math.atan2(pose[0][1] , pose[0][0]))
                    yaw = math.degrees(math.atan((-1 * pose[2][0]) / math.sqrt((pose[2][1]) ** 2 + (pose[2][2]) ** 2)))
                    pitch = math.degrees(math.atan(pose[2][1] / pose[2][2]))
                    position['roll'] = roll - 90
                    entry=[format(float(time.time()),'.4f'),format(float(new_coord[0]),'.4f'),format(float(new_coord[1]),'.4f'),format(float(new_coord[2]),'.4f'),format(float(roll),'.4f'),format(float(yaw),'.4f'),format(float(pitch),'.4f'),]
                    start_time=time.time()
                    cv2.putText(overlay,"X ="+str(float(new_coord[0]))+"cm",(10,20),cv2.FONT_HERSHEY_PLAIN,1,(255,255,0),1)
                    cv2.putText(overlay,"Y ="+str(float(new_coord[1]))+"cm",(10,50),cv2.FONT_HERSHEY_PLAIN,1,(255,255,0),1)
                    cv2.putText(overlay,"Z ="+str(float(new_coord[2]))+"cm",(10,80),cv2.FONT_HERSHEY_PLAIN,1,(255,255,0),1)
                    cv2.putText(overlay,"ROll ="+str(roll-90)+"cm",(350,20),cv2.FONT_HERSHEY_PLAIN,1,(255,255,0),1)
                    cv2.putText(overlay,"Yaw ="+str(yaw)+"cm",(350,50),cv2.FONT_HERSHEY_PLAIN,1,(255,255,0),1)
                    cv2.putText(overlay,"Pitch ="+str(pitch)+"cm",(350,80),cv2.FONT_HERSHEY_PLAIN,1,(255,255,0),1)
                
                #print(hash(self.bu))
                #self.bu.pri(flag)
                #self.bu.tag=flag


                if(flag==1):
                    self.changePixmap.emit(self.conImg(overlay))
                    #self.changePixmap2.emit(self.conImg2(frame2))
                    with open('data.csv', 'w') as csvFile:
                        row = entry
                        #print("writrfyuiojkc v")
                        writer = csv.writer(csvFile)
                        writer.writerow(row)
                        csvFile.close()

                else: 
                    cv2.putText(overlay,"Tag:"+self.tagId+" not visible!",(20,200),cv2.FONT_HERSHEY_PLAIN,4,(255,255,0),1)
                    self.changePixmap.emit(self.conImg(overlay))
                    #self.changePixmap2.emit(self.conImg2(frame2))
                    with open('data.csv', 'w') as csvFile:
                        row = []
                        writer = csv.writer(csvFile)
                        writer.writerow(row)
                        csvFile.close()

            else:
                img=cv2.imread("nocam.jpg")
                
                self.changePixmap.emit(self.conImg(img)) 

                           


    def conImg(self,img):
        rgbImage = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
        h, w, ch = rgbImage.shape
        bytesPerLine = ch * w
        convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
        p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
        return p

    def conImg2(self,img):
        rgbImage = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
        h, w, ch = rgbImage.shape
        bytesPerLine = ch * w
        convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
        p = convertToQtFormat.scaled(180, 120)
        return p
            

class CvThread2(QThread):
    changePixmap2 = pyqtSignal(QImage)
    startvideo=True
    def Stop(self):
        self.startvideo=False

    def run(self):
        cap2 = cv2.VideoCapture('http://192.168.137.96:80/?action=stream')
        while self.startvideo:
            ret2, frame2 = cap2.read()
            frame2=cv2.flip(frame2,flipCode=0)
            if ret2:
                self.changePixmap2.emit(self.conImg2(frame2))
            else:
                img2=cv2.imread("nocam.jpg")
                self.changePixmap2.emit(self.conImg2(img2))
                    

    def conImg2(self,img):
        rgbImage = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
        h, w, ch = rgbImage.shape
        bytesPerLine = ch * w
        convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
        p = convertToQtFormat.scaled(200, 140)
        return p


class CvCap(QWidget):

    def __init__(self):
        super(CvCap,self).__init__()
        self.label=None
        self.label2=None
        self.tagId=""
        self.event=[]
        self.bu=gi.CvTag()


    def setObjects(self,label,tagId,label2):
        self.label=label
        self.tagId=tagId
        self.label2=label2

    def StartCvThread(self):
        self.th = CvThread(self)
        self.th2 = CvThread2(self)
        self.th.setTerminationEnabled(True)
        self.th2.setTerminationEnabled(True)
        self.th.changePixmap.connect(self.setImage)
        self.th2.changePixmap2.connect(self.setImage2)
        self.th.tagId=self.tagId
        #print(self.tagId)
        self.th.start()
        self.th2.start()
        print('Video Thread Started!')

    def StopCv(self):
        self.th.Stop()
        self.th2.Stop()
        print("Stop")  

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))
        #self.bu.flg(flag)
        #self.bu.eve(entry)

    @pyqtSlot(QImage)
    def setImage2(self, image):
        self.label2.setPixmap(QPixmap.fromImage(image))    
