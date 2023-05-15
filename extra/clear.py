from Pico_ePaper import Eink
from machine import Pin

epd = Eink(rotation=0)
led = Pin(25, Pin.OUT)
led.value(0)
epd.fill()

# Show images and put display controller to sleep.
epd.show()
epd.sleep()

