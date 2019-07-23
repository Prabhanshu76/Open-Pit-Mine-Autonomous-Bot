import csv
import socket
import sys
import termios
import time
import tty
from multiprocessing import Process, Queue
from tkinter import *
from aptag import apr
import aptag
import requests


def charInput():
    """
    Functon reacts to any keypress
    :return:
    """
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def quit():
    global TkTop
    TkTop.destroy()


def leftMove():
    """
    Function to decrement steer angle by 20 degrees

    """
    global steerAngle

    if steerAngle >= 30:
        steerAngle = steerAngle - 20
    else:
        steerAngle = 10
    print(steerAngle)


def rightMove():
    """
    Function to increment steer angle by 20 degrees

    """
    global steerAngle

    if steerAngle <= 150:
        steerAngle = steerAngle + 20
    else:
        steerAngle = 170
    print(steerAngle)


def sendToServer(encodedKey):
    """
    Sends data to Pi using socket
    :param encodedKey:
    """
    host = '192.168.43.187'
    port = 1040
    buffer_size = 64

    global imu

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.settimeout(3)    
    try:
        s.connect((host, port))
    except socket.timeout :
        print("Caught exception: " + socket.error)
        aptag.logger.critical("Unable to connect with the server !")
        aptag.logger.warning("Exiting training mode \n")
        sys.exit()
    
    s.send(encodedKey)
    data = s.recv(buffer_size)
    imu = data.decode()
    print("speed: "+ imu)
    s.close()
    

def keyControl():
    """
    Records any keypress and maps it with the current apriltag coordinates
    and store them in a csv file
    """
    global currentAngle
    global steerAngle
    global process
    global imu
    url = 'http://127.0.0.1:5000/postjson'
    while True:

        start_time = time.time()
        keyPressed = charInput()

        if keyPressed == 'w':
            if (time.time() - start_time) > 0.001:
                sendToServer(str(0).encode())
                steerAngle = 0
                print("forward")

        elif keyPressed == 's':
            if (time.time() - start_time) > 0.001:
                sendToServer(str(1).encode())
                steerAngle = 1
                print("backward")

        elif keyPressed == 'a':
            if (time.time() - start_time) > 0.001:
                steerAngle = currentAngle
                leftMove()
                currentAngle = steerAngle
                sendToServer(str(steerAngle).encode())
                print("leftMove")

        elif keyPressed == 'd':
            if (time.time() - start_time) > 0.001:
                steerAngle = currentAngle
                rightMove()
                currentAngle = steerAngle
                sendToServer(str(steerAngle).encode())
                print("rightMove")

        elif keyPressed == 'r':
            if (time.time() - start_time) > 0.001:
                sendToServer(str(2).encode())
                steerAngle = 2
                print("reset")

        elif keyPressed == 'z':
            if (time.time() - start_time) > 0.001:
                sendToServer(str(3).encode())
                steerAngle = 3
                print("stop")

        elif keyPressed == 'p':
            sendToServer(str(4).encode())
            print("Program Terminated")
            aptag.logger.warning("Exiting training mode \n")
            break

        with open('spider.csv', 'a') as csvFile:
            row = queue.get()
            row.append(keyPressed)
            row.append(steerAngle)
            print(row)
            #imu=float(imu)
            #liveCoord = {'Time': str(time.ctime(int(time.time()))), 'X':format(float(row[1]), '.4f'), 'Y': format(float(row[2]), '.4f'), 'Z': format(float(row[3]), '.4f'), 'Roll': format(float(row[4]), '.4f'), 'Yaw':format(float(row[5]), '.4f') , 'Pitch': format(float(row[6]), '.4f'),'Speed':format(float(90),'.4f')}
            #requests.post(url, json=liveCoord)            
            writer = csv.writer(csvFile)
            writer.writerow(row)
            csvFile.close()


def main():
    global currentAngle
    global steerAngle

    steerAngle = 90
    currentAngle = 90

    print("Connecting to Arduino")
    time.sleep(3)
    print("Arduino connected")
    print("Enter the movement")

    keyControl()


if __name__ == '__main__':
    aptag.logger.warning("Inside training Mode /n")    
    host = '192.168.43.187'
    port = 1040
    buffer_size = 1024
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send('5'.encode())
    data = s.recv(buffer_size)
    print(data)
    
    global queue
    global process
    global imu
    imu=0.0
    queue = Queue()
    process = Process(target=apr, args=(queue,))
    process.start()
    main()
