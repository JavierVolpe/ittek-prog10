# 4.1 - lav menu-item med calback funktion til at sætte ESP32 i deepsleep og sørg for 
# at den kan vækkes efterfølgende ved et knaptryk (kræver at filen køres som main.py)

from gpio_lcd import GpioLcd
from rotary_encoder import RotaryEncoder
from machine import Pin, deepsleep
from lcd_menu import LCDMenu
from lmt84 import LMT84
from time import sleep
import esp32
from hcsr04 import HCSR04


lmt84 = LMT84()

rot_pb = Pin(14, Pin.IN, Pin.PULL_UP)
rot = RotaryEncoder()

lcd = GpioLcd(rs_pin=Pin(27), enable_pin=Pin(25),
                  d4_pin=Pin(33), d5_pin=Pin(32),
                  d6_pin=Pin(21), d7_pin=Pin(22),
                  num_lines=4, num_columns=20)

menu = LCDMenu(lcd, rot, rot_pb)
led1 = Pin(26, Pin.OUT)

# https://maxpromer.github.io/LCD-Character-Creator/
lcd_custom_char_degrees = bytearray([0x0E, 0x0A,
                                     0x0E, 0x00,
                                     0x00, 0x00,
                                     0x00, 0x00])


def lcd_temperature_celsius():
    """callback function to display temperature celsius on lcd"""
    lcd.move_to(1, menu.selected)  # moves to selected line
    lcd.putstr("                  ")  # delete selected line text by adding whitespaces
    lcd.move_to(1, menu.selected)
    lcd.putstr(f"Temp is {lmt84.celsius_temperature():.1f} ")
    lcd.custom_char(2, lcd_custom_char_degrees)
    lcd.putchar(chr(2))
    lcd.putstr("C")


def lcd_temperature_fahrenheit():
    """callback function to display temperature fahrenheit on lcd"""
    lcd.move_to(1, menu.selected)  # moves to selected line
    lcd.putstr("                  ")  # delete selected line text by adding whitespaces
    lcd.move_to(1, menu.selected)
    lcd.putstr(f"Temp is {lmt84.fahrenheit_temperature():.1f} ")
    lcd.custom_char(2, lcd_custom_char_degrees)
    lcd.putchar(chr(2))
    lcd.putstr("F")


def lcd_temperature_kelvin():
    """callback function to display temperature kelvin on lcd"""
    lcd.move_to(1, menu.selected)  # moves to selected line
    lcd.putstr("                  ")  # delete selected line text by adding whitespaces
    lcd.move_to(1, menu.selected)
    lcd.putstr(f"Temp is {lmt84.kelvin_temperature():.1f}K")


def lcd_toggle_led1():
    """callback to Toggle led1"""
    lcd.move_to(1, menu.selected)  # moves to selected line
    lcd.putstr("                  ")  # delete selected line text by adding whitespaces
    lcd.move_to(1, menu.selected)
    lcd.putstr("LED1 is toggled!")
    led1.value(not led1.value())


def go_to_sleep():
    print("Sleeping in 4 sec. Wake me up before with pb1")
    wake_pin = Pin(4, Pin.IN, Pin.PULL_UP)
    
    lcd.move_to(1, 1)
    lcd.clear()
    lcd.putstr("Sleeping in 4 sec")
    lcd.move_to(1, 2)
    lcd.putstr("Wake me up with pb1")
    sleep(4)
    esp32.wake_on_ext0(pin = wake_pin, level = esp32.WAKEUP_ALL_LOW)
    deepsleep()

def lcd_distance():
    ultrasonic = HCSR04(15, 34)
    distance = ultrasonic.distance_cm()
    """callback function to display distance on lcd"""
    lcd.move_to(1, menu.selected)  # moves to selected line
    lcd.putstr("                  ")  # delete selected line text by adding whitespaces
    lcd.move_to(1, menu.selected)
    lcd.putstr(f"Distance: {ultrasonic.distance_cm():.2f}cm")
    
    



menu.add_menu_item("Temp celsius", lcd_temperature_celsius)
menu.add_menu_item("Temp fahrenheit", lcd_temperature_fahrenheit)
menu.add_menu_item("Temp kelvin", lcd_temperature_kelvin)
menu.add_menu_item("Toggle LED1", lcd_toggle_led1)
menu.add_menu_item("Go to sleep ", go_to_sleep)
menu.add_menu_item("Measure distance", lcd_distance)

menu.display_menu()
menu.run()
