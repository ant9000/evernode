# MicroPython lora simple_rxtx example - asynchronous API version
# MIT license; Copyright (c) 2023 Angus Gratton
import asyncio
from machine import Pin, SPI
import zephyr_pm, time

pinset = {
        'busy':       Pin(("gpio0_31", 16)),
        'reset':      Pin(("gpio0_31", 17)),
        'chipselect': Pin(("gpio0_31", 11)),
        'dio':        Pin(("gpio0_31", 15)),
}

pm_resume("spi1")
spi = SPI("spi1", baudrate=10_000_000, polarity=0, phase=0)

radio_power = Pin(("gpio32_63", 14), Pin.OUT)
radio_power.off()
rf_switch = Pin(("gpio0_31", 18), Pin.OUT)
rf_switch.on()
time.sleep(.2)

lora_cfg = {
   "freq_khz": 868300,
   "sf": 7,
   "bw": "125",  # kHz
   "coding_rate": 5,
   "preamble_len": 12,
   "output_power": 14,  # dBm
}

def get_async_modem():
    from lora import AsyncSX1262
    return AsyncSX1262(
        spi=spi,
        cs=pinset["chipselect"],
        busy=pinset["busy"],
        dio1=pinset["dio"],
        reset=pinset["reset"],
        lora_cfg=lora_cfg,
        dio3_tcxo_millivolts=1800,
    )


async def main_task():
    modem = get_async_modem()
    await asyncio.gather(
        asyncio.create_task(send_coro(modem)),
        asyncio.create_task(recv_coro(modem)),
    )

async def recv_coro(modem):
    while True:
        print("Receiving...")
        rx = await modem.recv(2000)
        if rx:
            print(f"Received: {rx!r}")
        else:
            print("Receive timeout!")

async def send_coro(modem):
    counter = 0
    while True:
        tx = f"PING: Hello world from async MicroPython #{counter}"
        print(f"Sending...{tx}")
        await modem.send(tx.encode())
        print("Sent!")
        await asyncio.sleep(5)
        counter += 1

try:
    asyncio.run(main_task())
except KeyboardInterrupt:
    pass

print("radio power = 1")
radio_power.on()
print("rf switch = 0")
rf_switch.off()
print("pm_busy_clear spi1")
pm_busy_clear("spi1")
pm_suspend("spi1")
for key in pinset:
    print(f"{key} = 0")
    pinset[key].init(0)
