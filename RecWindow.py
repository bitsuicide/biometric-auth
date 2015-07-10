import AudioAnalyzer as aa
import Recorder as rc
import SentenceGenerator as sg
import os
from PyQt4 import QtGui, QtCore


class RecWindow(QtGui.QMainWindow):

    def __init__(self, userId, title, description, recognition):
        self._userId = userId
        self._recognition = recognition
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle(title)
        cWidget = QtGui.QWidget(self)
        mainLayout = QtGui.QVBoxLayout()

        # Title
        titleLabel = QtGui.QLabel(description)
        titleLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Sentence
        sentenceGenerator = sg.SentenceGenerator()
        sentence = sentenceGenerator.getRandomSentence()
        sentenceLabel = QtGui.QLabel(sentence)
        sentenceLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Command button
        buttonLayout = QtGui.QHBoxLayout()
        startButton = QtGui.QPushButton("Recording")
        self.connect(startButton, QtCore.SIGNAL("clicked()"), self.startRec)
        buttonLayout.addWidget(startButton)

        # Button
        cancelButton = QtGui.QPushButton("Cancel")
        self.connect(cancelButton,
                     QtCore.SIGNAL("clicked()"),
                     QtCore.SLOT("close()"))
        buttonLayout.addWidget(cancelButton)

        mainLayout.addWidget(titleLabel)
        mainLayout.addWidget(sentenceLabel)
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
        centerPoint = QtGui.QApplication.desktop().screenGeometry(
            screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def startRec(self):
        """ Start recording """
        rec = rc.Recorder(rate=22050, channels=1)
        filePath = "rec"
        with rec.open(filePath + ".wav", "wb") as recfile:
            recfile.record(duration=5.0)
        audioAnalyzer = aa.AudioAnalyzer()
        if self._recognition:
            voice = audioAnalyzer.checkAudio(filePath + ".wav")
            bestUsers = audioAnalyzer.getBestUsers(voice)
            print "Best users: {}".format(bestUsers)
            print "_userId: " + self._userId
            if self._userId in bestUsers:
                msgBox = QtGui.QMessageBox()
                msgBox.setText(
                    "Welcome {}! You have been authenticated.".format(
                        self._userId))
                msgBox.setStandardButtons(QtGui.QMessageBox.Close)
                msgBox.exec_()
            else:
                msgBox = QtGui.QMessageBox()
                msgBox.setText("Two step authentication failed.")
                msgBox.setStandardButtons(QtGui.QMessageBox.Close)
                msgBox.exec_()
        else:
            print "Adding new user " + self._userId + " with file " + filePath
            try:
                success = audioAnalyzer.addUser(self._userId, filePath)
            except IOError, e:
                success = False
                print "Error adding user: " + str(e)
            os.system("rm -R " + filePath + "*")  # remove all temp file
            if success:
                self.close()
                return
            msgBox = QtGui.QMessageBox()
            msgBox.setText("Please speak more loudly.")
            msgBox.setStandardButtons(QtGui.QMessageBox.Close)
            msgBox.exec_()
