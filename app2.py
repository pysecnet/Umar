import openai
from customtkinter import *
from translate import Translator as ElevenLabTranslator
from gtts import gTTS
import pyttsx3
from tkinter import Text, Scrollbar
import os
import pygame
import threading

openai.api_key = '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'

set_default_color_theme("blue")
# engine = pyttsx3.init()
window = CTk()
window.title("ChatGPT")

# Make the window fullscreen using wininfo
window.state('-fullscreen', True)

company = "saif"

window.configure()

label = CTkLabel(window, text="Your Personal Assistant")
label.pack(padx=5, pady=5)

entry = CTkEntry(window, fg="white", width=250, borderwidth=2, placeholder_text="Ask Anything")
entry.pack(padx=5, pady=5)

language_menu = CTkComboBox(window, values=["English", "Urdu", "Sindhi"], state="readonly")
language_menu.entry.configure(readonlybackground="#3e3e42")
language_menu.pack(pady=5)

response_frame = CTkFrame(window, width=400, height=200)
response_frame.pack(side="top", pady=10)

# Create a Text widget for displaying responses
response_text = Text(response_frame, wrap="word", height=20, width=120)
response_text.pack(side="top", fill="both", expand=True)

# Create a vertical scrollbar for the Text widget
scrollbar = Scrollbar(response_frame, bg=window.cget("bg"))  # Set background color
scrollbar.pack(side="right", fill="y")
response_text.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=response_text.yview)

# Set default language to English
language_menu.set("English")


def respond():
    user_input = entry.get()
    label2 = CTkLabel(text=f"You said: {user_input}", bg="gray", fg="white")
    label2.pack()

    selected_lang = language_menu.get()
    print("Selected Language:", selected_lang)

    prompt_template = f"""
    [Customer] {user_input}
    [Assistant]
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a personal assistant and a search engine"},
            {"role": "system", "content": f"Your company is {company}"},
            {"role": "system", "content": "dont redirect someone, give all answers yourself"},
            {"role": "system", "content": "response must be shorter as possible"},
            {"role": "system", "content": "use Google as your search engine"},
            {"role": "user", "content": user_input}
        ]
    )
    result = response['choices'][0]['message']['content'].strip()
    display_response(result)

    if "Urdu" in selected_lang:
        urdu_text = translate_to_urdu(result)
        print("Translated Text (Urdu):", urdu_text)
        speak_response(urdu_text, lang="ur")

    elif "Sindhi" in selected_lang:
        sindhi_text = translate_to_sindhi(result)
        print("Translated Text (Sindhi):", sindhi_text)
        speak_response(sindhi_text, lang="sd")

    else:
        speak_response(result)


def stop_speech():
    pygame.mixer.quit()


def display_response(text):
    response_text.insert("end", text + "\n")
    response_text.see("end")


def translate_to_urdu(text):
    translator = ElevenLabTranslator(to_lang='ur')
    translation = translator.translate(text)
    return translation


def translate_to_sindhi(text):
    translator = ElevenLabTranslator(to_lang='sd')
    translation = translator.translate(text)
    return translation


def speak_response(text, lang="en"):
    if lang == "en":
        myobj = gTTS(text=text, lang='en', slow=False)
    elif lang == "ur":
        myobj = gTTS(text=text, lang='ur', slow=False)
    elif lang == "sd":
        myobj = gTTS(text=text, lang='ur', slow=True)
    else:
        myobj = gTTS(text=text, lang='en', slow=False)

    myobj.save("welcome.mp3")

    # Start a new thread for audio playback
    threading.Thread(target=play_audio, args=("welcome.mp3",)).start()


def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.quit()
    os.remove(file_path)


stop_button = CTkButton(window, text="Stop", command=stop_speech)
stop_button.pack(side="top", pady=5)

button = CTkButton(window, text="Submit", command=respond)
button.pack(pady=10)

scrollbar.config(command=response_text.yview)
stop_button.configure(command=stop_speech)
window.bind('<Return>', lambda event=None: respond())

window.mainloop()
