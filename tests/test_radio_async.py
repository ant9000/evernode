# MicroPython lora simple_rxtx example - asynchronous API version
# MIT license; Copyright (c) 2023 Angus Gratton
import asyncio
from machine import Pin, SPI

pinset = {
        'busy':       Pin(("gpio0_31", 16)),
        'reset':      Pin(("gpio0_31", 17)),
        'chipselect': Pin(("gpio0_31", 11)),
        'dio':        Pin(("gpio0_31", 15)),
}
spi = SPI("spi1", baudrate=10_000_000, polarity=0, phase=0)

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
        print("Sending...")
        await modem.send(f"Hello world from async MicroPython #{counter}".encode())
        print("Sent!")
        await asyncio.sleep(5)
        counter += 1

asyncio.run(main_task())
