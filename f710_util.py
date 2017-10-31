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

for event in gamepad.read_loop():

    
    if event.type == ecodes.EV_KEY:
        keyevent = categorize(event)
        print("you pressed: '",keyevent.keycode[0],"'")
        if keyevent.keystate == KeyEvent.key_down:
            if keyevent.keycode[0] == 'BTN_A':
                continue
            
    if event.type == ecodes.EV_ABS:
        absevent = categorize(event)
##        print(ecodes.bytype[absevent.event.type][absevent.event.code], absevent.event.value)
       
    
        if(ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_X"):
            if(absevent.event.value < 0):
##                print("abs min: ",absevent.event.value)
                print("Left %: ", float(absevent.event.value/ABS_X_min*100))
            elif(absevent.event.value > 0):
##                print("abs max: ",absevent.event.value)
                print("Right %: ", float(absevent.event.value/ABS_X_max*100))
            else:
                continue
            
        if(ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_RZ"):
            print("Forward %: ", float(absevent.event.value/ABS_RZ_max*100))

        if(ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_Z"):
            print("Backward %: ", float(absevent.event.value/ABS_Z_max*100))
            

        
