from machine import mem32

def u32bit(v):
    s = f"{v:032b}"
    return " ".join([s[i:i+8] for i in range(0,32,8)])

def dump_reg(name, addr):
    value = mem32[addr] & 0xffffffff
    print(f"\t{name:-15s}  {u32bit(value)} | 0x{value:08x}")

# unlock info0 top half
mem32[0x40030078] = 1
mem32[0x40030080] = 0xEFBEADDE
mem32[0x40030084] = 0xEFBEADDE
mem32[0x40030088] = 0xEFBEADDE
mem32[0x4003008C] = 0xEFBEADDE
print(mem32[0x4003007C])
