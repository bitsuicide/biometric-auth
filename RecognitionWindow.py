from PyQt4 import QtGui, QtCore
import VideoSampling as vs
import Recognition as rec

class RecognitionWindow(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.recognition = rec.Recognition()
        self.setWindowTitle("Authorization system")
        cWidget = QtGui.QWidget(self) 
        mainLayout = QtGui.QVBoxLayout()

        # Title
        titleLabel = QtGui.QLabel("Show your credential!")
        titleLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Webcam 
        self.imgLabel = QtGui.QLabel();
        self.webcamSampling = vs.VideoSampling()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.refreshWebcam)
        self.timer.start(27)
        self.update()

        # Button
        cancelButton = QtGui.QPushButton("Cancel")
        self.connect(cancelButton, QtCore.SIGNAL("clicked()"), QtCore.SLOT("close()"))

        mainLayout.addWidget(titleLabel)
        mainLayout.addWidget(self.imgLabel)
        mainLayout.addWidget(cancelButton)

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

    def refreshWebcam(self):
        self.webcamSampling.captureNextFrame()
        # Recognition System
        self.webcamSampling.currentFrame = self.recognition.checkFrame(self.webcamSampling.currentFrame) 
        self.imgLabel.setPixmap(self.webcamSampling.convertFrame())