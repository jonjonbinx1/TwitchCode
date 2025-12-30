import random
from BaseCode import KeyAndMouseInputs

class GenericInputListener:
    message_to_action = {}
    check_for_mouse = False
    action_threshold = 0.3
    application_name = None
    allow_actions = True

    def set_messages_to_check(self, messages):
        self.message_to_action = messages
    def set_mouse_check(self, check):
        self.check_for_mouse = check
    def set_action_threshold(self, threshold):
        self.action_threshold = threshold
    def set_application_name(self, name):
        self.application_name = name

    def call(self, messages):
        action_options = []
        for message in messages:
            if self.allow_actions:
                if message["message"] == "stop" and message["username"] == "jonjon_binx":
                    self.allow_actions = False
                    break
                elif message["message"] in self.message_to_action.keys():
                    action_options.append(message["message"])
                elif self.check_for_mouse:
                    parts = message["message"].split()
                    if len(parts) == 2 and all(part.isdigit() for part in parts):
                        x, y = map(int, parts)
                        if 0 <= x <= 100 and 0 <= y <= 100:
                            coordinate = f"mouse:{x},{y}"
                            action_options.append(coordinate)
                for action in action_options:
                    if random.random() < self.action_threshold:
                        print(f"Executing action: {action}")
                        if action.startswith("mouse:") and self.application_name != None:
                            x, y = map(int, action.split(":")[1].split(","))
                            KeyAndMouseInputs.make_mouse_movement(x, y, self.application_name)
                        else:
                            KeyAndMouseInputs.press_key(self.message_to_action[action])
            else:
                if message["message"] == "start" and message["username"] == "jonjon_binx":
                    self.allow_actions = True
                    break