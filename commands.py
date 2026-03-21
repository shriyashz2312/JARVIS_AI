import webbrowser
import datetime
import sys


class CommandProcessor:
    def __init__(self, voice):
        self.voice = voice

    def process(self, text):
        if not text:
            return

        text = text.lower().strip()

        # --- TIME ---
        if "time" in text:
            now = datetime.datetime.now().strftime("%I:%M %p")
            self.voice.speak(f"The time is {now}")
            return

        # --- DATE ---
        if "date" in text:
            today = datetime.datetime.now().strftime("%B %d, %Y")
            self.voice.speak(f"Today's date is {today}")
            return

        # --- OPEN BROWSER ---
        if "open browser" in text or "open chrome" in text:
            self.voice.speak("Opening browser")
            webbrowser.open("https://www.google.com")
            return

        # --- OPEN YOUTUBE ---
        if "open youtube" in text or "youtube" in text:
            self.voice.speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")
            return

        # --- OPEN GMAIL ---
        if "open gmail" in text:
            self.voice.speak("Opening Gmail")
            webbrowser.open("https://mail.google.com")
            return

        # --- GOOGLE SEARCH ---
        if text.startswith("search"):
            query = text.replace("search", "").strip()
            if query:
                self.voice.speak(f"Searching for {query}")
                webbrowser.open(f"https://www.google.com/search?q={query}")
            else:
                self.voice.speak("What should I search for?")
            return

        # --- HELLO ---
        if "hello" in text or "hi" in text:
            self.voice.speak("Hello. I am online.")
            return

        # --- EXIT ---
        if "exit" in text or "quit" in text or "stop" in text:
            self.voice.speak("Goodbye.")
            sys.exit()

        # --- FALLBACK ---
        self.voice.speak("I heard you, but this command is not programmed yet.")
