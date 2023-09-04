from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import speech_recognition as sr
import spacy
import io
import os

# Initialize recognizer and NLP model
recognizer = sr.Recognizer()
nlp = spacy.load("en_core_web_sm")

# Function to handle voice notes
def handle_voice(update: Update, _: CallbackContext) -> None:
    file = update.message.voice.get_file()
    file.download("voice.ogg")
    
    # TODO: Convert OGG to WAV (ffmpeg)

    # Perform STT
    with sr.AudioFile("voice.wav") as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            update.message.reply_text(f"I heard: {text}")
            
            # Perform NLP
            doc = nlp(text)
            for token in doc:
                # print text and part-of-speech tag
                update.message.reply_text(f"Word: {token.text}, POS: {token.pos_}")
            
        except sr.UnknownValueError:
            update.message.reply_text("Sorry, I didn't understand.")

# Initialize the Updater
updater = Updater("BOT_TOKEN_HERE")

# Get the dispatcher to register handlers
dp = updater.dispatcher

# Register the handler
dp.add_handler(MessageHandler(Filters.voice & ~Filters.command, handle_voice))

# Start the Bot
updater.start_polling()
updater.idle()
