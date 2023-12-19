# 3.1 - Prøv eksemplet med watchdog timer og prøv at ændre watchdog time_0 til at 
# vente 2100 ms for at se den i aktion

from machine import WDT, Timer, Pin
led1 = Pin(26, Pin.OUT)

def reset_watchdog(obj):
    print("Feed the dog")
    led1.value(not led1.value())
    wdt.feed()
    
wdt = WDT(timeout=2200)
timer_0 = Timer(0)
timer_0.init(period=2100, mode=Timer.PERIODIC, callback=reset_watchdog)




