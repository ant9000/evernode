import machine
from micropython import const
from collections import OrderedDict
import time

def u32bit(v):
    s = f"{v:032b}"
    return " ".join([s[i:i+8] for i in range(0,32,8)])

def odict(lst):
    return OrderedDict([(name, idx) for idx, name in enumerate(lst)])

REGS = OrderedDict()
REGS["DEVPWREN"] = {
    "addr": const(0x40021008),
    "bits": odict(["IOS", "IOM0", "IOM1", "IOM2", "IOM3", "IOM4", "IOM5", "UART0", "UART1", "ADC", "SCARD", "MSPI", "PDM", "BLEL"]),
}
REGS["DEVPWRSTATUS"] = {
    "addr": const(0x40021018),
    "bits": odict(["MCUL", "MCUH", "HCPA", "HCPB", "HCPC", "PWRADC", "PWRMSPI", "PWRPDM", "BLEL", "BLEH"]),
}

def print_state():
    for name in REGS:
        reg = REGS[name]
        value = machine.mem32[reg["addr"]] & 0xffffffff
        print(f"{name:-15s}  {u32bit(value)} | 0x{value:08x} | ", end="")
        for label, bit in reg["bits"].items():
            if value & (1 << bit):
                print(f"{label} ", end="")
        print("")
    print("")

def power_device(dev, enable):
    reg = REGS["DEVPWREN"]
    addr = reg["addr"]
    bits = reg["bits"]
    if dev not in bits:
        raise ValueError(f"Unknown device {dev}")
    state = machine.disable_irq()
    if enable:
        mask = (1 << bits[dev])
        machine.mem32[addr] |= mask
    else:
        mask = 0xffffffff & ~(1 << bits[dev])
        machine.mem32[addr] &= mask
    machine.enable_irq(state)

print("### Current state ###")
print_state()
for device in ["IOM1", "IOM3", "BLEL"]:
    print(f"### Enabling {device} ###")
    power_device(device, True)
    time.sleep_ms(10)
    print_state()
    print(f"### Disabling {device} ###")
    power_device(device, False)
    time.sleep_ms(10)
    print_state()
