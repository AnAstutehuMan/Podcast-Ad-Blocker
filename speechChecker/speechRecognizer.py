import speech_recognition as sr

r = sr.Recognizer()

clip = sr.AudioFile('speechChecker\clip.wav')

with clip as source:
    audio = r.record(source)

print(r.recognize_google(audio))