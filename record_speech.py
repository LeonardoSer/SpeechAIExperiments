'''import sounddevice as sd
from scipy.io.wavfile import write

fs = 44100  # Sample rate
seconds = 10  # Duration of recording

myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
sd.wait()  # Wait until recording is finished
write('./wav/output.wav', fs, myrecording)  # Save as WAV file 
'''
import speech_recognition as sr

def main():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)

        print("Please say something")

        audio = r.listen(source)

        print("Recognizing Now .... ")


        # recognize speech using google

        try:
            
            text = r.recognize_google(audio)
            print("You have said \n" + text)
            print("Audio Recorded Successfully \n ")


        except Exception as e:
            print("Error :  " + str(e))

        # write audio
        with open("recorded.wav", "wb") as f:
            f.write(audio.get_wav_data())


if __name__ == "__main__":
    main()