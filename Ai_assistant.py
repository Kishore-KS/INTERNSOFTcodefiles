import speech_recognition as sr
import os
import datetime
import subprocess
import json
import wolframalpha
import requests
import webbrowser
import wikipedia
import pyttsx3

print("Loading your AI assistant")

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty("voice", 'voices[0].id')

def speak(text):
    engine.say(text)
    engine.runAndWait()
    print(text)
    
def wishMe():
    speak("Hello, I am your personal AI Assistant")
    
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("I am listening")
        #Listening to voice command
        audio = r.listen(source)
        try:
            #Recognizing voice command
            stat = r.recognize_google(audio, language='en-in')
            print(stat)
        except Exception as e:
            print("Exception: ",e)
            speak("Pardon")
            return "None"
        return stat

def news():
    main_url = "http://newsapi.org/v2/top-headlines?country=in&apiKey=8ca0760cfb7542ce86b1c790e362622d"
    #fetching data
    open_bbc_page = requests.get(main_url).json() 
    #getting all articles 
    article = open_bbc_page["articles"]       
    #printing all trending news  
    for i in range(5):
        speak(article[i]["title"])          
        speak(article[i]["description"])
        print(article[i]["title"],"\n",article[i]["url"])
        
def weather():
    city = 'bangalore'
    if "at" in stat:
        #Extrcting city name
        city = stat[stat.find(" at ")+4:]
    else:
        url = "https://api.openweathermap.org/data/2.5/weather?" + "appid=" + "8ef61edcf1c576d65d836254e11ea420" + "&q=" + city
        response = requests.get(url)
        #Fetching data
        x = response.json()
        #Checking for 404 error
        if x["cod"] != 404:
            weather_disc = "The weather is as follows The temperature is " + str(x['main']['temp']) + " and the Humidity is " + str(x['main']['humidity']) + " Expect some " + str(x['weather'][0]['main'])
            speak(weather_disc)
        else:
            speak("Can you repeat?")
    

if __name__ == '__main__':
    wishMe()
    while True:
        speak("How can I help you?")
        stat = takeCommand().lower()
        if stat == 0:
            continue
        if "shutdown" in stat or "shut down" in stat:
            speak("Shutting down")
            break
        elif "wikipedia" in stat:
            speak("Looking up on wikipedia")
            stat = stat.replace("wikipedia", " ")
            wiki_answer = wikipedia.summary(stat, sentences = 3)
            speak(wiki_answer)
            print(wiki_answer)
        elif "open" in stat:
            website = stat.replace("open ","")
            webbrowser.open_new_tab("www."+website+".com")
            speak("Opening "+website)            
        elif "weather" in stat:
            weather()
        elif "news" in stat:
            news()
        elif "Good morning" in stat:
            weather()
            news()
        elif "take notes" in stat:
            note_file = open("notes.txt", 'w')
            while stat != "done":
                stat = takeCommand()
                print(stat)
                note_file.write(stat + "\n")
            note_file.close()
        elif "search" in stat or "look up" in stat:
            query = stat.replace("search ","")
            query = stat.replace("look up ","")
            webbrowser.open_new_tab(query)
        else:
            client = wolframalpha.Client("R2K75H-7ELALHR35X")
            res = client.query(takeCommand())
            try:
                speak(str(next(res.results).text))
            except Exception:
                speak("Can you repeat your question?")
                 