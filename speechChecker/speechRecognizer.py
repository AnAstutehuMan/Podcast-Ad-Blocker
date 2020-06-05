import json
import math

import speech_recognition
from pydub import AudioSegment

filterwords = ["sponser"]


def splitAudio(filePath, interval):
    # Mutiformat support
    audio = AudioSegment.from_file(filePath, "wav")
    amountToStep = interval * 1000
    numberOfSteps = math.floor(audio.duration_seconds / interval)

    # More simple spliting
    for i in range(numberOfSteps):
        AudioSegment.from_wav(filePath)[
            i * amountToStep:(i + 1) * amountToStep].export("clip (" + str(i) + ").wav", format="wav")

    recognizeAudio(filePath, numberOfSteps)


def recognizeAudio(filePath, numberOfSteps):
    r = speech_recognition.Recognizer()
    f = open("transcript.json", "w+")
    f.write("{")
    for i in range(numberOfSteps):
        with speech_recognition.AudioFile("clip (" + str(i) + ").wav") as source:
            f.write('"' + str(i) + '":"' +
                    r.recognize_google(r.record(source)) + '"')
        if i != numberOfSteps - 1:
            f.write(','+"\n")
    f.write("}")
    f.close()
    filterAudio()


def filterAudio():
    f = open("transcript.json", "r+")
    for line in f:
        for i in range:
            if (line.split() == filterwords[i]):
                line.strip("\n")
                f.write(line)


splitAudio('clip.wav', 1.5)
