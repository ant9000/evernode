from machine import Pin, I2C

class Lis2dw12:
    def __init__(self, i2c_dev, i2c_addr, int1_pin = None):
        self._bus = type(i2c_dev) == I2C and i2c_dev or I2C(i2c_dev)
        self._addr = i2c_addr
        if int1_pin is not None:
            self._int1 = type(int1_pin) == Pin and int1_pin or Pin(int1_pin, Pin.IN)
        else:
            self._int1 = None

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

    def on_tap(self, cb):
        if not self._int1:
            raise Exception("Int1 pin not configured")
        def wrapper(t):
            int_src = self.read(0x3b, 1)[0]
            if int_src & 0x0c:
                cb((int_src & 0x0c) >> 2)
        self._int1.irq(wrapper)
        # route single and double tap to int1
        self.write(0x23, b'\x48')
        # set tap threshold on x, y, z
        self.write(0x30, bytes([self.read(0x30, 1)[0] | 0b0000_1100]))
        self.write(0x31, bytes([self.read(0x31, 1)[0] | 0b0000_1100]))
        self.write(0x32, bytes([self.read(0x32, 1)[0] | 0b0000_1100]))
        # enable taps on x, y, z
        self.write(0x32, bytes([self.read(0x32, 1)[0] | 0b1110_0000]))
        # configure double tap
        self.write(0x33, b'\xff')
        # enable wake up on taps and sleep mode
        self.write(0x34, b'\xc0')
        # wake up duration
        self.write(0x35, b'\x00')
        # enable interrupts
        ctrl7 = bytes([self.read(0x3f, 1)[0] | 0x20])
        self.write(0x3f, ctrl7)

if __name__ == "__main__":
    import time
    from machine import lightsleep

    DEV = "i2c3"
    ADDR = 0x19
    INT1 = ("gpio0_31", 4)
    def on_tap(tap_type):
        print(f"TAP: {tap_type}")

    accel = Lis2dw12(DEV, ADDR, INT1)
    if accel.available():
        accel.on_tap(on_tap)
        accel.start()
        lightsleep(60_000) # 1 min lightsleep, waiting for taps
        time.sleep(.01)
        if accel.ready():
            x, y, z = accel.xyz()
            t = accel.temp()
            print(f'({x:8.3f}, {y:8.3f}, {z:8.3f}) g | {t:.1f} °C')
        accel.stop()
        print("Measure stopped.")
    else:
        print(f"No accel found at {DEV}, {hex(ADDR)}.")
