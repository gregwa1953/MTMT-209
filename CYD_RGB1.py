# ===================================================
# CYD RGB TEST 1
# ---------------------------------------------------
# Written by Greg Walters
# August 30, 2024
# ===================================================

from cydr import CYD
import time

def init():
    cyd = CYD(rgb_pmw=False, speaker_gain=512,
          display_width=240, display_height=320,
          wifi_ssid = None, wifi_password = None)

def demo():
    cyd = CYD(rgb_pmw=False, speaker_gain=512,
          display_width=320, display_height=240,
          wifi_ssid = None, wifi_password = None)    
    print("Greg's CYD RGB Demo")
    time.sleep(2)
    print("ASSUMING rgb_pwm = False")
    print("RGB OFF")
    cyd.rgb((0,0,0))
    time.sleep(4)
    print("RGB WHITE")
    cyd.rgb((1,1,1))
    time.sleep(2)
    print("RGB RED")
    cyd.rgb((1,0,0))
    time.sleep(2)
    print("RGB GREEN")
    cyd.rgb((0,1,0))
    time.sleep(2)
    print("RGB BLUE")
    cyd.rgb((0,0,1))
    time.sleep(2)
    print("PWM Mode")
    cyd.rgb_pwm=True
    print("RGB RED")
    cyd.rgb((255,0,0))
    time.sleep(2)
    print("RGB GREEN")    
    cyd.rgb((0,255,0))
    time.sleep(2)
    print("RGB BLUE")
    
    cyd.rgb((0,0,255))
    time.sleep(2)    
    #time.sleep(2)
    colors = {"pink": (255, 0, 255), "yellow": (255,255,0), "skyblue": (0, 255, 255)
          , "orange": (230, 138 , 0), "white": (255, 255 , 255)}
    for key,color in colors.items():
        
        print(f"Displaying Color:: {key}")
        red,green,blue=color
        cyd.rgb(color)
        time.sleep(2)
        

    
    print("Turning off RGB LED - PWM Mode")
    cyd.rgb((0,0,0))
    print("Shuting Down")
    cyd.shutdown()
    

demo()