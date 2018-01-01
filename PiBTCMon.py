#!/usr/bin/python

import sys, time, urllib2, socket, json, os
from Adafruit_CharLCD import Adafruit_CharLCDPlate
import Adafruit_CharLCD as LCD
from PiBTCMonDisplay import PiBTCMonDisplay

# read config file
configuration = json.load(open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'configuration.json')))

display = PiBTCMonDisplay(configuration)
lcd = display.lcd
prevCol = -1
prev = ""
lastTime = time.time()

'''
#WIP - startup on boot
def internetOn():
  try:
    response=urllib2.urlopen('http://google.com',timeout=3)
    return True
  except urllib2.URLError as err:
    pass
  return False
'''

#Check for network connection at startup
t = time.time()
while True:
  lcd.clear()
  lcd.message('checking network\nconnection (' + str(int(time.time() - t)) + 's)...')
  time.sleep(1)
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 0))

    # set background color: set_color(red, green, blue)
    lcd.set_color(1.0, 1.0, 1.0)
    lcd.clear()
    lcd.message('IP address:\n' + s.getsockname()[0])
    s.shutdown(socket.SHUT_RDWR)
    s.close()
    time.sleep(1)
    display.initInfo()  # Start info gathering/display
    time.sleep(configuration["rotation_delay"])
    break             # Success
  except:
    time.sleep(3)     # Pause a moment, keep trying
'''
  if internetOn() == True:
    time.sleep(5)
    break         # Success
  else:
    time.sleep(1) # Pause a moment, keep trying
'''

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
