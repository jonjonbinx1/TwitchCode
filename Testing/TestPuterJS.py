import requests
import simpleaudio as sa

def get_tts_audio(text):
    url = "https://js.puter.com/v2/tts"
    payload = {
        "text": text,
        "lang": "en"
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Error: {response.status_code}")
        return None

def play_audio(audio_data):
    if audio_data:
        wave_obj = sa.WaveObject(audio_data, sample_width=2, channels=1, frame_rate=22050)
        play_obj = wave_obj.play()
        play_obj.wait_done()

def main():
    text = "Hello! This is a test of the Puter.js text-to-speech API."
    audio_data = get_tts_audio(text)
    if audio_data:
        play_audio(audio_data)

if __name__ == "__main__":
    main()
