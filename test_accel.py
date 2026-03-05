from machine import Pin, I2C


DEV = "i2c3"
ADDR = 0x1d

def cvt(arr):
    v = arr[0] + (arr[1] << 8)
    if v & 0x1000:
        v = -0x10000 + v
    return v >> 6

bus = I2C(DEV)
bus.writeto_mem(ADDR, 0x20, bytearray(0x80))
try:
    while True:
        buff = bus.readfrom_mem(ADDR, 0xa8, 6)
        x, y, z = cvt(buff[0:2]), cvt(buff[2:4]), cvt(buff[4:6])
        print(x, y, z)
except KeyboardInterrupt:
    pass

bus.writeto_mem(ADDR, 0x20, 0x00)
