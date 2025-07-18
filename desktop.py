import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import wikipedia
import pyjokes
import wolframalpha
import requests

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) 

def speak(audio):
    """Convert text to speech"""
    engine.say(audio)
    engine.runAndWait()

def take_command():
    """Take voice command from user"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query.lower()

def greet():
    """Greet the user based on time"""
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your desktop assistant. How can I help you?")

if __name__ == "__main__":
    greet()
    while True:
        query = take_command()
        
      
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(results)
        
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
            
        elif 'open google' in query:
            webbrowser.open("google.com")
            
        elif 'what time' in query:
            str_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {str_time}")
            
        elif 'date today' in query:
            today = datetime.date.today().strftime("%B %d, %Y")
            speak(f"Today's date is {today}")
            
        elif 'joke' in query:
            speak(pyjokes.get_joke())
            
        elif 'calculate' in query:
            app_id = "YOUR_WOLFRAMALPHA_APP_ID"
            client = wolframalpha.Client(app_id)
            indx = query.lower().split().index('calculate')
            query = query.split()[indx+1:]
            res = client.query(' '.join(query))
            answer = next(res.results).text
            speak("The answer is " + answer)
            
        elif 'weather' in query:
            api_key = "YOUR_OPENWEATHERMAP_API_KEY"
            speak("Which city?")
            city = take_command()
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            complete_url = base_url + "appid=" + api_key + "&q=" + city
            response = requests.get(complete_url)
            x = response.json()
            if x["cod"] != "404":
                weather = x["main"]
                temp = round(weather["temp"] - 273.15, 2)
                pressure = weather["pressure"]
                humidity = weather["humidity"]
                speak(f"Weather in {city}: Temperature {temp}°C, "
                      f"Atmospheric Pressure {pressure} hPa, "
                      f"Humidity {humidity}%")
            else:
                speak("City not found")
                
        elif 'open notepad' in query:
            os.system("notepad.exe")
            
        elif 'shutdown' in query:
            os.system("shutdown /s /t 1")
            
        elif 'restart' in query:
            os.system("shutdown /r /t 1")
            
        elif 'sleep' in query:
            speak("Goodbye!")
            break
