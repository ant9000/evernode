import time
from machine import Pin, SPI
from lora import SX1262

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

def get_modem():
    return SX1262(
        spi=spi,
        cs=pinset["chipselect"],
        busy=pinset["busy"],
        reset=pinset["reset"],
        dio1=pinset["dio"],
        lora_cfg=lora_cfg,
    )

def main():
    print("Initializing...")
    modem = get_modem()

    counter = 0
    while True:
        print("Sending...")
        modem.send(f"Hello world from MicroPython #{counter}".encode())

        print("Receiving...")
        rx = modem.recv(timeout_ms=5000)
        if rx:
            print(f"Received: {rx!r}")
        else:
            print("Timeout!")
        time.sleep(2)
        counter += 1

main()
