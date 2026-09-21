import speech_recognition as sr
import pyttsx3
import subprocess
import pyautogui
import keyboard
import screen_brightness_control as sbc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import tkinter as tk
import requests
import webbrowser
import psutil
import datetime
import os
import sys

# Text-to-Speech Engine
engine = pyttsx3.init()
engine.setProperty('rate', 175)

# ChromeDriver Path (Update this with the *actual* path to your chromedriver.exe)
CHROMEDRIVER_PATH = r"chromedriver.exe"  # IMPORTANT: Change this to your actual path

# Name to number dictionary
contacts = {
    "alpha": "91906723191",
    "boss": "919422688537"
}

def speak(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Consider adjusting for noise
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)
        return command
    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""
    except Exception as e: #Catch All other exceptions
        print(f"An unexpected error occurred: {e}")
        return ""

def open_chrome():
    global driver
    options = Options()
    options.add_experimental_option("detach", True)
    service = Service(CHROMEDRIVER_PATH)
    try:
        driver = webdriver.Chrome(service=service, options=options)
    except Exception as e:
        speak(f"Error opening Chrome: {e}")
        return None  # Important: Return None on error
    return driver

def send_whatsapp_message(number, message):
    webbrowser.open(f"https://wa.me/{number}?text={message}")
    speak(f"Opening WhatsApp chat with {number}")

def get_weather(city):
    url = f"https://wttr.in/{city}?format=3"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        weather = response.text
        print(weather)
        speak(weather)
    except requests.exceptions.RequestException as e:
        speak(f"Error getting weather: {e}")

def get_battery_level():
    try:
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            print(f"Battery level is {percent}%")
            speak(f"Battery level is {percent} percent")
        else:
            print("Unable to get battery status.")
            speak("Unable to get battery status.")
    except Exception as e:
        speak(f"Error getting battery level: {e}")

def get_datetime():
    now = datetime.datetime.now()
    date = now.strftime("%A, %d %B %Y")
    time = now.strftime("%I:%M %p")
    print(f"Date: {date}, Time: {time}")
    speak(f"Today is {date} and the time is {time}")

def take_screenshot():
    file_path = "screenshot.png"
    try:
        pyautogui.screenshot(file_path)
        print("Screenshot saved as screenshot.png")
        speak("Screenshot taken")
    except Exception as e:
        speak(f"Error taking screenshot: {e}")

def open_application(app_name):
    """Opens the specified application.

    Args:
        app_name: The name of the application to open (e.g., "WhatsApp", "Visual Studio Code", "Word").
    """
    app_name_lower = app_name.lower()
    possible_paths = []

    if "whatsapp" in app_name_lower:
        possible_paths = [
            "C:\\Users\\YourUsername\\AppData\\Local\\WhatsApp\\WhatsApp.exe",
            "C:\\Program Files\\WhatsApp\\WhatsApp.exe",
            "whatsapp"
        ]
    elif "visual studio code" in app_name_lower or "code" in app_name_lower:
        possible_paths = [
            "C:\\Users\\YourUsername\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
            "C:\\Program Files\\Microsoft VS Code\\Code.exe",
            "code"
        ]
    elif "word" in app_name_lower:
        possible_paths = [
            "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
            "C:\\Program Files\\Microsoft Office\\Office16\\WINWORD.EXE",
            "WINWORD.EXE"
        ]
    else:
        speak(f"I don't know how to open {app_name}.")
        return

    for path in possible_paths:
        if os.path.exists(path):
            try:
                subprocess.Popen(path)
                speak(f"Opening {app_name}")
                return
            except Exception as e:
                speak(f"Error opening {app_name} from {path}: {e}")
        else:
            # try to open directly
            try:
                subprocess.Popen(path)
                speak(f"Opening {app_name}")
                return
            except FileNotFoundError:
                pass #ignore and try next path
            except Exception as e:
                speak(f"Error opening {app_name} using {path}: {e}")

    speak(f"I couldn't find {app_name} on your system.")
def execute_command(command):
    global driver

    if "open youtube" in command:
        speak("Opening YouTube")
        if not driver:
            driver = open_chrome() # open_chrome now returns the driver
            if not driver:
                return  # Exit if Chrome couldn't open
        driver.get("https://www.youtube.com")

    elif "search" in command:
        query = command.replace("search", "").strip()
        speak(f"Searching for {query}")
        if not driver:
            driver = open_chrome()
            if not driver:
                return
        driver.get(f"https://www.google.com/search?q={query}")

    elif "open google" in command:
        speak("Opening Google")
        if not driver:
           driver = open_chrome()
           if not driver:
                return
        driver.get("https://www.google.com")

    elif "shutdown" in command:
        speak("Shutting down")
        try:
            subprocess.call("shutdown /s")
        except Exception as e:
            speak(f"Error shutting down: {e}")

    elif "restart" in command:
        speak("Restarting")
        try:
            subprocess.call("shutdown /r")
        except Exception as e:
            speak(f"Error restarting: {e}")

    elif "volume up" in command:
        pyautogui.press("volumeup")

    elif "volume down" in command:
        pyautogui.press("volumedown")

    elif "mute" in command:
        pyautogui.press("volumemute")

    elif "unmute" in command:
        pyautogui.press("volumemute")

    elif "brightness up" in command:
        try:
            sbc.set_brightness("+10")
            speak("Brightness increased")
        except Exception as e:
            speak(f"Error adjusting brightness: {e}")

    elif "brightness down" in command:
        try:
            sbc.set_brightness("-10")
            speak("Brightness decreased")
        except Exception as e:
             speak(f"Error adjusting brightness: {e}")

    elif "pause" in command:
        pyautogui.press("space")

    elif "play" in command:
        pyautogui.press("space")

    elif "scroll up" in command:
        print("Received scroll up command")  # Debugging
        try:
            pyautogui.scroll(500)
            speak("Scrolling up")
        except Exception as e:
            print(f"Error scrolling up: {e}")  # Debugging
            speak("Failed to scroll up")

    elif "scroll down" in command:
        print("Received scroll down command")  # Debugging
        try:
            pyautogui.scroll(-500)
            speak("Scrolling down")
        except Exception as e:
            print(f"Error scrolling down: {e}")  # Debugging
            speak("Failed to scroll down")

    elif "dark mode" in command:
        keyboard.press_and_release('win + ctrl + c')

    elif "light mode" in command:
        keyboard.press_and_release('win + ctrl + c')

    elif "open whatsapp" in command:
        speak("Opening WhatsApp in Chrome")
        if not driver:
            driver = open_chrome()
            if not driver:
                return
        driver.get("https://web.whatsapp.com/")

    elif "open visual studio code" in command:
        open_application("Visual Studio Code")

    elif "open word" in command:
        open_application("Word")

    elif "send message to" in command:
        try:
            parts = command.split("send message to")[-1].strip()
            if "saying" in parts:
                number, message = parts.split("saying")
                number = number.strip().replace(" ", "")
                message = message.strip()
                send_whatsapp_message(number, message)
            else:
                speak("Please specify the message to send using the format: 'send message to <contact name/number> saying <your message>'")
        except Exception as e:
            speak(f"Could not send the message.  Error: {e}")

    elif "call" in command:
        contact_found = False
        for name, number in contacts.items(): #changed to items()
            if name in command:
                send_whatsapp_message(number, "")
                contact_found = True
                break # Added break
        if not contact_found:
            speak("Contact not found")

    elif "weather in" in command:
        city = command.replace("weather in", "").strip()
        get_weather(city)

    elif "battery level" in command:
        get_battery_level()

    elif "what's the time" in command or "what's the date" in command:
        get_datetime()

    elif "take screenshot" in command:
        take_screenshot()

    elif "stop" in command or "exit" in command:
        speak("Goodbye")
        if driver: # added this
            driver.quit()
        sys.exit() # Use sys.exit() for a cleaner exit

# GUI Interface
root = tk.Tk()
root.title("Echo Voice Assistant")
root.geometry("800x400")
label = tk.Label(root, text="Welcome to Echo Voice Assistant!", font=("Arial", 14))
label.pack(pady=20)

# Start assistant
def start_assistant():
    root.withdraw()
    speak("Echo initialized. Listening now.")
    global driver
    driver = None #initialize
    while True:
        command = listen()
        if command:
            execute_command(command)

btn = tk.Button(root, text="Start Echo", command=start_assistant, font=("Arial", 12))
btn.pack(pady=20)

root.mainloop()
