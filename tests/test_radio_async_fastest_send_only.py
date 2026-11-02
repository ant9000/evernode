import asyncio
from radio import Radio
from machine import lightsleep

lora_cfg = {
   "freq_khz": 868300,
   "sf": 5,
   "bw": "500",  # kHz
   "coding_rate": 5,
   "preamble_len": 12,
   "output_power": -9,  # dBm
}

with Radio(lora_cfg) as modem:
    async def main_task():
        counter = 0
        while True:
            tx = f"{counter:08x}"
            print(f"Sending...{tx}")
            await modem.send(tx.encode())
            print("Sent!")
            try:
                modem.sleep()
            except:
                print("modem.sleep failed")
            modem.pinset['busy'].init(0)
            lightsleep(5_000)
            modem.pinset['busy'].init(Pin.IN)
            try:
                modem.standby()
            except:
                print("modem.standby failed")
            counter += 1

    try:
        asyncio.run(main_task())
    except KeyboardInterrupt:
        pass

print("test end")
