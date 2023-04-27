from os import path
from pydub import AudioSegment

from pydub import AudioSegment

AudioSegment.from_file("voice.mp3").export("voice.wav", format="wav")