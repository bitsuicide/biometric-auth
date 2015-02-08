#!/usr/bin/python

"""
Add new user to auth system
"""

import ConfigParser
import os
import sys
from PyQt4 import QtGui, QtCore
import MainWindow as mw

def readConfig():
    """ read data from config """
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
    main = mw.MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
