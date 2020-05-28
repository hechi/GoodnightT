import appdaemon.plugins.hass.hassapi as hass

SINGLE_CLICK=1002
DOUBLE_CLICK=1004
TRIPLE_CLICK=1005
QUAD_CLICK=1006
FIVE_CLICK=1010
PRESS=1000
PRESS_3SEC=1001
PRESS_LONG=1003

class Goodnight(hass.Hass):
  global SINGLE_CLICK
  global DOUBLE_CLICK

  def initialize(self):
      self.log(self.args)
      self.log("Hello from Goodnight module")
      ids = self.args["light_ids"]
      self.light_ids=[]
      for light_id in self.split_device_list(ids):
        self.light_ids.append(light_id)
        self.log('register '+str(light_id))
      self.switch_id = self.args["switch_id"]
      SINGLE_CLICK = self.args["switch_single_click_event_code"] if 'switch_single_click_event_code' in self.args else SINGLE_CLICK
      DOUBLE_CLICK = self.args["switch_double_click_event_code"] if 'switch_double_click_event_code' in self.args else DOUBLE_CLICK
      self.durationInSeconds = self.args["durationInSeconds"] if 'durationInSeconds' in self.args else 120
      self.brightness = self.args["start_brightness"] if 'start_brightness' in self.args else 254
      self.stepSize = self.brightness/self.durationInSeconds
      self.timer = None
      self.currentBrightness = None
      self.handle = self.listen_event(self.handle_event, "deconz_event")
  
  def handle_event(self, event_name, data, kwargs):
    if 'id' not in data or data['id'] != self.switch_id:
      return
    # self.log("Movement {}".format(data))
    eventCode = data['event']
    if eventCode == SINGLE_CLICK:
      self.setStepBasedOnCurrentBirghtness()
      self.getTimer().startTimer()
    if eventCode == DOUBLE_CLICK:
      self.getTimer().stopTimer()

  def setStepBasedOnCurrentBirghtness(self):
    brightness_max = None
    # find brightest light
    for light_id in self.light_ids:
      try:
        temp_brightness = int(self.get_state(light_id, "brightness")) # get lights current brightness
        if not brightness_max or temp_brightness > brightness_max:
          brightness_max=temp_brightness
      except:
        counter = 3
        while(counter>0):
          try:
            temp_brightness = int(self.get_state(light_id, "brightness"))
            if not brightness_max or temp_brightness > brightness_max:
              brightness_max=temp_brightness
          except:
            time.sleep(1)
          counter = counter - 1
    if not brightness_max:
      self.brightness = 254 # maximum light if nothing can be received
    else:
      self.brightness = brightness_max
    self.stepSize = self.brightness/self.durationInSeconds

  def startNightMode(self):
    self.log('start night mode')
    self.turnOnLight(brightness=self.brightness)

  def stopNightMode(self):
    self.log('stop night mode')
    self.turnOffLight()

  def turnOnLight(self, brightness=254):
    for light_id in self.light_ids:
      if self.get_state(light_id) == "off":
        self.log('turn on light '+str(light_id)+' with '+str(brightness)+' brightness')
        self.turn_on(light_id, brightness=brightness)

  def turnOffLight(self):
    for light_id in self.light_ids:
      if self.get_state(light_id) == "on":
        self.log('turn of light'+str(light_id))
        self.turn_off(light_id)

  def dimLights(self):
    self.brightness = self.brightness - self.stepSize
    for light_id in self.light_ids:
      self.turn_on(light_id, brightness=self.brightness)

  def getTimer(self):
    if not self.timer or not self.timer.isAlive():
      self.timer = Timer(controller=self,startFunction=self.startNightMode, stopFunction=self.stopNightMode, stepFunction=self.dimLights, stepInSeconds=1, timerInSeconds=self.durationInSeconds)
    return self.timer


import threading
import time
# somehow i cant use this class outside of this script :(
class Timer(threading.Thread):

  def __init__(self, controller, startFunction, stopFunction, stepFunction=None, stepInSeconds=1, timerInSeconds=120): 
    threading.Thread.__init__(self)
    self.controller = controller
    self.startFunction = startFunction
    self.stopFunction = stopFunction
    self.stepFunction = stepFunction
    self.stepInSeconds = stepInSeconds
    self.timerInSeconds = timerInSeconds
    self.counter = 0
    self.setDaemon(True)
    self.stop=True
  
  def startTimer(self):
    self.stop=False
    if self.isAlive():
      self.counter = 0
    else:
      self.start()

  def stopTimer(self):
    self.stop=True
    self.counter=0

  def resetTimer(self):
    self.counter = 0

  def run(self):
    if self.startFunction:
      self.startFunction()
    while self.counter < self.timerInSeconds:
      time.sleep(self.stepInSeconds)
      self.counter = self.counter + self.stepInSeconds
      if self.stepFunction:
        self.stepFunction()
      if self.stop:
        break
    if self.stopFunction:
      self.stopFunction()
