import speech_recognition as sr
import pydub as pd
import math
from playsound import playsound
from os import path
import wave
import soundfile as sf
import librosa

r = sr.Recognizer()

audiopath = path.join(path.dirname(__file__), "files/test.wav")

audioclip = []

loadedaudio = []
reconaudio = []


def recognize_clips(step, repeat):
    global audioclip, loadedaudio, reconaudio
    for i in range(repeat):
        print(audioclip[i])
        with sr.AudioFile(audioclip[i]) as source:
            loadedaudio[i] = r.record(source)
            reconaudio[i] = r.recognize_google(loadedaudio[i])
            print(str(i)+"   "+reconaudio[i])


def populate_times(path, time):
    global audioclip, loadedaudio, reconaudio
    audio = pd.AudioSegment.from_file(audiopath, "wav")
    step = time * 1000
    repeat = audio.duration_seconds % step
    carry = repeat - math.floor(repeat)
    repeat = math.floor(repeat)
    for i in range(repeat):
        export = audio[i * step: (i+1) * step].export("clip"+str(i)+".wav")
        audioclip.append(export)
    print(type(step))
    print(type(repeat))
    #  recognize_clips(step, repeat)


populate_times(audiopath, 5)

# playsound(audiopath)
