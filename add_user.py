#!/usr/bin/python

"""
Add new user to auth system
"""

import sys
from PyQt4 import QtGui
import MainWindow as mw


def main():
    app = QtGui.QApplication(sys.argv)
    main = mw.MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
