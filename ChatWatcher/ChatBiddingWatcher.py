import pyttsx3
engine = pyttsx3.init()

import multiprocessing
import keyboard
from BaseCode.TwitchChatMessageRunner import MessageRunner
from ChatListeners.BiddingListener import BiddingListener
from Audio.TextToSpeech import TextToSpeechRunner

# Initialize pyttsx3 engine in the main thread
textToSpeechRunner = TextToSpeechRunner(engine)

def listen_for_space(bidding_active):
    def on_space_key(event):
        if event.name == 'space' and event.event_type == 'down':
            print("Space key pressed")
            if bidding_active.is_set():
                bidding_active.clear()
                textToSpeechRunner.runTextToSpeech("Bidding has been Deactivated", "internal")
            else:
                bidding_active.set()
                textToSpeechRunner.runTextToSpeech("Bidding Is Now Active", "internal")
            print(f"Bidding Active : {bidding_active.is_set()}")

    keyboard.hook(on_space_key)
    keyboard.wait('esc')  # Keep the listener running until 'esc' is pressed

def main():
    with multiprocessing.Manager() as manager:
        event = manager.Event()
        runner = MessageRunner()
        bidding_listener = BiddingListener(event)
        
        runner_process = multiprocessing.Process(target=runner.start, args=(0, [bidding_listener]))
        runner_process.start()

        listen_for_space_process = multiprocessing.Process(target=listen_for_space, args=(event,))
        listen_for_space_process.start()

        runner_process.join()
        listen_for_space_process.join()

if __name__ == "__main__":
    multiprocessing.set_start_method('spawn')  # Ensure 'spawn' method is used
    main()
