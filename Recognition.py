# -*- coding: utf-8 -*-
import numpy as np
import cv2
import sys
import ConfigParser

class Recognition():
    EIGEN_MODEL = "eigen"
    FISHER_MODEL = "fisher"
    LBPH_MODEL = "lbph"
    MAX_MATCH_ELEM = 25

    def __init__(self, recognition):
        """ Create a FaceRecognizer and train it on the given images """
        self.config = ConfigParser.ConfigParser()
        self.config.read("config.ini")

        if recognition:
            modelType = self.config.get("Alg Parameters", "recognitionModel")
            if modelType == self.EIGEN_MODEL:
                self.model = cv2.createEigenFaceRecognizer()
            elif modelType == self.FISHER_MODEL:
                self.model = cv2.createFisherFaceRecognizer()
            elif modelType == self.LBPH_MODEL:
                self.model = cv2.createLBPHFaceRecognizer()

            print "Inizializing face recognizer model: " + modelType + "..."

            self.model = cv2.createLBPHFaceRecognizer()
            self.model, self.nameList = self.trainModel(self.model)
            self._matchList = {} # list of captured subjects or unknowns
            self._maxMatchList = ["unknown", 0]
            self._countMatchElem = 0
            self._bestUsersMatch = []
            self.frameFaceCounter = 0

    def checkFrame(self, frame):
        """ Check face in current frame """
        # Clone Frame
        copyFrame = frame.copy()
        # Convert Frame to Grey Scale
        copyFrame = cv2.cvtColor(copyFrame, cv2.COLOR_BGR2GRAY)
        # Detect face in frame
        faceImg, detection, x, y, h, w = self.detectFace(copyFrame)
        if detection and recognition:
            self.frameFaceCounter += 1
            # Crop Image
            faceImg = cv2.resize(faceImg, (92 ,112))
            # Prediction
            [pLabel, pConfidence] = self.model.predict(np.asarray(faceImg))
            threshhold = int(self.config.get("Alg Parameters", "threshhold"))
            if pConfidence < threshhold: # user known
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                label = self.nameList[pLabel].rstrip("\n")
                cv2.putText(frame, label, (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))
                self._addUserToMatchList(label)
                #print "Known"
                return frame
            else: # user unknown
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                self._addUserToMatchList("unknown")
                #print "Unknown"
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
        imgList, labelList, nameList = self.readImages("face/")
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

    def getBestUser(self):
        """ Return best user matching """
        lenList = len(self._bestUsersMatch)
        if lenList == 0:
            return []
        else: 
            return self._bestUsersMatch[lenList - 1]

    def _addUserToMatchList(self, label):
        if self._countMatchElem == self.MAX_MATCH_ELEM:
            self._bestUsersMatch.append(self._maxMatchList[0])
            self._matchList = {}
            self._maxMatchList = ["unknown", 0]
            self._countMatchElem = 0
        else: 
            if not label in self._matchList:
                self._matchList[label] = 1
            else:
                occorrenza = self._matchList[label] + 1
                self._matchList[label] = occorrenza
                if self._maxMatchList[1] < occorrenza:
                    self._maxMatchList = [label, occorrenza]
                    #print self._maxMatchList
            self._countMatchElem += 1
