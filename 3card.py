"""
this function was scrapped after I decided it was too janky compared to the normal card draw. It might contain something useful, though.
"""

from Alt_ePaper import EinkPIO
import framebuf
from machine import Pin
import gc
import random
import sys
import card_dict as cards
import time

led = Pin(25, Pin.OUT)
led.value(1)


#get random from adc
analog0 = machine.ADC(0)
analog1 = machine.ADC(1)
analog2 = machine.ADC(2)
analog3 = machine.ADC(3)
analog4 = machine.ADC(4)
reading = 0
for iN in range(1,6000):
    reading += analog0.read_u16() + analog1.read_u16() + analog2.read_u16() + analog3.read_u16() + analog4.read_u16() - 25000
reading += time.ticks_ms()
random.seed(reading)

#pick our images
i1 = random.randint(1,78)
i2 = random.randint(1,78)
i3 = random.randint(1,78)
while i2 == i1:
    i2 = random.randint(1,78)
while i3 == i1 or i3 == i2:
    i3 = random.randint(1,78)
del random

# def scale_down(bytearr, N, bytes_per_line, start_offset=0):
#     new_bytearr = bytearray()
#     for i in range(start_offset, len(bytearr), bytes_per_line):
#         if (i // bytes_per_line) % N == 0:
#             continue
#         end = min(i + bytes_per_line, len(bytearr))
#         for j in range(i + start_offset, end, N):
#             new_bytearr.append(bytearr[j])
#     return new_bytearr
def set_bit(value, bit_index):
    return value | (1 << bit_index)
def get_normalized_bit(value, bit_index):
    return (value >> bit_index) & 1

def scale_down(bytearr, N, bytes_per_line, alt_mode=False):
    new_bytearr = bytearray()
    for i in range(0, len(bytearr), bytes_per_line * 2):
        end = min(i + bytes_per_line, len(bytearr))
        for j in range(i, end,N):
            if alt_mode:
                avgbyte = 0
                for bi in range(0,8):
                    if bi < 4:
                        if get_normalized_bit(bytearr[j + 1],bit_index=((bi) * 2)):
                            avgbyte = set_bit(avgbyte, bit_index=bi)
                    else:
                        if get_normalized_bit(bytearr[j],bit_index=((bi - 4) * 2)):
                            avgbyte = set_bit(avgbyte, bit_index=bi)
                    
                #print(bin(avgbyte))
                new_bytearr.append(avgbyte)
            else:
                avgbyte = ((bytearr[j - 1] << 4) & 0b11111111) | ((bytearr[j] >> 4) & 0b11111111)
                new_bytearr.append(avgbyte)
                
    return new_bytearr

def unloadModule(mod):
    # removes module from the system
    mod_name = mod.__name__
    if mod_name in sys.modules:
        del sys.modules[mod_name]

#fetch names
name1 = cards.dict[i1]["name"]
name2 = cards.dict[i2]["name"]
name3 = cards.dict[i3]["name"]

#load in epd and start drawing
led.value(0)
epd = EinkPIO(rotation=90)
#loading...
epd.fill(c=epd.black)
epd.text("Gathering chaos...", 50,130,epd.white)
epd.text("reading...",100,160,epd.white)
epd.show()
led.value(1)
epd.fill(c=epd.black)
#Banner
epd.fill_rect(60, 6, 330, 18, epd.darkgray)

epd.fill_rect(35, 6, 9, 21, epd.lightgray)
epd.fill_rect(44, 4, 120, 22, epd.lightgray)
epd.fill_rect(173, 4, 134, 22, epd.lightgray)
epd.fill_rect(316, 4, 120, 22, epd.lightgray)
epd.fill_rect(436, 6, 9, 21, epd.lightgray)

epd.text("- Past", 73,13,epd.darkgray)
epd.text("Present", 212,13,epd.darkgray)
epd.text("Future -", 350,13,epd.darkgray)

#namecards
epd.fill_rect(16, 251, 148, 25, epd.lightgray)
epd.rect(16, 251, 148, 25)
epd.fill_rect(166, 251, 148, 25, epd.lightgray)
epd.rect(166, 251, 148, 25)
epd.fill_rect(316, 251, 148, 25, epd.lightgray)
epd.rect(316, 251, 148, 25)

#name1
text_position = (90 - int(len(name1) / 2) * 8)
epd.text(name1, text_position + 1, 261, epd.white)
epd.text(name1, text_position - 1, 259, epd.darkgray)
epd.text(name1, text_position, 260)
#name2
text_position = (240 - int(len(name2) / 2) * 8)
epd.text(name2, text_position + 1, 261, epd.white)
epd.text(name2, text_position - 1, 259, epd.darkgray)
epd.text(name2, text_position, 260)
#name3
text_position = (390 - int(len(name3) / 2) * 8)
epd.text(name3, text_position + 1, 261, epd.white)
epd.text(name3, text_position - 1, 259, epd.darkgray)
epd.text(name3, text_position, 260)

# load image 1
img = __import__("i" + str(i1))
led.value(0)
img_tmp = framebuf.FrameBuffer(scale_down(img.img_bw,2,35, alt_mode=True), 140, 220, framebuf.MONO_HLSB)
epd.blit(img_tmp, 20, 31, ram=epd.RAM_BW)
led.value(1)
img_tmp = framebuf.FrameBuffer(scale_down(img.img_red,2,35, alt_mode=True), 140, 220, framebuf.MONO_HLSB)
epd.blit(img_tmp, 20, 31, ram=epd.RAM_RED)

unloadModule(img)
del img
gc.collect()

# # load image 2
img = __import__("i" + str(i2))
led.value(0)
img_tmp2 = framebuf.FrameBuffer(scale_down(img.img_bw,2,35, alt_mode=True), 140, 220, framebuf.MONO_HLSB)
epd.blit(img_tmp2, 170, 31, ram=epd.RAM_BW)
led.value(1)
img_tmp2 = framebuf.FrameBuffer(scale_down(img.img_red,2,35, alt_mode=True), 140, 220, framebuf.MONO_HLSB)
epd.blit(img_tmp2, 170, 31, ram=epd.RAM_RED)

unloadModule(img)
del img
gc.collect()

# # load image 3
img = __import__("i" + str(i3))
led.value(0)
img_tmp = framebuf.FrameBuffer(scale_down(img.img_bw,2,35, alt_mode=True), 140, 220, framebuf.MONO_HLSB)
epd.blit(img_tmp, 320, 31, ram=epd.RAM_BW)
led.value(1)
img_tmp = framebuf.FrameBuffer(scale_down(img.img_red,2,35, alt_mode=True), 140, 220, framebuf.MONO_HLSB)
epd.blit(img_tmp, 320, 31, ram=epd.RAM_RED)




# Show images and put display controller to sleep.
epd.show()
epd.sleep()
led.value(0)