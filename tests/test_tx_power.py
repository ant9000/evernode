import asyncio
from radio import Radio
import time

lora_cfg = {
   "freq_khz": 868300,
   "sf": 11,
   "bw": "125",  # kHz
   "coding_rate": 5,
   "preamble_len": 12,
   "output_power": -9,  # dBm
}

with Radio({}) as modem:
    async def main_task():
       for PWR in range(-9, 23):
           lora_cfg["output_power"] = PWR
           payload = "{freq_khz}, {bw}, {coding_rate}, {sf}, {output_power:-2d}".format(**lora_cfg)
           print(f"payload = '{payload}', length = {len(payload)}")
           modem.standby()
           modem.configure(lora_cfg)
           await modem.send(payload.encode())
           time.sleep(1)

    try:
        asyncio.run(main_task())
    except KeyboardInterrupt:
        pass

print("test end")
