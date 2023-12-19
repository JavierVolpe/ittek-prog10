# 1.1 Lav et eventloop med asyncio der printer distancen i CM der måles af HC-SR04
# ultralydssensoren.

# 1.2 - Vis distancen på LCD display på educaboard og sørg for at den opdateres hvert
# sekund. Asyncio skal også anvendes til denne del.

# 1.3 - prøv at styre brighthes med PWM på LED1, så brightness øges jo længere væk
# noget er fra educaboard

# 1.4 - brug async io til at lave et eventloop der tjekker for om en knap trykkes og
# hvis distancen er under 30CM når der trykkes skal der stå “Too close på display” og
# hvis distancen er mellem 30CM og 60CM skal der stå “Good distance” og hvis den er
# over 60CM skal der stå “Too far”


# # Dependencies
from hcsr04 import HCSR04
import uasyncio as asyncio
from gpio_lcd import GpioLcd
from machine import Pin, PWM
from time import sleep

# # Objekts
lcd = GpioLcd(
    rs_pin=Pin(27),
    enable_pin=Pin(25),
    d4_pin=Pin(33),
    d5_pin=Pin(32),
    d6_pin=Pin(21),
    d7_pin=Pin(22),
    num_lines=4,
    num_columns=(20),
    backlight_pin=Pin(23, Pin.OUT),
)
lcd.clear()  # starts clean


pin_led_red = 26
led_red = PWM(Pin(pin_led_red))  # # Red LED PWM

pb1 = Pin(4, Pin.IN)  # Push bottum 1

ultrasonic = HCSR04(15, 34) # Pin 15: Trig / Pin 34: Echo + 3v + GND


async def distance_display():  # Del 1: Viser info på display
    while True:
        distance_cm = round(ultrasonic.distance_cm(), 2)  # Tjekker kun ên gang
        distance_str = str(distance_cm)  # String til at vise på display

        if distance_cm < 0:  # Fejl læsning
            distance_cm = 0

        elif distance_cm < 30:
            lcd.clear()
            lcd.move_to(2, 1)
            lcd.putstr(distance_str)
            lcd.move_to(2, 3)
            lcd.putstr("Too close!")
            led_red.duty(0)
            led_red.freq(10)

        elif distance_cm > 30 and distance_cm < 60:
            lcd.clear()
            lcd.move_to(2, 1)
            lcd.putstr(distance_str)
            lcd.move_to(2, 3)

            lcd.putstr("Good distance")
            led_red.duty(100)
            led_red.freq(100)

        elif distance_cm < 0:
            lcd.move_to(2, 3)
            lcd.clear()
            lcd.move_to(2, 1)
            lcd.putstr(distance_str)
            lcd.putstr("Negative distance :/")
            led_red.duty(250)
            led_red.freq(250)

        elif distance_cm > 60:
            lcd.clear()
            lcd.move_to(2, 1)
            lcd.putstr(distance_str)
            lcd.move_to(2, 3)
            lcd.putstr("Too far!")
            led_red.duty(500)
            led_red.freq(500)
            print("Distance: ", distance_cm)

        await asyncio.sleep_ms(1000)


async def distance_knap():  # Del 2: Viser info når man trykker på knappen
    while True:

        distance_cm = round(ultrasonic.distance_cm(), 2)  # Tjekker kun ên gang

        if pb1.value() != 1:
            if distance_cm < 30:
                print("Too close på display")
            elif distance_cm > 30 and distance_cm < 60:
                print("Good distance")
            elif distance_cm >= 60:
                print("Too far")

        await asyncio.sleep_ms(200)


loop = asyncio.get_event_loop()
loop.create_task(distance_knap())
loop.create_task(distance_display())
loop.run_forever()
