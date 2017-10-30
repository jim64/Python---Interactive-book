#simple class to load book for different users: used to switch between 
#for evaluation sessions. 

import sys
from PiCap import PiCap


done = False

print "enter user name"
name  = raw_input()
if name == "h" or name == "m" or name =="d" or name == "test" :
    while not done: 
      print "enter low (l) medium (m) or high (h) for sensor setting"
      setting = raw_input()
      if setting == "l" or setting == "m" or setting == "h":
        done = True
     
    print setting, "  finished" 
    new = PiCap(name, setting)
    new.run()
else:
  print "name not recognised. Exiting"


