import os
import soundfile as sf
import torch
from TTS.api import TTS
import torchaudio
import pyaudio
import wave
import threading
import keyboard

class BinxyVoice:
    def __init__(self):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # Load TTS model
        self.tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC").to(device)
        self.p = pyaudio.PyAudio()
        self.stream_virtual_cable = None
        self.stream_default = None

        # Find and store audio device indices
        self.virtual_cable_index = self.find_virtual_cable_index()
        self.default_device_index = self.p.get_default_output_device_info()["index"]

        # Set up hotkey to stop playback
        self.stop_flag = threading.Event()
        keyboard.add_hotkey('ctrl+shift+t', self.stop_playback)

    def find_virtual_cable_index(self):
        virtual_cable_name = "Speakers (VB-Audio Virtual Cabl"
        for i in range(self.p.get_device_count()):
            info = self.p.get_device_info_by_index(i)
            print(f"{i}: {info['name']} (Channels: {info['maxInputChannels']})")
            if virtual_cable_name == info['name'] and info["maxInputChannels"] == 0:
                return i
        print("Virtual cable device not found.")
        return None

    def generate_and_play_speech(self, text):
        # Generate speech
        wav = self.tts.tts(text)
        
        # Convert to tensor
        waveform = torch.tensor(wav).unsqueeze(0)

        # Adjust pitch and speed
        sample_rate = self.tts.synthesizer.output_sample_rate
        pitch_factor = 1.1  # Slightly higher pitch
        speed_factor = 0.8  # Slightly faster speed
        waveform = torchaudio.functional.resample(waveform, orig_freq=sample_rate, new_freq=int(sample_rate * speed_factor))
        waveform = torchaudio.functional.resample(waveform, orig_freq=sample_rate, new_freq=int(sample_rate / pitch_factor))

        # Save the generated speech to a WAV file using soundfile
        wav_file = 'output.wav'
        sf.write(wav_file, waveform.squeeze().cpu().numpy(), sample_rate)

        # Play the generated WAV file to multiple audio output devices
        self.play_to_multiple_sources(wav_file)

        # Delete the WAV file after playing
        os.remove(wav_file)

    def play_audio(self, device_index, audio_data):
        stream = self.p.open(format=self.sample_format,
                             channels=self.num_channels,
                             rate=self.sample_rate,
                             output=True,
                             output_device_index=device_index)
        self.streams.append(stream)
        
        # Play audio in chunks and check for the stop flag
        chunk_size = 1024
        for i in range(0, len(audio_data), chunk_size):
            if self.stop_flag.is_set():
                break
            stream.write(audio_data[i:i+chunk_size])
        
        stream.close()
        self.streams.remove(stream)

    def play_to_multiple_sources(self, wav_file):
        if self.virtual_cable_index is None:
            print("Virtual cable device index is not set.")
            return

        # Open the WAV file
        wf = wave.open(wav_file, 'rb')

        # Get audio format info
        self.num_channels = wf.getnchannels()
        self.sample_rate = wf.getframerate()
        self.sample_format = self.p.get_format_from_width(wf.getsampwidth())
        audio_data = wf.readframes(wf.getnframes())
        wf.close()

        # List to keep track of streams
        self.streams = []

        # Reset the stop flag
        self.stop_flag.clear()

        # Create threads to play audio on both devices simultaneously
        thread_virtual_cable = threading.Thread(target=self.play_audio, args=(self.virtual_cable_index, audio_data))
        thread_default_device = threading.Thread(target=self.play_audio, args=(self.default_device_index, audio_data))

        # Start the threads
        thread_virtual_cable.start()
        thread_default_device.start()

        # Wait for both threads to finish
        thread_virtual_cable.join()
        thread_default_device.join()

    def stop_playback(self):
        self.stop_flag.set()
        print("Playback stopped.")

# Example usage
def main():
    binxy_voice = BinxyVoice()
    playback_thread = threading.Thread(target=binxy_voice.generate_and_play_speech, args=("Hey there! It's Binxy, ready to rock the stream with you!",))
    playback_thread.start()

    # Wait for hotkeys
    while True:
        pass

if __name__ == "__main__":
    main()
