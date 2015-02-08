from PyQt4 import QtGui, QtCore
import VideoSampling as vs

class CaptureWindow(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle("New User - Face")
        cWidget = QtGui.QWidget(self) 

        mainLayout = QtGui.QVBoxLayout()

        # Title
        titleLabel = QtGui.QLabel("Take a picture of you")
        titleLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Webcam 
        self.imgLabel = QtGui.QLabel();
        self.webcamSampling = vs.VideoSampling()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.refreshWebcam)
        self.timer.start(27)
        self.update()

        # Button 
        buttonLayout = QtGui.QHBoxLayout()
        startButton = QtGui.QPushButton("Take!")
        self.connect(startButton, QtCore.SIGNAL("clicked()"), self.savePicture)
        cancelButton = QtGui.QPushButton("Cancel")
        self.connect(cancelButton, QtCore.SIGNAL("clicked()"), QtCore.SLOT("close()"))
        buttonLayout.addWidget(startButton)
        buttonLayout.addWidget(cancelButton)

        mainLayout.addWidget(titleLabel)
        mainLayout.addWidget(self.imgLabel)
        mainLayout.addLayout(buttonLayout)

        mainLayout.setAlignment(QtCore.Qt.AlignCenter)
        cWidget.setLayout(mainLayout)
        self.setCentralWidget(cWidget)
        
    def savePicture(self):
        print "Save picture..."

    def refreshWebcam(self):
        self.webcamSampling.captureNextFrame()
        self.imgLabel.setPixmap(self.webcamSampling.convertFrame())