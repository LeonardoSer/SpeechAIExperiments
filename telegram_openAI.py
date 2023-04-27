import openai
import os
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
from TTS.utils.synthesizer import Synthesizer
from TTS.utils.manage import ModelManager
from telegram.ext import * 
import sys
from os import path
from pydub import AudioSegment
import io
# AI config
API_KEY = "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"
openai.api_key = API_KEY
chat_log = None

# Speech to text config
r = sr.Recognizer()

#  Text to speech config
path = "/home/rorschach/Desktop/flags/Jarvis /lib/python3.8/site-packages/TTS/.models.json"

model_mngr = ModelManager(path)

model_path, config_path, model_item = model_mngr.download_model("tts_models/en/ljspeech/tacotron2-DDC")  # tts list models

voc_path, vonc_config_path, model_item = model_mngr.download_model(model_item["default_vocoder"])

syn = Synthesizer(
    tts_checkpoint=model_path,
    tts_config_path=config_path,
    vocoder_checkpoint= voc_path,
    vocoder_config=vonc_config_path
)


START_CHAT_LOG = '\nHuman: Hello, who are you? \nAI: I am doing great. How can I help you today?\n\n'
MAX_ANSWER_TOKEN = 2000

# telegram bot stuff
BOT_API_KEY = "5828582310:AAHWdMvOfJiA5Wyvy4wEOtITwrEf6Gp7Gdk"

print("Bot Started")

# Ask to open AI
def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None:
        chat_log = START_CHAT_LOG
    return f'{chat_log}Human: {question}\nAI: {answer}\n\n'

def ask(question, chat_log=None):
    if chat_log is None:
        chat_log = START_CHAT_LOG
        
    prompt = f'{chat_log}Human: {question}\nAI:'
    
    response = openai.Completion.create(
        prompt=prompt, engine="text-davinci-002",  stop=['\nHuman'], temperature=0.9,
        top_p=1, frequency_penalty=0, presence_penalty=0.6, best_of=1,
        max_tokens=MAX_ANSWER_TOKEN)
        
    answer = response.choices[0].text.strip()
    return answer, append_interaction_to_chat_log(question, answer, chat_log)


# BOT stuff
def start_command(update, context):
    update.message.reply_text("Ask something")
    
def help_command(update, context):
    update.message.reply_text("You need help? Ask your mom.")
    
def handle_msg(update, context):
    global chat_log 

    question = str(update.message.text).lower()
    print("HUMAN:", question)
    # ask question 
    answer, chat_log = ask(question, chat_log)  
    response = answer
    print('MACHINE:', answer)
    
    update.message.reply_text(response)
    

def voice_handler(update, context):
    
    global chat_log
    
    bot = context.bot
    file = bot.getFile(update.message.voice.file_id)
    file.download('voice.mp3')
    
    ## [!!!] convert to wav

    AudioSegment.from_file("voice.mp3").export("voice.wav", format="wav")
    global r
    with sr.AudioFile("voice.wav") as source:
        audio = r.record(source)

    question = str(r.recognize_google(audio)).lower()
    answer, chat_log = ask(question, chat_log)  
    
    os.remove("voice.mp3")
    os.remove("voice.wav")
    
    # update.message.reply_text(answer)

    ## [!!!] convert response in wav
    ## [!!!] convert to wav in mp3
    ## [!!!] send mp3
    global syn
    outputs = syn.tts(answer)
    syn.save_wav(outputs, "voice.wav")
    AudioSegment.from_file("voice.wav").export("voice.mp3", format="mp3")

    data = open('voice.mp3', 'rb').read()
    
    update.message.reply_voice(io.BytesIO(data))
    
    os.remove("voice.mp3")
    os.remove("voice.wav")

 

    


def error(update, context):
    print(f'Update {update} caused error {context.error}')
    

def main():
    
    updater = Updater(BOT_API_KEY, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    
    try:
        dp.add_handler(MessageHandler(Filters.text, handle_msg))
        dp.add_handler(MessageHandler(Filters.voice, voice_handler))
    except Exception as e:
        print(e)
        sys.exit(0)
    # dp.add_error_handler(error)
    
    updater.start_polling()
    updater.idle()
    
main()
