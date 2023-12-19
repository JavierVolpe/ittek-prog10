# 2.3 Lav et program der viser distance på Educaboardets LCD display, og opdaterer
# hvert sekund. Når distancen er mere end 100CM skal tekst fjernes fra display. ESP32
# skal derefter printe en besked på LCD om at den vil gå i deepslep, og derefter gå i
# deepsleep. Den skal først vågne igen når der trykkes på en af trykknapperne.

# # Dependencies
from hcsr04 import HCSR04
import uasyncio as asyncio
from gpio_lcd import GpioLcd
from machine import Pin, PWM, deepsleep
from time import sleep
import esp32

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
led_red = PWM(Pin(pin_led_red))

pb1 = Pin(4, Pin.IN)

ultrasonic = HCSR04(15, 34)


async def check_distance():
    while True:
        distance_cm = round(ultrasonic.distance_cm(), 2)
        distance_str = str(distance_cm)

        if distance_cm < 30:
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
            lcd.putstr("Negative distance")
            led_red.duty(250)
            led_red.freq(250)

        elif distance_cm > 100:
            lcd.clear()
            lcd.move_to(1, 1)
            lcd.putstr("Going to sleep now.")
            lcd.move_to(1, 2)
            lcd.putstr("Wake me up with pb1")
            wake_pin = Pin(4, Pin.IN, Pin.PULL_UP)
            sleep(4)
            esp32.wake_on_ext0(pin=wake_pin, level=esp32.WAKEUP_ALL_LOW)
            print("Sleeping. Wake me up with PB1.")
            deepsleep()

        await asyncio.sleep_ms(1000)


loop = asyncio.get_event_loop()
loop.create_task(check_distance())
loop.run_forever()
