from PyQt4 import QtGui, QtCore
import VideoSampling as vs
import RecWindow as rw
import time

class CaptureWindow(QtGui.QMainWindow):
    WAIT_TIME = 1

    def __init__(self, userId, title, description, cam):
        self.userId = userId
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
        print "Save picture"
        self.timer.stop()
        detection, newUser = self.webcamSampling.saveFrame(self.userId)
        if detection:
            if not newUser:
                msgBox = QtGui.QMessageBox()
                msgBox.setText("User already exists and your image is used for improving recognition system.");
                msgBox.setInformativeText("Do you want to record your voice one more time? Your voice will always be overwritten.");
                msgBox.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Close);
                msgBox.setDefaultButton(QtGui.QMessageBox.Close);
                ret = msgBox.exec_();
            if newUser or ret == QtGui.QMessageBox.Ok:
                self.recWindow = rw.RecWindow(self.userId, "New User - Voice", "Push Recording button and read the famous quotation.", False)
                time.sleep(self.WAIT_TIME)
                self.close()
                self.recWindow.show()
            else:
                self.close()
        else:
            print "Procedure aborted."
            msgBox = QtGui.QMessageBox()
            msgBox.setText("There is a problem with your photo!");
            msgBox.setInformativeText("Try to assume a different position of your face.");
            msgBox.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Close);
            msgBox.setDefaultButton(QtGui.QMessageBox.Ok);
            if msgBox.exec_() == QtGui.QMessageBox.Ok:
                self.timer.start(27)
            else:
                self.close()

    def refreshWebcam(self):
        self.webcamSampling.captureNextFrame()
        self.imgLabel.setPixmap(self.webcamSampling.convertFrame())
