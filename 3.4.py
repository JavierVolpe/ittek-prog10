# # 3.4 - Find viden selv om ntptime på internettet hvis ESP32 skal kunne få den 
# # korrekte tid fra internettet.
# # 
# # Kilde: https://www.engineersgarage.com/micropython-esp8266-esp32-rtc-utc-local-time/

from machine import RTC
import network
import ntptime
import time

station = network.WLAN(network.STA_IF)

def connect(id, pswd):
  ssid = id
  password = pswd
  if station.isconnected() == True:
    print("Already connected")
    return
  station.active(True)
  station.connect(ssid, password)
  while station.isconnected() == False:
    pass
  print("Connection successful")
  print(station.ifconfig())
 
def disconnect():
  if station.active() == True: 
   station.active(False)
  if station.isconnected() == False:
    print("Disconnected") 
 
connect("Jwifi5", "jajajaja2021")

rtc = RTC()
ntptime.settime()
(year, month, day, weekday, hours, minutes, seconds, subseconds) = rtc.datetime()
print ("UTC Time: ")
print((year, month, day, hours, minutes, seconds))

sec = ntptime.time()
timezone_hour = 5.50
timezone_sec = timezone_hour * 3600
sec = int(sec + timezone_sec)
(year, month, day, hours, minutes, seconds, weekday, yearday) = time.localtime(sec)
print ("IST Time: ")
print((year, month, day, hours, minutes, seconds))
rtc.datetime((year, month, day, 0, hours, minutes, seconds, 0))
disconnect()