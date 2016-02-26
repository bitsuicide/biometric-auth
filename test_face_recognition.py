import os
import sys
from collections import defaultdict, Counter
from pprint import pprint as pp
from PyQt4 import QtGui
import RecognitionWindow
import AudioAnalyzer


def main():
    impostors = []
    audio_results = defaultdict(list)
    face_results = {
        "eigen": defaultdict(Counter),
        "fisher": defaultdict(Counter),
        "lbph": defaultdict(Counter)
    }
    ranges = {
        "eigen": [0, 5501, 100],
        "fisher": [0, 5501, 100],
        "lbph": [0, 201, 5],
    }
    app = QtGui.QApplication(sys.argv)
    video_dir_name = os.path.join(os.getcwd(), 'tests', 'video')
    audio_dir_name = os.path.join(os.getcwd(), 'tests', 'audio')
    video_files = os.listdir(video_dir_name)
    audio_files = os.listdir(audio_dir_name)

    for audio_file_name in audio_files:
        if audio_file_name.endswith('.wav'):
            username, extension = os.path.splitext(audio_file_name)
            print "Computing {}'s audio".format(username)
            audio = os.path.join(audio_dir_name, audio_file_name)
            audioAnalyzer = AudioAnalyzer.AudioAnalyzer()
            voice = audioAnalyzer.checkAudio(audio)
            bestUsers = audioAnalyzer.getBestUsers(voice)
            print username, bestUsers
            audio_results[username] = bestUsers

    for model in face_results:
        for threshold in range(*ranges[model]):
            print threshold
            for video_file_name in video_files:
                if video_file_name.endswith('.mov'):
                    username, extension = os.path.splitext(video_file_name)
                    video = os.path.join(video_dir_name, video_file_name)
                    print "Computing {}'s video".format(username)
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

                    face_results[model][threshold]['Total'] += 1

                    if username in impostors:
                        if bestUser == 'unknown':
                            face_results[model][threshold]['TR'] += 1
                            face_results[model][threshold]['TTR'] += 1
                        else:
                            face_results[model][threshold]['FA'] += 1
                            if bestUser in audio_results[username]:
                                face_results[model][threshold]['TFA'] += 1
                            else:
                                face_results[model][threshold]['TTR'] += 1

                    elif bestUser == 'unknown':
                        face_results[model][threshold]['FR'] += 1
                        face_results[model][threshold]['TFR'] += 1
                    else:
                        face_results[model][threshold]['GA'] += 1
                        if bestUser in audio_results[username]:
                            face_results[model][threshold]['TGA'] += 1
                        else:
                            face_results[model][threshold]['TFR'] += 1

                        # Valid user logged as another user
                        if bestUser != username:
                            face_results[model][threshold]['AE'] += 1
                            if bestUser in audio_results[username]:
                                face_results[model][threshold]['TAE'] += 1

                    print username, bestUser

    for model in face_results:
        print 'MODEL: {}'.format(model)
        for threshold in sorted(face_results[model]):
            print 'THRESHOLD: {}\tFAR: {}\tFRR: {}\tTFAR: {}\tFRR: {}\tTOTAL: {}\tGA: {}\tAE: {}\tTR: {}\tFR: {}\tFA: {}\tTGA: {}\tTAE: {}\tTTR: {}\tTFR: {}\tTFA: {}'.format(
                threshold,
                round((face_results[model][threshold]['FA']*30/21)/((face_results[model][threshold]['FA']*30/21) + (face_results[model][threshold]['TR']*30/21)), 2),
                round((face_results[model][threshold]['FR']*30/21)/((face_results[model][threshold]['FR']*30/21) + (face_results[model][threshold]['GA']*30/21)), 2),
                round((face_results[model][threshold]['TFA']*30/21)/((face_results[model][threshold]['TFA']*30/21) + (face_results[model][threshold]['TTR']*30/21)), 2),
                round((face_results[model][threshold]['TFR']*30/21)/((face_results[model][threshold]['TFR']*30/21) + (face_results[model][threshold]['TGA']*30/21)), 2),
                face_results[model][threshold]['Total']*30/21,
                face_results[model][threshold]['GA']*30/21,
                face_results[model][threshold]['AE']*30/21,
                face_results[model][threshold]['TR']*30/21,
                face_results[model][threshold]['FR']*30/21,
                face_results[model][threshold]['FA']*30/21,
                face_results[model][threshold]['TGA']*30/21,
                face_results[model][threshold]['TAE']*30/21,
                face_results[model][threshold]['TTR']*30/21,
                face_results[model][threshold]['TFR']*30/21,
                face_results[model][threshold]['TFA']*30/21)
    pp(audio_results)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
