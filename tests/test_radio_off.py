import asyncio
from radio import Radio

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
    lightsleep(60_000)
    modem.pinset["busy"].init(Pin.IN)

    async def test_send_after_sleep():
        await modem.send(b"Hello, World!")
        print("message sent.")

    asyncio.run(test_send_after_sleep())

print("test end")
