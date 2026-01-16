import speech_recognition as sr
import pyttsx3
import datetime
import pywhatkit

# Initialize speech engine
engine = pyttsx3.init()

def talk(text):
    engine.say(text)
    engine.runAndWait()

def listen_command():
    listener = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("🎤 Listening...")
            listener.adjust_for_ambient_noise(source)
            audio = listener.listen(source)
            command = listener.recognize_google(audio)
            command = command.lower()
            print(f"✅ You said: {command}")
    except sr.UnknownValueError:
        print("❌ Sorry, I did not catch that.")
        command = ""
    except sr.RequestError:
        print("❌ Service is down.")
        command = ""
    return command

def run_assistant():
    command = listen_command()

    if 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        talk(f"The current time is {current_time}")

    elif 'open youtube' in command:
        talk("Opening YouTube")
        pywhatkit.playonyt("YouTube")  
     
    elif 'search' in command:
        topic = command.replace('search', '')
        talk(f"Searching for {topic}")
        pywhatkit.search(topic)
     
    elif 'hello' in command or 'hi' in command:
        talk("Hello! How can I assist you today?")
     
    elif 'stop' in command or 'exit' in command:
        talk("Goodbye!")
        exit()

    else:
        talk("Sorry, I did not understand. Please say it again.")

# Run in loop
while True:
    run_assistant()
