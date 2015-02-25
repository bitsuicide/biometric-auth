from PyQt4 import QtGui, QtCore
import VideoSampling as vs
import Recognition as rec
import RecWindow as rw


class RecognitionWindow(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.recognition = rec.Recognition(True)
        self.setWindowTitle("Authorization system - Face")
        cWidget = QtGui.QWidget(self)
        mainLayout = QtGui.QVBoxLayout()

        # Title
        titleLabel = QtGui.QLabel("Show your credential!")
        titleLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Webcam
        self.imgLabel = QtGui.QLabel()
        self.webcamSampling = vs.VideoSampling()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.refreshWebcam)
        self.timer.start(27)
        self.update()

        # Button
        startButton = QtGui.QPushButton("Authenticate")
        cancelButton = QtGui.QPushButton("Cancel")
        self.connect(
            startButton, QtCore.SIGNAL("clicked()"), self.startAuthentication)
        self.connect(
            cancelButton, QtCore.SIGNAL("clicked()"), QtCore.SLOT("close()"))

        mainLayout.addWidget(titleLabel)
        mainLayout.addWidget(self.imgLabel)
        mainLayout.addWidget(startButton)
        mainLayout.addWidget(cancelButton)

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

    def startAuthentication(self):
        print "Start face authentication..."
        self._authTimer = QtCore.QTimer(self)
        self._authTimer.singleShot(3000, self.authenticate)

    def authenticate(self):
        self.timer.stop()
        bestUser = str(self.recognition.getBestUser())
        print ("Best user: " + bestUser + " Frame Count: "
               + str(self.recognition.frameFaceCounter))
        if bestUser == "unknown":
            msgBox = QtGui.QMessageBox()
            msgBox.setText("Unknown user. Try to authenticate yourself.")
            msgBox.setStandardButtons(QtGui.QMessageBox.Ok |
                                      QtGui.QMessageBox.Cancel)
            msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
            if msgBox.exec_() == QtGui.QMessageBox.Ok:
                self.timer.start(27)
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
