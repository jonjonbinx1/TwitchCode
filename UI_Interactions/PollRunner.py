from BaseCode.TwitchChatMessageAgregator import Aggregator
from Constants.FilesToRead import FileMap

class PollRunner:
    aggregator = Aggregator()
    last_poll_sum = 0
    file_codes = {
        0 : "firstplace",
        1 : "secondplace",
        2 : "thirdplace",
        3 : "fourthplace", 
        4 : "fifthplace"
    } 
    def setPollTitle(self, pollTitle):
        with open(FileMap.files["polltitle"], "w") as f:
            f.write(pollTitle)

    def updatePollResults(self, pollResults):
        #Sort the results so max is first
        sorted_results = dict(sorted(pollResults.items(), key=lambda item: item[1], reverse=True))
        #Trigger value to update the poll standings
        do_update_standings = False
        #If there are any results
        if len(sorted_results) > 0:
            #Get the total
            results_sum = sum(sorted_results.values())
            #Counter to break after 5 results
            count = 0
            for key, value in sorted_results.items():
                if count >= 5:
                    break
                if self.last_poll_sum != results_sum:
                    print(key)
                    percent_as_length = int(value/results_sum * 10)
                    solid_bar = self.create_solid_bar(percent_as_length)
                    key_word = key
                    if len(key_word) > 6:
                        key_word = key_word[0:6]
                        key_word = key_word + ".."
                    elif len(key_word) < 7:
                        to_add = " " *(11 - len(key_word))
                        key_word = key_word + to_add
                    print(len(key_word))
                    with open(FileMap.files[self.file_codes[count]], "w", encoding="utf-8") as f:
                        f.write(key_word + " : " + solid_bar)
                count += 1
            self.last_poll_sum = results_sum
    def create_solid_bar(self, length): 
        return '█' * length

    def runPoll(self, pollTitle, duration, pollType=None):
        self.setPollTitle(pollTitle)
        for key in self.file_codes.values():
            with open(FileMap.files[key], "w") as f:
                f.write("")
        filePath = None
        if pollType != None:
            filePath = FileMap.files[pollType]
        pollDict = {}
        self.aggregator.start(duration, pollDict, filePath, listener=self.updatePollResults)
