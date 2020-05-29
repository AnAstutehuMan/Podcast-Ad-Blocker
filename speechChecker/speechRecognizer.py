import speech_recognition as sr
import pydub as pd
import math
from playsound import playsound
from os import path

r = sr.Recognizer()

audiopath = path.join(path.dirname(__file__),"files/test.wav")

audioclip = []

loadedaudio = []
reconaudio = []

def recognize_clips(step, repeat):
    global audioclip, loadedaudio, reconaudio
    for i in range(repeat):
        with sr.AudioFile(audioclip[i]) as source:
            loadedaudio.append(r.record(source))
            reconaudio.append(r.recognize_google(loadedaudio[i]))
            print("Time : "+str(i*step/1000)+" - "+str((i+1)*step/1000)+"| Words : "+str(reconaudio[i]))

def populate_times(path, time):
    global audioclip, loadedaudio, reconaudio
    audio = pd.AudioSegment.from_file(audiopath, "wav")
    step = time * 1000
    repeat = audio.duration_seconds / time
    carry =  repeat - math.floor(repeat)
    repeat = math.floor(repeat)
    for i in range(repeat):
        export = audio[i * step: (i+1) * step].export("clip"+str(i)+".wav", format = "wav")
        audioclip.append("clip"+str(i)+".wav")
    recognize_clips(step, repeat)


populate_times(audiopath, 1.5)

#playsound(audiopath)

