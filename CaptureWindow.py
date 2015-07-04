from PyQt4 import QtGui, QtCore
import VideoSampling as vs
import RecWindow as rw
import time


class CaptureWindow(QtGui.QMainWindow):
    WAIT_TIME = 1
    MIN_PHOTOS = 5
    TITLE = "Take a picture of yourself"

    def __init__(self, user_id, is_registered):
        self.photos_taken = 0
        self.user_id = user_id
        self.is_registered = is_registered
        self._save_picture = {
            False: self._save_picture_new_user,
            True: self._save_picture_registered_user
        }

        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle("{} - Face Capture".format(user_id))
        cWidget = QtGui.QWidget(self)
        mainLayout = QtGui.QVBoxLayout()

        # Title
        title = self.TITLE
        if not is_registered:
            title += " ({}/{})".format(self.photos_taken+1, self.MIN_PHOTOS)
        self.titleLabel = QtGui.QLabel(title)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        # Webcam
        self.imgLabel = QtGui.QLabel()
        self.webcamSampling = vs.VideoSampling()
        # if cam is None:
        #     self.webcamSampling = vs.VideoSampling()
        # else:
        #     self.webcamSampling = cam
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.refreshWebcam)
        self.timer.start(33)
        self.update()

        # Button
        buttonLayout = QtGui.QHBoxLayout()
        startButton = QtGui.QPushButton("Take!")
        self.connect(
            startButton, QtCore.SIGNAL("clicked()"), self.save_picture)
        buttonLayout.addWidget(startButton)
        cancelButton = QtGui.QPushButton("Cancel")
        self.connect(cancelButton,
                     QtCore.SIGNAL("clicked()"),
                     QtCore.SLOT("close()"))
        buttonLayout.addWidget(cancelButton)

        mainLayout.addWidget(self.titleLabel)
        mainLayout.addWidget(self.imgLabel)
        mainLayout.addLayout(buttonLayout)

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

    def _save_picture_registered_user(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setInformativeText(
            "User already exists and your image is used for improve "
            "recognition system. Do you want to take another shot?")
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok |
                                  QtGui.QMessageBox.Close)
        msgBox.setDefaultButton(QtGui.QMessageBox.Close)
        ret = msgBox.exec_()
        if ret == QtGui.QMessageBox.Ok:
            self.timer.start(33)
            return True

        msgBox.setInformativeText(
            "Do you want to record your voice one more time?"
            " Your voice will always be overwritten.")
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok |
                                  QtGui.QMessageBox.Close)
        msgBox.setDefaultButton(QtGui.QMessageBox.Close)
        ret = msgBox.exec_()
        if ret == QtGui.QMessageBox.Close:
            self.close()
            return True
        return False

    def _save_picture_new_user(self):
        if self.photos_taken < self.MIN_PHOTOS:
            self.titleLabel.setText(self.TITLE + " ({}/{})".format(
                self.photos_taken+1, self.MIN_PHOTOS))
            self.timer.start(33)
            return True
        return False

    def save_picture(self):
        print "Saving picture"
        self.timer.stop()
        detection, _ = self.webcamSampling.saveFrame(self.user_id)
        if detection:
            self.photos_taken += 1
            if self._save_picture[self.is_registered]():
                return
            self.recWindow = rw.RecWindow(
                self.user_id,
                "New User - Voice",
                "Push Recording button and read the famous quotation.",
                False)
            time.sleep(self.WAIT_TIME)
            self.close()
            self.recWindow.show()
        else:
            print "Procedure aborted."
            msgBox = QtGui.QMessageBox()
            msgBox.setText("There is a problem with your photo!")
            msgBox.setInformativeText(
                "Try to assume a different position of your face.")
            msgBox.setStandardButtons(QtGui.QMessageBox.Ok |
                                      QtGui.QMessageBox.Close)
            msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
            if msgBox.exec_() == QtGui.QMessageBox.Ok:
                self.timer.start(33)
            else:
                self.close()

    def refreshWebcam(self):
        self.webcamSampling.captureNextFrame()
        self.imgLabel.setPixmap(self.webcamSampling.convertFrame())
