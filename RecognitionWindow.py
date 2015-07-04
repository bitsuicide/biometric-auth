from PyQt4 import QtGui, QtCore
import VideoSampling as vs
import Recognition as rec
import RecWindow as rw


class RecognitionWindow(QtGui.QMainWindow):

    def __init__(self, video_src=None, modelType=None, threshold=None):
        QtGui.QMainWindow.__init__(self)
        self.recognition = rec.Recognition(True, modelType, threshold)
        self.setWindowTitle("Authorization system - Face")
        cWidget = QtGui.QWidget(self)
        mainLayout = QtGui.QVBoxLayout()

        # Title
        # titleLabel = QtGui.QLabel("Show your credential!")
        # titleLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Webcam
        self.imgLabel = QtGui.QLabel()
        self.webcamSampling = vs.VideoSampling(video_src)
        self.update()

        # Button
        self.startButton = QtGui.QPushButton("Authenticate")
        self.cancelButton = QtGui.QPushButton("Cancel")
        self.connect(self.startButton, QtCore.SIGNAL("clicked()"),
                     self.startAuthentication)
        self.connect(self.cancelButton, QtCore.SIGNAL("clicked()"),
                     QtCore.SLOT("close()"))

        # mainLayout.addWidget(titleLabel)
        mainLayout.addWidget(self.imgLabel)
        mainLayout.addWidget(self.startButton)
        mainLayout.addWidget(self.cancelButton)

        mainLayout.setAlignment(QtCore.Qt.AlignCenter)
        cWidget.setLayout(mainLayout)
        self.setCentralWidget(cWidget)
        self.center()

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(
            QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop(
            ).screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def refreshWebcam(self):
        self.webcamSampling.captureNextFrame()
        # Recognition System
        self.webcamSampling.currentFrame = self.recognition.checkFrame(
            self.webcamSampling.currentFrame)
        self.imgLabel.setPixmap(self.webcamSampling.convertFrame())
        if self.recognition._totalMatches == self.recognition.TOTAL_MATCHES:
            self.timer.stop()
            self.authenticate()

    def startAuthentication(self):
        print "Start face authentication..."
        self.startButton.setEnabled(False)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.refreshWebcam)
        self.timer.start(33)

    def authenticate(self):
        bestUser = self.recognition.getBestUser()
        print ("Best user: " + str(bestUser) + " Frame Count: "
               + str(self.recognition.frameFaceCounter))
        if bestUser is None:
            msgBox = QtGui.QMessageBox()
            msgBox.setText("Please wait a few seconds.")
            msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
            msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
            msgBox.exec_()
            self.timer.start(33)
            self.startButton.setEnabled(True)
        elif bestUser == 'unknown':
            msgBox = QtGui.QMessageBox()
            msgBox.setText("Unknown user. Try to authenticate yourself.")
            msgBox.setStandardButtons(QtGui.QMessageBox.Ok |
                                      QtGui.QMessageBox.Cancel)
            msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
            if msgBox.exec_() == QtGui.QMessageBox.Ok:
                self.timer.start(33)
                self.startButton.setEnabled(True)
            else:
                self.close()
        else:
            self.recWindow = rw.RecWindow(
                bestUser,
                "Authorization system - Voice",
                "Push Recording button and read the famous quotation.",
                True)
            self.close()
            self.recWindow.show()
