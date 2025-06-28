import smtplib
import speech_recognition as sr
import pyttsx3

# Initialize the speech engine
speech_engine = pyttsx3.init()

# Prompt user through voice
def speak(text):
    print(text)
    speech_engine.say(text)
    speech_engine.runAndWait()

# Capture user voice and convert to text
def capture_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as mic:
        print(" Listening...")
        audio = recognizer.listen(mic)

    try:
        command = recognizer.recognize_google(audio).lower()
        print(f" You said: {command}")

        
        command = command.replace("at the rate", "@").replace(" at ", "@").replace(" dot ", ".")
        if "@" in command:
            parts = command.split("@")
            if len(parts) == 2:
                user = parts[0].replace(" ", "")
                domain = parts[1].replace(" ", "")
                command = f"{user}@{domain}"
        return command

    except sr.UnknownValueError:
        speak("Sorry, I couldn't understand that.")
        return None
    except sr.RequestError:
        speak("There's an issue with the speech recognition service.")
        return None

# Send an email using Gmail SMTP
def send_email(subject, body, recipient):
    smtp_host = 'smtp.gmail.com'
    smtp_port = 587
    sender = 'badalchaudhary80578368@gmail.com'
    password = 'adnfxmxssuyvljua'

    try:
        # Connect to server
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(sender, password)

        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(sender, recipient, message)

        print(f"✅ Email sent to: {recipient}")
        speak("Email was sent successfully!")

    except Exception as e:
        print(f" Failed to send email: {e}")
        speak("Oops! Something went wrong while sending the email.")

    finally:
        server.quit()

def run_assistant():
    speak("Hi Badal Sir, I'm ready. What would you like to do?")

    while True:
        command = capture_command()

        if command:
            if "send email" in command:
                speak("What should be the subject?")
                subject = capture_command()

                speak("What should I write in the email?")
                body = capture_command()

                speak("Please say the recipient's email address.")
                recipient = capture_command()

                if recipient and "@" in recipient:
                    send_email(subject, body, recipient)
                else:
                    speak("Hmm, that doesn't look like a valid email address.")

            elif "exit" in command or "quit" in command:
                speak("Thank you, Badal Sir. Signing off.")
                break

            else:
                speak("Sorry, I didn't catch that command. Try saying 'send email' or 'exit'.")

if __name__ == "__main__":
    run_assistant()
