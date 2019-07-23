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
from aptag import apr
import aptag
import requests

def sendToServer(encodedKey):
    """
    Sends data to Pi using socket
    :param encodedKey:
    """
    global value
    #global s
    host = '192.168.43.187'
    port = 1040
    buffer_size = 1024
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(30)
    
    try:
        s.connect((host, port))
    except socket.error:
        print("Caught exception: " + socket.error)
        aptag.logger.critical("Unable to connect with the server !")
        aptag.logger.warning("Exiting test mode \n")
        sys.exit()

    s.send(str(encodedKey).encode())
    data = s.recv(buffer_size)
    value = data.decode()
    s.close()
    



def compareCoordinates(entry):
    """
    Compares current coordinate with the dataset and returns the steer angle
    :param entry:
    :return:
    """
    start=0
    end=0
    df = pd.read_csv('spider.csv', names=["Time", "X", "Y", "Z", "Roll", "Yaw", "Pitch", "steerAngle", "angle"])
    if(float(entry[3])>230):
        start=0
        end=20
    elif(float(entry[3])>220):
        start=20
        end=62
    elif(float(entry[3])>210):
        start=62
        end=111
    elif(float(entry[3])>200):
        start=111
        end=143
    else:
        start=143
        end=158
    distance = 100000
    steerAngle = 0
    index = 0
    global value
    print(entry)
    

    for i in range(start,end):
        dist = math.sqrt((float(df['X'][i]) - float(entry[1])) ** 2 + (float(df['Y'][i]) - float(entry[2])) ** 2 + (
                float(df['Z'][i]) - float(entry[3])) ** 2)

        if dist < distance:
            index = i
            distance = dist
            steerAngle = str(df["angle"][i])

    #with open('test.csv', 'a') as csvFile:
    #    entry.append([index, df['X'][index], df['Y'][index], df['Z'][index], df["Roll"][index], df["Yaw"][index],
    #                df["Pitch"][index], df["steerAngle"][index], df["angle"][index]])
    #    writer = csv.writer(csvFile)
    #    writer.writerow(entry)
    #    value=float(value)
    #    liveCoord = {'Time': str(time.ctime(int(time.time()))), 'X':format(float(row[1]), '.4f'), 'Y': format(float(row[2]), '.4f'), 'Z': format(float(row[3]), '.4f'), 'Roll': format(float(row[4]), '.4f'), 'Yaw':format(float(row[5]), '.4f') , 'Pitch': format(float(row[6]), '.4f'),'Speed':format(float(value),'.4f')}
    #   requests.post(url, json=liveCoord)
    #csvFile.close()
    return steerAngle


def autoControl():
    """
    Gets the steer angle and sends the data to pi using socket
    """
    start_time=time.time()
    while True:
        #start_time = time.time()

        if((time.time() - start_time)>0.25):
            steerAngle = compareCoordinates(queue.get())
            print(steerAngle)
            sendToServer(steerAngle)
            start_time=time.time()

            if steerAngle == 0:
                print("Forward")
            elif steerAngle == 1:\
                print("Backward")
            elif steerAngle == 2:
                print("Reset")
            elif steerAngle == 3:
                print("Stop")
            elif steerAngle == 4:
                print("Program Terminated")
                aptag.logger.warning("Exiting test mode \n")
            else:
                print("Steer")


def main():
    print("Connecting to Arduino")
    time.sleep(3)
    print("Arduino connected")
    print("Enter the movement")

    autoControl()


if __name__ == '__main__':
    aptag.logger.warning("Inside test Mode /n")
    global queue
    global value
    #global s
    host = '192.168.43.187'
    port = 1040
    buffer_size = 1024
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send('6'.encode())
    data = s.recv(buffer_size)
    value =0.0
    queue = Queue()
    process = Process(target=apr, args=(queue,))
    process.start()
    main()
