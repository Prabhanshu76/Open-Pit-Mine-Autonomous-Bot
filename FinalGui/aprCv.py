import numpy as np
import cv2
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import (QCoreApplication, QObject, QRunnable, QThread,
                          QThreadPool, pyqtSignal, pyqtSlot, Qt)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel
import math
from argparse import ArgumentParser
import time
import cv2
import numpy
import csv
import menuform2 as gi
import apriltag

camera_params = (834.65688267, 832.75807601, 244.3682, 318.55439201)
size = 8.3
position = {'tag0': None, 'roll': None, 'time': None}


class CvThread(QThread):

    changePixmap = pyqtSignal(QImage)
    tagId = ""
    startvideo = True
    entry = []
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('up123.mp4', fourcc, 20.0, (640, 480))

    def stop(self):
        """
        Used to stop QThtead
        """
        self.startvideo = False

    def run(self):
        """
        Function running under QThread used to detect AprilTag and generate its Coordinates
        """
        parser = ArgumentParser(
            description='test apriltag Python bindings')

        parser.add_argument('device_or_movie', metavar='INPUT', nargs='?', default=0,
                            help='Movie to load or integer ID of camera device')

        apriltag.add_arguments(parser)

        options = parser.parse_args()

        cap = cv2.VideoCapture(-1)

        start_time = time.time()
        # entry=[]
        detector = apriltag.Detector(options,
                                     searchpath=apriltag._get_demo_searchpath())
        # print(self.tagId)
        while (self.startvideo):
            ret, frame = cap.read()

            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                detections, dimg, tag_id = detector.detect(gray, return_image=True)
                index = 33
                flag = 0
                if int(self.tagId) in tag_id:
                    index = tag_id.index(int(self.tagId))
                    flag = 1

                overlay = frame // 2
                for i, detection in enumerate(detections):
                    if i != index:
                        continue
                    pose, e0, e1 = detector.detection_pose(detection,
                                                           self.camera_params,
                                                           self.size)

                    apriltag._draw_pose(overlay,
                                        self.camera_params,
                                        self.size,
                                        pose)
                    b = numpy.matrix([[0], [0], [0], [1]])
                    coordinate = numpy.matmul(pose, b)
                    new_coord = coordinate
                    self.position['tag0'] = new_coord
                    roll = math.degrees(math.atan2(pose[0][1], pose[0][0]))
                    yaw = math.degrees(math.atan((-1 * pose[2][0]) / math.sqrt((pose[2][1]) ** 2 + (pose[2][2]) ** 2)))
                    pitch = math.degrees(math.atan(pose[2][1] / pose[2][2]))
                    self.position['roll'] = roll - 90
                    entry = [format(float(time.time()), '.4f'), format(float(new_coord[0]), '.4f'),
                             format(float(new_coord[1]), '.4f'), format(float(new_coord[2]), '.4f'),
                             format(float(roll), '.4f'), format(float(yaw), '.4f'), format(float(pitch), '.4f'), ]
                    cv2.putText(overlay, "X =" + str(float(new_coord[0])) + "cm", (10, 20), cv2.FONT_HERSHEY_PLAIN, 1,
                                (255, 255, 0), 1)
                    cv2.putText(overlay, "Y =" + str(float(new_coord[1])) + "cm", (10, 50), cv2.FONT_HERSHEY_PLAIN, 1,
                                (255, 255, 0), 1)
                    cv2.putText(overlay, "Z =" + str(float(new_coord[2])) + "cm", (10, 80), cv2.FONT_HERSHEY_PLAIN, 1,
                                (255, 255, 0), 1)
                    cv2.putText(overlay, "ROll =" + str(roll - 90) + "cm", (350, 20), cv2.FONT_HERSHEY_PLAIN, 1,
                                (255, 255, 0), 1)
                    cv2.putText(overlay, "Yaw =" + str(yaw) + "cm", (350, 50), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0),
                                1)
                    cv2.putText(overlay, "Pitch =" + str(pitch) + "cm", (350, 80), cv2.FONT_HERSHEY_PLAIN, 1,
                                (255, 255, 0), 1)

                if flag == 1:
                    self.changePixmap.emit(self.con_img(overlay))
                    self.out.write(overlay)
                    with open('data.csv', 'w') as csvFile:
                        row = entry
                        # print("writrfyuiojkc v")
                        writer = csv.writer(csvFile)
                        writer.writerow(row)
                        csvFile.close()

                else:
                    cv2.putText(overlay, "Tag:" + self.tagId + " not visible!", (20, 200), cv2.FONT_HERSHEY_PLAIN, 4,
                                (255, 255, 0), 1)
                    self.changePixmap.emit(self.con_img(overlay))
                    with open('data.csv', 'w') as csvFile:
                        row = []
                        writer = csv.writer(csvFile)
                        writer.writerow(row)
                        csvFile.close()

            else:
                img = cv2.imread("nocam.jpg")
                self.changePixmap.emit(self.con_img(img))

    def con_img(self, img):
        """
        Convert captured frame to QImage to view it on QLabel(Passed from cvwindow.py)
        """
        rgbImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgbImage.shape
        bytesPerLine = ch * w
        convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
        p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
        return p


class CvCap(QWidget):

    def __init__(self):
        super(CvCap, self).__init__()
        self.label = None
        self.tagId = ""
        self.event = []
        self.bu = gi.CvTag()

    def set_objects(self, label, tagId):
        self.label = label
        self.tagId = tagId

    def start_cv_thread(self):
        self.th = CvThread(self)
        self.th.setTerminationEnabled(True)
        self.th.changePixmap.connect(self.set_image)
        self.th.tagId = self.tagId
        # print(self.tagId)
        self.th.start()
        print('Video Thread Started!')

    def stop_cv(self):
        self.th.stop()
        print("Stop")

    @pyqtSlot(QImage)
    def set_image(self, image):
        """
        Set Frames on Qlable passed from cvwindow.py
        """
        self.label.setPixmap(QPixmap.fromImage(image))
