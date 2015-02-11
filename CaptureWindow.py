from PyQt4 import QtGui, QtCore
import VideoSampling as vs
import time

class CaptureWindow(QtGui.QMainWindow):
    GESTURE_TYPE = "gesture"
    FACE_TYPE = "face"
    WAIT_TIME = 1

    def __init__(self, userId, captureType, title, description, cam):
        self.userId = userId
        self.captureType = captureType
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle(title)
        cWidget = QtGui.QWidget(self) 
        mainLayout = QtGui.QVBoxLayout()

        # Title
        titleLabel = QtGui.QLabel(description)
        titleLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Webcam 
        self.imgLabel = QtGui.QLabel();
        self.webcamSampling = None
        if cam == None:
            self.webcamSampling = vs.VideoSampling()
        else:
            self.webcamSampling = cam
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.refreshWebcam)
        self.timer.start(27)
        self.update()

        # Button 
        buttonLayout = QtGui.QHBoxLayout()
        startButton = QtGui.QPushButton("Take!")
        self.connect(startButton, QtCore.SIGNAL("clicked()"), self.savePicture)
        buttonLayout.addWidget(startButton)
        
        if self.captureType == self.FACE_TYPE:
            cancelButton = QtGui.QPushButton("Cancel")
            self.connect(cancelButton, QtCore.SIGNAL("clicked()"), QtCore.SLOT("close()"))
            buttonLayout.addWidget(cancelButton)

        mainLayout.addWidget(titleLabel)
        mainLayout.addWidget(self.imgLabel)
        mainLayout.addLayout(buttonLayout)

        mainLayout.setAlignment(QtCore.Qt.AlignCenter)
        cWidget.setLayout(mainLayout)
        self.setCentralWidget(cWidget)
        self.center()

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
        
    def savePicture(self):
        print "Save picture - " + self.captureType
        self.timer.stop()
        detection, newUser = self.webcamSampling.saveFrame(self.userId, self.captureType)
        if self.captureType == self.FACE_TYPE:
            if detection:
                if not newUser:
                    msgBox = QtGui.QMessageBox()
                    msgBox.setText("User allready exist and your image is used for improve recognition system.");
                    msgBox.setInformativeText("Do you want to recapture your gesture? Gesture is always overwritten.");
                    msgBox.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Close);
                    msgBox.setDefaultButton(QtGui.QMessageBox.Close);
                    ret = msgBox.exec_();
                if newUser or ret == QtGui.QMessageBox.Ok:
                    self.gestureWindow = CaptureWindow(self.userId, self.GESTURE_TYPE, "New User - Gesture", "Take a picture of your gesture", self.webcamSampling)
                    time.sleep(self.WAIT_TIME)
                    self.close()
                    self.gestureWindow.show()
                else:
                    self.close()
            else:
                print "Procedure aborted."
                msgBox = QtGui.QMessageBox()
                msgBox.setText("There is a problem with your photo!");
                msgBox.setInformativeText("Try to choose a different position of your face.");
                msgBox.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Close);
                msgBox.setDefaultButton(QtGui.QMessageBox.Close);
                if msgBox.exec_() == QtGui.QMessageBox.Ok:
                    self.timer.start(27)
                else:
                    self.close()
        elif self.captureType == self.GESTURE_TYPE:
            print "Procedure completed."
            time.sleep(self.WAIT_TIME)
            self.close()

    def refreshWebcam(self):
        self.webcamSampling.captureNextFrame()
        self.imgLabel.setPixmap(self.webcamSampling.convertFrame())