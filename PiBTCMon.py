#!/usr/bin/python

import sys, signal, time, json, os
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
lastTime = time.time()
display.initInfo()

while True:
  now = time.time()
  since = now - lastTime
  if since > configuration["rotation_delay"] or since < 0.0:
    display.modeUp()
    lastTime = now
