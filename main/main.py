def unloadModule(mod):
    import sys
    # removes module from the system
    mod_name = mod.__name__
    if mod_name in sys.modules:
        del sys.modules[mod_name]
        
def cubic_ease(start, end, progress):
    # Ensure progress is between 0 and 1
    progress = max(0, min(1, progress))
    
    # Apply the cubic easing function
    eased_progress = progress * progress * (3 - 2 * progress)
    
    # Map the eased progress to the start and end values
    return int(start + (end) * eased_progress)

        
if __name__ == "__main__":
    from machine import Pin, PWM
    import sounds
    import time

    #connect switch to GP1 and GND. when switch is closed we run a short version of the main code.
    #this lets us choose between short or long card times on the device
    option_switch = Pin(14, mode=Pin.IN, pull=Pin.PULL_UP)
    #for now, GP2 will be what starts the execution
    draw_button = Pin(17, mode=Pin.IN, pull=Pin.PULL_UP)

    pwm = PWM(Pin(21))
    pwm.freq(1000)
    
    #dont play startup sounds if we reset ourselves (only when powered on)
    if machine.reset_cause() != 3:
        sounds.play(sounds.startup,2,'slide')

    #breath LED while waiting
    max_duty = const(65025)
    duty = 0.05
    going_up = True
    #track time in idle to trigger warning sound
    startup_time = time.mktime(time.localtime())
    while True:
        if draw_button.value() != 1:
            sounds.play(sounds.click,4)
            #memory clear
            unloadModule(PWM)
            #unloadModule(sounds)
            del going_up
            del duty
            del pwm
            del draw_button
            del Pin
            del PWM
            del sounds
            #draw cards!
            if option_switch.value() == 1:
                import mshort
                try:
                    mshort.draw()
                except:
                    machine.reset()
            else:
                import mlong
                mlong.draw()
        else:
            pwm.duty_u16(cubic_ease(0,max_duty,duty))
            if (time.ticks_cpu() % 8 == 0):
                if going_up:
                    if duty < 1:
                        #duty += (max(int(duty / 1000),1))
                        duty += 0.00005 + (duty / 500)
                    else:
                        going_up = False
                else:
                    if duty > 0:
                        #duty -= (max(int(duty / 2000),1))
                        duty -= 0.00001 + (duty / 1000)
                    else:
                        going_up = True
            
            if (time.mktime(time.localtime()) - startup_time > 300) and (time.mktime(time.localtime()) % 6 == 0):
                
                if (time.mktime(time.localtime()) - startup_time > 330):
                    import greensleeves
                    sounds.play(greensleeves.song,1,'slide',2)
                else:
                    sounds.play(sounds.powerwarning,1)
        
