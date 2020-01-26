import pyautogui
import autoit
from pynput.keyboard import Key, Listener

import os
import sys
import time

import setup

settings_dict = setup.load_settings('settings.txt')

center_mouse_when_inv_opens = settings_dict['center_mouse_when_inv_opens']

selected_pixel_position_x = settings_dict['selected_pixel_position_x']
selected_pixel_position_y = settings_dict['selected_pixel_position_y']

center_mouse_position_x = settings_dict['center_mouse_position_x']
center_mouse_position_y = settings_dict['center_mouse_position_y']

exit_script_key = settings_dict['exit_script_key']
restart_script_key = settings_dict['restart_script_key']

hotbarToPos = { "1": 745,
                "2": 800,
                "3": 850,
                "4": 900,
                "5": 960,
                "v": 1015,
                "c": 1070,
                "r": 1120,
                "f": 1175 }

def center_mouse(delay):
    time.sleep(delay) # Pause a bit so the mouse move registers
    autoit.mouse_move(center_mouse_position_x, center_mouse_position_y, 0) # Moves the mouse to the center of the screen

def on_press(key):
    # Get a color value from a pixel that has a specific value when we are inside the inventory or chest
    pixel_value = sum(pyautogui.pixel(selected_pixel_position_x, selected_pixel_position_y))

    # Try to convert the "key" to a char. If it fails, it is a special charachter like shift for example
    try: pressed_key = key.char
    except: return True # Skips the rest of the code below
    
    # Check if we are inside the inventory. The pixel_value of our selected pixel is 594 when we are inside the inventory/chest
    if pixel_value == 594:
        if pressed_key == "1": hotkey("1")
        elif pressed_key == "2": hotkey("2")
        elif pressed_key == "3": hotkey("3")
        elif pressed_key == "4": hotkey("4")
        elif pressed_key == "5": hotkey("5")
        elif pressed_key == "v": hotkey("v")
        elif pressed_key == "c": hotkey("c")
        elif pressed_key == "r": hotkey("r")
        elif pressed_key == "f": hotkey("f")
        print('{0} pressed (Inside inventory/chest)'.format(key))
    else:
        if (center_mouse_when_inv_opens.lower() == 'true') and (pressed_key == "e"): center_mouse(0.06)
        print('{0} pressed - #{1}'.format(key, pixel_value))

    # If user presses the exit_script_key as listed in settings.txt we exit the program
    if pressed_key == exit_script_key: return False

    # Check if the pixel we've selected has the value 509. If that is true we restart the script because it will then get stuck on that value and never change. We can also manually restart the script by pressing "z". The script also restarts if it gets buggy and starts outputtin "\x17" when the user presses "w"
    if (pixel_value == 509) or (pressed_key == restart_script_key) or (pressed_key == '\x17'):
        print("Restarting script...")
        os.execl(sys.executable, sys.executable, * sys.argv)

def hotkey(key):
    position = pyautogui.position()
    autoit.mouse_click("left")
    autoit.mouse_click("left", hotbarToPos[key], 745, 1, 0)
    autoit.mouse_click("left", position[0], position[1], 1, 0)
    time.sleep(0.05)

def main():
    os.system('mode con: cols=60 lines=20')
    print("Started listening for keys...\n(press '" + exit_script_key + "' to exit and '" + restart_script_key + "' to restart)\n")
    with Listener(on_press=on_press) as listener:
        listener.join()
    print("Program successfully terminated")
    time.sleep(1)

if __name__ == "__main__":
    main()