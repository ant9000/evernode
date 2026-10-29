from machine import Pin, I2C, reset
import time
from zephyr_pm import *
from rtc_lib import *
from adc_lib import *
from reg_lib import *

try:
    import bluetooth
    bt = bluetooth.BLE()
    bt.active(True)
    del bt
except:
    pass

try:
    import zephyr_pm
    zephyr_pm.pm_suspend("mspi0")
except:
    pass

pm_busy_clear("adc0")

DEV = "i2c5"
ADDR = 0x69

bus = I2C(DEV)

wake = wake_reason()
if wake == None:
	print(" boot.py without RTC")
else:
	print(" boot.py with RTC")
	rtc_restore()
chip_id()
powered_up()
