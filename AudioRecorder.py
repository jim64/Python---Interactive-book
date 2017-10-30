#################################################################
#   adpated from library example : http://people.csail.mit.edu/hubert/pyaudio/
#   changed to a class so instances of this can be called to record for different pictures
#   also changed will record until stop method is called.
#################################################################

#this class initiates an instance of a recorder that can then be started, run 
#continuously until a new sensor touch is recieved then it will stop and write the 
#array of chunks which made up the recording to a wav file.

import pyaudio
import wave
import MPR121
from Songs import Songs

class AudioRecorder(object) :
  
  def __init__(self, name, rand, owner) :
    self.name = name
    self.path = "tracks/"+owner+"/"+str(int(self.name)-6) + str(rand)+".wav"
    self.recording = True
    self.frames = []
    self.stream = 1
    self.p = pyaudio.PyAudio()
    self.CHUNK = 516 #reduced for pi
    self.CHANNELS = 1 # mono
    self.RATE = 44100 #frequency Hz

  #starts the recording, opens the stream with the correct 
  #parameters, then appends each chunk receieved to the array
  #continues to do so until a new sensor touch is received
  def start(self, sensor, songs) :
    print("recording")
    self.stream = self.p.open(format=pyaudio.paInt16,
                    channels=self.CHANNELS,
                    rate=self.RATE,
                    input=True,
                    frames_per_buffer=self.CHUNK)

    while self.recording == True: 
      data = self.stream.read(self.CHUNK)
      self.frames.append(data)
      if sensor.touch_status_changed():
        sensor.update_touch_data()
        for i in range(6, 12) :
          if sensor.is_new_touch(i) :
            self.recording = False
          
    self.stop(songs)
    
  #stops the recording, closes the stream
  def stop(self, songs) :
    print("finished recording")
    self.stream.stop_stream()
    self.stream.close()
    self.p.terminate()
    self.writeFile(songs)

  #converts the array of chunked data to a wav file, then adds
  #this to the correct songs class
  def writeFile(self, songs):
    wf = wave.open(self.path, 'wb')
    wf.setnchannels(self.CHANNELS)
    wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(self.RATE)
    wf.writeframes(b''.join(self.frames))
    wf.close()
    position = int(self.name) - 6
    songs[position].addAudio(self.path)

if __name__ == "__main__" :
  test = AudioRecorder("test")
  test.start()
