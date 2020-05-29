import math
import wave
import pydub as pd
import speech_recognition as sr
from pydub import AudioSegment

import soundfile as sf

def splitAudio(filePath, interval):
    #Mutiformat support
    audio = pd.AudioSegment.from_file(filePath, "wav")
    amountToStep = interval * 1000
    numberOfSteps = math.floor(audio.duration_seconds / interval)

    #More simple spliting
    for i in range(numberOfSteps):
        AudioSegment.from_wav(filePath)[i * amountToStep:(i+1) * amountToStep].export("clip" + str(i) + ".wav", format="wav")
    
    recognizeAudio(filePath, numberOfSteps)


def recognizeAudio(filePath, numberOfSteps):
    r = sr.Recognizer()
    f = open("transcript.json", "w+")
    f.write("{")
    for i in range(numberOfSteps):
        with sr.AudioFile("clip" + str(i) + ".wav") as source:
            f.write('"'+str(i)+'":"'+r.recognize_google(r.record(source))+'"')
        if i != numberOfSteps - 1:
            f.write(','+"\n")
    f.write("}")
    f.close()


splitAudio('test.wav', 1.5)
