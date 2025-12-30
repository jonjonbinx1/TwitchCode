import pyttsx3
engine = pyttsx3.init()
import Constants.ChatCheckers as ChatCheckers
import random
import keyboard
from Audio.TextToSpeech import TextToSpeechRunner
class BiddingListener:
    bidding_active = None
    textToSpeechRunner = TextToSpeechRunner(engine)
    def __init__(self, bidding_active):
        print(type(bidding_active))
        self.bidding_active = bidding_active
    def call(self, messages):
        bid_attempts = []
        tts_regex = ChatCheckers.chat_bid_list["bid"]
        # print(self.bidding_active.is_set())
        if self.bidding_active is not None and self.bidding_active.is_set():
            for message in messages:
                print(message["message"])
                if message["message"].startswith(tts_regex):
                    # message["message"] = message["message"].replace(tts_regex,"")
                    bid_attempts.append(message)
            for message in bid_attempts:
                if random.randint(1,5) == 1:
                    message_to_say = f"{message['username']} is raising the bid!"
                    keyboard.write('e')
                    self.textToSpeechRunner.runTextToSpeech(message_to_say, message['username'])
                    print(f"Bid attempt: {message['message']} by {message['username']}")
                    print(message)
        else:
            for message in messages:
                if message["message"].startswith(tts_regex):
                    print("Bidding is not active")
                    print(f"{message['username']} attempted to bid, but bidding is not active")
