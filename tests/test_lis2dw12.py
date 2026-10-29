from machine import Pin, I2C

class Lis2dw12:
    def __init__(self, i2c_dev, i2c_addr):
        self._bus = type(i2c_dev) == I2C and i2c_dev or I2C(i2c_dev)
        self._addr = i2c_addr

    def write(self, reg, buff):
        self._bus.writeto_mem(self._addr, reg, buff)

    def read(self, reg, num):
        return self._bus.readfrom_mem(self._addr, reg, num)

    def available(self):
        try:
            result = self.read(0x0F, 1)[0] == 0x44
        except:
            result = False
        return result

    def start(self):
        self.write(0x20, b'\x41')

    def stop(self):
        self.write(0x20, b'\x00')

    def ready(self):
        status = self.read(0x37, 1)[0]
        return status & 0x41 == 0x41

    def temp(self):
        buff = accel.read(0x0D, 2)
        val = (buff[0] + (buff[1] << 8))
        if val & 0x8000:
            val -= 0x10000
        val = (val >> 4) * 62_500
        val += 25_000_000
        val /= 1_000_000.
        return val

    def xyz(self):
        BITS = 14
        SCALE = 2. / (1<<13)
        def cvt(arr, bits, scale):
            val = arr[0] + (arr[1] << 8)
            if val & 0x8000:
                val -= 0x10000
            val >>= (16 - bits)
            val *= scale
            return val
        buff = accel.read(0x26, 6)
        x, y, z = [cvt(buff[i:i+2], BITS, SCALE) for i in range(0,6,2)]
        return (x,y,z)

if __name__ == "__main__":
    import time

    DEV = "i2c3"
    ADDR = 0x19

    accel = Lis2dw12(DEV, ADDR)
    if accel.available():
        accel.start()
        try:
            while True:
                if accel.ready():
                    x, y, z = accel.xyz()
                    t = accel.temp()
                    print(f'({x:8.3f}, {y:8.3f}, {z:8.3f}) g | {t:.1f} °C')
                time.sleep(.1)
        except KeyboardInterrupt:
            pass
        accel.stop()
        print("Measure stopped.")
    else:
        print(f"No accel found at {DEV}, {hex(ADDR)}.")
