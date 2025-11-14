from display import Display
import board
import busio
import displayio
import keypad
import usb_hid
import time
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from scanner import scan_i2c

displayio.release_displays()

SPI = busio.SPI(clock=board.GP2, MOSI=board.GP3)
I2C = busio.I2C(scl=board.GP15, sda=board.GP14)
scan_i2c(I2C)

ROWS = (board.GP16,)
COLS = (board.GP17, board.GP18, board.GP19, board.GP20,)
KEYCODES = ('switch', Keycode.KEYPAD_ONE, Keycode.KEYPAD_TWO, Keycode.ENTER)

matrix = keypad.KeyMatrix(row_pins=ROWS, column_pins=COLS)
keeb = Keyboard(usb_hid.devices)
display = Display(SPI, I2C)

lt = time.monotonic()

def base_interrupt() -> None:           # Sensor update in Base mode
    global lt
    ct = time.monotonic()

    if ct-lt > 3:
        display.base.update()
        lt = ct

def keyboard_interrupt(pos) -> None:    # Handles button press
    keycode = KEYCODES[pos]

    if keycode != 'switch':     # Normal button press
        if event.pressed: keeb.press(keycode)   # button = pressed
        else: keeb.release(keycode)     # button = released
    
    else:                       # Button switches display state ==> keycode == 'switch'
        if event.pressed: display.switch()  # button = pressed
        else: return    # button = released


while True:         # Main loop
    if display.base.state: base_interrupt() # Sensor update if display is in Base mode

    event = matrix.events.get()

    if event:       # if theres a button press
        pos = event.key_number

        if event.pressed & display.calc.state: display.calc.main(pos)   # If display is in calculator mode
        else: keyboard_interrupt(pos)   # If display is in base mode






