from voiceid.sr import Voiceid
from voiceid.db import GMMVoiceDB

#create voice db   
db = GMMVoiceDB("voice")

# add models to db: params the basename of 'giov_wave.wav' and the speaker, Giovanni
db.add_model("rec", "test")
#db.add_model("irina", "irina")

#print db.get_speakers()


"""
# process a video/audio file containing various speakers
v = Voiceid(db, "irina.wav")

# extract the speakers from file and search into db 
v.extract_speakers()

bestUsers = v.get_user()
print "Dict: " + str(bestUsers)
print "Max: " + max(bestUsers, key = bestUsers.get)

for c in v.get_clusters():
	cluster = v.get_cluster(c)
	print cluster.get_best_speaker()
"""

