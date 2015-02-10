"""
Sampling webcam and prepare for QT
"""

import cv2
from PyQt4 import QtGui
import ConfigParser
import os
import CaptureWindow as cw

class VideoSampling():

    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read("config.ini")
        self.capture = cv2.VideoCapture(int(self.config.get("Cam", "id")))
        self.capture.set(3, float(self.config.get("Cam", "heigth")))
        self.capture.set(4, float(self.config.get("Cam", "weigth")))
        currentDir = os.getcwd()
        self.faceDir = currentDir + self.config.get("Paths", "faceDir")
        self.gestureDir = currentDir + self.config.get("Paths", "gestureDir")
 
    def captureNextFrame(self):
        """ capture frame and reverse RBG BGR and return opencv image """
        ret, readFrame = self.capture.read()
        if ret == True:
            self.currentFrame = cv2.cvtColor(readFrame, cv2.COLOR_BGR2RGB)
 
    def convertFrame(self):
        """ converts frame for QtGui """
        height, width = self.currentFrame.shape[:2]
        image = QtGui.QImage(self.currentFrame, width, height, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(image)   
        return pixmap

    def saveFrame(self, userId, imgType):
        """ write frame to disk """
        imgPath = ""
        if imgType == cw.CaptureWindow.FACE_TYPE:
            if not os.path.isdir(self.faceDir):  
                os.mkdir(self.faceDir)
            imgPath = self.faceDir + "/" + imgType + "_" + userId
        elif imgType == cw.CaptureWindow.GESTURE_TYPE:
            if not os.path.isdir(self.gestureDir): 
                os.mkdir(self.gestureDir)
            imgPath = self.gestureDir + "/" + imgType + "_" + userId
        cv2.imwrite(imgPath + "." + self.config.get("Cam", "imgExtension"), cv2.cvtColor(self.currentFrame, cv2.COLOR_RGB2GRAY))
