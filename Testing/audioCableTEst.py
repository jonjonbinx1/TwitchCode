import pyttsx3
import pyaudio
import wave
import os

# Initialize pyttsx3
engine = pyttsx3.init()

# Generate audio from text and save to a temporary file
audio_file = "output.wav"
engine.save_to_file("Hello, this is a test.", audio_file)
engine.runAndWait()

# List all available audio devices
p = pyaudio.PyAudio()

print("Available audio devices:")
virtual_cable_name = "Speakers (VB-Audio Virtual Cabl"
virtual_cable_index = None

for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print(f"{i}: {info['name']} (Channels: {info['maxInputChannels']})")
    if virtual_cable_name == info['name'] and 0 == info["maxInputChannels"]:
        virtual_cable_index = i
if virtual_cable_index is None:
    raise ValueError(f"Audio device '{virtual_cable_name}' not found")

# Open the audio file
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

print("Audio played through both devices and file cleaned up.")
