import csv
import math
import socket
import sys
import termios
import time
import tty
from multiprocessing import Process, Queue
from tkinter import *
import pandas as pd
import threading
from threading import *
from PyQt5.QtCore import QThread
#from aptag import apr
#import aptag
#import requests
global value
value =0.0
global currentAngle
currentAngle=90
#apr.logger.warning("Inside test Mode /n")
    
class Autonomous():
 def __init__(self):
    #super(Autonomous, self).__init__()
    global value
    self.startt=True
    value =0.0
    self.th = threading.Thread(target=self.autoControl)
           
 def sendToServer(self,encodedKey):
    """
    Sends data to Pi using socket
    :param encodedKey:
    """
    global value
    host = '192.168.43.187'
    port = 1040
    buffer_size = 1024


    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    try:
        s.connect((host, port))
    except socket.error:
        print("Caught exception: " + socket.error)
        #aptag.logger.critical("Unable to connect with the server !")
        #aptag.logger.warning("Exiting test mode \n")
        sys.exit()

    s.send(str(encodedKey).encode())
    data = s.recv(buffer_size)
    value = data.decode()    
    s.close()



 def compareCoordinates(self):
    """
    Compares current coordinate with the dataset and returns the steer angle
    :param entry:
    :return:
    """
    global currentAngle
    global value
    start=0
    end=0
    try:
        df1 = pd.read_csv('data.csv', names=["Time", "X", "Y", "Z", "Roll", "Yaw", "Pitch"])
        entry=[df1['Time'][0],df1['X'][0],df1['Y'][0],df1['Z'][0],df1['Roll'][0],df1['Yaw'][0],df1['Pitch'][0]]
        #print(entry)

        #print(df1)
        df = pd.read_csv('trainData2.csv', names=["Time", "X", "Y", "Z", "Roll", "Yaw", "Pitch", "angle"])
        
        if(float(entry[3]>float(df['Z'][len(df)//4]))):
            start=0
            end=len(df)//4
        elif(float(entry[3]>float(df['Z'][2*len(df)//4]))): 
            start=len(df)//4
            end=2*len(df)//4
        elif(float(entry[3]>float(df['Z'][3*len(df)//4]))): 
            start=2*len(df)//4
            end=3*len(df)//4
        else:
            start=3*len(df)//4
            end=len(df)-1  
                   
        distance = 100000
        steerAngle = 0
        index = 0

        #print(entry)

        for i in range(start,end):
            dist = math.sqrt((float(df['X'][i]) - float(entry[1])) ** 2 + (float(df['Y'][i]) - float(entry[2])) ** 2 + (
                    float(df['Z'][i]) - float(entry[3])) ** 2)

            if dist < distance and float(entry[3])<float(df['Z'][i]):
                index = i
                distance = dist
                steerAngle = str(df["angle"][i])

        print("Start",start,"end",end,"index",index,"steerAngle",steerAngle,"Current Z",entry[3],"Stored Z",df['Z'][index])        
        with open('test.csv', 'a') as csvFile:
            entry.append([index, df['X'][index], df['Y'][index], df['Z'][index], df["Roll"][index], df["Yaw"][index],
                        df["Pitch"][index], df["angle"][index]])
            writer = csv.writer(csvFile)
            writer.writerow(entry)
            #value=float(value)
            #liveCoord = {'Time': str(time.ctime(int(time.time()))), 'X':format(float(row[1]), '.4f'), 'Y': format(float(row[2]), '.4f'), 'Z': format(float(row[3]), '.4f'), 'Roll': format(float(row[4]), '.4f'), 'Yaw':format(float(row[5]), '.4f') , 'Pitch': format(float(row[6]), '.4f'),'Speed':format(float(value),'.4f')}
            #requests.post(url, json=liveCoord)
        csvFile.close()
        return steerAngle
    except Exception as e:
        print("File Empty",str(e))
        return currentAngle
 def StartAuc(self):
    
    self.th.start()

 def StopAuc(self):
    print("STOP12345678907654321`234576890765432413`11234567890")
    
    #self.th._Thread_stop()
    self.startt=False 
       

 def autoControl(self):
    global currentAngle
    print("Connecting to Arduino")
    #time.sleep(3)
    print("Arduino connected")
    print("Enter the movement")
    """
    Gets the steer angle and sends the data to pi using socket
    """
    while self.startt:
        start_time = time.time()
        steerAngle = self.compareCoordinates()
        print(steerAngle)
        steerAngle=int(steerAngle)
        currentAngle=steerAngle
        self.sendToServer(currentAngle)
        #print(time.time() - start_time)
        if steerAngle == 0:
            print("Forward")
        elif steerAngle == 1:
            print("Backward")
        elif steerAngle == 2:
            print("Reset")
        elif steerAngle == 3:
            print("Stop")
        elif steerAngle == 4:
            print("Program Terminated")
            #aptag.logger.warning("Exiting test mode \n")

        else:
            print("Steer")


 
