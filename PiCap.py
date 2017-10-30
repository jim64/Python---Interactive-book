#this program has been adapted from the touch-mp3.py program example that comes with
#the picap. Changed to a class so that instances of it can be called for each user
#takes parameter to modify the sensitivity of the touch sensor
#while running listens for sensor activation and calls songs class to play the sounds
#or audioRecorder to record a story




################################################################################
#
# Bare Conductive Pi Cap
# ----------------------
#
# touch-mp3.py - polyphonic touch triggered MP3 playback
#
# Written for Raspberry Pi.
#
# Bare Conductive code written by Stefan Dzisiewski-Smith and Szymon Kaliski.
#
# This work is licensed under a MIT license https://opensource.org/licenses/MIT
#
# Copyright (c) 2016, Bare Conductive
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
################################################################################

#from time import sleep
#from subprocess import call
#from Songs import Songs 
#from AudioRecorder import AudioRecorder
#from getRandom import getRandom
#import signal, sys, pygame, MPR121
#import RPi.GPIO as GPIO


class PiCap(object) :

  #initiates instance of class
  def __init__(self, name, setting) :
    self.name = name
    self.sensor = self.testConnection()
    self.recordNode = 12
    self.playNode = 6
    self.touch_threshold = 0
    self.release_threshold = 0
    self.setSettings(setting)
    self.setUp()
    self.songs = []
    self.rand = getRandom()

  def run(self) :
    self.setUp()
    self.setUpSongs()
    self.MainLoop()

  #test Pi Cap connections
  def Connection(self) :   
    try:
      sensor = MPR121.begin()
      return sensor
    except Exception as e:
      print(e)
      sys.exit(1)

  #modifies touch sensors
  def setSettings(self, setting):
    if setting == "l":
      self.touch_threshold = 5
      self.release_threshold = 2
    elif setting == "m":
      self.touch_threshold = 15
      self.release_threshold = 5
    else:
      self.touch_threshold = 30
      self.release_threshold = 20

  #sets up sensors and initiates pygame
  def setUp(self) : 
    self.sensor.set_touch_threshold(self.touch_threshold) 
    self.sensor.set_release_threshold(self.release_threshold) 
    signal.signal(signal.SIGINT, self.signal_handler)
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    pygame.mixer.pre_init(frequency = 44100, channels = 64, buffer = 1024)
    pygame.init()

  #exits program safely on close
  def signal_handler(self, signal, frame):
    sys.exit(0)

  #gets all songs to associate with sensor
  def setUpSongs(self) : 
    for i in range(self.playNode): 
      current = Songs(i, self.name)
      current.getSongsFromFile()
      self.songs.append(current)

  #runs the main loop. Listens for sensor touch, when recognised
  #plays or stops songs, or records depending on sensor
  #set to play continually so that My Story is constantly running
  def MainLoop(self) : 
    while True:
      if self.sensor.touch_status_changed():
        self.sensor.update_touch_data()
        for i in range(self.playNode):
          if self.sensor.is_new_touch(i) :
            temp = self.songs[i].isPlaying()
            audioSet = self.songs[i].getAudio()
            if audioSet != 0:
              if temp == False:
                self.songs[i].getAudio().play() 
              else :
                self.songs[i].getAudio().stop()
                self.songs[i].updateCurrent()
              self.songs[i].changePlaying()
        for i in range(self.playNode, self.recordNode) :
          if self.sensor.is_new_touch(i) :
            randomNum = self.rand.getRand()
            record = AudioRecorder(str(i), randomNum, self.name)
            record.start(self.sensor, self.songs)
    sleep(0.01)
    

