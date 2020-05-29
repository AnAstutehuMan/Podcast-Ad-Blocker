import math
import wave
from os import path

import pydub as pd
import speech_recognition as sr
from pydub import AudioSegment

import soundfile as sf

r = sr.Recognizer()

audiopath = path.join(path.dirname(__file__), "files/test.wav")

audioclip = []

loadedaudio = []
reconaudio = []

# Saketh: rewrote the code


r = sr.Recognizer()
f = open("transcript", "a")


def splitAudio(filePath, interval):
    intervalOne = 0
    intervalTwo = interval * 1000

    numberOfSplits = math.floor(AudioSegment.from_wav(
        filePath).duration_seconds / interval)

    for i in range(numberOfSplits):
        AudioSegment.from_wav(filePath)[intervalOne:intervalTwo].export("clip" + str(i) + ".wav", format="wav")
        intervalOne = intervalTwo
        intervalTwo = intervalTwo + (interval * 1000)

    recognizeAudio(filePath, numberOfSplits)


def recognizeAudio(filePath, numberOfSplits):
    for i in range(numberOfSplits):
        with sr.AudioFile("clip" + str(i) + ".wav") as source:
            f.write(r.recognize_google(r.record(source))+"\n")
    f.close()


splitAudio('test.wav', 1.5)
