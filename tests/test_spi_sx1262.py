import time
from machine import Pin, SPI

busy       = Pin(("gpio0_31", 16), Pin.IN)
reset      = Pin(("gpio0_31", 17), Pin.OUT)
chipselect = Pin(("gpio0_31", 11), Pin.OUT)
spi        = SPI("spi1", baudrate=10_000_000, polarity=0, phase=0)

def command(opcode, data=None):
    if data != None:
        if isinstance(data,int): data = [data]
        payload = bytearray(1+len(data)) # opcode + payload
        payload[0] = opcode
        payload[1:] = bytes(data)
    else:
        payload = bytearray([opcode])
    reply = bytearray(len(payload))
    while busy.value():
        time.sleep_us(1)
    chipselect(0)
    print(">>> {}".format(payload.hex()))
    spi.write_readinto(payload,reply)
    print("<<< {}".format(reply.hex()))
    chipselect(1)
    return reply

for value in (0,1):
    reset(value)
    time.sleep_us(500)
status = command(0x80,0) # set standby
print("Standby:   Status = ", status)
#status = command(0x8a,0x01) # set LoRa mode
#print("LoRa mode: Status = ", status)
status = command(0x12,0)[1] # get IRQ status
print("Chip mode  = ", (status >> 4) & 7)
print("Cmd status = ", (status >> 1) & 7)
