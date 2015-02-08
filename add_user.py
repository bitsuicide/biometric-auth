#!/usr/bin/python

#################################
#  Add new user to auth system  #
#################################

import ConfigParser
import os
import cv2
import sys
from PyQt4 import QtGui, QtCore

class MainWindow(QtGui.QMainWindow):
    
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.resize(700, 700)
        self.setWindowTitle("Add new user")
        cWidget = QtGui.QWidget(self)

        # First line box
        grid = QtGui.QGridLayout(cWidget)

        firstBox = QtGui.QHBoxLayout()
        firstBox.setSpacing(5)
        userLabel = QtGui.QLabel("Insert your name: ", cWidget)
        self.userEdit = QtGui.QLineEdit(cWidget)
        self.userEdit.setReadOnly(False)
        firstBox.addWidget(userLabel)
        firstBox.addWidget(self.userEdit)

        secondBox = QtGui.QHBoxLayout()
        secondBox.setSpacing(5)
        startButton = QtGui.QPushButton("Start")
        self.connect(startButton, QtCore.SIGNAL("clicked()"), self.startProcess)
        cancelButton = QtGui.QPushButton("Cancel")
        self.connect(cancelButton, QtCore.SIGNAL("clicked()"), QtCore.SLOT("close()"))
        secondBox.addWidget(startButton)
        secondBox.addWidget(cancelButton)

        grid.addLayout(firstBox, 0, 0)
        grid.addLayout(secondBox, 1, 0)
        cWidget.setLayout(grid)
        self.setCentralWidget(cWidget)

    def startProcess(self):
        print "Start process. Username: " + self.userEdit.text()

def readConfig():
    #read data from config
    config = ConfigParser.ConfigParser()
    config.read("config.ini")
    currentDir = os.getcwd()
    faceDir = currentDir + config.get("Paths", "faceDir")
    gestureDir = currentDir + config.get("Paths", "gestureDir")

    if not os.path.isdir(faceDir):  
        os.mkdir(faceDir)
    if not os.path.isdir(gestureDir): 
        os.mkdir(gestureDir)

def main():
    readConfig()
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
