import zsensor, time

accel = zsensor.Sensor("lis2dw12")
try:
    while True:
        x = accel.get_float(zsensor.ACCEL_X)
        y = accel.get_float(zsensor.ACCEL_Y)
        z = accel.get_float(zsensor.ACCEL_Z)
        print(f'({x:8.3f}, {y:8.3f}, {z:8.3f}) g')
        time.sleep(.1)
except KeyboardInterrupt:
    pass
