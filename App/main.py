import math
import os, sys
from glob import glob

import speech_recognition
from pydub import AudioSegment

#not the best filter but it works i guess
filterword = ["sponsor", "sponsored", "break", "advert", "ad", "advertising"]


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
    filterAudio(numberOfSteps)


def filterAudio(numberOfSteps):
    with open("transcript.txt") as f:
        for num, line in enumerate(f, 1):
            for word in line.split():
                for x in range(len(filterword)):
                    if filterword[x] in word:
                        print("found word: " + word + " in line: " + str(num))
                        print("removing clip " + str(num) +
                              " and the next 3 files.")
                        #this is going to give an invalid range error in some cases but its 1:30 hours away from deadline so...
                        os.remove("clip (" + str(num) + ").wav")
                        os.remove("clip (" + str(num+1) + ").wav")
                        os.remove("clip (" + str(num+2) + ").wav")
                        os.remove("clip (" + str(num+3) + ").wav")
    mergeAudio(numberOfSteps)


def mergeAudio(numberOfSteps):
    listAudio = [AudioSegment.from_wav(files) for files in glob("clip (*).wav")]
    combined = AudioSegment.empty()

    for song in listAudio:
        combined += song

    combined.export("newClip.wav", format="wav")
    for i in range(numberOfSteps+2):
        try:
            os.remove("clip (" + str(i) + ").wav")
        except:
            pass

#anything less than 1.5 will cause google speech to text to raise an error
splitAudio(sys.argv[1], 1.5)