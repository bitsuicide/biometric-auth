"""
Sampling webcam and prepare for QT
"""

import cv2
from PyQt4 import QtGui
import ConfigParser
import os
import Recognition as rec
import ReadWriteIndex as rwi


class VideoSampling():

    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read("config.ini")
        self.capture = cv2.VideoCapture(int(self.config.get("Cam", "id")))
        self.capture.set(3, float(self.config.get("Cam", "heigth")))
        self.capture.set(4, float(self.config.get("Cam", "weigth")))
        self.currentDir = os.getcwd()
        self.faceDir = self.config.get("Paths", "faceDir")

    def captureNextFrame(self):
        """ capture frame and reverse RBG BGR and return opencv image """
        ret, readFrame = self.capture.read()
        if ret is True:
            self.currentFrame = cv2.cvtColor(readFrame, cv2.COLOR_BGR2RGB)

    def convertFrame(self):
        """ converts frame for QtGui """
        height, width = self.currentFrame.shape[:2]
        image = QtGui.QImage(
            self.currentFrame, width, height, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(image)
        return pixmap

    def saveFrame(self, userId):
        """ write frame to disk and add row to file config
        Return:
        detection - face is detected
        newUser - created new user
        """
        imgBasePath = ""
        imgBasePath = self.faceDir + "/" + "face_" + userId
        recognition = rec.Recognition(False)
        # faceImg, detection, x, y, h, w = recognition.detectFace(
        #     cv2.cvtColor(self.currentFrame, cv2.COLOR_RGB2GRAY))
        # faceImg2, detection2 = recognition.getCroppedImageByEyes(
        #     cv2.cvtColor(self.currentFrame, cv2.COLOR_RGB2GRAY), (0.2, 0.2))
        #faceImg, detection = recognition.getCroppedImageByEyes(
        faceImg, detection, x, y, h, w = recognition.detectFace(
            cv2.cvtColor(self.currentFrame, cv2.COLOR_RGB2GRAY))

        if detection:
            writer = rwi.ReadWriteIndex()
            faceImg = cv2.resize(faceImg, (92, 112))
            fileExtension = "." + self.config.get("Cam", "imgExtension")
            filePath = (imgBasePath + "#" +
                        str(writer.getCountUserElem(userId)) + fileExtension)
            cv2.imwrite(self.currentDir + filePath, faceImg)
            newUser = writer.checkUser(userId)
            writer.addRow(userId, filePath)  # add new line to file index
            return detection, not newUser

        return detection, 0
