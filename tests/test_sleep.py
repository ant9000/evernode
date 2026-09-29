import machine
from machine import Pin, lightsleep

def touch(p):
    print(f"Pin {p} IRQ")

pin = machine.Pin(("gpio0_31", 27), Pin.IN)
pin.irq(handler=touch, trigger=Pin.IRQ_RISING)
print("Going to sleep...")
lightsleep(30000)
print("Now awake again!")
