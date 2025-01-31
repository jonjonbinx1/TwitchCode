import speech_recognition as sr

class Listener:
    recognizer = sr.Recognizer()

    def listen_to_audio(self):
        try:
            # Use the default microphone (no device_index specified)
            with sr.Microphone() as source:
                # print("Please speak something...")
                
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source)
                
                # Set pause threshold to 2 seconds
                self.recognizer.pause_threshold = 2.0
                
                # # Set timeout to 10 seconds
                # timeout_duration = 10

                # Keep listening until speech is detected or timeout occurs
                print("Listening for speech...")
                audio = self.recognizer.listen(source)
                print("Audio captured successfully")

            try:
                # Convert speech to text
                text = self.recognizer.recognize_google(audio)
                print("You said: " + text)
                return text
            except sr.UnknownValueError:
                return "Sorry, I could not understand the audio."
            except sr.RequestError as e:
                print("Error: " + str(e))
                return "Sorry, I could not understand the audio."
        except Exception as e:
            print(f"An error occurred with the microphone: {e}")
            return "Sorry, I could not understand the audio."
