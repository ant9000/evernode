from sx1262 import *
import time

pinset = {
        'busy':       ("gpio0_31", 16),
        'reset':      ("gpio0_31", 17),
        'chipselect': ("gpio0_31", 11),
        'clock':      ("gpio0_31",  8),
        'mosi':       ("gpio0_31", 10),
        'miso':       ("gpio0_31",  9),
        'dio':        ("gpio0_31", 15),
}
def onrx(lora_instance,packet,rssi,bad_crc):
        print(f"Received packet {packet} RSSI:{rssi} bad_crc:{bad_crc}")

lora = SX1262(pinset=pinset,rx_callback=onrx)
lora.begin()
lora.configure(868.3, 125000, 5, 7, 14)
lora.receive()
lora.show_status()
payload=bytearray(b'Hello from Apollo3!')
while True:
    lora.send(payload)
    lora.receive()
    print(".", end="")
    time.sleep(5)
