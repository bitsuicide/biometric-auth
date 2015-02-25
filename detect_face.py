import sys
from PyQt4 import QtGui
import RecognitionWindow as rw


def main():
    app = QtGui.QApplication(sys.argv)
    main = rw.RecognitionWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
