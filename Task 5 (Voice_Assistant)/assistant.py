import os
import json #
import ctypes #
import random #
import winshell #
import pyjokes # Jokes
import pygetwindow as gw #
import datetime # Date and Time
import win32com.client as wincl #
from urllib.request import urlopen #
import webbrowser # perform websearch
import requests # Get and Post Request
import wikipedia # get info from Wikipedia
import pyttsx3 # Conversion of text to Speech
import requests # making GET and POST requests.
import wikipedia # get information from Wikipedia
import subprocess # get system subprocess details
from urllib.request import urlopen # open web page
import wolframalpha # reponde you at computer expert level
from twilio.rest import Client # Make calls and send messages
from bs4 import BeautifulSoup # scrape information form web page
import speech_recognition as sr # assistant recognizes your voice
from ecapture import ecapture as capture # capture image from the camera

active = False  # Flag to indicate whether the voice assistant is active

# Microsoft speech application platform
engine = pyttsx3.init('sapi5')
voice = engine.getProperty('voices')
engine.setProperty('voice', voice[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def greet():
    hour = int(datetime.datetime.now().hour)
    if hour == 0 and hour < 12:
        speak("Good Morning Sir !, How can I help you?")
    elif hour == 12 and hour < 18:
        speak("Good Afternoon sir!,  How can I help you?")
    else:
        speak("Good Evening sir!,  How can I help you?")


def get_time():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    response = f"The current time is {current_time}"
    speak(response)

def web_search(query):
    response = f"Searching the web for {query}"
    speak(response)
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)

def application_open(application_name):
    try:
        speak(f"opening {application_name.strip('.exe')}")
        subprocess.Popen([application_name], shell=True)
    except Exception as e:
        speak(f"Sorry, I couldn't open {application_name}. Please check if the application is installed.")

def toggle_voice_assistant_state():
    global active
    active = not active
    state_message = "active" if active else "inactive"
    speak(f"The voice assistant is now {state_message}.")

def close(application_name):
    if application_name:
        application_name.close()
        speak(f"Closed the {application_name.title}.")
    else:
        speak("No active window found.")


def takeCommand():
    
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language = 'en-in')
        print(f"User said: {query}\n")

    except sr.UnknownValueError:
        print("Sorry, Unable to Recognize your voice.")
        return "None"
 
    except sr.RequestError:
        speak("There was an error connecting to the Google API. Please check your internet connection.")
        return "None"
    
    return query

if __name__ == "__main__":
    clear = lambda:os.system('cls') # cleans the terminal
    clear()

    while True:
        # global active
        query = takeCommand().lower()

        if active:
            if "hi alex" in query:
                greet()
                
            elif "time" in query:
                get_time()

            elif "alex find" in query:
                query = query.split("alex")[-1].strip()
                web_search(query)

            elif "search" in query:
                query = query.split("search")[-1].strip()
                web_search(query)

            elif "open youtube" in query:
                speak("Opening YouTube\n")
                webbrowser.open('youtube.com')
            
            elif 'play music' in query or 'play song' in query:
                speak('Here you go with music')
                music_dir = "C:/Users/alway/Music/Music"
                songs = os.listdir(music_dir)
                print(songs)
                r = os.startfile(os.path.join(music_dir, songs[random.randint(0,len(songs)-1 )]))
                toggle_voice_assistant_state()
                

            elif 'search' in query or 'play' in query:
                query = query.replace("search", "") 
                query = query.replace("play", "")          
                webbrowser.open(query)
            
            elif 'how are you' in query:
                speak("I am fine, Thank you")
                speak("How are you, Sir")
            
            elif "goodbye alex" in query:
                speak("Goodbye sir!, Thanks for giving me your time")
                exit()
            
            elif 'fine' in query or "good" in query:
                speak("It's good to know that you'r fine")

            elif "what's your name" in query or "What is your name" in query:
                speak("My friends call me, Alex")
                print("My friends call me Alex")
            
            elif "who made you" in query or "who created you" in query or "who devloped you"  in query:
                speak("I have been created by Sonu.")
            
            elif 'tell me a joke' in query:
                speak(pyjokes.get_joke())

            elif "calculate" in query: 
                app_id = "6XHK2Y-RVRJ7QUVV7"
                client = wolframalpha.Client(app_id)
                indx = query.lower().split().index('calculate') 
                query = query.split()[indx + 1:] 
                res = client.query(' '.join(query)) 
                answer = next(res.results).text
                print("The answer is " + answer) 
                speak("The answer is " + answer) 
            
            elif "alex open" in query:
                application_name = query.split("open")[-1].strip()
                application_open(f"{application_name}.exe")

            elif "close my active window" in query:
                active_window = gw.getActiveWindow()
                close(active_window)
            
            elif "why you came to world" in query:
                speak("Thanks to Sonu. Here I'm to assist you and further it's a secret")
                
            elif "stop listening" in query:
                toggle_voice_assistant_state()
            
            elif 'is love' in query:
                speak("It is 7th sense that destroy all other senses")
            
            elif 'change background' in query:
                ctypes.windll.user32.SystemParametersInfoW(20,0,"C:/Users/alway/Pictures/Pikachu.jpg",0)
                speak("Background changed successfully")

            elif 'empty recycle bin' in query:
                try:
                    winshell.recycle_bin().empty(confirm = False, show_progress = False, sound = True)
                    speak("Recycle Bin Recycled")
                except Exception as e:
                    print(e)
                    speak("No trash to empty recycle bin")
            
            elif "click a picture" in query or "take a photo" in query:
                capture.capture(0, "Jarvis Camera ", f"{datetime.datetime.now()}.jpg")
            
            elif "where is" in query:
                query = query.replace("where is", "")
                location = query
                speak("User asked to Locate")
                speak(location)
                webbrowser.open("https://www.google.com/maps/place/" + location + "")

            elif 'wikipedia' in query:
                speak("Searching Wikipedia")
                results = wikipedia.summary(query, sentances = 3)
                speak("According to Wikipedia")
                print(results)
                speak(result)

            elif "send message " in query:
                # Twilio to send message (Twilio account)
                account_sid ='ACdece749276b895760ee28d0934ee9b4b'
                auth_token ='f5f09342b9a79f881eaf0137ccc0b15a'
                client = Client(account_sid, auth_token)
 
                message = client.messages.create(
                                    body = query.split("send message ")[-1],
                                    from_='+14254092050',
                                    to ='+919109538258'
                                )
 
                print(message.sid)
            
            elif "write a note" in query:
                speak("What should i write, sir")
                note = takeCommand()
                file = open('jarvis.txt', 'a')
                # speak("Sir, Should i include date and time")
                # snfm = takeCommand()
                # if 'yes' in snfm or 'sure' in snfm:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                file.write(strTime)
                file.write(" :- ")
                file.write(note)
                # else:
                #     file.write(note)
            
            elif "show the note" in query:
                speak("Showing Notes")
                file = open("jarvis.txt", "r") 
                print(file.read())
                speak(file.read(6))

            elif "what is" in query or "who is" in query:
             
                client = wolframalpha.Client("6XHK2Y-RVRJ7QUVV7")
                res = client.query(query)
                try:
                    print (next(res.results).text)
                    speak (next(res.results).text)
                except StopIteration:
                    print ("No results")

            elif "weather" in query:             
                # to get API of Open weather 
                api_key = "b834d100667d85b9dc5c25d3d4f49894"
                base_url =  "https://api.openweathermap.org/data/2.5/weather"
                speak(" City name ")
                print("City name : ")
                city_name = takeCommand().lower()
                params = {"q": city_name, "appid": api_key}
                response = requests.get(base_url, params=params) 
                x = response.json() 
                
                if response.status_code == 200: 
                    y = x["main"] 
                    current_temperature = y["temp"] 
                    current_pressure = y["pressure"] 
                    current_humidiy = y["humidity"] 
                    z = x["weather"] 
                    weather_description = z[0]["description"] 
                    print(" Temperature (in kelvin unit) = " +str(current_temperature)+"\n atmospheric pressure (in hPa unit) ="+str(current_pressure) +"\n humidity (in percentage) = " +str(current_humidiy) +"\n description = " +str(weather_description)) 
                    speak(f"It's {int (current_temperature * (-457.87))} with {weather_description}, atmopheric presure with {current_pressure} and humidity with {current_humidiy}")
                else: 
                    speak("Error fetching weather data.")

            elif 'news' in query:
             
                try: 
                    jsonObj = urlopen('''https://newsapi.org/v1/articles?source=the-times-of-india&sortBy=top&apiKey=53ecf92067264e08882e2aa66cdc8e22''')
                    data = json.load(jsonObj)
                    i = 1
                    
                    speak('here are some top news from the times of india')
                    print('''=============== TIMES OF INDIA ============'''+ '\n')
                    
                    for item in data['articles'][:5]:
                        
                        print(str(i) + '. ' + item['title'] + '\n')
                        print(item['description'] + '\n')
                        speak(str(i) + '. ' + item['title'] + '\n')
                        i += 1
                except Exception as e:
                    print(str(e))
                    speak("Error fetching weather data.")

            elif "restart" in query:
                subprocess.call(["shutdown", "/r"])
             
            elif "hibernate" in query or "sleep" in query:
                speak("Hibernating")
                subprocess.call("shutdown / h")
    
            elif "log off" in query or "sign out" in query:
                speak("Make sure all the application are closed before sign-out")
                time.sleep(5)
                subprocess.call(["shutdown", "/s"])

            elif 'lock my window' in query:
                speak("locking the device")
                ctypes.windll.user32.LockWorkStation()
            
            elif "restart" in query:
                subprocess.call(["shutdown", "/r"])

            else:
                speak("Sorry, I don't understand that query. Try again.")
        else:
            if "hi alex" in query:
                toggle_voice_assistant_state()
                greet()