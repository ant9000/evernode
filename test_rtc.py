from machine import I2C

DEV = "i2c3"
ADDR = 0x69

bus = I2C(DEV)
for i in range(3):
    reg = 0x28 + i
    val = bus.readfrom_mem(ADDR, reg, 1)
    print(f'[{reg:02x}] {val.hex()')
