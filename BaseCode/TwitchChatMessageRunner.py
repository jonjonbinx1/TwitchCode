from .DougDougTwitchConnection import Twitch
import time
class MessageRunner:
    twitch = Twitch()
    def getChatMessages(self, duration, listeners=[]):
        start_time = time.time()
        keep_alive = False
        if duration == 0:
            duration = 100
            keep_alive = True
        while time.time() < start_time + duration:
            messages = self.twitch.twitch_receive_messages()
            for listener in listeners:
                listener(messages)
            if keep_alive:
                start_time = time.time()
            return messages
    
    def start(self, duration, listener=[]):
        print(duration)
        self.twitch.twitch_connect("jonjon_binx")
        return self.getChatMessages(duration, listeners=listener)



