# Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will move channel 0 from min to max position repeatedly.
# Author: Tony DiCola
# License: Public Domain
from __future__ import division
from time import sleep
import time
import csv
from picamera import PiCamera

# Import the PCA9685 module.
import Adafruit_PCA9685

import evdev
from evdev import InputDevice, categorize, ecodes, KeyEvent

event_time=0
ABS_X_min= -32768
ABS_X_max= 32767

##LT
ABS_Z_max= 152
##RT
ABS_RZ_max= 255

gamepad= InputDevice('/dev/input/event5')
print(gamepad)

##for i in range(6):
##    inp_dev=InputDevice('/dev/input/event'+str(i))
##    print(inp_dev)

##min=10 max=100, for slow smooth driving 20~
forward_sensivity=20
backward_sensivity=20

##Start camera
camera = PiCamera()
camera_on = False
video_on = False

# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Configure min and max servo pulse lengths
##Sol Donus
servo_min = 300  # Min pulse length out of 4096
##Orta
servo_mid = 400  # Min pulse length out of 4096
##Sag Donus
servo_max = 500  # Max pulse length out of 4096

dc_max = 4000  # Max pulse length out of 4096

# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

print('Moving servo on channel 0, press Ctrl-C to quit...')
    
for event in gamepad.read_loop():
    
    if event.type == ecodes.EV_KEY:
        keyevent = categorize(event)
        print("you pressed: '",keyevent.keycode[0],"'")
        if keyevent.keystate == KeyEvent.key_down:
            if keyevent.keycode[0] == 'B' and camera_on == False:
                camera.start_preview(fullscreen=False, window=(0,0,640,480))
                camera_on=True
##                time.sleep(5)
            elif keyevent.keycode[0] == 'B' and camera_on == True:
                camera.stop_preview()
                camera_on=False
##            elif keyevent.keycode[0] == 'BTN_B' and camera_on == True:
##                while True:
##                    camera.capture('img/img_'+
##                                   str(time.localtime(time.time())[0])+"_"+
##                                   str(time.localtime(time.time())[1])+"_"+
##                                   str(time.localtime(time.time())[2])+"_"+
##                                   str(time.localtime(time.time())[3])+"_"+
##                                   str(time.localtime(time.time())[4])+"_"+
##                                   str(time.localtime(time.time())[5])+"_"+
##                                   str(time.localtime(time.time())[6])+
##                                   '.jpg')
##                    sleep(100.0 / 1000.0)
                    
##                camera.start_recording('video_time.h264')
##                sleep(5)
            elif keyevent.keycode[0] == 'BTN_B' and camera_on == True and video_on == False:
                video_on = True
                camera.start_recording('img/video_time.h264')
            elif keyevent.keycode[0] == 'BTN_B' and camera_on == True and video_on == True:
                camera.stop_recording()
                video_on = False
                                           
            
    if event.type == ecodes.EV_ABS:
        absevent = categorize(event)
##        print(ecodes.bytype[absevent.event.type][absevent.event.code], absevent.event.value)
       
    
        if(ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_X"):
            if(absevent.event.value < 0):
##                Turning Servo To Left, 300 (servo_min) is max left, 400 is middle (servo_mid)
##                Multiplying by percentage of left analog joystick
                print("left servo: ",servo_mid-(servo_mid-servo_min)*float(absevent.event.value/ABS_X_min))
                servo_left=int(servo_mid-(servo_mid-servo_min)*(absevent.event.value/ABS_X_min))
                print("Left %: ", float(absevent.event.value/ABS_X_min*100))
                pwm.set_pwm(1,0,servo_left)

            elif(absevent.event.value > 0):
##                Turning Servo To Right, 500 (servo_max) is max right, 400 is middle (servo_mid)
##                Multiplying by percentage of left analog joystick
                servo_right=int(servo_mid+(servo_max-servo_mid)*(absevent.event.value/ABS_X_max))
                print("right servo: ", servo_right)
                pwm.set_pwm(1,0,servo_right)

            
        if(ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_RZ"):
            print("Forward %: ", float(absevent.event.value/ABS_RZ_max*100))
            fwr = int(350 + float(absevent.event.value/ABS_RZ_max*forward_sensivity))
            print("fwr: ",fwr)
            pwm.set_pwm(0,0,fwr)
            

        if(ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_Z"):
            print("Backward %: ", float(absevent.event.value/ABS_Z_max*100))
            bck = int(350 - float(absevent.event.value/ABS_Z_max*backward_sensivity))
            print("bck: ",bck)
            pwm.set_pwm(0,0,bck)
