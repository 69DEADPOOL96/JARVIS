import datetime
import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import smtplib
import tkinter as tk
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Initialize text-to-speech engine
engine = pyttsx3.init("sapi5")
voice = engine.getProperty("voices")[0]
engine.setProperty("voice", voice.id)

# Global variable for output preference
output_preference = None


def set_output_preference():
    global output_preference
    while True:
        choice = input("Do you prefer text or voice output? (T/V): ").upper()
        if choice in ["T", "V"]:
            output_preference = choice
            break
        else:
            print("Invalid choice. Please enter 'T' for text or 'V' for voice.")


def speak(audio):
    if output_preference == "V":
        engine.say(audio)
        engine.runAndWait()
    print(audio)


def wish_user():
    hour = datetime.datetime.now().hour
    greeting = (
        "Good morning!"
        if hour < 12
        else "Good afternoon!" if hour < 18 else "Good evening!"
    )
    speak(f"{greeting} I am JARVIS, your AI assistant. How may I help you?")


def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User: {query}")
        return query.lower()
    except Exception as e:
        print("Unable to recognize. Please speak again...")
        return None


def send_email(to, content):
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to, content)


def calculator():
    def on_button_click(value):
        current = entry.get()
        entry.delete(0, tk.END)
        entry.insert(tk.END, current + str(value))

    def clear_entry():
        entry.delete(0, tk.END)

    def calculate():
        try:
            result = eval(entry.get())
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(result))
        except Exception:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Error")

    root = tk.Tk()
    root.title("Calculator")

    entry = tk.Entry(root, width=20, font=("Arial", 16), justify="right")
    entry.grid(row=0, column=0, columnspan=4)

    buttons = [
        "7",
        "8",
        "9",
        "/",
        "4",
        "5",
        "6",
        "*",
        "1",
        "2",
        "3",
        "-",
        "0",
        ".",
        "=",
        "+",
    ]

    row_val, col_val = 1, 0
    for button in buttons:
        tk.Button(
            root,
            text=button,
            padx=20,
            pady=20,
            font=("Arial", 14),
            command=lambda x=button: calculate() if x == "=" else on_button_click(x),
        ).grid(row=row_val, column=col_val)
        col_val += 1
        if col_val > 3:
            col_val, row_val = 0, row_val + 1

    tk.Button(
        root, text="C", padx=20, pady=20, font=("Arial", 14), command=clear_entry
    ).grid(row=row_val, column=col_val)

    root.mainloop()


def main():
    set_output_preference()
    wish_user()
    while True:
        query = recognize_speech()
        if not query:
            continue

        if "wikipedia" in query:
            speak("What should I search?")
            search_query = recognize_speech()
            try:
                result = wikipedia.summary(search_query, sentences=3)
                speak("According to Wikipedia...")
                print(result)
                speak(result)
            except Exception as e:
                print(e)
                speak("Topic not found. Please try something else.")

        elif "send email" in query:
            speak("Type the recipient's email address:")
            to = input("Email address: ").lower()
            if not to.endswith(
                (
                    "@gmail.com",
                    "@outlook.com",
                    "@hotmail.com",
                    "@yahoo.com",
                    "@icloud.com",
                )
            ):
                print("Invalid email address")
                speak("Invalid email address detected")
                continue

            speak(
                "Would you prefer keyboard or speech input? Type 'K' for keyboard or 'S' for speech:"
            )
            choice = input().upper()

            if choice == "S":
                speak("What should I say?")
                content = recognize_speech()
            elif choice == "K":
                print("What should I say?")
                content = input("Write your content here: ")
            else:
                print("Invalid choice")
                continue

            try:
                send_email(to, content)
                speak("Email has been sent")
            except Exception as e:
                print(e)
                speak("An error occurred while sending the email")

        elif "open youtube" in query:
            speak("Opening YouTube...")
            webbrowser.open("https://www.youtube.com")

        elif "open mail" in query or "open gmail" in query:
            speak("Opening your mailbox...")
            webbrowser.open("https://www.gmail.com")

        elif "search in google" in query:
            speak("What should I search for?")
            search_query = (
                recognize_speech()
                if input("'K' for text, 'S' for speech: ").upper() == "S"
                else input("Type here: ")
            )
            webbrowser.open(f"https://www.google.com/search?q={search_query}")

        elif "the time" in query:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {current_time}")
            print(current_time)

        elif "calculator" in query:
            calculator()

        elif "how are you" in query:
            speak("I am fine! How are you?")

        elif "bye" in query or "quit" in query:
            speak("Goodbye! See you later.")
            break


if __name__ == "__main__":
    main()