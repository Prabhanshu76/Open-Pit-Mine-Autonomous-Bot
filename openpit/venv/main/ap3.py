import math
from argparse import ArgumentParser
import time
import cv2
import numpy
import json
import apriltag
import csv
import socket
import pickle
host = '192.168.137.235'
port = 1034
buffer_size = 1024
start_time=time.time()

# for some reason pylint complains about members being undefine429.02356763d :(
# pylint: disable=E1101
#camera_params = (834.65688267, 832.75807601, 244.3682, 318.55439201) 
#(648.329284815438, 665.1984893547117, 297.3558498244366, 241.85205324200447)
camera_params =(816.5348873614328, 818.5099487197449, 309.06679467676815, 233.04620465593146)
#camera_params=(
size = 5.6
#32
position = {'tag0': None, 'roll': None ,'time':None}
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('up1.mp4',fourcc, 20.0, (640,480))
def tagDetect():
    global position
    '''Main function.'''

    parser = ArgumentParser(
        description='test apriltag Python bindings')

    parser.add_argument('device_or_movie', metavar='INPUT', nargs='?', default=0,
                        help='Movie to load or integer ID of camera device')

    apriltag.add_arguments(parser)

    options = parser.parse_args()

    cap = cv2.VideoCapture(0)

    cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)

    window = 'Camera'
    cv2.namedWindow(window)

    # set up a reasonable search path for the apriltag DLL inside the
    # github repo this file lives in;
    #
    # for "real" deployments, either install the DLL in the appropriate
    # system-wide library directory, or specify your own search paths
    # as needed.
    start_time=time.time()
    detector = apriltag.Detector(options,
                                  searchpath=apriltag._get_demo_searchpath())

    while True:
        success, frame = cap.read()
        if not success:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        # gray = clahe.apply(gray)
        detections, dimg = detector.detect(gray, return_image=True)

        num_detections = len(detections)
        # print('Detected {} tags.\n'.format(num_detections))
        overlay = frame // 2 + dimg[:, :, None] // 2
        for i, detection in enumerate(detections):
            pose, e0, e1 = detector.detection_pose(detection,
                                                   camera_params,
                                                   size)

            apriltag._draw_pose(overlay,
                                 camera_params,
                                 size,
                                 pose)

            if num_detections > 0:
             
                b = numpy.matrix([[0], [0], [0], [1]])
                coordinate = numpy.matmul(pose, b)
                #
                # print('Detection {} of {}:'.format(i + 1, num_detections))
                # print()
                #print('x', coordinate[0], 'y', coordinate[1], 'z', coordinate[2])
                # print()
                #new_coord = transformRx(56, coordinate)
                new_coord=coordinate
                position['tag0'] = new_coord
                print('x', new_coord[0], 'y', new_coord[1], 'z', new_coord[2])
                print()
                #print(90-math.degrees(math.acos(new_coord[0]/new_coord[2])))
                roll = math.degrees(math.atan2(pose[0][1] , pose[0][0]))
                yaw = math.degrees(math.atan((-1 * pose[2][0]) / math.sqrt((pose[2][1]) ** 2 + (pose[2][2]) ** 2)))
                pitch = math.degrees(math.atan(pose[2][1] / pose[2][2]))
                position['roll'] = roll - 90
                #position['time'] = rospy.Time.now()
                print('Roll ', roll)
                print('Yaw ', yaw)
                print('Pitch ', pitch)
                print()

                
                if((time.time()-start_time)>0.5):
                    with open('final.csv', 'a') as csvFile:
                        row = [format(time.time()-start_time,'.4f'),format(float(new_coord[0]),'.4f'),format(float(new_coord[1]),'.4f'),format(float(new_coord[2]),'.4f'),format(roll,'.4f'),format(yaw,'.4f'),format(pitch,'.4f')]
                        
                        
                        writer = csv.writer(csvFile)
                        writer.writerow(row)
                    
                    csvFile.close()
                    start_time=time.time()
                cv2.putText(overlay,"X ="+str(float(new_coord[0]))+"cm",(10,20),cv2.FONT_HERSHEY_PLAIN,1,(255,255,0),1)
                cv2.putText(overlay,"Y ="+str(float(new_coord[1]))+"cm",(10,50),cv2.FONT_HERSHEY_PLAIN,1,(255,255,0),1)
                cv2.putText(overlay,"Z ="+str(float(new_coord[2]))+"cm",(10,80),cv2.FONT_HERSHEY_PLAIN,1,(255,255,0),1)
                cv2.putText(overlay,"ROll ="+str(roll-90)+"cm",(350,20),cv2.FONT_HERSHEY_PLAIN,1,(255,255,0),1)
                cv2.putText(overlay,"Yaw ="+str(yaw)+"cm",(350,50),cv2.FONT_HERSHEY_PLAIN,1,(255,255,0),1)
                cv2.putText(overlay,"Pitch ="+str(pitch)+"cm",(350,80),cv2.FONT_HERSHEY_PLAIN,1,(255,255,0),1)   
        cv2.imshow(window, overlay)
        out.write(overlay)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        

def transformRx(deg, cood):
    # print(cood)

    Rx = numpy.matrix(
        [[1, 0, 0, 0], [0, math.cos(deg), -math.sin(deg), 0], [0, math.sin(deg), math.cos(deg), 0], [0, 0, 0, 1]])
    # print(Rx)
    # coll=numpy.transpose(cood)
    return numpy.matmul(Rx, cood)


tagDetect()
