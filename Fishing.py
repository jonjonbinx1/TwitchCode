from BaseCode import KeyAndMouseInputs
from time import sleep, time
from random import randint
import win32gui as w
from pynput import keyboard

message_options = [["h", "e", "c", "k", "e", "m" , "s"], 
                   ["l", "e", "g", "i", "t", "m", "e", "s", "s", "a", "g", "e", "h", "e", "r", "e", "!"],
                   ["d", "o", " ", "h", "a", "v", "e", " " , "a", "n", "y", " ", "c", "u", "p", "c", "a", "c", "k","e","s"]]
def main():
    sleep(5)
    title = w.GetWindowText(w.GetForegroundWindow())
    print(title)
    window_name = title#"Nysaliwow - Twitch and 2 more pages - Personal - Microsoft​ Edge" 
    while True:
        KeyAndMouseInputs.make_mouse_movement(85, 87, window_name)
        sleep(1)
        KeyAndMouseInputs.press_key("!")
        sleep(1)
        KeyAndMouseInputs.press_key("f")
        sleep(1)
        KeyAndMouseInputs.press_key("i")
        sleep(1)
        KeyAndMouseInputs.press_key("s")
        sleep(1)
        KeyAndMouseInputs.press_key("h")
        sleep(1)
        KeyAndMouseInputs.press_key(keyboard.Key.enter)
        if randint(0, 5) == 0:
            sleep(randint(5, 10))
            KeyAndMouseInputs.make_mouse_movement(86, 87, window_name)
            for message in message_options[randint(0, 1)]:
                KeyAndMouseInputs.press_key(message)
            KeyAndMouseInputs.press_key(keyboard.Key.enter)

        sleep(randint(120, 145))

if __name__ == "__main__":
    main()