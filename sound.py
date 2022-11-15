from pygame import mixer
import time
mixer.init()

#Load audio file
mixer.music.load('alert.mp3')
mixer.music.set_volume(0.7)
#Play the music


while True:
      
    mixer.music.play()
    time.sleep(5)