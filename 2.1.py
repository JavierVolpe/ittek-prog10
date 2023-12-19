# 2.1 - Vælg en sensor og anvend den til at vække ESP32 fra deepsleep og print en
# besked i REPL og toggle en LED 10 gange. (husk at filen skal ligge på ESP32 som
# main.py) - brug wake_on_ext0:
# https://docs.micropython.org/en/latest/library/esp32.html#esp32.wake_on_ext0
# Wake up om PB1


from machine import Pin, deepsleep

from time import sleep
import esp32
import random

# Skal lægge som main.py
print("Hi")


led1 = Pin(26, Pin.OUT)

for i in range(20):
    led1.value(not led1.value())
    sleep(0.25)


wake_pin = Pin(4, Pin.IN, Pin.PULL_UP)
sleep(2)
esp32.wake_on_ext0(pin=wake_pin, level=esp32.WAKEUP_ALL_LOW)
print("Sleeping: Wake me up with pb1")
deepsleep()
