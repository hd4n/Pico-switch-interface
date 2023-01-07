import usb_cdc
import storage
import board
import digitalio

# enable usb drive mode for reprogramming if GPIO 16 is shorted to ground,
# hide usb device otherwise

program_pin = digitalio.DigitalInOut(board.GP16)
program_pin.direction = digitalio.Direction.INPUT
program_pin.pull = digitalio.Pull.UP

usb_cdc.enable(console=True, data=True)
storage.remount("/", not program_pin.value)

if program_pin.value:
    storage.disable_usb_drive()
else:
    storage.enable_usb_drive()
