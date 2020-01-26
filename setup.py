import pyautogui
from pynput.keyboard import Key, Listener
import time
import os

def load_settings(path):
	content_in_dict_form = {}
	with open(path, 'r') as file:
		content = file.readlines()
		for setting in content:
			setting = setting.strip().split(' = ')
			try: int(setting[1])
			except: content_in_dict_form[setting[0]] = setting[1]; continue
			content_in_dict_form[setting[0]] = int(setting[1])
	return content_in_dict_form

def update_settings(settings_dict, path):
	content = ""
	with open(path, 'r') as file:
		for key in settings_dict:
			content += key + " = " + str(settings_dict[key]) + "\n"
	with open(path, 'w') as file:
		file.write(content)

def on_press(key):
	try: pressed_key = key.char
	except: return True

	if pressed_key == 'y':
		position = pyautogui.position()
		print("New selected position: ", position)
		settings_dict = load_settings('settings.txt')
		settings_dict['selected_pixel_position_x'] = position[0]
		settings_dict['selected_pixel_position_y'] = position[1]
		update_settings(settings_dict, 'settings.txt')
		print("Script finished successfully!\nExiting in 2 seconds...")
		time.sleep(2)
		return False

	if pressed_key == 'n': return False

def calibrate_pixel_position():
    os.system('mode con: cols=70 lines=10')
    print("Hover your cursor over your Minecraft client\nand move it to the red circle area as shown in the included picture.")
    print("Then when you're ready, press the button 'y'.\nIf you want to exit the program, press 'n'\n")
    print("waiting...")
    with Listener(on_press=on_press) as listener:
    	listener.join()

if __name__ == "__main__":
	calibrate_pixel_position()