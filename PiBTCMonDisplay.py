#!/usr/bin/python

from PiBTCMonInfo import PiBTCMonInfo
from Adafruit_CharLCD import Adafruit_CharLCDPlate
import time

class PiBTCMonDisplay(object):
  
  lcd = Adafruit_CharLCDPlate()
  info = None
  mode = 0
  offset = 0
  maxOffset = 0
  screen = [] 
  
  def __init__(self,configuration):
    self.configuration = configuration
    self.lcd.clear()

    # start with the LCD backlight blue
    self.lcd.set_color(1.0,1.0,0.0)
  
  #Show initial info (call after network connected)
  def initInfo(self):
    self.info = PiBTCMonInfo(self.configuration)
    # display the main screen after initializing
    self.dispScreen(self.info.screen[0])
  
  #Send text to display
  def dispScreen(self, newScreen):
    self.screen = newScreen
    self.offset = 0
    try:
      self.maxOffset = max((len(self.screen[0]) - 16), (len(self.screen[1]) - 16))
      self.lcd.clear()
      s = self.screen[0] + '\n' + self.screen[1]
      self.lcd.message(s)

      # scroll left if the screen is longer than the display
      while self.maxOffset > self.offset:
        time.sleep(1)
        self.scrollLeft()
    except TypeError:
      self.lcd.clear()

  #Offset text to the right
  def scrollLeft(self):
    if self.offset >= self.maxOffset: return
    self.lcd.move_left()
    self.offset += 1
  
  #Offset text to the left
  def scrollRight(self):
    if self.offset <= 0: return
    self.lcd.scrollDisplayRight()
    self.offset -= 1
  
  #Display next info screen
  def modeUp(self):
    self.mode += 1
    if self.mode >= len(self.info.screen): self.mode = 0
    self.update()
  
  #Display previous info screen
  def modeDown(self):
    self.mode -= 1
    if self.mode < 0: self.mode = len(self.info.screen)
    self.update()
  
  #Update display
  def update(self):
    # refresh screens and data
    self.info.refresh()
    # display screen
    self.dispScreen(self.info.screen[self.mode])
