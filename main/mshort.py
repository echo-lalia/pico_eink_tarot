from Pico_ePaper import EinkPIO
#from ePaperOfficial import EPD_3in7
import framebuf
import chaos
import machine
from machine import Pin, PWM
import random
import gc
import time
import sys
import sounds

def unloadModule(mod):
    # removes module from the system
    mod_name = mod.__name__
    if mod_name in sys.modules:
        del sys.modules[mod_name]
        
def draw():
    
    #turn led on
    pwm = PWM(Pin(21))
    pwm.freq(1000)
    pwm.duty_u16(2000)
    epd = EinkPIO(rotation=0)

    sounds.play(sounds.thump,4)
    #generate random info from adc
    reading = chaos.get(50)
    reading2 = chaos.get(5)
    str_reading = str(reading) + str(abs(reading2))
    reading = int(str_reading)

    del reading2
    del str_reading
    
    #also add the current ticks time because it non-scientifically feels better to me to add random from multiple sources
    reading += time.ticks_cpu()
    pwm.duty_u16(0)

    #init random with our chaos we collected
    print("Seed: " + str(reading))
    random.seed(reading)
    
    #get our image
    imageNum = random.randint(1,78)
    #decide if were reversed
    displayrotation = 0
    if random.randint(1,5) == 5:
        displayrotation = 180
    #decide now if we will glitch
    glitchrand = random.randint(1,100)


    #load in the image driver
    if displayrotation == 180:
        epd = EinkPIO(rotation=180)
        #change rotation without re-initializing
        #epd._rotation = 180
        #epd._send(0x11, 0x00)
        #epd._set_window(epd.width - 1, 0, epd.height - 1, 0)
        print("REVERSED")
        
    #use random to import specific image
    filename = "images/i" + str(imageNum) + ".py"

    #the 'partial' version of the image driver does not always set the color channels correctly for some reason
    colorchannel1 = epd.RAM_BW
    colorchannel2 = epd.RAM_RED

    # Import image files
    #import i + whichimage as img
    img = __import__(filename[:-3])

    
    #randomly decide if we will add glitch
    if glitchrand == 1 or glitchrand == 2:
        #image split down the middle
        print("Glitch: Xsplit")
        img_tmp = framebuf.FrameBuffer(img.img_bw, 280, 480, framebuf.MONO_HLSB)
        epd.blit(img_tmp, 140, 0, ram=colorchannel1)
        img_tmp = framebuf.FrameBuffer(img.img_red, 280, 480, framebuf.MONO_HLSB)
        epd.blit(img_tmp, 140, 0, ram=colorchannel2)
        img_tmp = framebuf.FrameBuffer(img.img_bw, 280, 480, framebuf.MONO_HLSB)
        epd.blit(img_tmp, -140, 0, ram=colorchannel1)
        img_tmp = framebuf.FrameBuffer(img.img_red, 280, 480, framebuf.MONO_HLSB)
        epd.blit(img_tmp, -140, 0, ram=colorchannel2)
    elif glitchrand == 3:
        print("Glitch: Ysplit")
        #split vertically with a horizontal line in the middle
        img_tmp = framebuf.FrameBuffer(img.img_bw, 280, 480, framebuf.MONO_HLSB)
        epd.blit(img_tmp, 0, 240, ram=colorchannel1)
        img_tmp = framebuf.FrameBuffer(img.img_red, 280, 480, framebuf.MONO_HLSB)
        epd.blit(img_tmp, 0, 240, ram=colorchannel2)
        img_tmp = framebuf.FrameBuffer(img.img_bw, 280, 480, framebuf.MONO_HLSB)
        epd.blit(img_tmp, 0, -240, ram=colorchannel1)
        img_tmp = framebuf.FrameBuffer(img.img_red, 280, 480, framebuf.MONO_HLSB)
        epd.blit(img_tmp, 0, -240, ram=colorchannel2)
    elif glitchrand == 4:
        print("Glitch: HMSB")
        #HMSB color error
        img_tmp = framebuf.FrameBuffer(img.img_bw, 280, 480, framebuf.MONO_HMSB)
        epd.blit(img_tmp, 0, 0, ram=colorchannel1)
        img_tmp = framebuf.FrameBuffer(img.img_red, 280, 480, framebuf.MONO_HMSB)
        epd.blit(img_tmp, 0, 0, ram=colorchannel2)
    elif 5 <= glitchrand <= 8:
        print("Glitch: Shift")
        #select part of image and copy it to a random location
        randXplacement = random.randint(-270, 270)
        randYplacement = random.randint(-10,450)
        rand_numrows = random.randint(10,400)
        rand_rowaddress = random.randint(0, 480 - rand_numrows)
        rowlength = 35
        selectlength = rowlength * rand_numrows
        selected_img = bytearray(selectlength)
        #bw
        for i in range(rand_numrows):
            start = (rand_rowaddress + i) * rowlength
            end = start + rowlength
            selected_img[i*rowlength:(i+1)*rowlength] = img.img_bw[start:end]
        img_tmp = framebuf.FrameBuffer(img.img_bw, img.width, img.height, framebuf.MONO_HLSB)
        epd.blit(img_tmp, 0, 0, ram=colorchannel1)
        img_tmp = framebuf.FrameBuffer(selected_img, 280, rand_numrows, framebuf.MONO_HLSB)
        epd.blit(img_tmp, randXplacement, randYplacement, ram=colorchannel1)
        #red
        for i in range(rand_numrows):
            start = (rand_rowaddress + i) * rowlength
            end = start + rowlength
            selected_img[i*rowlength:(i+1)*rowlength] = img.img_red[start:end]
        img_tmp = framebuf.FrameBuffer(img.img_red, img.width, 480, framebuf.MONO_HLSB)
        epd.blit(img_tmp, 0, 0, ram=colorchannel2)
        img_tmp = framebuf.FrameBuffer(selected_img, 280, rand_numrows, framebuf.MONO_HLSB)
        epd.blit(img_tmp, randXplacement, randYplacement, ram=colorchannel2)
    else:
        #invert only if also reversed
        if displayrotation == 180 and glitchrand <= 14:
            #invert+reverse
            print("Glitch: inverted")
            bArray = img.img_bw
            for i, v in enumerate(bArray):
                bArray[i] = 0xFF & ~v
            img_tmp = framebuf.FrameBuffer(bArray, 280, 480, framebuf.MONO_HLSB)
            epd.blit(img_tmp, 0, 0, ram=epd.RAM_BW)
            bArray = img.img_red
            for i, v in enumerate(bArray):
                bArray[i] = 0xFF & ~v
            img_tmp = framebuf.FrameBuffer(bArray, 280, 480, framebuf.MONO_HLSB)
            epd.blit(img_tmp, 0, 0, ram=epd.RAM_RED)
        else:
            print("Glitch: none")
            #show image with 4 level grayscale
            img_tmp = framebuf.FrameBuffer(img.img_bw, 280, 480, framebuf.MONO_HLSB)
            epd.blit(img_tmp, 0, 0, ram=colorchannel1)
            img_tmp = framebuf.FrameBuffer(img.img_red, 280, 480, framebuf.MONO_HLSB)
            epd.blit(img_tmp, 0, 0, ram=colorchannel2)


    print("card: " + str(imageNum))
    pwm.duty_u16(20000)
    if displayrotation == 180:
        sounds.play(sounds.tada_rev,4)
    else:
        sounds.play(sounds.tada,4)
    if glitchrand < 9 or (displayrotation == 180 and glitchrand <= 14):
        sounds.play(sounds.glitch,2)
    # Show images and put display controller to sleep.
    epd.show()
    epd.sleep()
    

    machine.reset()
