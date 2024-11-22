#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pyttsx3 as p
import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime  
import wolframalpha
import json
import webbrowser
from urllib.request import urlopen
import requests
import os
import randfacts 

class Email():
    def sendEmail(to, content):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('youremail@gmail.com', 'your-password')
        server.sendmail('youremail@gmail.com', to, content)
        server.close()

class Music():
    def __init__(self):
        self.driver = webdriver.Chrome()

    def play(self, query):
        self.query = query
        self.driver.get(url = "https://www.youtube.com/results?search_query=" + query)
        video = self.driver.find_element(By.XPATH, '//*[@id="video-title"]/yt-formatted-string')
        video.click()


class Infow():
    def __init__(self):
        self.driver = webdriver.Chrome()

    # query means text we want to search on wikipedia
    def get_info(self,query):                         
        self.query = query
        self.driver.get(url = "https://www.wikipedia.org")
        search = self.driver.find_element(By.XPATH,'//*[@id="searchInput"]')
        search.click()
        search.send_keys(query)
        enter = self.driver.find_element(By.XPATH,'//*[@id="search-form"]/fieldset/button')
        enter.click()

def WolfRamAlpha(query):
    apikey = "32X22R-JGKG6V62KY"
    requester = wolframalpha.Client(apikey)
    requested = requester.query(query)

    try:
        answer = next(requested.results).text
        return answer

    except:
        speak("The value is not answerable")

def Calc(text2):
    Term = str(text2)
    Term = Term.replace("robo","")
    Term = Term.replace("multiply","*")
    Term = Term.replace("plus","+")
    Term = Term.replace("minus","-")
    Term = Term.replace("divide","/")
    Term = Term.replace("log","log")

    Final = str(Term)
    result = WolfRamAlpha(Final)
    try:
        result = WolfRamAlpha(Final)
        print(f"{result}")
        speak(result)

    except:
        speak("The value is not answerablr")



#----------------------------------------------------------------------------------------#
# for speak text:- speak()
engine = p.init('sapi5')

voices = engine.getProperty('voices')

for voice in voices:
    if 'en' in voice.languages:
        engine.setProperty('voice', voice.id)
        break
def speak(text):
    engine.say(text)
    engine.runAndWait()


# --------------------------------------------------------------------------------------- #


rate =engine.getProperty('rate')
print(rate)
engine.setProperty('rate', 150)

r = sr.Recognizer()



#speak("hello sir i am your voice assistant")
hour = int(datetime.datetime.now().hour)
if hour>=0 and hour<12:
    speak("Good Morning!")

elif hour>=12 and hour<18:
    speak("Good Afternoon!")   

else:
    speak("Good Evening!")  

speak("I am robo")
# ------------------------- for listen voice -----------------------------#
with sr.Microphone() as source:
    r.energy_threshold = 10000
    r.adjust_for_ambient_noise(source,1.2)
    print("listening")
    audio = r.listen(source)
    text = r.recognize_google(audio)
    print(text)
    
if "hello" and "are" and "you" in text:
    speak("i am fine")


speak("what can i do for you")  
with sr.Microphone() as source:                # listening...
    r.energy_threshold = 10000
    r.adjust_for_ambient_noise(source,1.2)
    print("listening")
    audio = r.listen(source)
    text2 = r.recognize_google(audio)



# -------------------------------------------------------------------------------------#
# For information from wikipedia
if "information" in text2:
    speak("you need information related to which topic?")

    
    with sr.Microphone() as source:
         r.energy_threshold = 10000
         r.adjust_for_ambient_noise(source,1.2)
         print("listening")
         audio = r.listen(source)
         infor = r.recognize_google(audio)  
   
    speak("searching in wikipedia".format(infor))
    assist = Infow()
    assist.get_info(infor)

    with sr.Microphone() as source:
         r.energy_threshold = 10000
         r.adjust_for_ambient_noise(source,1.2)
         print("listening")
         audio = r.listen(source)
         text2 = r.recognize_google(audio)
         print(text2)


# ------------------------------------------------------------------------------------------ #
# for playing videos on Youtube
if "play" and "video" in text2:
    speak("you want me to play which video?")
    with sr.Microphone() as source:
         r.energy_threshold = 10000
         r.adjust_for_ambient_noise(source,1.2)
         print("listening")
         audio = r.listen(source)
         vid = r.recognize_google(audio)
    assist = Music()
    assist.play(vid)



if "time" and "date" in text2:
    print(text2)
    strTime = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"sir, the time is {strTime}")
    with sr.Microphone() as source:
        r.energy_threshold = 10000
        r.adjust_for_ambient_noise(source,1.2)
        print("listening")
        audio = r.listen(source)
        text2 = r.recognize_google(audio)
        print(text2)
    
if "who made you" in text2 or "who created you" in text2: 
    speak("My Creaters are Akash, Tusshar, Ashish.")


if 'exit' in text2:
    speak("Thanks for giving me your time")
    exit()

if 'reason for you' in text2:
    speak("I was created as a Minor project. ")
    
if "calculate" in text2:
    text2 = text2.replace("calulculate","")
    print(text2)
    Calc(text2)



# ----------------------------------------------------------------------------------- #
# Telling us latest news using API(Newsapi.org)
if 'news' in text2:
    def get_latest_news():
        try:
            url = 'https://newsapi.org/v1/articles'
            params = {
                'source': 'the-times-of-india',
                'from': '2024-04-01',
                'sortBy': 'top',
                'apiKey': 'cb6f4ddba861453baa74efc603b3ab0d'
            }
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()

            if 'articles' in data:
                articles = data['articles']
                for i, article in enumerate(articles, 1):
                    print(f"{i}. {article['title']}")
                    print(article['description'] + '\n')
                    # You can add speak functionality here to read out the news
            else:
                print("No articles found in the response.")
        except requests.RequestException as e:
            print(f"Error fetching news: {e}")
    print(text2)
    speak("Todays news is")
    get_latest_news()


# --------------------------------------------------------------------------------------------- #
# telling random facts 
if "fact" or "facts" in text2:
    speak(sure, sir, " ")
    x = randfacts.getFact()
    print(x)
    speak("Did you know that, "+x)

if 'open pdf' in text2:
    speak("Opening pdf")
    print(text2)
    pdf_path = r'C:\Users\AKASH\Downloads\BDA Thanks to The Phenomena.pdf'
    document = fitz.open(r'C:\Users\AKASH\Downloads\BDA Thanks to Phenomena.pdf')





