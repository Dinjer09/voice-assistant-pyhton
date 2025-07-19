import speech_recognition as sr
import pyttsx3
import os
from datetime import datetime
import time

# Initialize the speech recognizer and engine
recognizer = sr.Recognizer()
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8

engine = pyttsx3.init()
engine.setProperty('rate', 180)

# Set Dinjer's voice properties
#voices = engine.getProperty('voices')
#engine.setProperty('voice', voices[0].id) # Change the index to select different voices
#engine.setProperty('rate', 180) # Speed of speech (Count in words per minute)

def print_microphones():
    """Helper to list available microphones"""
    print("Available microphones:")
    for i, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"{i}: {name}")

def speak(text):
    """Make Dinjer speak the given text"""
    print(f"DINJER: {text}") #Print to console with Dinjer prefix
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.3)  # Short pause after speaking
    
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=None, phrase_time_limit=10)
            text = recognizer.recognize_google(audio)
            print(f"You (voice): {text}")
            return text
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            return ""
        
def greet():
    """Greet the user based on time of the day"""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        speak("Good morning, sir! Dinjer here, ready to assist. How can I help you today?")
    elif 12 <= hour < 18:
        speak("Good afternoon, sir! Dinjer online. Is there any task you want to assign me?")
    else:
        speak("Good evening! I'm Dinjer. What can I do for you?")
        
def main():
    greet()  # Start with a greeting
    
    while True:
        command = listen()
        
        if command:
            if "hello" in command:
                speak("Hello there! How are you doing?")
            elif "goodbye" in command or "exit" in command or "bye" in command:
                speak("Goodbye! Have a wonderful day!")
                break
            elif "time" in command:
                current_time = datetime.now().strftime("%I:%M %p")
                speak(f"The current time is {current_time}")
            elif "date" in command:
                current_date = datetime.now().strftime("%A, %B %d, %Y")
                speak(f"Today is {current_date}")
            elif "your name" in command:
                speak("I am Dinjer, your personal assistant.")
            else:
                speak(f"I heard you say: {command}. I'm still learning more commands!")

if __name__ == "__main__":
    main()