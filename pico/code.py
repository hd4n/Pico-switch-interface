import time
import board
import digitalio
import usb_hid
import usb_cdc

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

from keycodes import Codes

def send_key(command):
    if command[0] == '1':
        keyboard.press(Keycode.LEFT_CONTROL)
    if command[1] == '1':
        keyboard.press(Keycode.LEFT_ALT)
    if command[2] == '1':
        keyboard.press(Keycode.LEFT_SHIFT)

    if len(command) > 3:
        keyboard.press(Codes[command[3:]])

    keyboard.release_all()

def read_config():
    try:
        with open(config_filename, "r") as config:
            lines = config.readlines()
            config = []
            for line in lines:
                config.append(line[:-1])  # remove trailing newline
            return config
    except:
        return default_keys.copy()

def save_config(cf):
    try:
        with open(config_filename, "w") as config:
            for k in cf:
                config.write(f"{k}\n")
    except:
        pass

############

keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)

pins = [board.GP0, board.GP2, board.GP6, board.GP9, board.GP12]
input_GPIOs = []

default_keys = ["000 ", "000re", "000la", "000ra", "000a"]
config_filename = "/config.txt"

############

for i in range(len(pins)):
    input_GPIOs.append(digitalio.DigitalInOut(pins[i]))
    input_GPIOs[i].direction = digitalio.Direction.INPUT
    input_GPIOs[i].pull = digitalio.Pull.UP

serial = usb_cdc.data

keys = read_config()

released = True

while True:
    if released:
        for i in range(5):
            # logic is flipped because of the input pull up
            if not input_GPIOs[i].value:
                send_key(keys[i])

    # check if all inputs have been released
    released = True
    for i in range(5):
        if not input_GPIOs[i].value:
            released = False

    # handle commands sent over serial
    if serial.in_waiting > 0:
        serial_input = serial.read(serial.in_waiting)
        command = ''.join([chr(b) for b in serial_input])

        # commands used by the customization software
        if command == "GET_NAME":
            usb_cdc.data.write(bytes("SW_INTERFACE\n", "utf-8"))

        elif command == "GET_CONFIG":
            usb_cdc.data.write(bytes(";".join(keys) + "\n", "utf-8"))

        # reassign keystroke
        # message format: CF_<target_input>_<ctrl_bit><alt_bit><shift_bit><keycode>
        # e.g. CF_0_100re -> assign CTRL+Return to input 0
        elif "CF_" in command:
            target = int(command[3])
            keys[target] = command[5:]
            save_config(keys)

    time.sleep(0.1)
