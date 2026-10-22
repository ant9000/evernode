def decode_padreg(value):
    pull       = value & 1
    inp_enable = (value & (1 << 1)) >> 1
    strength   = (value & (1 << 2)) >> 2
    func_sel   = (value & (0b111 << 3)) >> 3
    res_sel    = (value & (0b11 << 6)) >> 6
    return f"pullup {pull} in enable {inp_enable} str {strength} func {func_sel} res {res_sel}"

def decode_cfg(value):
    in_cfg  = value & 1
    out_cfg = (value & (0b11 << 1)) >> 1
    intd    = (value & (1 < 3)) >> 3
    return f"in cfg {in_cfg}, out cfg {out_cfg}, int dir {intd}"

def print_pin(pin):
    assert 0 <= pin < 50
    print(f"Pin: {pin:02d}", end=" ")

    BASE = 0x40010000
    REGS = [
        ('PADREG', 0, 8, decode_padreg),
        ('CFG', 0x40, 4, decode_cfg),
        ('RD', 0x80, 1, None),
        ('EN', 0xA0, 1, None),
    ]
    for (name, offset, bits, decode) in REGS:
        b = (pin * bits)
        reg = BASE + offset + (b // 32) * 4
        mask = ((1 << bits) - 1) << (b % 32)
        value = (machine.mem32[reg] & mask) >> (b % 32)
        if decode:
            value = decode(value)
        else:
            value = f"{name.lower()} {value}"
        #print(f"{name:10s} 0x{reg:08x} {mask:032b} {value}")
        print(value, end=" ")
    print("")

def print_pins():
    for pin in range(50):
        print_pin(pin)
