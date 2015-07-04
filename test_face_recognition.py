import os
import sys
from collections import defaultdict, Counter
from pprint import pprint as pp
from PyQt4 import QtGui
import RecognitionWindow


def main():
    results = {
        "eigen": defaultdict(lambda: defaultdict(Counter)),
        "fisher": defaultdict(lambda: defaultdict(Counter)),
        "lbph": defaultdict(lambda: defaultdict(Counter))
    }
    app = QtGui.QApplication(sys.argv)
    dir_name = os.path.join(os.getcwd(), 'video')
    videos = os.listdir(dir_name)
    for model in results:
        for threshold in range(70, 150, 5):
            for video_file_name in videos:
                if video_file_name.endswith('.mov'):
                    username, extension = os.path.splitext(video_file_name)
                    video = os.path.join(dir_name, video_file_name)
                    print "Computing {} video".format(username)
                    rw = RecognitionWindow.RecognitionWindow(video, model,
                                                             threshold)
                    while rw.recognition._totalMatches != \
                            rw.recognition.TOTAL_MATCHES:
                        rw.webcamSampling.captureNextFrame()
                        rw.webcamSampling.currentFrame = \
                            rw.recognition.checkFrame(
                                rw.webcamSampling.currentFrame)
                        rw.imgLabel.setPixmap(rw.webcamSampling.convertFrame())
                    bestUser = rw.recognition.getBestUser()

                    results[model][threshold]['Total'] += 1
                    if bestUser == username:
                        results[model][threshold]['GA'] += 1
                    elif bestUser == 'unknown':
                        results[model][threshold]['FR'] += 1
                    else:  # Wrong user
                        results[model][threshold]['FA'] += 1

                    print username, bestUser
    pp(results)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()












