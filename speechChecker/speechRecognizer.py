import json
import math
import os
from glob import glob

import speech_recognition
from pydub import AudioSegment

filterword = ["sponsor", "sponsored", "break"]


def splitAudio(filePath, interval):
    # Mutiformat support
    audio = AudioSegment.from_file(filePath, "wav")
    amountToStep = interval * 1000
    numberOfSteps = math.floor(audio.duration_seconds / interval)

    # More simple spliting
    for i in range(numberOfSteps):
        AudioSegment.from_wav(filePath)[
            i * amountToStep:(i + 1) * amountToStep].export("clip (" + str(i+1) + ").wav", format="wav")

    recognizeAudio(filePath, numberOfSteps)


def recognizeAudio(filePath, numberOfSteps):
    r = speech_recognition.Recognizer()
    f = open("transcript.txt", "w+")
    for i in range(numberOfSteps):
        with speech_recognition.AudioFile("clip (" + str(i+1) + ").wav") as source:
            f.write(r.recognize_google(r.record(source)))
        if i != numberOfSteps - 1:
            f.write("\n")
    f.close()
    filterAudio()


def filterAudio():
    with open("transcript.txt") as f:
        for num, line in enumerate(f, 1):
            for word in line.split():
                for x in range(len(filterword)):
                    if filterword[x] in word:
                        print("found word: " + word + " in line: " + str(num))
                        print("removing clip " + str(num) +
                              " and the next 2 files.")
                        os.remove("clip (" + str(num) + ").wav")
                        os.remove("clip (" + str(num+1) + ").wav")
                        os.remove("clip (" + str(num+2) + ").wav")

    mergeAudio()


def mergeAudio():
    listAudio = [AudioSegment.from_wav(files)
                 for files in glob("clip (*).wav")]
    combined = AudioSegment.empty()

    for song in listAudio:
        combined += song

    combined.export("newClip.wav", format="wav")


splitAudio('clip.wav', 1.5)
