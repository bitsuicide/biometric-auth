from PyQt4 import QtGui, QtCore
import CaptureWindow as cw

class MainWindow(QtGui.QMainWindow):
    
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle("Add new user")
        cWidget = QtGui.QWidget(self)        
        mainLayout = QtGui.QVBoxLayout()

        # Title
        titleLabel = QtGui.QLabel("Authorize new user to access the system")
        titleLabel.setAlignment(QtCore.Qt.AlignCenter)

        # User
        userLayout = QtGui.QHBoxLayout()
        userLabel = QtGui.QLabel("Insert your name: ")
        self.userEdit = QtGui.QLineEdit()
        self.userEdit.setReadOnly(False)
        userLayout.addWidget(userLabel)
        userLayout.addWidget(self.userEdit)

        # Button  
        buttonLayout = QtGui.QHBoxLayout()
        startButton = QtGui.QPushButton("Start")
        self.connect(startButton, QtCore.SIGNAL("clicked()"), self.newWindow)
        cancelButton = QtGui.QPushButton("Cancel")
        self.connect(cancelButton, QtCore.SIGNAL("clicked()"), QtCore.SLOT("close()"))
        buttonLayout.addWidget(startButton)
        buttonLayout.addWidget(cancelButton)

        mainLayout.addWidget(titleLabel)
        mainLayout.addLayout(userLayout)
        mainLayout.addLayout(buttonLayout)
        mainLayout.setAlignment(QtCore.Qt.AlignCenter)
        cWidget.setLayout(mainLayout)
        self.setCentralWidget(cWidget)

    def newWindow(self):
        user = str(self.userEdit.text())
        print "Start process. Username: " + user
        self.faceWindow = cw.CaptureWindow(user, cw.CaptureWindow.FACE_TYPE, "New User - Face", "Take a picture of you", None)
        self.close()
        self.faceWindow.show()