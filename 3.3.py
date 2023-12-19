# 3.3 - Prøv at lave et program der bruger RTC til at tjekke om datetime() er på 22. 
# sekund, og kald derefter en funktion der printer ”triggered” og rtc.datetime()og 
# sørg derefter for at den kun bliver triggered én gang.

from machine import RTC, Timer

triggered = 0

def check_tid(asd):
    rtc = RTC()
    tid = rtc.datetime()
    global triggered
    if triggered == 0:
        print("Current sec: ", tid[6])
    
        if tid[6] == 22:
            print()
            print("Triggered: ", tid)
            triggered = 1

timer_0 = Timer(0)
timer_0.init(period=900, mode=Timer.PERIODIC, callback=check_tid)

while True:
    ... # Do not sleep