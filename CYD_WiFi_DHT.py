# ========================================================
# CYD_Wifi_DHT.py
# --------------------------------------------------------
# Written by G.D. Walters
# August 31, 2024
# --------------------------------------------------------
# Version 0.1.1
# --------------------------------------------------------
# This program demonstrates using DHT11/22, Wifi (for local
# temperature) and the CYD (ESP32-2432S028R) ESP32 and
# ili9341 display board display.
#
# You will need to obtain an API key for OpenWeatherMap at
# https://openweathermap.org/appid.  You can use the free key.
# ========================================================
# Note on imports...
# --------------------------------------------------------
# machine, network, urequests, dht, time are all part of the ESP32 Micropython firmware
# cydr, xglcd_font, ili9341 and xpt2046 are all required and should be placed in the lib folder
# secrets.py is a special modified file that holds network ssid,password,lat, lon and openweathermap API key.
# Unispace12x24.c must exist in the font folder
# ========================================================

from machine import Pin, SoftI2C
import network
import urequests
import ujson
import dht
import time
from cydr import CYD
from xglcd_font import XglcdFont
import secrets

_debug=False

# =========================================================
# Create an instance of the CYD object and clear the screen
# ---------------------------------------------------------
# Use the CYD module network init to speed things up.
# =========================================================
displaywidth=320
displayheight=240
cyd = CYD(rgb_pmw=False, speaker_gain=512,
          display_width=displaywidth, display_height=displayheight,
          wifi_ssid = secrets.SSID, wifi_password = secrets.PASSWORD)

# =========================================================
# Load the font(s)
# =========================================================

unispace = XglcdFont('fonts/Unispace12x24.c', 12, 24)



# =========================================================
# Create a splash screen and show it for 5 seconds.
# =========================================================
cyd.display.clear()
cyd.display.draw_text(x=displaywidth//2-50,y=80,text="Greg's CYD",font=unispace,color=cyd.GREEN)
cyd.display.draw_text(x=displaywidth//2-70,y=160,text="Weather Display",font=unispace,color=cyd.GREEN)
time.sleep(5)
cyd.display.clear()

# define the openweathermap api url


austinLat = '30.26715'
austinLon = '-97.74306'

url1=f"http://api.openweathermap.org/data/2.5/weather?lat={secrets.LAT}&lon={secrets.LON}&appid={secrets.KEY}&units=imperial"
#url1=f"http://api.openweathermap.org/data/2.5/weather?lat={austinLat}&lon={austinLon}&appid={secrets.KEY}&units=imperial"


end_time = 0   # OpenWeatherMap API call
end_time2 = 0  # DHT22 Call
print("Connecting to network...")

#while not cyd.wifi.isconnected():

    #cyd.wifi.connect(secrets.SSID,secrets.PASSWORD)
    #print(".",end="")
    #time.sleep(0.1)
    
print("")
print('network config:', cyd.wifi.ipconfig('addr4'))

# =============================================================
# initialize si7021 Temp & Humidity sensor
# =============================================================
d=dht.DHT22(Pin(27))
d.measure()
#d.temperature()
#d.humidity()



# ===================================
# Create Screen
# ===================================
# left side
cyd.display.draw_rectangle(10,10,150,210,cyd.GREEN)
cyd.display.draw_hline(11,40,149,cyd.GREEN)
cyd.display.draw_text(x=40,y=14,text="Outside",font=unispace,color=cyd.GREEN)
# right side
cyd.display.draw_rectangle(160,10,150,210,cyd.GREEN)
cyd.display.draw_hline(161,40,149,cyd.GREEN)
cyd.display.draw_text(x=190,y=14,text="Inside",font=unispace,color=cyd.GREEN)

cond = "                  "
# ===================================
# Start the loop
# ===================================
while cyd.wifi.isconnected():
    #x, y = cyd.touches()
    # Clear the data area

    
    
    if time.ticks_ms() > end_time:
        cyd.display.draw_text(x=20,y=160,text=cond,font=unispace,color=cyd.BLACK)        
        print('Attempting to contact OpenWeatherMap...')
        resp = urequests.get(url1)
        info=resp.json()
        #print(info)
        location=info['name']
        outsideTemp=info['main']['temp']
        outsideFeelsLike=info['main']['feels_like']
        outsideHumidity=info['main']['humidity']
        weather=info['weather']
        outsideCurrent=info['weather'][0]['description']
        if _debug:
            print(f"Location: {location}")
            print(f"outside Temp: {outsideTemp}")
            print(f"outside Feels like: {outsideFeelsLike}")
            print(f"outside Humidity: {outsideHumidity}")
            print(f"Conditions: {outsideCurrent}")        

        # ======================================================
        # Now display the outside temp in the left "frame"
        # ======================================================
        cyd.display.draw_text(x=20,y=70,text=location,font=unispace,color=cyd.GREEN)
        otemp=f"T: {outsideTemp:.2f}"
        ohum=f"H: {outsideHumidity:.2f}"
        ofl=f"Feels: {outsideFeelsLike:.2f}"
        cond=f"{outsideCurrent}"
        cyd.display.draw_text(x=20,y=100,text=otemp,font=unispace,color=cyd.GREEN)
        cyd.display.draw_text(x=20,y=130,text=ohum,font=unispace,color=cyd.GREEN)
        cyd.display.draw_text(x=20,y=160,text=cond,font=unispace,color=cyd.GREEN)
        
        end_time=time.ticks_ms() + 180000  # 60000ms = 1 minute so 180000 would = 3 minutes
        print(f"{end_time=}")
        
    # ================================================
    # Now read the DHT sensor
    # Only read once every 5 seconds
    # ================================================
    #d=dht.DHT22(Pin(27))
    if time.ticks_ms() > end_time2:
        if _debug:
            print('Reading DHT Sensor')
        d.measure() 
        temp=d.temperature()
        tempf = temp*9/5+32
        hum = d.humidity()    
        end_time2 = time.ticks_ms() + 5000
    # ================================================   
    # Now display the inside (DHT) info in the right "frame"
    # ================================================
    strngF = f"T: {tempf:.2f}"
    strngH = f"H: {hum:.2f}"
    cyd.display.draw_text(x=170,y=100,text=strngF,font=unispace,color=cyd.GREEN)
    cyd.display.draw_text(x=170,y=130,text=strngH,font=unispace,color=cyd.GREEN)

    # ================================================
    # Set up for double tap
    # ================================================
    x, y = cyd.touches()
    if x == 0 and y == 0:
        continue
    
    # Check for double tap to exit
    # NOTE: For double_tap to recognize, the x,y must be greater than 10 pixels from last
    if cyd.double_tap(x,y):
        cyd.shutdown()
        cyd.wifi.disconnect()
        time.sleep(1)
        break

   
# When the user double taps the display,
# the system should shutdown the Wifi connection and
# exit the while loop.
