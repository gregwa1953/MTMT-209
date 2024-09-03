# ----------------------------------
# CYD_si7021
# Written by G.D. Walters
# 08/20/2024
# ----------------------------------
# While similar to the CYD_WiFi_DHT.py program, this only
# demonstrates how to use the si7021 Temp/Humidity I2C sensor.
# ----------------------------------
from machine import Pin, SoftI2C
from SI7021 import SI7021
import time
from cydr import CYD
from xglcd_font import XglcdFont
import secrets

displaywidth=320
displayheight=240
# =============================================================
# initialize CYD
# =============================================================
cyd = CYD(rgb_pmw=False, speaker_gain=512,
          display_width=displaywidth, display_height=displayheight,
          wifi_ssid = None, wifi_password = None)


cyd.display.clear()

text="Greg's CYD/Si7021 Demo"
cyd.display.draw_text8x8(cyd.display.width // 2 - 80, 0, text, cyd.WHITE)

# =============================================================
# initialize si7021 Temp & Humidity sensor
# =============================================================
i2c = SoftI2C(scl=Pin(27), sda=Pin(22), freq=100000)
si7021 = SI7021(i2c)

humidity = si7021.humidity()
temperature = si7021.temperature()

# =============================================================
# Get ready to loop, reading and displaying the temperature
# =============================================================

loop=True

print("Loading UbuntuMono12x24 font")
# ubuntumono=XglcdFont('fonts/UbuntuMono12x24.c',12,24)
# espresso_dolce = XglcdFont('fonts/EspressoDolce18x24.c', 18, 24)
unispace = XglcdFont('fonts/Unispace12x24.c', 12, 24)

print(f"{cyd.display.width=} - {cyd.display.width//2=}")
while loop:
    temp = si7021.temperature()
    tempf = temp*9/5+32
    hum = si7021.humidity()
    dp = si7021.dew_point()
    # print('T: {0:.2f}C  {1:.2f}F  H: {2:.2f}  D: {3:.2f}'.format(temp,tempf,hum,dp))
    #print('T: {0:.2f}F  H:{1:.2f}'.format(tempf,hum))
    print(f"{temp:.2f}c - {tempf:.2f}f - Humidity: {hum:.2f}% - Dew Point: {dp}")
    strngF = f"Indoor Temp: {tempf:.2f}"
    strngH = f"Indoor Humidity: {hum:.2f}"
    
    
    cyd.display.draw_text(x=cyd.display.width // 2 - 140,y=90,text=strngF,font=unispace,color=cyd.GREEN)
    cyd.display.draw_text(x=cyd.display.width // 2 - 140,y=120,text=strngH,font=unispace,color=cyd.GREEN)
    time.sleep(5)
