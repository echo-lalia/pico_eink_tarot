def unloadModule(mod):
    # removes module from the system
    import sys
    mod_name = mod.__name__
    if mod_name in sys.modules:
        del sys.modules[mod_name]
        
def wrap_string(string, max_width):
    """Wraps a string into multiple lines based on a maximum width"""
    lines = []
    current_line = ""

    # Loop through each character in the string
    for i in range(len(string)):
        char = string[i]

        # If the current line is too long, add it to the list of lines and start a new line
        if len(current_line) >= max_width:
            lines.append(current_line)
            current_line = ""

        # Add the current character to the current line
        current_line += char

        # If the current character is a comma, add the current line to the list of lines and start a new line
        if char == ",":
            lines.append(current_line)
            current_line = ""

    # Add the last line to the list of lines
    lines.append(current_line)

    return lines

def draw():
    import sounds
    from Pico_ePaper import EinkPIO
    import framebuf
    import chaos
    from machine import Pin, PWM
    import random
    import gc
    import time
    from images import card_dict as cards

    gc.collect()

    #turn on led to low to show that the device is working
    pwm = PWM(Pin(21))
    pwm.freq(1000)
    pwm.duty_u16(2000)
    #init epd for animation
    epd = EinkPIO(rotation=0,use_partial_buffer=True)
    epd.show(lut=1)
    epd.partial_mode_on()
    epd.rect(0,0,280,480,epd.white,f=True)
    epd.text("Gathering chaos from", 60, 32, epd.black)
    epd.text("environment...", 84, 42, epd.black)

    #generate random info from adc
    reading = chaos.get()

    animY = 0
    while animY < 3:
        
        lineY = 0
        while lineY < 160:
            #bg for line
            anim_line_height = const(1)
            anim_line_position = ((3 - animY) * 160) - ((lineY + 1) * anim_line_height)

            epd.hline(0,anim_line_position, 280, epd.black)
            
            #white big line
            new_chaos = chaos.small()
            line_mid = 140 + int(new_chaos >> 2)
            reading += new_chaos
            
            new_chaos = chaos.small()
            line_start = line_mid - int(abs(new_chaos) >> 2) - 20
            line_width = (int(abs(new_chaos) >> 2) * 2) + 40
            epd.hline(line_start, anim_line_position, line_width, epd.white)
            reading += new_chaos
            
            lineY += 1
        sounds.play(sounds.thump,10)
        epd.show()
        animY += 1

    # grab a bit more random just for fun, since its fast anyways.
    reading += chaos.get(50)
    reading2 = chaos.get(5)
    str_reading = str(reading) + str(abs(reading2))
    reading = int(str_reading)

    #also add the current ticks time because it non-scientifically feels better to me to add random from multiple sources
    reading += time.ticks_cpu()
    pwm.duty_u16(100)

    #init random with our chaos we collected
    print("Seed: " + str(reading))
    random.seed(reading)
    #get our image
    imageNum = random.randint(1,78)
    #decide if we're reversed
    displayrotation = 0
    if random.randint(1,5) == 5:
        displayrotation = 180
    #get name and keywords from dictionary, store what we need and delete dictionary
    #card_name = cards.dict[imageNum]["name"]
    
    card_keywords = cards.dict[imageNum]["key"]
    if displayrotation == 180:
        card_keywords = cards.dict[imageNum]["reversed"]
    #del cards.dict
    print(cards.dict[imageNum]["name"])
    print("Keywords: " + card_keywords)
    #decide now if we will glitch
    glitchrand = random.randint(1,100)

    gc.collect()

    #display keywords as animation before loading final tarot card image
    lines = wrap_string(card_keywords, 30)
    currentline = 1
    #keywords
    for oneline in lines:
        if glitchrand < 9 or (displayrotation == 180 and glitchrand <= 14):
            oneline = "?" * len(oneline)
        line_width =  len(oneline) * 8
        line_pos = int(140 - (line_width / 2))
        line_Y = 250 + (40 * currentline)
        epd.rect(line_pos - 18, line_Y - 18, line_width + 44, 42, epd.black,f=True)
        epd.rect(line_pos - 14, line_Y - 14, line_width + 36, 34, epd.white,f=True)
        epd.text(oneline, line_pos, line_Y)
        currentline += 1
    sounds.play(sounds.thump,4)
    epd.show()
    time.sleep_ms(1300)

    #name
    cardname_width = int(len(cards.dict[imageNum]["name"]) * 8)
    cardname_pos = int(140 - (cardname_width / 2))
    cardname_box = (cardname_pos - 18)
    cardname_box_width = cardname_width + 32
    epd.rect(cardname_box - 4,106,cardname_box_width + 8,48, epd.black,f=True)
    epd.rect(cardname_box, 110, cardname_box_width, 40, epd.white,f=True)
    epd.text(cards.dict[imageNum]["name"], cardname_pos, 126)
    epd.text(cards.dict[imageNum]["name"], cardname_pos, 125)

    if displayrotation == 180:
        cardname_width = int(len("in REVERSE") * 8)
        cardname_pos = int(140 - (cardname_width / 2))
        cardname_box = (cardname_pos - 12)
        cardname_box_width = cardname_width + 24
        epd.rect(cardname_box - 4,154,cardname_box_width + 8,43, epd.black,f=True)
        epd.rect(cardname_box, 158, cardname_box_width, 35, epd.white,f=True)
        epd.text("in REVERSE", cardname_pos, 172)
    sounds.play(sounds.keywords,2)
    epd.show()
    time.sleep_ms(600)
    #load in the image driver
    if displayrotation == 180:
        #epd = Eink(180)
        #change rotation without re-initializing
        epd._rotation = 180
        epd._send(0x11, 0x00)
        epd._set_window(epd.width - 1, 0, epd.height - 1, 0)
        print("REVERSED")
        
    #use random to import specific image
    filename = "images/i" + str(imageNum) + ".py"

    #the 'partial' version of the image driver does not always set the color channels correctly for some reason
    colorchannel1 = epd.RAM_RED
    colorchannel2 = epd.RAM_BW
    
    
    pwm.duty_u16(0)
    #before importing, clean up ram to prevent errors
    unloadModule(cards)
    unloadModule(chaos)
    #unloadModule(sounds)
    #unloadModule(Pin)
    del time
    #del sounds
    del cards.dict
    del cards
    del chaos
    del cardname_width
    del cardname_pos
    del cardname_box
    del cardname_box_width
    del card_keywords
    del currentline
    del lines
    del line_pos
    del line_width
    del line_Y
    del lineY
    del reading
    del reading2
    del str_reading
    gc.collect()
    
    # Import image files
    #import i + whichimage as img
    #img = __import__(filename[:-3])
    img = __import__(filename[:-3])

    epd.partial_mode_off()
    
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
        randYplacement = random.randint(-10,400)
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
            gc.collect()
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
        
    #sys.exit()
    import machine
    machine.reset()