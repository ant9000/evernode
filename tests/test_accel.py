from machine import Pin, I2C

DEV = "i2c3"
ADDR = 0x19
BITS = 14
SCALE = 2. / (1<<13)

def cvt(arr, bits, scale):
    v = arr[0] + (arr[1] << 8)
    if v & 0x8000:
        v -= 0x10000
    v >>= (16 - bits)
    v *= scale
    return v

bus = I2C(DEV)
bus.writeto_mem(ADDR, 0x20, b'\x41')
try:
    while True:
        buff = bus.readfrom_mem(ADDR, 0x28, 6)
        x, y, z = [cvt(buff[i:i+2], BITS, SCALE) for i in range(0,6,2)]
        print(f'({x:8.3f}, {y:8.3f}, {z:8.3f}) g')
except KeyboardInterrupt:
    pass

bus.writeto_mem(ADDR, 0x20, b'\x00')
