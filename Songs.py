#Looks in file for audio files associated with owner and
#sensor. Loads each as a pygame sound object into array
#methods to check if currently playing, to change playing
#boolean, to add to array and to return current object

import pygame
import os

class Songs(object) :

    def __init__(self,name, owner) :
        self.name = name
        self.owner = owner
        self.audio = []
        self.current = 0
        self.playing = False

    #loads audio from file
    def getSongsFromFile(self) :
        for files in os.listdir("./tracks/"+self.owner) :
            s = files
            if s[0] == str(self.name) :
                print(s)
		self.addAudio("./tracks/"+self.owner+"/" + s);

    #sets all as pygame audio objects and adds to array
    def addAudio(self, newAudio) :
        audio = pygame.mixer.Sound(newAudio)
        audio.set_volume(1.0)
        self.audio.append(audio)

    #to check if currently playing
    def isPlaying(self) :
        temp = self.playing
        return temp

    #to change boolean for playing
    def changePlaying(self) :
        if self.playing == False : 
            self.playing = True
        else : 
            self.playing = False

    #updates current position to switch to next song
    #if at end of array switches back to beginning
    def updateCurrent(self) :
        self.current += 1
        if self.current >= len(self.audio) :
            self.current = 0
            
    #returns name to tell which sensor this object is 
    #associated with
    def getName(self) :
        temp = self.name
        return temp

    #returns the current audio
    def getAudio(self):
        if not self.audio :
            return 0;
        else:
            temp = self.audio[self.current]
            return temp
    
    def getLen(self) :
        return len(self.audio)

#for testing
if __name__ == "__main__" :
    test = Songs("test")
    assert test.getAudio() == 0
    test.addAudio("one")
    test.addAudio("two")
    assert test.getAudio() == "one"
    assert test.getAudio() == "two"
    assert test.current == 2

    print ("success")
