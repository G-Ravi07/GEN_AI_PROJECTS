import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
from gtts import gTTS
import pygame
import os
import openai

# === Configuration ===
openai.api_key = "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"  # ← Keep your actual key secret
newsapi = "a1c9a8a263574786af20601055631e6f"

# === Music Library ===
music = {
    "lose your mind": "https://youtu.be/whbczRUgYQw?si=KIyWsblXy5_4ggBa",
    "finding her": "https://youtu.be/3Cp2QTBZAFQ?si=kK-eiULYNqlPuXrg",
    "skyfall": "https://www.youtube.com/watch?v=DeumyOzKqgI&pp=ygUHc2t5ZmFsbA%3D%3D",
    "wolf": "https://www.youtube.com/watch?v=ThCH0U6aJpU&list=PLnrGi_-oOR6wm0Vi-1OsiLiV5ePSPs9oF&index=21"
}

# === Text-to-Speech Function ===
def speak(text):
    try:
        tts = gTTS(text)
        tts.save('temp.mp3')
        pygame.mixer.init()
        pygame.mixer.music.load('temp.mp3')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.music.unload()
        os.remove("temp.mp3")
    except Exception as e:
        print(f"Error in speaking: {e}")

# === OpenAI Chat ===
def aiProcess(command):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud."},
                {"role": "user", "content": command}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI Error: {e}"

# === Command Processor ===
def processCommand(c):
    c = c.lower()
    
    if "open google" in c:
        webbrowser.open("https://google.com")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")
    
    elif c.startswith("play"):
        try:
            song = c.split(" ", 1)[1].lower()
            if song in music:
                speak(f"Playing {song}")
                webbrowser.open(music[song])
            else:
                speak("Song not found in music library.")
        except IndexError:
            speak("Please say the song name after 'play'.")

    elif "news" in c:
        try:
            r = requests.get("https://newsapi.org/v2/everything?q=india&sortBy=publishedAt&apiKey=a1c9a8a263574786af20601055631e6f")
            if r.status_code == 200:
                articles = r.json().get('articles', [])
                for article in articles[:5]:
                    speak(article['title'])
            else:
                speak("Unable to fetch news at the moment.")
        except Exception as e:
            speak("An error occurred while fetching news.")
    else:
        output = aiProcess(c)
        speak(output)

# === Main Wake Word Listener ===
def main():
    recognizer = sr.Recognizer()
    speak("Initializing Jarvis...")
    
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word 'Jarvis'...")
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)
                word = recognizer.recognize_google(audio).lower()
                
                if word == "jarvis":
                    speak("Yes?")
                    with sr.Microphone() as source:
                        print("Jarvis activated. Listening for command...")
                        audio = recognizer.listen(source, timeout=5)
                        command = recognizer.recognize_google(audio)
                        processCommand(command)
        except sr.WaitTimeoutError:
            continue
        except sr.UnknownValueError:
            continue
        except Exception as e:
            print(f"Error: {e}")

# === Run the Assistant ===
if __name__ == "__main__":
    main()
