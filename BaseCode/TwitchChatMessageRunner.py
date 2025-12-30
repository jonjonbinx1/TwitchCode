from .DougDougTwitchConnection import Twitch
import time
class MessageRunner:
    twitch = Twitch()
    def __init__(self):
        self._running = True

    def getChatMessages(self, duration, listeners=[], sleep_time=0):
        self._running = True
        start_time = time.time()
        keep_alive = False
        if duration == 0:
            duration = 100
            keep_alive = True
        while self._running and time.time() < start_time + duration:
            messages = self.twitch.twitch_receive_messages()
            for listener in listeners:
                listener.call(messages)
            if keep_alive:
                start_time = time.time()
            if sleep_time > 0:
                time.sleep(sleep_time)
            # return messages

    def stop(self):
        self._running = False
    
    def start(self, duration, listener=[], sleep_time=0):
        print(duration)
        self.twitch.twitch_connect("jonjon_binx")
        return self.getChatMessages(duration, listeners=listener, 
                                    sleep_time=sleep_time)



