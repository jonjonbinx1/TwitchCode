import pyttsx3

# Initialize pyttsx3 engine in the main thread
engine = pyttsx3.init()

from BaseCode.TwitchChatMessageRunner import MessageRunner
from ChatListeners.TextToSpeechListeners import TTSListener

def main():
    runner = MessageRunner()
    tts_listener = TTSListener(engine)
    runner.start(0, [tts_listener])

if __name__ == "__main__":
    main()