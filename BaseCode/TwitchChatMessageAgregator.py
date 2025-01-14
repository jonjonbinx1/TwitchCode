from .DougDougTwitchConnection import Twitch
import time
class Aggregator:
    twitch = Twitch()
    def getCommand(self,duration, commandsToSearch, commandAndCount, listener=None):
        start_time = time.time()
        keep_alive = False
        if duration == 0:
            duration = 100
            keep_alive = True
        while time.time() < start_time + duration:
            messages = self.twitch.twitch_receive_messages()
            for message in messages:
                if message["message"].upper() in commandsToSearch:
                    if message["message"] in commandAndCount.keys():
                        commandAndCount[message["message"]] = commandAndCount[message["message"]] + 1
                    else:
                        commandAndCount.update({message["message"] : 1})
            if listener != None:
                time.sleep(10)
                listener(commandAndCount)
            if keep_alive:
                start_time = time.time()
        return commandAndCount
    
    def getChatMessages(self, duration, regex=None, listner=None):
        commandAndCount = {}
        start_time = time.time()
        keep_alive = False
        if duration == 0:
            duration = 100
            keep_alive = True
        if regex == None:
            regex = "!poll "
        while time.time() < start_time + duration:
            messages = self.twitch.twitch_receive_messages()
            for message in messages:
                if message["message"].startswith(regex):
                    content = message["message"].replace(regex, "")
                    if content in commandAndCount.keys():
                        commandAndCount[content] = commandAndCount[content] + 1
                    else:
                        commandAndCount.update({content : 1})
            if listner != None:
                listner(commandAndCount)
            if keep_alive:
                start_time = time.time()
        return commandAndCount
    
    def start(self, duration, commandAndCount, regex=None, filePath=None, listener=None):
        print(duration)
        self.twitch.twitch_connect("jonjon_binx")
        commands = []
        if filePath != None:
            with open(filePath, 'r') as file: 
                # Read all lines and strip newline characters 
                commands = [line.strip() for line in file.readlines()]
        if len(commands) > 0:
            return self.getCommand(duration, commands, commandAndCount)
        else:
            return self.getChatMessages(duration, regex=regex, listner=listener)



