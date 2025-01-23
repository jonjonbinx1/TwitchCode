import pyttsx3
import time
import random
import soundcard as sc
import pyaudio
import wave
import os
class TextToSpeechRunner:
    engine = None
    voices = None
    players_and_voices = None
    def __init__(self, engine):
        
        # Initialize pyttsx3
        self.engine = engine
        engine.setProperty('rate', 140)
        # Set the specific voices
        self.voices = {
            "david" : "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0",
            "hazel" : "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0",
            "zira" : "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
        }

        self.players_and_voices = {}
    def readMessage(self, voice, message):
        self.engine.setProperty('voice', voice)
        audio_file = "output.wav"
        self.engine.save_to_file(message, audio_file)
        self.engine.runAndWait()
        p = pyaudio.PyAudio()

        virtual_cable_name = "Speakers (VB-Audio Virtual Cabl"
        virtual_cable_index = None
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            print(f"{i}: {info['name']} (Channels: {info['maxInputChannels']})")
            if virtual_cable_name == info['name'] and 0 == info["maxInputChannels"]:
                virtual_cable_index = i

        with wave.open(audio_file, 'rb') as wf:
            # Open streams with the selected audio device and the default device
            stream_virtual_cable = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                                        channels=wf.getnchannels(),
                                        rate=wf.getframerate(),
                                        output=True,
                                        output_device_index=virtual_cable_index)

            stream_default = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                                    channels=wf.getnchannels(),
                                    rate=wf.getframerate(),
                                    output=True)

            # Play the audio file through both devices
            data = wf.readframes(1024)
            while data:
                stream_virtual_cable.write(data)
                stream_default.write(data)
                data = wf.readframes(1024)

            # Close the streams
            stream_virtual_cable.close()
            stream_default.close()

        # Close PyAudio
        p.terminate()

        # Clean up the temporary audio file
        os.remove(audio_file)
    def runTextToSpeech(self, message, username=None):
        print(username)
        print(self.players_and_voices)
        voice = random.choice(list(self.voices.values()))
        if username is not None:
            if username in self.players_and_voices.keys():
                voice = self.players_and_voices[username].voiceId
            else:
                newUser = UserTextToSpeech()
                newUser.start_time = time.time()
                newUser.username = username
                newUser.voiceId = voice
                self.players_and_voices.update({username : newUser})
        self.readMessage(voice, message)
    
class UserTextToSpeech:
    start_time = time.time()
    username = ""
    voiceId = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"
        
  
# # List all available speakers 
# speakers = sc.all_speakers() # Print out the list of available speakers 
# for idx, speaker in enumerate(speakers): print(f"{idx}: {speaker.name}")

