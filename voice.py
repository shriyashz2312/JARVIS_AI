import pyttsx3


class JarvisVoice:
    def speak(self, text):
        print("🗣️ Jarvis speaking:", text)

        engine = pyttsx3.init()   # NEW engine every time
        engine.setProperty("rate", 170)
        engine.setProperty("volume", 1.0)

        engine.say(text)
        engine.runAndWait()
        engine.stop()
