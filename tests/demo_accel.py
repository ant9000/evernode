import asyncio, json
from struct import pack
from machine import Pin, lightsleep, mem32
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

def chip_id():
    id0 = mem32[const(0x40020004)] & 0xffffffff
    id1 = mem32[const(0x40020008)] & 0xffffffff
    return pack(">2L", id0, id1).hex()

with Radio(lora_cfg) as modem:
    accel = Lis2dw12("i2c3", 0x19, Pin(("gpio0_31", 0), Pin.IN, Pin.PULL_UP))
    node = chip_id()

    tap = None
    def on_tap(tap_type):
        global tap
        tap = tap_type
    accel.on_tap(on_tap)
    accel.start()

    async def main():
        global tap
        while True:
            data = { 'node': node }
            data.update({
                f'V{k}': f'{v/1000:.3f}' for k, v in zip(["panel", "cap"], adc_read_values())
            })
            if tap is not None:
                data['tap'] = tap
                tap = None
            if accel.ready():
                data.update({
                    f'a{k}': f'{v:.3f}' for k, v in zip("XYZ", accel.xyz())
                })
                data['T'] = f'{accel.temp():.1f}'
            tx = json.dumps(data, separators=(',', ':'))
            print(f"Sending: '{tx}'")
            try:
                modem.standby()
            except:
                pass
            await modem.send(tx.encode())
            print("Sent.")
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
