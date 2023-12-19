# 3.2 - Lav en hardware Timer med en callback-funktion der periodisk toggler en LED 
# hvert 100 millisekund

from machine import Pin, Timer


led_pin = Pin(26, Pin.OUT) 


# Callback
def toggle_led(timer):
    led_pin.value(not led_pin.value())
    
    

timer_0 = Timer(0)
timer_0.init(period=100, mode=Timer.PERIODIC, callback=toggle_led)

