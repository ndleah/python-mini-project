import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import pyautogui
import time
import os
import pywhatkit
import spotipy
from spotipy.oauth2 import SpotifyOAuth
#from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
#import python_weather
engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')

engine.setProperty('voice',voices[1].id)



def speak(audio):
    engine.say(audio)
    engine.runAndWait()
def wishMe():
    hour=int(datetime.datetime.now().hour)
    if hour>=7 and hour<12:
        speak("Good Morning")
    elif hour>=12 and hour<18:
        speak("Good Afternoon")
    elif hour>=18 and hour<21:
        speak("Good Evening!")
    else:
        speak("Good night")
    speak("Hello I am your personal desktop assistant. Please tell me how may i help you ")
def takeCommand():
    '''It takes microphone input from the user and returns string output'''
    r=sr.Recognizer()
    with sr.Microphone() as source:
        speak("Go Ahead, I am listening to you......")
        print("Go Ahead, I am listening to you......")
        r.pause_threshold = 1
        audio=r.listen(source)

    try:
        print("Recognizing")
        
        query=r.recognize_google(audio, language='hi-in')
        print(f"User said:{query}\n")
    except Exception as e:
        #print(e)
        speak("sorry i can't able to hear you Say that again please....")
        return "None"
    return query



if __name__=="__main__":
    wishMe()
    while True:
        query=takeCommand().lower()
        sites=[["youtube","https://youtube.com"],["wikipedia","https://www.wikipedia.com"],["google","https://google.com"]]
        if 'wikipedia' in query:
            speak('Searching wikipedia...')
            query = query.replace("wikipedia", "").strip()
            speak("Please provide a topic to search for on Wikipedia.")
            mkv = takeCommand()
            speak(f"playing {mkv}")
            print(f"playing {mkv}...")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
       
        
                

        elif 'open youtube' in query:
             speak('Which youtube video do you want to watch ?')
             mkv = takeCommand()
             speak(f"playing {mkv}")
             print(f"playing {mkv}...")
             pywhatkit.playonyt(mkv, open_video=True)
        elif 'open google' or 'search on google' in query:
             webbrowser.open("https://google.com")
        elif 'open stackoverflow' in query:
            webbrowser.open("https://stackoverflow.com")
        
        elif 'open leetcode' in query:
            webbrowser.open("leetcode.com")
        elif "the time" in query:
            strfTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Okay now its {strfTime}")
        elif 'open code' in query:
            codePath="C:\\Program Files\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)
        
        elif 'stop and exit' in query:
            False
        break

    #logic for executing task based on query