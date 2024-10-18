#for starting assistant
import pvporcupine
import pyaudio

import speech_recognition as sr
import pyttsx3
import webbrowser
import struct

# Initializing recognizer and text-to-speech engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# Function to audio reply
def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Function for capturing speech and converting it to text
def speech_to_text():
    with sr.Microphone() as source:
        speak("Starting mic plzz wait.... ")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
        speak ("plzz say something:) ")
        audio = recognizer.listen(source)
        
        try:
            text = recognizer.recognize_google(audio)
            print("you said "+ text)
            
            
            if 'youtube' in text.lower():
                speak ('opening youtube')
                webbrowser.open('https://www.youtube.com/')
            else:
                speak("You said: " + text)
            
            
        except sr.UnknownValueError:
            speak ("sorry i couldent understand the audio")
        except sr.RequestError:
            speak ("service Error")    
            
# speech_to_text() 
            
def detect_wake_word():
    access_key = "FdXwao9qT9LmA/5md4JeN1gpJOIunAY9MJhcWBDTlVGOcrGBxqywXw=="
    porcupine = pvporcupine.create(access_key=access_key, keywords=["hey barista"])
    pa = pyaudio.PyAudio()
    
    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length,
        input_device_index=None
    )


    print("Listening for the wake word...")
    
    try:
        while True:
            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm_unpacked = struct.unpack_from("h" * porcupine.frame_length, pcm)
            
            keyword_index = porcupine.process(pcm_unpacked)
            
            if keyword_index >= 0:
                print("Wake word detected!")
                speak("I'm listening...")
                speech_to_text()
    
    except KeyboardInterrupt:
        print("Terminated the assistant..")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        audio_stream.close()
        pa.terminate()
        porcupine.delete()
        

detect_wake_word()
