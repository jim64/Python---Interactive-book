#used to get random numbers between 0 and 100. Numbers will
#not be repeated in this range

import random

class getRandom(object) :

  #used holds all previous used numbers
  def __init__(self) :
    self.used = []

  #gets a number and returns if not yet seen
  def getRand(self):
    temp = random.randint(0, 100)
    if self.seenRandom(temp) == True :
      temp = self.getRand()
    return temp

  #scans array to check for seen numbers
  def seenRandom(self, temp) :
    for x in range(0, len(self.used)) :
      if self.used[x] == temp :
        return True
    self.used.append(temp)
    return False

  #test function
  def testCheck(self) :
    used = []
    i = 0
    while (i!=100) :
      temp = self.getRand()
      used.append(temp)
      for x in range(0, len(used)-1) :
        assert(temp != used[x])
      i+=1
  
    
if __name__ == "__main__" :
  test = getRandom()
  temp = test.getRand()
  assert temp >= 0 and temp <= 100
  test.testCheck()
