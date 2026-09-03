import os
import sys
import time
import datetime
import webbrowser

def speak(audio: str):
    """Speak text audio using pyttsx3 or fallback print."""
    try:
        import pyttsx3
        try:
            engine = pyttsx3.init('sapi5')
        except Exception:
            engine = pyttsx3.init()
        engine.say(audio)
        engine.runAndWait()
    except Exception:
        print(f"🔊 Assistant: {audio}")

def wish_me():
    """Greet user based on current hour of day."""
    hour = int(datetime.datetime.now().hour)
    if 5 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    elif 18 <= hour < 21:
        speak("Good Evening!")
    else:
        speak("Good Night!")
    speak("Hello, I am your personal desktop assistant. How may I help you today?")

def take_command() -> str:
    """Take microphone audio input or fallback console prompt."""
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        with sr.Microphone() as source:
            speak("Go ahead, I am listening to you...")
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source, timeout=5, phrase_time_limit=5)

        print("Recognizing speech...")
        query = r.recognize_google(audio, language='en-US')
        print(f"User said: {query}\n")
        return query.lower()
    except Exception as e:
        print(f"Notice: Microphone input unavailable or timed out ({e}).")
        return "none"

def main():
    wish_me()
    while True:
        query = take_command()
        if query == "none":
            query = input("Enter command prompt manually (or 'exit' to quit): ").strip().lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            topic = query.replace("wikipedia", "").strip()
            if not topic:
                topic = "Python (programming language)"
            try:
                import wikipedia
                results = wikipedia.summary(topic, sentences=2)
                speak("According to Wikipedia:")
                print(results)
                speak(results)
            except Exception as e:
                speak(f"Could not retrieve Wikipedia summary for '{topic}'.")

        elif 'open youtube' in query:
            speak('Opening YouTube...')
            webbrowser.open("https://youtube.com")

        elif 'open google' in query or 'search on google' in query:
            speak('Opening Google...')
            webbrowser.open("https://google.com")

        elif 'open stackoverflow' in query:
            speak('Opening StackOverflow...')
            webbrowser.open("https://stackoverflow.com")

        elif 'open leetcode' in query:
            speak('Opening LeetCode...')
            webbrowser.open("https://leetcode.com")

        elif "the time" in query or "current time" in query:
            strf_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The current time is {strf_time}")

        elif 'stop' in query or 'exit' in query or 'quit' in query:
            speak("Goodbye! Have a great day!")
            break

if __name__ == "__main__":
    main()