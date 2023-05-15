import machine

analog0 = machine.ADC(0)
analog1 = machine.ADC(1)
analog2 = machine.ADC(2)
analog3 = machine.ADC(3)
analog4 = machine.ADC(4)



#this module uses ADC to generate random from electromagnetic noise. the returning value is meant to be plugged into random.seed().
#The exact formula I am using is not perfect. But, it arrived at this through testing, and is fairly fast and more random compared to simply adding the values together.

def small():
    return int((analog0.read_u16() * analog1.read_u16() / analog2.read_u16() - analog3.read_u16() + analog4.read_u16()) - (analog0.read_u16() * analog1.read_u16() / analog2.read_u16() - analog3.read_u16() + analog4.read_u16()))

def get(numsToGenerate=1):
    #use ADC pins to collect environmental chaos and return a random number
    final_number = 0
    for i in range(0,numsToGenerate):
        seed = int((analog0.read_u16() * analog1.read_u16() / analog2.read_u16() - analog3.read_u16() + analog4.read_u16()) - (analog0.read_u16() * analog1.read_u16() / analog2.read_u16() - analog3.read_u16() + analog4.read_u16()))
        subseed = int((analog0.read_u16() * analog1.read_u16() / analog2.read_u16() - analog3.read_u16() + analog4.read_u16()) - (analog0.read_u16() * analog1.read_u16() / analog2.read_u16() - analog3.read_u16() + analog4.read_u16()))
    
        seed2 = int((analog0.read_u16() * analog1.read_u16() / analog2.read_u16() - analog3.read_u16() + analog4.read_u16()) - (analog0.read_u16() * analog1.read_u16() / analog2.read_u16() - analog3.read_u16() + analog4.read_u16()))
        stringseed = str(seed) + str(abs(seed2))
        seed = int(stringseed)

        seed2 = int((analog0.read_u16() * analog1.read_u16() / analog2.read_u16() - analog3.read_u16() + analog4.read_u16()) - (analog0.read_u16() * analog1.read_u16() / analog2.read_u16() - analog3.read_u16() + analog4.read_u16()))
        stringseed = str(seed) + str(abs(seed2))
        subseed = int(stringseed)
        seed = seed - subseed
        final_number += seed
        
    return final_number
        
if __name__ == "__main__":
    print(get(5))