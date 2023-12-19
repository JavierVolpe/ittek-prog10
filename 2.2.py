# 2.2 - Prøv at vække ESP32 fra deepsleep med en timer, og kør en funktion der sætter 
# en random farve på RGB LED eller led ringen hver gang den vækkes.

from machine import Pin, deepsleep
from neopixel import NeoPixel
from time import sleep
import esp32
from random import choice

# Skal lægge som main.py
print("Hi")


n = 16 # number of pixels in the Neopixel ring
p = 26 # pin atached to Neopixel ring
np = NeoPixel(Pin(p, Pin.OUT), n) # create NeoPixel instance

colours = [(255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]





for i in range (12):
    random_colour = choice(colours)
#     print (random_colour)
    np[i] = random_colour
    np.write()
    i = i + 1






wake_pin = Pin(4, Pin.IN, Pin.PULL_UP)
sleep(4)
esp32.wake_on_ext0(pin = wake_pin, level = esp32.WAKEUP_ALL_LOW)
print("Sleeping for 4 sec. Wake me up before with pb1")
deepsleep(4000)

