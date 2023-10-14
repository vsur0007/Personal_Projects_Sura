import speech_recognition as sr
import pyaudio

s = sr.Recognizer()

with sr.Microphone() as Source:
    print("Speak Now : ")
    audio = s.listen(Source)

    try:
        text = s.recognize_google(audio)
        print('You said : {}'.format(text))
    except:
        print("Sorry unable to recognize your voice")

