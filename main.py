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
KEYCODES = (
    'calc', Keycode.KEYPAD_ONE, Keycode.KEYPAD_TWO, Keycode.ENTER
)

matrix = keypad.KeyMatrix(
    row_pins=ROWS,
    column_pins=COLS
)

keeb = Keyboard(usb_hid.devices)
display = Display(SPI, I2C)

lt = time.monotonic()
def base_interrupt():
    global lt
    ct = time.monotonic()

    if ct - lt > 1:
        #print('main')
        display.base.main()
        lt = ct

#   Handle Key Press (event)
def keyboard_interrupt(pos):
    if event.pressed:
        if display.calc.state:
            display.calc.main(pos)

        else:
            if KEYCODES[pos] != 'calc':
                keeb.press(KEYCODES[pos])
            else:
                display.switch()
            
    elif event.released and KEYCODES[pos] != 'calc':
        keeb.release(KEYCODES[pos])

#   Main Loop   
while True:
    event = matrix.events.get()

    if display.base.state:
        base_interrupt()

    if event:
        pos = event.key_number
        keyboard_interrupt(pos)





