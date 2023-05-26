from machine import Pin, PWM
import time
import gc
buzzer = PWM(Pin(1))

noisy = const((1.0,0.9,1.2,1.1,1.1,0.9,1.31,0.97,0.99,1.08,1.17,1.22,0.95,0.88,1.02,1.1,1.2,0.9,1.1,1.18,1.1,2.5,0.8,1.0,0.5,0.9,1.7,1.1))

tones = {
"LOW": 50,
"B0": 31,
"C1": 33,
"CS1": 35,
"D1": 37,
"DS1": 39,
"E1": 41,
"F1": 44,
"FS1": 46,
"G1": 49,
"GS1": 52,
"A1": 55,
"AS1": 58,
"B1": 62,
"C2": 65,
"CS2": 69,
"D2": 73,
"DS2": 78,
"E2": 82,
"F2": 87,
"FS2": 93,
"G2": 98,
"GS2": 104,
"A2": 110,
"AS2": 117,
"B2": 123,
"C3": 131,
"CS3": 139,
"D3": 147,
"DS3": 156,
"E3": 165,
"F3": 175,
"FS3": 185,
"G3": 196,
"GS3": 208,
"A3": 220,
"AS3": 233,
"B3": 247,
"C4": 262,
"CS4": 277,
"D4": 294,
"DS4": 311,
"E4": 330,
"F4": 349,
"FS4": 370,
"G4": 392,
"GS4": 415,
"A4": 440,
"AS4": 466,
"B4": 494,
"C5": 523,
"CS5": 554,
"D5": 587,
"DS5": 622,
"E5": 659,
"F5": 698,
"FS5": 740,
"G5": 784,
"GS5": 831,
"A5": 880,
"AS5": 932,
"B5": 988,
"C6": 1047,
"CS6": 1109,
"D6": 1175,
"DS6": 1245,
"E6": 1319,
"F6": 1397,
"FS6": 1480,
"G6": 1568,
"GS6": 1661,
"A6": 1760,
"AS6": 1865,
"B6": 1976,
"C7": 2093,
"CS7": 2217,
"D7": 2349,
"DS7": 2489,
"E7": 2637,
"F7": 2794,
"FS7": 2960,
"G7": 3136,
"GS7": 3322,
"A7": 3520,
"AS7": 3729,
"B7": 3951,
"C8": 4186,
"CS8": 4435,
"D8": 4699,
"DS8": 4978,
"HIGH": 8000
}

startup = const(('C2','C4'))
tada = const(('C4','','C7'))
tada_rev = const(('C7','','C4'))
glitch = const(('C2','NC2'))
click = const(('ND8','E5'))
keywords = const(('NB1','NB2'))
thump = ('LOW', 'NB0')
powerwarning = const(('HIGH','B0','HIGH','E4','E4'))


def play_tone(frequency):
    buzzer.duty_u16(10000)
    buzzer.freq(tones[frequency])
    
def noise(tone, speed=1):
    buzzer.duty_u16(10000)
    freq = tones[tone]
    for j in range (0,3):
        for i in range(0,len(noisy)):
            buzzer.freq(int(noisy[i] * freq))
            time.sleep_us(int(100 / speed))
    stop()

# def play(mysong, speed=1, mode='jingle'):
#     try:
#         if mode == 'slide':
#             _thread.start_new_thread(slide,(mysong,speed))
#         else:
#             _thread.start_new_thread(jingle,(mysong,speed))
#     except:
#         print("error playing sound")
#     gc.collect()

def play(mysong, speed=1, mode='jingle',slidespeed=1):
    if mode == 'slide':
        slide(mysong,speed,slidespeed)
    else:
        jingle(mysong,speed)
    gc.collect()

def stop():
    buzzer.duty_u16(0)

def slide(mysong,speed=1,slide=1):
    if mysong[0] != '':
        buzzer.freq(tones[mysong[0]])
    for i in range(len(mysong)):
        if (mysong[i] == ""):
            stop()
            time.sleep(0.15 / speed)
        elif (mysong[i] == "-"):
            stop()
            time.sleep(0.02 / speed)
            try:
                buzzer.freq(tones[mysong[i+1]])
            except:
                pass
        else:
            buzzer.duty_u16(10000)
            targetfreq = tones[mysong[i]]
            currentfreq = buzzer.freq()
            while currentfreq != targetfreq:
                if targetfreq > currentfreq:
                    if targetfreq - currentfreq > 15:
                        currentfreq += 15
                    elif targetfreq - currentfreq > 5:
                        currentfreq += 5
                    else:
                        currentfreq += 1
                else:
                    if currentfreq - targetfreq > 15:
                        currentfreq -= 15
                    elif currentfreq - targetfreq > 5:
                        currentfreq -= 5
                    else:
                        currentfreq -= 1
                buzzer.freq(currentfreq)
                time.sleep(0.01 / slide)
            time.sleep(0.2 / speed)
    gc.collect()
    stop()
    
def jingle(mysong,speed=1):
    for i in range(len(mysong)):
        if (mysong[i] == ""):
            stop()
            time.sleep(0.15 / speed)
        elif (mysong[i] == "-"):
            stop()
            time.sleep(0.02 / speed)
        elif ('N' in mysong[i]):
            noise(mysong[i].replace('N',''),speed)
        else:
            play_tone(mysong[i])
            time.sleep(0.15 / speed)
    stop()
    gc.collect()
    
if __name__ == "__main__":
    #slide(greensleeves,1,2)
    play(thump,10)
    stop()