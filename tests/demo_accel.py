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
                    data['accel'] = '{:.3f},{:.3f},{:.3f}'.format(*accel.xyz())
                elif tap == 2:
                    data['temp'] = '{:.1f}'.format(accel.temp())
                else:
                    print("Unknown tap type {tap}")
                if data:
                    data['Vpanel'], data['Vcap'] = [f"{v/1000:.3f}" for v in adc_read_values()]
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
