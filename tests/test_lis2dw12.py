from machine import Pin, I2C
from lis2dw12 import Lis2dw12
import time

DEV = "i2c3"
ADDR = 0x19

accel = Lis2dw12(DEV, ADDR)
if accel.available():
    accel.start()
    try:
        while True:
            if accel.ready():
                x, y, z = accel.xyz()
                t = accel.temp()
                print(f'({x:8.3f}, {y:8.3f}, {z:8.3f}) g | {t:.1f} °C')
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    accel.stop()
    print("Measure stopped.")
else:
    print(f"No accel found at {DEV}, {hex(ADDR)}.")
