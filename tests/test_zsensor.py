import zsensor, time

accel = zsensor.Sensor("lis2dw12@19")
try:
    while True:
        accel.measure()
        x = accel.get_float(zsensor.ACCEL_X)
        y = accel.get_float(zsensor.ACCEL_Y)
        z = accel.get_float(zsensor.ACCEL_Z)
        t = accel.get_float(zsensor.DIE_TEMP)
        print(f'({x:8.3f}, {y:8.3f}, {z:8.3f}) g | {t:.1f} °C')
        time.sleep(.1)
except KeyboardInterrupt:
    pass
