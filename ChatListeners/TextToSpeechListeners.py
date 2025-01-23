import Constants.ChatCheckers as ChatCheckers
from Audio.TextToSpeech import TextToSpeechRunner
class TTSListener:
    tts_runner = None
    def __init__(self, engine):
        self.tts_runner = TextToSpeechRunner(engine)
    def call(self, messages):
        messages_to_read = []
        tts_regex = ChatCheckers.chat_regex_list["tts"]
        for message in messages:
            if message["message"].startswith(tts_regex):
                message["message"] = message["message"].replace(tts_regex,"")
                messages_to_read.append(message)
        for message in messages_to_read:
            self.tts_runner.runTextToSpeech(message["message"], message["username"])
        