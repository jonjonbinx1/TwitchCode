import pygetwindow as gw
import pynput

# Function to get the specific application's window
def get_app_window(window_title):
    windows = gw.getWindowsWithTitle(window_title)
    if windows:
        return windows[0]
    return None

def make_mouse_movement(x,y,window_name):
    app_window = get_app_window(window_name)
    print(app_window)
    if app_window:
        screen_width, screen_height = app_window.width, app_window.height
        app_window.activate()
    screen_x = int(x * (screen_width / 100)) + app_window.left
    screen_y = int(y * (screen_height / 100)) + app_window.top
    move_mouse(screen_x, screen_y)

def move_mouse(x, y):
    mouse = pynput.mouse.Controller()
    mouse.position = (x, y)
    mouse.click(pynput.mouse.Button.left)

def press_key(key):
    keyboard = pynput.keyboard.Controller()
    keyboard.press(key)
    keyboard.release(key)
