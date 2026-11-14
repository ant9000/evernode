from machine import Pin

print("START")

SEL1 = Pin(("gpio0_31", 5), Pin.IN, Pin.PULL_UP)
DEMO1 = SEL1.value() == 0
SEL1.init(0)
if DEMO1:
    print("DEMO1")
    import demo_accel
    # never returns
    
SEL2 = Pin(("gpio0_31", 6), Pin.IN, Pin.PULL_UP)
DEMO2 = SEL2.value() == 0
SEL2.init(0)
if DEMO2:
    print("DEMO2")
    import demo_sleep

print("MAIN")
