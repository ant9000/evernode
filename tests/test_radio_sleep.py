import asyncio
from radio import Radio
from pin_cfg import *

lora_cfg = {
   "freq_khz": 868300,
   "sf": 5,
   "bw": "500",  # kHz
   "coding_rate": 5,
   "preamble_len": 12,
   "output_power": -9,  # dBm
}

with Radio(lora_cfg) as modem:
    modem.sleep()
    modem.pinset["busy"].init(0)
    print_pins()
    lightsleep(3600_000)
    modem.pinset["busy"].init(Pin.IN)

print("test end")
