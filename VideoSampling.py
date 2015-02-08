"""
Sampling webcam and prepare for QT
"""

import cv2
from PyQt4 import QtGui

class VideoSampling():

    def __init__(self):
        self.capture = cv2.VideoCapture(0)
        self.capture.set(3, 640)
        self.capture.set(4, 480)
 
    def captureNextFrame(self):
        """ capture frame and reverse RBG BGR and return opencv image """
        ret, readFrame=self.capture.read()
        if ret == True:
            self.currentFrame = cv2.cvtColor(readFrame, cv2.COLOR_BGR2RGB)
 
    def convertFrame(self):
        """ converts frame for QtGui """
        height, width = self.currentFrame.shape[:2]
        image = QtGui.QImage(self.currentFrame, width, height, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(image)   
        return pixmap