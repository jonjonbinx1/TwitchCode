from BaseCode.TwitchChatMessageRunner import MessageRunner
from ChatListeners.GenericInputListener import GenericInputListener
from Constants import WordToInputMapping
def main():
    runner = MessageRunner()
    input_listener = GenericInputListener()
    action_input = WordToInputMapping.rpg_inputs
    action_input.update(WordToInputMapping.numbers)
    print(action_input)
    input_listener.set_messages_to_check(action_input)
    input_listener.set_mouse_check(True)
    input_listener.set_action_threshold(0.99)
    input_listener.set_application_name("LiP_Demo")
    runner.start(0, [input_listener])

if __name__ == "__main__":
    main()