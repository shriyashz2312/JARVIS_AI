import speech_recognition as sr
import time


class JarvisListener:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        self.running = True

    def listen_once(self):
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
            audio = self.recognizer.listen(source)

        try:
            text = self.recognizer.recognize_google(audio)
            print("🧠 Heard:", text)
            return text.lower()
        except:
            return ""

    def stop(self):
        self.running = False
