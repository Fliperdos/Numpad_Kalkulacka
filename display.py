import board
import busio
import displayio
import terminalio
from adafruit_display_text import label
from fourwire import FourWire
from adafruit_st7735r import ST7735R
import adafruit_ahtx0
import adafruit_bmp280

class Display:
    def __init__(self, spi, i2c):
        self.db = FourWire(spi, command = board.GP5,
                           chip_select = board.GP6, 
                           reset = board.GP4)
        self.display = ST7735R(self.db, width=160, height=128, rotation=90, bgr=True)

        self.base = Base(i2c, self)
        self.calc = Calculator(self)

    def switch(self):
        self.base.toggle()
        self.calc.toggle()

    def call(self, group):
        self.display.root_group = group


class Base(Display):
    def __init__(self, i2c, parent):
        self.parent = parent
        self.state = True
        self.aht = adafruit_ahtx0.AHTx0(i2c)
        self.group = displayio.Group()

        self.temp = label.Label(font=terminalio.FONT,
                           text='',
                           x=5, y=30, color=0x0062ff)
        self.hum = label.Label(font=terminalio.FONT,
                           text='',
                           x=5, y=45, color=0x0062ff)
        
        self.group.append(self.temp)
        self.group.append(self.hum)

    def toggle(self):
        self.state = not self.state
        print(f'- Base {self.state}')

        if self.state: self.parent.call(self.group)

    def main(self):
        self.temp.text = f'AHT temperature: {self.aht.temperature}'
        self.hum.text = f'AHT humidity: {self.aht.relative_humidity}'

class Calculator(Display):
    def __init__(self, parent):
        self.parent = parent
        self.state = False
        self.group = displayio.Group()
         
        self.eq = label.Label(font=terminalio.FONT, text='',
                              x=5, y=40, color=0x0062ff)
        self.result = label.Label(font=terminalio.FONT, text='',
                                  x=5, y=50, color=0x0062ff)
        self.txt = label.Label(font=terminalio.FONT, text='CALC ON',   
                              x=5, y=20, color=0x0062ff)
        self.group.append(self.txt)
        self.group.append(self.eq)
        self.group.append(self.result)
        
    
    def toggle(self):
        self.state = not self.state
        print(f'- Calc {self.state}')

        if self.state:
            self.eq.text = ''
            self.result.text = ''
            self.parent.call(self.group)

    def main(self, pos):
        if pos == 0:
            self.parent.switch()

        if pos == 1:
            self.eq.text += '1'
            print(self.eq.text)

        if pos == 2:
            self.eq.text += '+'
            print(self.eq.text)

        if pos == 3:
            try:
                x = eval(self.eq.text)  
                self.result.text = f'Result: {x}'
            except Exception as e: self.result.text = f'{e}'


