import speech_recognition as sr
from playsound import playsound
from os import path

r = sr.Recognizer()

audiopath = path.join(path.dirname(__file__),'test.wav')

with sr.AudioFile(audiopath) as source:
    audio = r.record(source)

print(r.recognize_google(audio))

playsound(audiopath)
