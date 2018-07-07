# This file goes onto the RPi Zero Camera device

from __future__ import print_function
from picamera import PiCamera
from time import sleep
import os
from datetime import datetime, time
from config.defaults import *

camera = PiCamera()
i = 0

def timeCheck():
    now = datetime.now()
    now_time = now.time()
    offTime = time(3,0)
    onTime = time(13,0)
    if now_time < offTime or now_time > onTime:
        return 1
    else:
        sleep(300)
        return 0


while(1):
    print("Sleeping")
    sleep(5)
    curTimeCheck = timeCheck()
    if curTimeCheck:
        print("Taking picture #{}".format(i))
        camera.capture("images/image{}.jpg".format(i))
        print("Copying file over to RPi3 device")
        os.system("scp -i /home/pi/.ssh/camera images/image{}.jpg pi@{}:~/chickens/images/".format(i, RPi3_IP))
        os.system("rm images/image{}.jpg".format(i))
        print()
        i+=1
