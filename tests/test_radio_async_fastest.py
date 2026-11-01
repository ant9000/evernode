import asyncio
from radio import Radio

lora_cfg = {
   "freq_khz": 868300,
   "sf": 7,
   "bw": "125",  # kHz
   "coding_rate": 5,
   "preamble_len": 12,
   "output_power": 14,  # dBm
}

with Radio(lora_cfg) as modem:
    async def main_task():
        await asyncio.gather(
            asyncio.create_task(send_coro(modem)),
            asyncio.create_task(recv_coro(modem)),
        )

    async def recv_coro(modem):
        while True:
            print("Receiving...")
            rx = await modem.recv()
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

print("test end")
