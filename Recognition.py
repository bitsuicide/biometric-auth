# -*- coding: utf-8 -*-
import numpy as np
import cv2
import os
import sys
import ConfigParser

class Recognition():

    def __init__(self):
        """ Create a FaceRecognizer and train it on the given images """
        self.config = ConfigParser.ConfigParser()
        self.config.read("config.ini")
        self.model = cv2.createEigenFaceRecognizer()
        self.model, self.nameList = self.trainModel(self.model)

    def checkFrame(self, frame):
        """ Check face in current frame """
        # Clone Frame
        copyFrame = frame.copy()
        # Convert Frame to Grey Scale
        copyFrame = cv2.cvtColor(copyFrame, cv2.COLOR_BGR2GRAY)
        # Detect face in frame
        faceImg, detection, x, y, h, w = self.detectFace(copyFrame)
        if detection:
            # Crop Image
            faceImg = cv2.resize(faceImg, (92 ,112))
            # Prediction
            [pLabel, pConfidence] = self.model.predict(np.asarray(faceImg))
            threshhold = int(self.config.get("Alg Parameters", "threshhold"))
            if pConfidence < threshhold:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, self.nameList[pLabel].rstrip("\n"), (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))
                print "Known"
                return frame
            else:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                print "Unknown"
                return frame
        else:
            return frame

    def readImages(self, path):
        """ Reads the images in a given folder.
        Returns:
        A list [imgList, labelList, nameList]
        imgList: The images, which is a Python list of numpy arrays.
        labelList: The corresponding labels (the unique number of the subject, person) in a Python list.
        nameList: Names of people
        """
        c = 0
        imgList, labelList, nameList = [], [], [] 
         
        faces = open(path + self.config.get("Alg Parameters", "indexFile"))
        count = 0
        for line in faces:
            data = line.split(";")
            img = cv2.imread(data[0], cv2.IMREAD_GRAYSCALE)
            imgList.append(np.asarray(img, dtype = np.uint8))
            labelList.append(count)
            nameList.append(data[1])
            count = count + 1
        total = count
        faces.close()
        return imgList, labelList, nameList

    def trainModel(self, model):
        """ Train model with faces """
        imgList, labelList, nameList = self.readImages("pradeep_collection/")
        model.train(np.asarray(imgList), np.asarray(labelList))
        print("Training Finished")
        return model, nameList

    def detectFace(self, img):
        """ Detect face on Frame.
        Returns:
        faceImg - image of detected face 
        detection
        x, y, h, w cordinate 
        """ 
        faceClassifier = cv2.CascadeClassifier("/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml")
           
        faces = faceClassifier.detectMultiScale(img, 1.3, 5)
        if len(faces) != 0:
            print "Detected face..."
            max = 0
            for (x, y, w, h) in faces:
                if h > max:
                    max = h
                    x1 = x
                    y1 = y
                    w1 = w
                    h1 = h        
            y1 = int(y1 - 0.1 * h)
            x1 = int(x1 - 0.1 * w)
            h1 = int(1.2 * h1)
            w1 = int(1.2 * w1)
            faceImg = img[y1:y1+h1, x1:x1+w1]
            if y1 < 0 or x1 < 0:
                return [0, 0, 0, 0, 0, 0]
            if y1 > 480 and x1 > 640:
                return [0, 0, 0, 0, 0, 0]
            return [faceImg, 1, x1, y1, h1, w1]
        else:
            return [0, 0, 0, 0, 0, 0]
