import time
from machine import Pin, I2C, reset, lightsleep
from adc_lib import *
from rtc_lib import *
import sys

#maxcycles = 1000000
maxcycles = 0
daysleep = 0
light_sleep = True
#light_sleep = False
#print(f"daysleep = {daysleep}")
#print(f"light_sleep = {light_sleep}")

#print(" main.py")
#Vp, Vc = adc_read_values()
#print ("adc6 (VPanel) = {:.0f}; adc7 (VCap) = {:.0f}".format(Vp, Vc))
#current_time = rtc_getDate()
#print("Now retrieved from RTC: {year:04d}-{month:02d}-{date:02d} {hour:02d}:{minute:02d}:{second:02d} (Weekday: {weekday})".format(**current_time))
#wake = wake_reason()
#print ("wake = ", wake)

#if wake == b'\x00':
#    print("  RTC: Normal Boot")
#if wake == b'\x01':
#    print("  RTC: EXTI Boot")
#if wake == b'\x02':
#    print("  RTC: WDI Boot")
#if wake == b'\x04':
#    print("  RTC: ALARM TIME!")
#if wake == b'\x10':
#    print("  RTC: VSolar Boot")
#    pol = wake_pol_reason()
#    print(f'[{0x0f:02x}] "    RTC: VSolar Polarity", {pol.hex()}')
   
rtc_restore()
xtCalibration = bus.readfrom_mem(ADDR, 0x14, 1)
print(f'  xtCalibration (reg 0x14): 0x{xtCalibration.hex()}')



if daysleep == 1:
# nel caso abbiamo fatto partire un allarme programmato continua ad eseguire le azioni qui sotto
    print ("wake = ", wake, wake.hex())
    mywake = int(wake.hex())
    if mywake & 0x04:
        print("wake = 4 !! go to sleep")
        Vp, Vc = adc_read_values()
        print ("adc6 (VPanel) = {:.0f}; adc7 (VCap) = {:.0f}".format(Vp, Vc))
        # Program alarm to trigger 15 seconds from now
        rtc_setAlarmTime(20)
#    wake = 0
        print("rtc_sleep: press WDI or EXTI or move solar panel: night sleep")
        GPIO45  = Pin(("gpio32_63", 13), Pin.OUT)
        GPIO45.off()     # disponibile per segnalare su logic analyzer
        rtc_sleep(False, True, True, True)
        for i in range(10):
            print(".")
            time.sleep(1)
    else:
        print("Not an Alarm boot!")
        print(wake_reason())
        print("wake = ", wake)

else:
    GPIO45  = Pin(("gpio32_63", 13), Pin.OUT)
    if light_sleep:

        for i in range(maxcycles):
            GPIO45.on()     # disponibile per segnalare su logic analyzer
            Vp, Vc = adc_read_values()
            print ("adc6 (VPanel) = {:.0f}; adc7 (VCap) = {:.0f}".format(Vp, Vc))
            current_time = rtc_getDate()
            print("Now retrieved from RTC: {year:04d}-{month:02d}-{date:02d} {hour:02d}:{minute:02d}:{second:02d} (Weekday: {weekday})".format(**current_time))
            GPIO45.off()     # disponibile per segnalare su logic analyzer
            sec_sleep = 299
            print(f"count = {i}, lightsleep for {sec_sleep}s")
            try:
                print(f"cycle {i} of {maxcycles}")
                time.sleep(1)
#                pm_busy_clear("i2c5")
#                pm_busy_clear("adc0")
#                pm_busy_clear("i2c3")
                lightsleep(sec_sleep*1000)
#                pm_busy_set("i2c5")
#                pm_busy_set("adc0")
#                pm_busy_set("i2c3")
            except KeyboardInterrupt:
                break

#rtc_getDate()
state = read_std_ram(0)
print("state = ", state)
time.sleep(1)

if state !=0 and state != 1 and state != 2 and state != 3:
    print("state è sbagliato, inizializzo")
    state = 0
    write_std_ram(0, state)
    
timetosleep = 30
#for i in range(1000):
for i in range(100):
    if state == 0:
        print ("RUNNING")
        state = 1
#        print("state = ", state)
        write_std_ram(0, state)
        current_time = rtc_getDate()
        print("Now retrieved from RTC: {year:04d}-{month:02d}-{date:02d} {hour:02d}:{minute:02d}:{second:02d} (Weekday: {weekday})".format(**current_time))
        Vp, Vc = adc_read_values()
        print ("adc6 (VPanel) = {:.0f}; adc7 (VCap) = {:.0f}".format(Vp, Vc))
        for j in range(timetosleep*10):
            sys.stdout.write(str(j))
            sys.stdout.write(" ")
            lightsleep(100)
        sys.stdout.write("\n")
    if state == 1:
        print ("LIGHT SLEEP")
        state = 2
#        print("state = ", state)
        write_std_ram(0, state)
        current_time = rtc_getDate()
        print("Now retrieved from RTC: {year:04d}-{month:02d}-{date:02d} {hour:02d}:{minute:02d}:{second:02d} (Weekday: {weekday})".format(**current_time))
        Vp, Vc = adc_read_values()
        print ("adc6 (VPanel) = {:.0f}; adc7 (VCap) = {:.0f}".format(Vp, Vc))
        lightsleep(timetosleep*1000)
    if state == 2:
        current_time = rtc_getDate()
        print("Now retrieved from RTC: {year:04d}-{month:02d}-{date:02d} {hour:02d}:{minute:02d}:{second:02d} (Weekday: {weekday})".format(**current_time))
        Vp, Vc = adc_read_values()
        print ("adc6 (VPanel) = {:.0f}; adc7 (VCap) = {:.0f}".format(Vp, Vc))
        rtc_setAlarmTime(timetosleep)
        print ("DAY DEEP SLEEP")
        state = 3
#        print("state = ", state)
        write_std_ram(0, state)
        rtc_sleep(False, True, True, True)    
    if state == 3:
        current_time = rtc_getDate()
        print("Now retrieved from RTC: {year:04d}-{month:02d}-{date:02d} {hour:02d}:{minute:02d}:{second:02d} (Weekday: {weekday})".format(**current_time))
        Vp, Vc = adc_read_values()
        print ("adc6 (VPanel) = {:.0f}; adc7 (VCap) = {:.0f}".format(Vp, Vc))
        rtc_setAlarmTime(timetosleep)
        print ("NIGHT DEEP SLEEP")
        state = 0
#        print("state = ", state)
        write_std_ram(0, state)
        rtc_sleep(True, True, True, True)    