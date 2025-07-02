import smtplib
import speech_recognition as sr
import pyttsx3
from tkinter import *
from threading import Thread
from email.message import EmailMessage

# Initialize TTS engine
speech_engine = pyttsx3.init()

# Speak text aloud
def speak(text):
    text_display.insert(END, f"\nAssistant: {text}")
    speech_engine.say(text)
    speech_engine.runAndWait()

# Capture voice and convert to text
def capture_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as mic:
        speak("Listening...")
        try:
            audio = recognizer.listen(mic, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            text_display.insert(END, f"\nYou: {command}")

            command = command.replace("at the rate", "@").replace(" at ", "@").replace(" dot ", ".")
            if "@" in command:
                parts = command.split("@")
                if len(parts) == 2:
                    user = parts[0].replace(" ", "")
                    domain = parts[1].replace(" ", "")
                    command = f"{user}@{domain}"
            return command

        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand.")
            return None
        except sr.RequestError:
            speak("Speech service is unavailable.")
            return None
        except Exception as e:
            speak(f"Error: {e}")
            return None

# Send Email Function
def send_email(subject, body, recipient):
    smtp_host = 'smtp.gmail.com'
    smtp_port = 587
    sender = 'badalchaudhary80578368@gmail.com'
    password = 'adnfxmxssuyvljua'  # Replace with environment variable in real use

    try:
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(sender, password)

        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = recipient
        msg.set_content(body)

        server.send_message(msg)
        speak("Email sent successfully!")

    except Exception as e:
        speak(f"Failed to send email: {e}")
    finally:
        server.quit()

# Assistant main logic
def run_assistant():
    speak("Hi Badal Sir, I am ready!")

    while True:
        command = capture_command()

        if command:
            if "send email" in command:
                speak("What's the subject?")
                subject = capture_command()

                speak("What should I write in the email?")
                body = capture_command()

                speak("Please say the recipient's email address.")
                recipient = capture_command()

                if recipient and "@" in recipient:
                    speak("Do you want to send it now?")
                    confirm = capture_command()
                    if confirm and "yes" in confirm:
                        send_email(subject, body, recipient)
                    else:
                        speak("Okay, I won't send it.")
                else:
                    speak("That doesn't look like a valid email.")

            elif "exit" in command or "quit" in command:
                speak("Thank you! Signing off.")
                break
            else:
                speak("Say 'send email' or 'exit'.")

# Start assistant in background thread
def start_assistant_thread():
    t = Thread(target=run_assistant)
    t.daemon = True
    t.start()

# ----------------- GUI Setup -----------------
app = Tk()
app.title("Voice Email Assistant")
app.geometry("500x400")
app.configure(bg="white")

Label(app, text="🎤 Voice Email Assistant", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

text_display = Text(app, height=15, width=60, wrap=WORD, font=("Arial", 10))
text_display.pack(padx=10, pady=10)

start_btn = Button(app, text="Start Assistant", font=("Arial", 12), command=start_assistant_thread, bg="green", fg="white")
start_btn.pack(pady=5)

exit_btn = Button(app, text="Exit", font=("Arial", 12), command=app.destroy, bg="red", fg="white")
exit_btn.pack(pady=5)

app.mainloop()
