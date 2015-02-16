import ConfigParser
import os 

class ReadWriteIndex():
    FILE_SEPARATOR = ";"
    
    def __init__(self):
        """ Read index file """
        self.config = ConfigParser.ConfigParser()
        self.config.read("config.ini")
        pathDir = os.getcwd() + self.config.get("Paths", "faceDir")
        if not os.path.isdir(pathDir):  
            os.mkdir(pathDir) 

        indexPath = pathDir + "/" + self.config.get("Alg Parameters", "indexFile")
        self.configIndex = open(indexPath, "r+")
        self.countElem = 0
        self.userImg = {} 
        print "Read file index of face"
        for line in self.configIndex:
            data = line.split(self.FILE_SEPARATOR) # img - user 
            self.addUserAndPath(data[1].strip(), data[0])

    def __del__(self):
        """ Close index file """
        self.configIndex.close()

    def addRow(self, user, path):
        """ Append row at index file """
        self.configIndex.write(path[1:len(path)] + self.FILE_SEPARATOR + user + "\n")
        self.addUserAndPath(user, path)

    def addUserAndPath(self, user, path):
        if self.checkUser(user):
            imgList = self.userImg[user]
            imgList.append(path)
            self.userImg[user] = imgList
        else:
            tempList = []
            tempList.append(path)
            self.userImg[user] = tempList
        self.countElem += 1

    def checkUser(self, user):
        """ Check if exist an user """
        return user in self.userImg

    def getUserImg(self):
        """ Get User & Image dictionary """
        return self.userImg

    def getCountTotalElem(self):
        """ Get count of total element """
        return self.countElem

    def getCountUserElem(self, user):
        """ Get count of user element """
        if self.checkUser(user):
            return len(self.userImg[user])
        else:
            return 0
