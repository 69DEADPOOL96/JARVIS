import pyttsx3  #pyttsx3 is a text-to-speech conversion library in Python. Unlike alternative libraries, it works offline.
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import smtplib
import subprocess as sub
import tkinter as tk


#using SAPI5 as a Speech API
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')


engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
# a wish me command to greet every time we start this code
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
    
    elif hour>=12 and hour<18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("I am JARVIS, your AI Friend, Tell me How may I help you?")
# defining a function to takecommand via speech recognition 
# defining our speech command as "query"
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...") 
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...") 
        query = r.recognize_google(audio, language='en-in')
        print(f"USER: {query}\n")

    except Exception as e:
        print("unable to recognize, please speak again...")
        return "None"
    return query
# a basic smtp tool for sending emails
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('RyomenSukuna697989@gmail.com', 'zepbmbatctgtxlsq')
    server.sendmail('RyomenSukuna697989@gmail.com', to, content)
    server.close()
# a simple calculator with GUI using Tkinter
def calculator():


    def on_button_click(value):
        current = str(entry.get())
        entry.delete(0, tk.END)
        entry.insert(tk.END, current + str(value))

    def clear_entry():
        entry.delete(0, tk.END)

    def calculate():
        try:
            result = eval(entry.get())
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(result))
        except Exception as e:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Error")


    root = tk.Tk()
    root.title("CALCULATOR")


    entry = tk.Entry(root, width=20, font=('Arial', 16), justify='right')
    entry.grid(row=0, column=0, columnspan=4)


    buttons = [
        '7', '8', '9', '/',
        '4', '5', '6', '*',
        '1', '2', '3', '-',
        '0', '.', '=', '+'
    ]

    row_val = 1
    col_val = 0

    for button in buttons:
        tk.Button(root, text=button, padx=20, pady=20, font=('Arial', 14),
                command=lambda button=button: on_button_click(button) if button != '=' else calculate()).grid(row=row_val, column=col_val)
        col_val += 1
        if col_val > 3:
            col_val = 0
            row_val += 1


    tk.Button(root, text='C', padx=20, pady=20, font=('Arial', 14), command=clear_entry).grid(row=row_val, column=col_val)


    root.mainloop()


# Here comes the main part of our code
# our speech command will be converted into lower case for avoiding case base errors
# if our query gets any phrase listed below the code will work accordingly
   
if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()
        
# a simple wikipedia module has been imported to summarise whatever topic we wish to learn about
        if 'search wikipedia' in query:
            try:
                speak("What should I search?")
                print("NOTE:--Only speak the topic name, nothing else")
                wik = takeCommand()
                res = wikipedia.summary(wik, sentences=3)
                speak("According to wikipedia...")
                print(res)
                speak(res)
            except Exception as e:
                print(e)
                speak("Topic not found, try something else")
        if 'search in wikipedia' in query:
            try:
                speak("What should I search?")
                print("NOTE:--Only speak the topic name, nothing else")
                wik = takeCommand()
                res = wikipedia.summary(wik, sentences=5)
                speak("According to wikipedia...")
                print(res)
                speak(res)
            except Exception as e:
                print(e)
                speak("Topic not found, try something else")
# using SMTP library, we'll be performing basic email sharing procedure                
        elif 'send email' in query:
            speak("Type the name of the receipent")
            rs=input("Type here: ")
            rs=rs.lower()
            if rs.endswith("@gmail.com") or rs.endswith("@outlook.com") or rs.endswith("@hotmail.com") or rs.endswith("@yahoo.com") or rs.endswith("@icloud.com") or rs.endswith("@protonmail.com") or rs.endswith("@zoho.com") or rs.endswith("@aol.com") or rs.endswith("@gmx.com") or rs.endswith("@tutanota.com") or rs.endswith("@mail.com"):
                speak("Select your preference")
                tos=input("Would you prefer Keyboard or speech? type 'K' for text or 'S' for speech:  ")
                if tos =='S':
                    try:
                        speak("What should I say?")
                        print("What should I say?")
                        content=takeCommand()
                        to = rs
                        sendEmail(to, content)
                        speak("email has been sent")
                        print("Email has been sent")
                    except Exception as e:
                        print(e)
                        speak("An unwanted error occured")
                elif tos =='K':
                    try:
                        print("What should I say?")
                        content=input("Write your content here: ")
                        to = rs
                        sendEmail(to, content)
                        speak("email has been sent")
                        print("Email has been sent")
                    except Exception as e:
                        print(e)
                        speak("An unwanted error occured")
            else:
                print("Incorrect email extension")
                speak("Incorrect email extension detected")

# using webbrowser module, we can directly open any website we wish to
# also if you want to open files/folder from local machine, you can use "os" module
        elif 'open youtube' in query:
            speak("Starting Youtube...")
            webbrowser.open("www.youtube.com")
        elif 'open mail'in query:
            speak("Here's your Mailbox")
            webbrowser.open("www.gmail.com")
        elif 'open gmail' in query:
            speak("Here's your Mailbox")
            webbrowser.open("www.gmail.com")
        elif 'search in google' in query:
            speak("Select your preference")
            ts= input("'K' for text, 'S' for speech:  ")
            if ts == "K":
                speak("What should I search for you?")
                print("What should I search for you?")
                srch=input("Type here:  ")
                webbrowser.open("www.google.com/search?q="+srch)
            elif ts == "S":
                srch=takeCommand()
                webbrowser.open("www.google.com/search?q="+srch)
            else:
                print("Error")
                speak("Error occurred")
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")
            print(strTime)
        elif 'calculator' in query:
            calculator()
        elif 'how are you' in query:
            speak("I am Fine!, what about you?")
            print("I am Fine")
        elif 'i am fine' in query:
            speak("Hope you always feel fine buddy")
            print("Hope, you always feel fine, buddy")
        elif 'bye' in query:
            speak("OK BYE, See you later!")
            print("OK BYE, See you later!")
            exit()
        elif 'quit' in query:
            exit()
        
        


