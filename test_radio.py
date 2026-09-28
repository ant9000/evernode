from sx1262 import *
import time

pinset = {
        'busy':       ("gpio0_31", 16),
        'reset':      ("gpio0_31", 17),
        'chipselect': ("gpio0_31", 11),
        'dio':        ("gpio0_31", 15),
}
def onrx(lora_instance,packet,rssi,bad_crc):
        print(f"Received packet {packet} RSSI:{rssi} bad_crc:{bad_crc}")

spi=SPI("spi1", baudrate=10_000_000, polarity=0, phase=0)
lora = SX1262(pinset=pinset,rx_callback=onrx, spi=spi)
lora.begin()
lora.reset()
lora.configure(868300000, 125000, 5, 11, 14)
lora.receive()
lora.show_status()
payload=bytearray(b'Hello from Apollo3!')
while True:
    lora.send(payload)
    lora.show_status()
    lora.receive()
    time.sleep(5)
