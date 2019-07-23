"""Demonstrate Python wrapper of C apriltag library by running on camera frames."""

import math
from argparse import ArgumentParser
import time
import cv2
import numpy
import json
import apriltag
from multiprocessing import Process, Pipe
import logging
import sys
import requests


logging.basicConfig(filename='Drive.log',
                    format='%(levelname)s -- %(asctime)s:  %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)

logger = logging.getLogger()
cameraPort = 0
def cameraTest():
    global cameraPort
    while(cameraPort != 3):

        try:
            cap = cv2.VideoCapture(cameraPort)
            cap.set(cv2.CAP_PROP_AUTOFOCUS, cameraPort)
            ret,img=cap.read()
            img.shape
            break
        except :
            cameraPort = cameraPort +1
            #print(type(img))
    if(cameraPort == 3):
        logger.critical("Camera not Detected !")
        sys.exit()
    return cap

def apr(queue):
    """
    Function to detect any apriltag in vision and to find the position of it .
    :param queue:
    """
    # Camera Parameters for the particular camera used computed using calibrate_camera.py
    url = 'http://127.0.0.1:5000/postjson'
    camera_params = (816.5348873614328, 818.5099487197449, 309.06679467676815, 233.04620465593146)
    size = 8.3  # Size of aprilTag
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('up123.mp4', fourcc, 15.0, (640, 480))
    position = {'tag0': None, 'roll': None, 'time': None}
    '''Main function.'''

    parser = ArgumentParser(
        description='test apriltag Python bindings')

    parser.add_argument('device_or_movie', metavar='INPUT', nargs='?', default=0,
                        help='Movie to load or integer ID of camera device')

    apriltag.add_arguments(parser)
    options = parser.parse_args()
    cap = cameraTest()
    window = 'Camera'
    cv2.namedWindow(window)
    start_time = time.time()
    detector = apriltag.Detector(options,
                                 searchpath=apriltag._get_demo_searchpath())

    while True:
        success, frame = cap.read()
        if not success:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        detections, dimg ,tag_id= detector.detect(gray, return_image=True)

        num_detections = len(detections)
        overlay = frame // 2 + dimg[:, :, None] // 2
        if num_detections > 0:
            #print(tag_id)
            for i, detection in enumerate(detections):
                pose, e0, e1 = detector.detection_pose(detection,
                                                       camera_params,
                                                       size)

                apriltag._draw_pose(overlay,
                                    camera_params,
                                    size,
                                    pose)



            b = numpy.matrix([[0], [0], [0], [1]])
            coordinate = numpy.matmul(pose, b)
            new_coord = coordinate
            position['tag0'] = new_coord
            roll = math.degrees(math.atan2(pose[0][1], pose[0][0]))
            yaw = math.degrees(math.atan((-1 * pose[2][0]) / math.sqrt((pose[2][1]) ** 2 + (pose[2][2]) ** 2)))
            pitch = math.degrees(math.atan(pose[2][1] / pose[2][2]))
            position['roll'] = roll - 90

            entry = [format(time.time() - start_time, '.4f'), format(float(new_coord[0]), '.4f'),
                             format(float(new_coord[1]), '.4f'), format(float(new_coord[2]), '.4f'), format(roll, '.4f'),
                             format(yaw, '.4f'), format(pitch, '.4f')]

            cv2.putText(overlay, "X =" + str(float(new_coord[0])) + "cm", (10, 20), cv2.FONT_HERSHEY_PLAIN, 1,
                                (255, 255, 0), 1)
            cv2.putText(overlay, "Y =" + str(float(new_coord[1])) + "cm", (10, 50), cv2.FONT_HERSHEY_PLAIN, 1,
                                (255, 255, 0), 1)
            cv2.putText(overlay, "Z =" + str(float(new_coord[2])) + "cm", (10, 80), cv2.FONT_HERSHEY_PLAIN, 1,
                                (255, 255, 0), 1)
            cv2.putText(overlay, "ROll =" + str(roll) + "cm", (350, 20), cv2.FONT_HERSHEY_PLAIN, 1,
                                (255, 255, 0), 1)
            cv2.putText(overlay, "Yaw =" + str(yaw) + "cm", (350, 50), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0), 1)
            cv2.putText(overlay, "Pitch =" + str(pitch) + "cm", (350, 80), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0),
                                1)
            logger.info("\n X -> {0:.4f} \n Y -> {1:.4f} \n Z -> {2:.4f} \n Roll -> {3:.4f} \n Yaw -> {4:.4f} \n Pitch -> {5:.4f} \n".format(float(new_coord[0]),
                                                                                                             float(new_coord[1]),
                                                                                                             float(new_coord[2]),
                                                                                                             float(roll), float(yaw),
                                                                                                             float(pitch)))
            #liveCoord = {'Time': str(time.ctime(int(time.time()))), 'X':format(float(new_coord[0]), '.4f'), 'Y': format(float(new_coord[1]), '.4f'), 'Z': format(float(new_coord[2]), '.4f'), 'Roll': format(float(roll), '.4f'), 'Yaw':format(float(yaw), '.4f') , 'Pitch': format(float(pitch), '.4f')}
            #requests.post(url, json=liveCoord)
            while not queue.empty():
                queue.get()
            queue.put(entry)

        else:
            logger.critical('No tag Detected')

        cv2.imshow(window, overlay)
        out.write(overlay)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            logger.warning("Camera Exited")
            break
