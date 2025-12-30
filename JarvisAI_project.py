import pyttsx3
from datetime import datetime
import speech_recognition as sr
import os
import wikipedia
import webbrowser
from pygame import mixer
import random
import smtplib
from email.message import EmailMessage
# from openai import OpenAI


email = "yashdeshwal09@gmail.com"
email_password = os.getenv("email_password")
openai_api = os.getenv("openai_api")


# def ask_chatgpt(ques):
#     client = OpenAI(api_key=openai_api )
#     try:
#         resp = client.chat.completions.create(
#             model="gpt-5.2",
#             messages=[
#                 {"role": "system", "content": "You are Jarvis, a helpful voice assistant."},
#                 {"role":"user", "content": ques}
#             ]
#         )
#         return resp.choices[0].message.content
#     except Exception:
#         return "I am having trouble connecting to ChatGPT. "

def playaudio(q):
    if q == "start":
        song = random.choice(os.listdir("C:/Users/yashd/PycharmProjects/PythonProject/music"))
        mixer.init()
        mixer.music.load(f"music/{song}")
        mixer.music.play()
    elif q == "pause":
        mixer.music.pause()
    elif q == "stop":
        mixer.music.stop()
    elif q == "continue":
        mixer.music.unpause()

def searching_tool(keyword, lst):
    keyword = keyword.lower()
    user_lst = keyword.split(" ")

    for i in range(len(lst)):
        lst[i] = lst[i].lower()

    sentence_dict = {}
    for sentence in lst:
        sentence_dict[sentence] = 0
        for user_word in user_lst:
            if user_word in sentence :
                sentence_dict[sentence] += sentence.count(user_word)

    new_sentence_dict = dict(sorted(sentence_dict.items(), key=lambda item: item[1], reverse=True))

    final_lst = []
    for key, value in new_sentence_dict.items():
        if value > 0:
            final_lst.append(key)
    return final_lst

def take_command():
    r = sr.Recognizer()
    print("Listening...Speak now")
    while True:
        with sr.Microphone() as source:
            audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language='en-IN')
            print("You said:",text)
            break
        except sr.exceptions.UnknownValueError:
            pass
        except Exception:
            return "none"
    return text

def response(string):
    print(f"Jarvis: {string}")
    engine = pyttsx3.init()
    engine.say(string)
    engine.runAndWait()

def wishme():
    hour = int(datetime.now().hour)
    if 0 <= hour < 12:
        return "Good Morning"
    elif 12<= hour < 18:
        return "Good Afternoon"
    else:
        return "Good Evening"

def wiki(q):
    try:
        return wikipedia.summary(q, sentences = 2, auto_suggest= False, redirect=True)
    except wikipedia.exceptions.PageError :
        return "Page not found on wikipedia"
    except Exception as e:
        return "An error occurred"

def sendemail(to, subject, mesg):
    msg = EmailMessage()
    msg["From"] = email
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(mesg)
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(email, email_password)
            server.send_message(msg)
        response("Email sent successfully")
    except Exception as e:
        response(f"Error occurred:")
        print(e)

response("Jarvis AI is Online")

while True:
    query = take_command().lower()
    if query == "none":
        continue

    elif "hello" in query:
        response(f"{wishme()} Sir! How may I help you")

    elif "your name" in query:
        response("I am Jarvis, your personal assistant")

    elif "search" in query:
        query = query.replace("search ", "")
        response(f"Searching {query}")
        webbrowser.open(f"https://www.google.com/search?query={query}")

    elif "date" in query:
        date = datetime.now().strftime("%d %B %Y, %A")
        response(f"Today is {date}")

    elif "time" in query:
        time = datetime.now().strftime("%I:%M %p")
        response(f"The time is {time}")

    elif "desktop" in query:
        query = query.replace("from desktop open ", "")
        apps = os.listdir("C:/Users/yashd/OneDrive/Desktop")
        try:
            var = list(filter(lambda x: x if (".lnk" in x) else None, searching_tool(query, apps)))[0]
            response(f"Opening {query}")
            os.startfile(f"C:/Users/yashd/OneDrive/Desktop/{var}")
        except Exception:
            response("Sorry Sir, I can't open that")

    elif "open chrome" in query:
        response("Opening chrome")
        os.startfile("chrome.exe")

    elif "open notepad" in query:
        response("Opening Notepad")
        os.startfile("notepad.exe")

    elif "open calculator" in query:
        response("Opening Calculator")
        os.startfile("calc.exe")

    elif "play music" in query or "play song" in query:
        playaudio("start")

    elif "pause music" in query or "pause song" in query:
        playaudio("pause")

    elif "stop music" in query or "stop song" in query:
        playaudio("stop")

    elif "continue music" in query or "continue song" in query:
        playaudio("continue")

    elif "wikipedia" in query:
        query = query.replace("wikipedia ", "")
        response(wiki(query))

    elif "send email" in query or "send an email" in query:
        response("Enter receiver's email")
        to_email = input(">>")
        response("Enter subject")
        subject = input(">>")
        response("Enter message")
        mesg = input(">>")
        sendemail(to_email, subject, mesg)

    # elif "chatgpt" in query.lower() or "chat gpt" in query.lower():
    #     query = query.replace("chatgpt ", "")
    #     response(ask_chatgpt(query))

    elif "exit" in query:
        response("Shutting down. Goodbye Sir!")
        break

    else:
        response("Sorry Sir! I didn't understand your command")




