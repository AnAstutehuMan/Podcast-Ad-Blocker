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


def recognize_clips(step, repeat):
    global audioclip, loadedaudio, reconaudio
    for i in range(repeat):
        with sr.AudioFile(audioclip[i]) as source:
            loadedaudio.append(r.record(source))
            reconaudio.append(r.recognize_google(loadedaudio[i]))
            print("Time : "+str(i*step/1000)+" - " +
                  str((i+1)*step/1000)+"| Words : "+str(reconaudio[i]))


def populate_times(path, time):
    global audioclip, loadedaudio, reconaudio
    audio = pd.AudioSegment.from_file(audiopath, "wav")
    step = time * 1000
    repeat = audio.duration_seconds / time
    carry = repeat - math.floor(repeat)
    repeat = math.floor(repeat)
    for i in range(repeat):
        export = audio[i * step: (i+1) * step].export("clip" +
                                  str(i)+".wav", format="wav")
        audioclip.append("clip"+str(i)+".wav")
    recognize_clips(step, repeat)


populate_times(audiopath, 1.5)

# playsound(audiopath)


# Saketh: rewrote the code


r = sr.Recognizer()
f = open("transcript.txt", "a")

def splitAudio(filePath, interval):
    intervalOne = 0
    intervalTwo = interval * 1000

    numberOfSplits = math.floor(AudioSegment.from_wav(
        filePath).duration_seconds / interval)

    for i in range(numberOfSplits):
        AudioSegment.from_wav(filePath)[intervalOne:intervalTwo].export(
            "clip" + str(i) + ".wav", format="wav")
        intervalOne = intervalTwo
        intervalTwo = intervalTwo + (interval * 1000)

    recognizeAudio(filePath, numberOfSplits)


def recognizeAudio(filePath, numberOfSplits):
    for i in range(numberOfSplits):
        with sr.AudioFile("clip" + str(i) + ".wav") as source:
            f.write(r.recognize_google(r.record(source))))
    f.close()


splitAudio('clip.wav', 2)
