from voiceid.sr import Voiceid
from voiceid.db import GMMVoiceDB
import ConfigParser
import os

class AudioAnalyzer():

    def __init__(self):
        """ Init voice model """
        self._config = ConfigParser.ConfigParser()
        self._config.read("config.ini")
        dbPath = os.getcwd() + "/" + self._config.get("Paths", "voiceDir")
        self._db = GMMVoiceDB(dbPath)

    def addUser(self, user, audio):
        """ Add user to voice db """
        self._db.add_model(audio, user)

    def getUserList(self):
        """ Return users of voice db """ 
        return db.get_speakers()

    def checkAudio(self, audio):
        """ Check voices inside audio file """
        return Voiceid(self._db, audio)

    def getTotalSpeakers(self, voiceObj):
        """ List of all speakers in voice file """
        return voiceObj.get_user()

    def getBestSpeaker(self, voiceObj):
        """ Best near speaker in voice file """
        userList = getTotalSpekers(voiceObj)
        return max(userList, key = userList.get)