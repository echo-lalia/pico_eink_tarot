# Pico Eink Tarot reader

## Description

[Photos](https://imgur.com/a/eFbvrGN), and a [video](https://i.imgur.com/E46DFaU.mp4).  
This device uses random EM noise to pull a random tarot card. The image persists without power thanks to the E-ink display, and it can provide keywords for the cards, as well as an occasional 'glitch' in the image (intentionally-coded random modification to the card image, which increases the vibe of digital-mysticism, to me)  


I learned a lot of new skills for this! This was my first time using a microcontroller, first time coding in MicroPython (or Python), first time 3D printing, and I had to learn a bunch about electronics to figure out how to wire it up!  


This project uses a Waveshare RP2040-Plus (Pi Pico clone; critically, it has 4mb of flash instead of the normal 2mb, and cost about the same for me at the time), and a Waveshare 'Pico e-Paper 3.7' display. The final thing has a 3D printed case, two switches and a button, a bone conduction transducer to make [sounds](https://i.imgur.com/HLvyiXz.mp4), and runs on 3 AAA batteries.   
It uses some custom code to generate a random seed from the ADC pins, and has an animation which visualizes the noise that it is reading. It then pulls one of 78 Raider Waite tarot cards at random, with a 1/4 chance to pull it in 'reverse', and a \~1/20 chance to apply a random '[glitch](https://i.imgur.com/QsZrDlS.mp4)' to the image. It also displays keywords for the cards it pulls, and includes alternate keywords for the reversed cards. (Glitched cards just get question marks).  


The glitches are coded-in sequences that modify the framebuffer images before sending them to the display. they include a *horizontal or vertical tracking glitch*(image is 'split' down the middle, with the two halves displaying on either side of the split), a *color channel* glitch(swaps dark and light greyscale framebuffers), an 'HSMB' glitch which applies the wrong color data mode, resulting in a jittery look to the image, a '*shift* glitch where it duplicates and moves one part of the image randomly, and lastly a '*negative*' glitch, where it inverts the image, but only if the card is already reversed.   


One switch works as a power switch, and another as an 'option' switch to toggle between 'fast' mode (only pull the card, no animation) and 'full' mode (animation, plus keywords displayed before card pulled). there is also a big white button with an led that is used to actually pull the card.

## Hardware

For this project, I used a [Waveshare Pico e-Paper 3.7](https://www.waveshare.com/wiki/Pico-ePaper-3.7), which supports partial refresh, 4 greyscale tones, and connects to the Pico using SPI. 

The controller I'm using is actually not the original Pi Pico, but a [Waveshare RP2040-Plus](https://www.waveshare.com/wiki/RP2040-Plus). I chose this primarily for the 4MB of flash it has rather than the 2MB on the normal Pico, which gives me enough space to store the images (though they need to be compiled with mpy-cross). If I were to redo this now, I might choose a cheaper 4MB Pico clone, since there are more options available now. 

I'm powering this thing with 3 AAA batteries. I use two slide switches; one for power and one to toggle between modes. I used a white, momentary button, with a white LED inside, to draw a card. I also use a bone-conduction transducer to make the sound, but you could probably use something else (I just happened to have one around, and it is much louder than the beep speakers I tried). The case is held together with M2x6 screws (chosen because they fit the display's threads) and nut nested in pockets. 

## Further Information

The **main** folder contains everything needed to run it exactly as I am. This folder contains the scripts, as well as a custom build of the MicroPython firmware which holds the image and dictionary modules.

The ***custom seed*** generating code I wrote is probably not necessary, but I find it to be cool and interesting. It basically polls all the ADC pins, and does some arbitrary math on them to generate a random number to use as the seed to initialize the Random class. I wrote a test for the seed-generating code, which uses Sets to check for duplicate seeds. I can generate around 10000 seeds before running out of memory, and I can compare the final size of the sets to the number of generated seeds to determine the number of repeats.The final code rarely ever included duplicates in a set, so I had to run it a bunch of times (I think I did 100) to determine if it is generating repeated numbers. Of those 100 sets, only about 3 repeats were found.Running the seed-generating code is actually really fast, if you are doing it once and not 10000 times, so I simply run it multiple times, and then use string addition to append the seeds into one long seed, and use it to initialize the RNG. Theoretically, it should be nearly impossible for it to ever generate the same long-seed twice.

***Memory management*** was a pretty persistent problem with this project. I had to comb through the code a bunch of times, and use a custom function that would remove modules that were no longer needed from the memory (then delete the reference to them) just to get the final image to actually load. This was primarily an issue due to fragmentation; the memory is usually not very full, but the imagebuffers need to be loaded all in one chunk, so they need a large continuous space to be available in the memory to load properly.That means that generating multiple images basically just didn't work, since the memory would just become more and more fragmented with each run-through, It would always run out after a few cards. My solution is both elegant and stupid; I just do a full reset of the device at the end of the image-gen code. You can actually check what the restart reason was using a function in micropython, which is how I stopped it from playing the 'startup' tone every time it resets; it just checks, and only plays the startup tone if it was reset due to power loss.

I used [this](https://github.com/phoreglad/pico-epaper) e-paper driver, alongside [this](https://github.com/phoreglad/pico-epaper/tree/partial-updates) driver that supports partial-refreshes. I simply load in the partial driver for the animation, then unload it and load in the other, for displaying the final image. I tried combining the drivers, but it was a bit too much for me to understand right now. I did, however, modify the init function on both of them, to make swapping between them faster, and to speed up the card-display.  


The ***images*** come from highres scans I found online of original Rider Waite cards. I edited them in photoshop by cropping, removing dust, and in a few case, redrawing details that were misprinted or destroyed.
