import time, struct
from machine import Pin, SPI

busy = Pin(("gpio0_31", 16), Pin.IN)
rst = Pin(("gpio0_31", 17), Pin.OUT)
cs = Pin(("gpio0_31", 11), Pin.OUT)
spi = SPI("spi1", baudrate=10_000_000, polarity=0, phase=0)

def write(payload, reply):
    for v in (0,1):
        rst(v)
        time.sleep_us(500)
    while busy.value():
        time.sleep_us(1)
    print(">>> {}".format(payload.hex()))
    cs(0)
    spi.write_readinto(payload,reply)
    cs(1)
    print("<<< {}".format(reply.hex()))

payload = bytearray([0x80, 0x00]) # set standby

print("FreakWAN:")
write(payload, bytearray(len(payload)))

print("Micropython-lib:")
write(payload, payload)
