import asyncio
from machine import lightsleep
from lis2dw12 import Lis2dw12
from radio import Radio

modem = Radio({
   "freq_khz": 868300,
   "sf": 5,
   "bw": "500",  # kHz
   "coding_rate": 5,
   "preamble_len": 12,
   "output_power": -9,  # dBm
})

accel = Lis2dw12("i2c3", 0x19, ("gpio0_31", 4))

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
            tx = None
            if tap == 1:
                x, y, z = accel.xyz()
                tx = f'({x:.3f},{y:.3f},{z:.3f}) g'
            elif tap == 2:
                t = accel.temp()
                tx = f'{t:.1f} °C'
            else:
                print("Unknown tap type {tap}")
            if tx:
                print(f"Sending: '{tx}'")
                try:
                    modem.standby()
                except:
                    pass
                await modem.send(tx.encode())
                print("Sent.")
            tap = None
        modem.sleep()
        lightsleep(60_000)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass

print("accel stop")
accel.stop()
del radio