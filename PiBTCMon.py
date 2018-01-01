#!/usr/bin/python

import sys, signal, time, json, os
# from Adafruit_CharLCD import Adafruit_CharLCDPlate
import Adafruit_CharLCD as LCD
from PiBTCMonDisplay import PiBTCMonDisplay

def sigint_handler(signal, frame):
    '''Print a message and cleanup the display before exit'''
    lcd.clear()
    lcd.message('Interrupted,\nshutting down.')
    time.sleep(2)
    lcd.clear()
    try:
      sys.exit(0)
    except SystemExit:
      os._exit(0)

# register the handler
signal.signal(signal.SIGINT, sigint_handler)

# read config file
configuration = json.load(open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'configuration.json')))

display = PiBTCMonDisplay(configuration)
lcd = display.lcd
prevCol = -1
prev = ""
lastTime = time.time()

display.initInfo()

buttons = ( (LCD.SELECT, 'Select', (1,1,1)),
            (LCD.LEFT,   'Left'  , (1,0,0)),
            (LCD.UP,     'Up'    , (0,0,1)),
            (LCD.DOWN,   'Down'  , (0,1,0)),
            (LCD.RIGHT,  'Right' , (1,0,1)) )

# Listen for button presses
while True:
  b = ""
  for button in buttons:
    if lcd.is_pressed(button[0]):
      b += button[1]
  if b != prev:
    if lcd.is_pressed(LCD.LEFT):
      display.scrollRight()
    elif lcd.is_pressed(LCD.RIGHT):
      display.scrollLeft()
    elif lcd.is_pressed(LCD.UP):
      display.modeUp()
    elif lcd.is_pressed(LCD.DOWN):
      display.modeDown()
    prev = b
    lastTime = time.time()
  else:
    now = time.time()
    since = now - lastTime
    if since > configuration["rotation_delay"] or since < 0.0:
      display.modeUp()
      lastTime = now
