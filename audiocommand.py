import pyaudio, os
import speech_recognition as sr

def authentication():
        os.system("python detect_face.py")

def addUser():
        os.system("python add_user.py")

def main(source):
        audio = r.listen(source)
        user = r.recognize(audio)
        print(user)
        if user == "authentication":
                authentication()
        elif user == "management":
                addUser()
        elif user == "exit":
                exit()
        else:
                print("Command unknown")
        exit()

if __name__ == "__main__":
    r = sr.Recognizer()
    with sr.Microphone() as source:
        main(source)