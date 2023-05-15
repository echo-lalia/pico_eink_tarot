import chaos
from machine import Pin
import time
import random



led = Pin(25, Pin.OUT)
analog0 = machine.ADC(0)
analog1 = machine.ADC(1)
analog2 = machine.ADC(2)
analog3 = machine.ADC(3)
analog4 = machine.ADC(4)

times_to_generate = 100
numsToGenerate = 1000
time_delta = 0
repeats = 0
cards = [0 for ir in range(1,79)]
reversecards = [0 for ir in range(1,79)]
glitchcards = [0 for ir in range(1,79)]
for j in range(0,times_to_generate):
    start_time = time.ticks_ms()
    #uniqueNums = set({})

    for i in range(0,numsToGenerate):
        seed = chaos.get(5)
        #uniqueNums.add(seed)
        if i % 10 == 0:
            led.toggle()
        random.seed(seed)
        onecard = random.randint(0,77)
        cards[onecard] += 1
        if random.randint(1,5) == 5:
            reversecards[onecard] += 1
        if random.randint(1,100) == 1:
            glitchcards[onecard] += 1
            
        
    time_delta += time.ticks_diff(time.ticks_ms(), start_time)
    #print(str(len(uniqueNums)) + " unique numbers")
    #repeats += numsToGenerate - len(uniqueNums)
    print("gen " + str(j))
print("cards: ")
print(cards)
print("reversed: ")
print(reversecards)
print("with one glitch: ")
print(glitchcards)
print("generated " + str(numsToGenerate * times_to_generate) + " seeds in " + str(time_delta) + "ms.")
#print("which contained " + str(repeats) + " repeat numbers.")

# for i in range(0,numsToGenerate):
#     s0 = analog0.read_u16()
#     s1 = analog1.read_u16()
#     s2 = analog2.read_u16()
#     s3 = analog3.read_u16()
#     s4 = analog4.read_u16()
#     delta0 = s0 - analog0.read_u16()
#     delta1 = abs(s1 - analog1.read_u16())
#     delta2 = abs(s2 - analog2.read_u16())
#     delta3 = abs(s3 - analog3.read_u16())
#     delta4 = abs(s4 - analog4.read_u16())
#     stringNums = str(delta0 * int(delta1 * 0.25)) + str(int(delta1 * (delta2 * delta3) / (delta3 + 0.5 + delta4))) + str(delta4 * abs(delta0))
#     uniqueNums.add(int(stringNums))
#     if (i % 10 == 0):
#         led.toggle()
#         print(stringNums)
    

# for i in range(0,numsToGenerate):
#     seed = int((analog0.read_u16() + analog1.read_u16() + analog2.read_u16() + analog3.read_u16() + analog4.read_u16()) - (analog0.read_u16() + analog1.read_u16() + analog2.read_u16() + analog3.read_u16() + analog4.read_u16()))
#     for j in range(0,50):
#         seed += int((analog0.read_u16() + analog1.read_u16() + analog2.read_u16() + analog3.read_u16() + analog4.read_u16()) - (analog0.read_u16() + analog1.read_u16() + analog2.read_u16() + analog3.read_u16() + analog4.read_u16()))
#     uniqueNums.add(seed)
#     if (i % 10 == 0):
#         led.toggle()
#         print(seed)


led.value(0)