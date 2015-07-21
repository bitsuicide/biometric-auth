# -*- coding: utf-8 -*-
from collections import Counter
import math
import numpy as np
import cv2
import ConfigParser
from PIL import Image


class Recognition():
    EIGEN_MODEL = "eigen"
    FISHER_MODEL = "fisher"
    LBPH_MODEL = "lbph"
    TOTAL_MATCHES = 3
    MAX_MATCH_ELEM = 9

    def __init__(self, recognition, modelType=None, threshold=None):
        """ Create a FaceRecognizer and train it on the given images """
        self._recognition = recognition
        self.config = ConfigParser.ConfigParser()
        self.config.read("config.ini")
        if threshold is None:
            self.threshold = int(self.config.get("Alg Parameters",
                                                 "threshold"))
        else:
            self.threshold = threshold
        if self._recognition:
            if modelType is None:
                modelType = self.config.get("Alg Parameters",
                                            "recognitionModel")
            if modelType == self.EIGEN_MODEL:
                self.model = cv2.createEigenFaceRecognizer()
            elif modelType == self.FISHER_MODEL:
                self.model = cv2.createFisherFaceRecognizer()
            elif modelType == self.LBPH_MODEL:
                self.model = cv2.createLBPHFaceRecognizer()

            print "Inizializing face recognizer model: " + modelType + "..."

            self.model, self.nameList = self.trainModel(self.model)
            self._matchCounter = Counter()  # captured subjects or unknowns
            self._bestUsersMatch = Counter()
            self._totalMatches = 0
            self._countMatchElem = 0
            self.frameFaceCounter = 0

    def checkFrame(self, frame):
        """ Check face in current frame """
        # Clone Frame
        copyFrame = frame.copy()
        # Convert Frame to Grey Scale
        copyFrame = cv2.cvtColor(copyFrame, cv2.COLOR_BGR2GRAY)
        # Detect face in frame
        faceImg, detection, x, y, h, w = self.detectFace(copyFrame)
        if detection and self._recognition:
            self.frameFaceCounter += 1
            # Crop Image
            faceImg = cv2.resize(faceImg, (92, 112))
            # Prediction
            [pLabel, pConfidence] = self.model.predict(np.asarray(faceImg))
            if pConfidence < self.threshold:  # known user
                # print "Known user"
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                label = self.nameList[pLabel].rstrip("\n")
                cv2.putText(frame, label, (x, y), cv2.FONT_HERSHEY_COMPLEX,
                            1, (0, 255, 0))
                self._addUserToMatchList(label)
            else:  # unknown user
                # print "Unknown user"
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                self._addUserToMatchList("unknown")
        return frame

    def readImages(self, path):
        """ Reads the images in a given folder.
        Returns:
        A list [imgList, labelList, nameList]
        imgList: The images, which is a Python list of numpy arrays.
        labelList: The corresponding labels
                   (the unique number of the subject, person) in a Python list.
        nameList: Names of people
        """
        imgList, labelList, nameList = [], [], []
        faces = open(path + self.config.get("Alg Parameters", "indexFile"))
        count = 0
        for line in faces:
            data = line.split(";")
            img = cv2.imread(data[0], cv2.IMREAD_GRAYSCALE)
            imgList.append(np.asarray(img, dtype=np.uint8))
            labelList.append(count)
            nameList.append(data[1])
            count = count + 1
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
        faceClassifier = cv2.CascadeClassifier(
            "/usr/local/share/OpenCV/haarcascades/"
            "haarcascade_frontalface_alt.xml")

        faces = faceClassifier.detectMultiScale(img, 1.3, 4)
        if len(faces) != 0:
            # print "Detected face..."
            max_height = 0
            for (x, y, w, h) in faces:
                if h > max_height:
                    max_height = h
                    x1 = x
                    y1 = y
                    w1 = w
                    h1 = h
            y1 = int(y1)
            x1 = int(x1 + 0.20 * w)
            h1 = int(h1)
            w1 = int(w1 * 0.80)
            faceImg = img[y1:y1+h1, x1:x1+w1]
            if y1 < 0 or x1 < 0:
                return [0, 0, 0, 0, 0, 0]
            if y1 > 480 and x1 > 640:
                return [0, 0, 0, 0, 0, 0]
            return [faceImg, 1, x1, y1, h1, w1]
        else:
            return [0, 0, 0, 0, 0, 0]

    def getBestUser(self):
        """ Return best user matching or None if empty """
        if self._bestUsersMatch:
            return max(self._bestUsersMatch, key=self._bestUsersMatch.get)

    def _addUserToMatchList(self, label):
        if self._countMatchElem == self.MAX_MATCH_ELEM:
            most_common = max(self._matchCounter, key=self._matchCounter.get)
            self._totalMatches += 1
            self._bestUsersMatch[most_common] += 1
            self._matchCounter.clear()
            self._countMatchElem = 0

        else:
            self._matchCounter[label] += 1
            self._countMatchElem += 1

    def distance(self, p1, p2):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        return math.sqrt(dx * dx + dy * dy)

    def scaleRotateTranslate(self, image, angle, center=None, new_center=None,
                             scale=None, resample=Image.BICUBIC):
        if (scale is None) and (center is None):
            return image.rotate(angle=angle, resample=resample)
        nx, ny = x, y = center
        sx = sy = 1.0
        if new_center:
            (nx, ny) = new_center
        if scale:
            (sx, sy) = (scale, scale)
        cosine = math.cos(angle)
        sine = math.sin(angle)
        a = cosine / sx
        b = sine / sx
        c = x - nx * a - ny * b
        d = -sine / sy
        e = cosine / sy
        f = y - nx * d - ny * e
        return image.transform(
            image.size, Image.AFFINE, (a, b, c, d, e, f), resample=resample)

    def cropFace(self, image, eye_left=(0, 0), eye_right=(0, 0),
                 offset_pct=(0.25, 0.25), dest_sz=(92, 112)):
        # calculate offsets in original image
        offset_h = math.floor(float(offset_pct[0]) * dest_sz[0])
        offset_v = math.floor(float(offset_pct[1]) * dest_sz[1])
        # get the direction
        eye_direction = (
            eye_right[0] - eye_left[0], eye_right[1] - eye_left[1])
        # calc rotation angle in radians
        rotation = -math.atan2(
            float(eye_direction[1]), float(eye_direction[0]))
        # distance between them
        dist = self.distance(eye_left, eye_right)
        # calculate the reference eye-width
        reference = dest_sz[0] - 2.0 * offset_h
        # scale factor
        scale = float(dist) / float(reference)
        # rotate original around the left eye
        image = self.scaleRotateTranslate(
            image, center=eye_left, angle=rotation)
        # crop the rotated image
        crop_xy = (
            eye_left[0] - scale * offset_h, eye_left[1] - scale * offset_v)
        crop_size = (dest_sz[0] * scale, dest_sz[1] * scale)
        image = image.crop((int(crop_xy[0]), int(crop_xy[1]), int(
            crop_xy[0] + crop_size[0]), int(crop_xy[1] + crop_size[1])))
        # resize it
        # image = image.resize(dest_sz, Image.ANTIALIAS)
        return np.array(image)

    # def positionEyes(self, pathImage):
    #     imcolor = cv2.cv.LoadImage(pathImage)  # input image
    #     loading the classifiers
    def positionEyes(self, image):
        haarEyes = cv2.cv.Load(
            '/usr/local/share/OpenCV/haarcascades/haarcascade_eye.xml')
        # running the classifiers
        storage = cv2.cv.CreateMemStorage()

        detectedEyes = cv2.cv.HaarDetectObjects(
            image, haarEyes, storage, 1.3, 3)
        eyes = []

        # draw a purple rectangle where the eye is detected
        if detectedEyes:
            for face in detectedEyes:
                p1 = face[0][0], face[0][1]
                p2 = face[0][0] + face[0][2], face[0][1] + face[0][3]
                eye_x = (p2[0] - p1[0]) / 2 + p1[0]
                eye_y = (p2[1] - p1[1]) / 2 + p1[1]
                eyes.append((eye_x, eye_y))

        return eyes

    def getCroppedImageByEyes(self, image):
        eye = self.positionEyes(cv2.cv.fromarray(image))
        if len(eye) >= 2:
            return self.cropFace(Image.fromarray(image), eye[0], eye[1]), True
        return None, False
