import speech_recognition as sr

def main():
    sound = 'Recording.wav'
    r = sr.Recognizer()
    with sr.AudioFile(sound) as source:
        r.adjust_for_ambient_noise(source)
        print("Converting audiofile to text")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print("Converted audio: " + text)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

if __name__== "__main__":
    main()
