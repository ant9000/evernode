import asyncio, json
from machine import Pin, lightsleep
from lis2dw12 import Lis2dw12
from adc_lib import adc_read_values
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
    accel = Lis2dw12("i2c3", 0x19, Pin(("gpio0_31", 0), Pin.IN, Pin.PULL_UP))

    tap = None
    def on_tap(tap_type):
        global tap
        tap = tap_type
    accel.on_tap(on_tap)
    accel.start()

    async def main():
        global tap
        while True:
            if tap is not None and accel.ready():
                print(f"TAP: {tap}")
                data = {}
                if tap == 1:
                    for k, v in zip("xyz", accel.xyz()):
                        data[f'accel_{k}'] = f'{v:.3f}'
                elif tap == 2:
                    v = accel.temp()
                    data['temp'] = f'{v:.1f}'
                else:
                    print("Unknown tap type {tap}")
                if data:
                    for k, v in zip(["panel", "cap"], adc_read_values()):
                        data[f'v_{k}'] = f"{v/1000:.3f}"
                    tx = json.dumps(data)
                    print(f"Sending: '{tx}'")
                    try:
                        modem.standby()
                    except:
                        pass
                    await modem.send(tx.encode())
                    print("Sent.")
                tap = None
            modem.sleep()
            modem.pinset["busy"].init(0)
            lightsleep(60_000)
            modem.pinset["busy"].init(Pin.IN)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass

    print("accel stop")
    accel.stop()
