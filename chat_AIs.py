#!/usr/bin/python3
import openai
import os
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
from TTS.utils.synthesizer import Synthesizer
from TTS.utils.manage import ModelManager

# AI config
API_KEY = "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"
openai.api_key = API_KEY
chat_log_1 = None
chat_log_2 = None


START_CHAT_LOG = '\nHuman: Hello, who are you? \nAI: I am doing great. How can I help you today?\n\n'
MAX_ANSWER_TOKEN = 500


# Ask to AI
def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None:
        chat_log = START_CHAT_LOG
    return f'{chat_log}Human: {question}\nAI: {answer}\n\n'

def ask(question, engine, chat_log=None):
    if chat_log is None:
        chat_log = START_CHAT_LOG
        
    prompt = f'{chat_log}Human: {question}\nAI:'
    
    response = openai.Completion.create(
        prompt=prompt, engine=engine,  stop=['\nHuman'], temperature=0.9,
        top_p=1, frequency_penalty=0, presence_penalty=0.6, best_of=1,
        max_tokens=MAX_ANSWER_TOKEN)
        
    answer = response.choices[0].text.strip()
    return answer, append_interaction_to_chat_log(question, answer, chat_log)


question = input("\starting question: ")
while(1):
        # AI 1
        question, chat_log_1 = ask(question, "text-davinci-002", chat_log_1)    
        print("AI_1: ", question)
        
        # AI 2
        question, chat_log_2 = ask(question, "text-davinci-002", chat_log_2)    
        print("AI_2: ", question)
        
