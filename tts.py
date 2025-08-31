from gtts import gTTS
import os
import tempfile
from playsound import playsound

def speak(text):
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
        temp_file = f.name
        tts.save(temp_file)
    playsound(temp_file)
    os.remove(temp_file)

#speak(input())