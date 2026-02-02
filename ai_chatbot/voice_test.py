import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr

fs = 16000
seconds = 5

print("🎙️ Speak now (5 seconds)...")

recording = sd.rec(
    int(seconds * fs),
    samplerate=fs,
    channels=1,
    dtype='int16'   # ⭐ IMPORTANT FIX
)
sd.wait()

wav.write("voice.wav", fs, recording)

r = sr.Recognizer()
with sr.AudioFile("voice.wav") as source:
    audio = r.record(source)

try:
    text = r.recognize_google(audio)
    print("You said:", text)
except sr.UnknownValueError:
    print("Sorry, could not understand audio")
except sr.RequestError as e:
    print("API error:", e)
