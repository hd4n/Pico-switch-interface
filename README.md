# Pico Switch Interface

## Map physical buttons to keystrokes

This Raspberry Pi Pico based device allows connecting up to 5 input switches with 3.5 mm jack plugs. Each input is mapped to a keystroke and can be reprogrammed over serial. Similar to the [Ablenet Hitch 2](https://www.ablenetinc.com/hitch-2/).

### Hardware

- Raspberry Pi Pico
- 5x 3.5 mm jack inputs
- Micro USB to USB A conversion for added rigidity

| GPIO | Connection|
| ---- | ---- |
| 0 | jack 1 |
| 2 | jack 2 |
| 6 | jack 3 | 
| 9 | jack 4 |
| 12 | jack 5 |
| 16 | GND when usb drive mode is enabled |

- The other pole of the jacks is tied to ground
- To access the files on the Pico, GPIO 16 must be shorted to ground when plugging in the device

### Firmware

A modified version of CircuitPython that works with iPhones/iPads. Boards using the original firmware normally get disabled on these devices for reporting a high maximum power consumption.

### Commands

The keystrokes can be reassigned by sending specific commands over serial.

``` CF_<target>_<ctrl><alt><shift><keycode> ```

- The target input ranges from 0-4
- Modifiers are represented by 1-1 bits
- Non-modifier keys are represented by 1 (alphanumerical keys) or 2 (special keys) letters. Available keycodes can be found in [keycodes.py](/pico/keycodes.py)

Example - assign CTRL+Return to input 0

``` CF_0_100re ```