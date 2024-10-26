import speech_recognition as sr
import socket
from deep_translator import GoogleTranslator
import tkinter as tk
from tkinter import Button, Text, Label
from PIL import Image, ImageTk
import numpy as np
import string
import matplotlib.pyplot as plt
from itertools import count

# Language Translation Configurations
supported_languages = {'Hindi': 'hi', 'Marathi': 'mr', 'Gujarati': 'gu', 'Punjabi': 'pa'}
default_lang = 'Hindi'  # Default language for speech recognition

# Image Configurations
gif_lst = ['all the best', 'are you sick', 'any questions', 'are you angry', 'are you busy', 'are you hungry',
           'be careful', 'can we meet tomorrow', 'clean the room', 'did you eat lunch', 'did you finish homework', 
           'do you go to office', 'do you have money', 'do you want something to drink', 'do you watch tv', 
           'dont worry', 'flower is beautiful', 'good afternoon', 'good morning', 'good question', 'good evening', 
           'good night', 'happy journey', 'what do you want tea or coffee', 'what is your name', 
           'how many people are in your family', 'i am a clerk', 'i am bored', 'i am fine', 'i am sorry', 
           'i am thinking', 'i am tired', 'i dont understand anything', 'i go to a theatre', 'i love to shop', 
           'i had to say something but i forgot', 'i have a headache', 'i like pink colour', 'lets go for lunch', 
           'my mother is a housewife', 'nice to meet you', 'please dont smoke', 'open the door', 'call me later', 
           'please call the ambulance', 'give me your pen', 'please wait for sometime', 'can i help you', 
           'shall we go together tomorrow', 'sign language interpreter', 'sit down', 'stand up', 'take care', 
           'there was a traffic jam', 'wait I am thinking', 'what are you doing', 'what is the problem', 
           'what is todays date', 'what does your father do', 'what is your job', 'what is your age', 
           'what is your mobile number', 'what is your name', 'whats up', 'when is your interview', 'when will we go', 
           'where do you live', 'where is the bathroom', 'where is the police station', 'you are wrong']

alphabet_lst = list(string.ascii_lowercase)

# Network Check
def is_connected():
    try:
        socket.create_connection(("1.1.1.1", 80), 2).close()
        return True
    except OSError:
        return False

# GIF and Alphabet Display
class ImageLabel(tk.Label):
    def load(self, img_path):
        img = Image.open(img_path)
        self.frames = [ImageTk.PhotoImage(img.copy())]
        try:
            for _ in count(1):
                img.seek(_)
                self.frames.append(ImageTk.PhotoImage(img.copy()))
        except EOFError:
            pass

        self.loc = 0
        self.delay = img.info.get('duration', 100)
        self.next_frame()

    def next_frame(self):
        if self.frames:
            self.config(image=self.frames[self.loc])
            self.loc = (self.loc + 1) % len(self.frames)
            self.after(self.delay, self.next_frame)

# Display Selected Animation
def animate_command(aud_text, original_text, display_label):
    if aud_text in gif_lst:
        display_label.load(f'Indian_Speech_Language_GIFS/{aud_text}.gif')
        text_area.insert(tk.END, f"\nRecognized: {original_text}\n")
    else:
        plt.figure(figsize=(2, 2))
        for char in aud_text:
            if char in alphabet_lst:
                img_path = f'Alphabets/{char}.jpg'
                img = Image.open(img_path)
                plt.imshow(np.array(img))
                plt.axis('off')
                plt.pause(0.5)
            plt.show()

# Recognize and Translate
def takeCommandHindi(selected_lang):
    if not is_connected():
        text_area.insert(tk.END, "\nError: No Internet Connection.\n")
        return

    r = sr.Recognizer()
    with sr.Microphone() as source:
        text_area.insert(tk.END, "\nListening...\n")
        r.energy_threshold = 300
        r.pause_threshold = 0.7
        audio = r.listen(source)
        
        try:
            lang_code = supported_languages[selected_lang]
            query = r.recognize_google(audio, language=f"{lang_code}-IN")
            text_area.insert(tk.END, f"Original ({selected_lang}): {query}\n")
            translated_text = GoogleTranslator(source='auto', target='en').translate(query)
            text_area.insert(tk.END, f"Translated (English): {translated_text}\n")
            
            # Format for animation function
            aud_text = translated_text.lower()
            aud_text = ''.join(char for char in aud_text if char not in string.punctuation)
            animate_command(aud_text, translated_text, gif_display_label)

        except sr.UnknownValueError:
            text_area.insert(tk.END, "Could not understand audio.\n")
        except sr.RequestError as e:
            text_area.insert(tk.END, f"API error: {e}\n")

# GUI Setup
app = tk.Tk()
app.title("Sign Language Translator")
app.geometry("600x500")

# Language Selection Dropdown
language_var = tk.StringVar(value=default_lang)
language_dropdown = tk.OptionMenu(app, language_var, *supported_languages.keys())
language_dropdown.pack()

# Display Label for GIFs
gif_display_label = ImageLabel(app)
gif_display_label.pack()

# Command and Feedback Display
text_area = Text(app, height=10)
text_area.pack()

# Action Buttons
def start_recognition():
    takeCommandHindi(language_var.get())

start_btn = Button(app, text="Speak", command=start_recognition)
start_btn.pack()

exit_btn = Button(app, text="Exit", command=app.quit)
exit_btn.pack()

app.mainloop()
