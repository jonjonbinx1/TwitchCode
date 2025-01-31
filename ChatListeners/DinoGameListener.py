class DinoGameListener:
    def __init__(self, action_options):
        self.action_options = action_options

    def call(self, messages):
        messagesToCheck = ["jump", "duck", "restart", "start"]
        for message in messages:
            if message["message"] in messagesToCheck:
                self.action_options.append(message["message"])
