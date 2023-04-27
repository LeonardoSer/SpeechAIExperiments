import pyttsx3


def pytts():
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)

    engine.say("Hello my name is Ultron and I'm here to clean this world from the human infection")
    engine.runAndWait()


from TTS.utils.synthesizer import Synthesizer
from TTS.utils.manage import ModelManager

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

text = "chill zi"

outputs = syn.tts(text)
syn.save_wav(outputs, "tts_test.wav")
