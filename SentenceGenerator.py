import os
from random import randint
import ConfigParser

class SentenceGenerator():

    def __init__(self):
        """ Read sentences from file """
        self._config = ConfigParser.ConfigParser()
        self._config.read("config.ini")
        path = os.getcwd() + "/" + self._config.get("Paths", "sentence")
        sentence = open(path, "r")
        self._senteceList = []
        print "Read sentences file"
        for line in sentence:
            self._senteceList.append(line)

    def getSentenceList(self):
        return self._senteceList

    def getRandomSentence(self):
        """ Return random sentence """
        i = randint(0, len(self._senteceList) - 1)
        return self._senteceList[i]