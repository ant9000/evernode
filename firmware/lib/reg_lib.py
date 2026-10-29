# reg_lib.py
import machine
from micropython import const

def powered_up():
    value = machine.mem32[const(0x40021008)] & 0xffffffff
    print("Peripherals powered up:")
    if value & 0x0001: print("\tIO Slave")
    if value & 0x0002: print("\tIO Master 0")
    if value & 0x0004: print("\tIO Master 1")
    if value & 0x0008: print("\tIO Master 2")
    if value & 0x0010: print("\tIO Master 3")
    if value & 0x0020: print("\tIO Master 4")
    if value & 0x0040: print("\tIO Master 5")
    if value & 0x0080: print("\tUART 0")
    if value & 0x0100: print("\tUART 1")
    if value & 0x0200: print("\tADC")
    if value & 0x0400: print("\tSDCARD")
    if value & 0x0800: print("\tMSPI")
    if value & 0x1000: print("\tPDM")
    if value & 0x2000: print("\tBLE")

def chip_id():
    chipid0 = machine.mem32[const(0x40020004)] & 0xffffffff
    chipid1 = machine.mem32[const(0x40020008)] & 0xffffffff
    print(f"\tchipid 0 = 0x{chipid0:08x}")
    print(f"\tchipid 1 = 0x{chipid1:08x}")

# ---------------------------------------------------------------------------
# Apollo3 Blue (AMA3B) GPIO pad inspector
# Register map: AmbiqSuite R3.2.0 (am_reg_gpio.h / am_hal_gpio.h / am_hal_pin.h)
# ---------------------------------------------------------------------------
GPIO_BASE = 0x40010000

PADREGA = 0x00   # PADREGA..PADREGM, 4 pads/reg, 8-bit field per pad:
                 #   [2:0] FNCSEL, b3 STRNG, b4 INPEN, b5 PULL, [7:6] RSEL/PWRSW
CFGA    = 0x40   # CFGA..CFGG, 8 pins/reg, 4-bit field per pin:
                 #   b0 INCFG(RDZERO), [2:1] OUTCFG, b3 INTD
RDA     = 0x80   # pad input levels   pins  0-31
RDB     = 0x84   # pad input levels   pins 32-49
WTA     = 0x88   # output data latch  pins  0-31
WTB     = 0x8C   # output data latch  pins 32-49
ENA     = 0xA0   # output enable      pins  0-31 (tristate / FastGPIO)
ENB     = 0xA4   # output enable      pins 32-49

# Pad function table, verbatim from am_hal_pin.h (AmbiqSuite R3.2.0, apollo3).
# Index = pad number; dict = {FNCSEL: function}.
# Pads 30-38, 42, 43, 45, 46 are BGA-package only (AM_PACKAGE_BGA).
PIN_FUNC = (
    {0:"SLSCL",     1:"SLSCK",    2:"CLKOUT",  3:"GPIO", 5:"MSPI4",    7:"NCE0"},      # 0
    {0:"SLSDAWIR3", 1:"SLMOSI",   2:"UART0TX", 3:"GPIO", 5:"MSPI5",    7:"NCE1"},      # 1
    {0:"UART1RX",   1:"SLMISO",   2:"UART0RX", 3:"GPIO", 5:"MSPI6",    7:"NCE2"},      # 2
    {0:"UART0RTS",  1:"SLnCE",    2:"NCE3",    3:"GPIO", 5:"MSPI7",    6:"TRIG1",  7:"I2S_WCLK"},  # 3 (PSOURCE)
    {0:"UART0CTS",  1:"SLINT",    2:"NCE4",    3:"GPIO", 5:"UART1RX",  6:"CTIM17", 7:"MSPI2"},     # 4
    {0:"M0SCL",     1:"M0SCK",    2:"UART0RTS",3:"GPIO", 5:"EXTHFA",   7:"CTIM8"},     # 5
    {0:"M0SDAWIR3", 1:"M0MISO",   2:"UART0CTS",3:"GPIO", 5:"CTIM10",   7:"I2S_DAT"},   # 6
    {0:"NCE7",      1:"M0MOSI",   2:"CLKOUT",  3:"GPIO", 4:"TRIG0",    5:"UART0TX", 7:"CTIM19"},   # 7
    {0:"M1SCL",     1:"M1SCK",    2:"NCE8",    3:"GPIO", 4:"SCCCLK",   6:"UART1TX"},   # 8
    {0:"M1SDAWIR3", 1:"M1MISO",   2:"NCE9",    3:"GPIO", 4:"SCCIO",    6:"UART1RX"},   # 9
    {0:"UART1TX",   1:"M1MOSI",   2:"NCE10",   3:"GPIO", 4:"PDMCLK",   5:"UART1RTS"},  # 10
    {0:"ADCSE2",    1:"NCE11",    2:"CTIM31",  3:"GPIO", 4:"SLINT",    5:"UART1CTS", 6:"UART0RX", 7:"PDMDATA"},  # 11
    {0:"ADCD0NSE9", 1:"NCE12",    2:"CTIM0",   3:"GPIO", 5:"PDMCLK",   6:"UART0CTS", 7:"UART1TX"}, # 12
    {0:"ADCD0PSE8", 1:"NCE13",    2:"CTIM2",   3:"GPIO", 4:"I2SBCLK",  5:"EXTHFB",  6:"UART0RTS", 7:"UART1RX"},  # 13
    {0:"ADCD1P",    1:"NCE14",    2:"UART1TX", 3:"GPIO", 4:"PDMCLK",   5:"EXTHFS",  6:"SWDCK",   7:"32KHZXT"}, # 14
    {0:"ADCD1N",    1:"NCE15",    2:"UART1RX", 3:"GPIO", 4:"PDMDATA",  5:"EXTXT",   6:"SWDIO",   7:"SWO"},     # 15
    {0:"ADCSE0",    1:"NCE16",    2:"TRIG0",   3:"GPIO", 4:"SCCRST",   5:"CMPIN0",  6:"UART0TX", 7:"UART1RTS"},# 16
    {0:"CMPRF1",    1:"NCE17",    2:"TRIG1",   3:"GPIO", 4:"SCCCLK",   6:"UART0RX",  7:"UART1CTS"},            # 17
    {0:"CMPIN1",    1:"NCE18",    2:"CTIM4",   3:"GPIO", 4:"UART0RTS", 5:"ANATEST2", 6:"UART1TX", 7:"SCCIO"},  # 18
    {0:"CMPRF0",    1:"NCE19",    2:"CTIM6",   3:"GPIO", 4:"SCCCLK",   5:"ANATEST1", 6:"UART1RX", 7:"I2SBCLK"},# 19
    {0:"SWDCK",     1:"NCE20",    3:"GPIO",    4:"UART0TX",5:"UART1TX",6:"I2SBCLK", 7:"UART1RTS"}, # 20
    {0:"SWDIO",     1:"NCE21",    3:"GPIO",    4:"UART0RX",5:"UART1RX",6:"I2SBCLK", 7:"UART1CTS"}, # 21
    {0:"UART0TX",   1:"NCE22",    2:"CTIM12",  3:"GPIO", 4:"PDMCLK",   5:"EXTLF",   6:"MSPI0",   7:"SWO"},     # 22
    {0:"UART0RX",   1:"NCE23",    2:"CTIM14",  3:"GPIO", 4:"I2SWCLK",  5:"CMPOUT",  6:"MSPI3",   7:"EXTXT"},   # 23
    {0:"UART1TX",   1:"NCE24",    2:"MSPI8",   3:"GPIO", 4:"UART0CTS", 5:"CTIM21",  6:"32KHZXT", 7:"SWO"},     # 24
    {0:"UART1RX",   1:"NCE25",    2:"CTIM1",   3:"GPIO", 4:"M2SDAWIR3",5:"M2MISO"},                # 25
    {0:"EXTHF",     1:"NCE26",    2:"CTIM3",   3:"GPIO", 4:"SCCRST",   5:"MSPI1",   6:"UART0TX", 7:"UART1CTS"},# 26
    {0:"UART0RX",   1:"NCE27",    2:"CTIM5",   3:"GPIO", 4:"M2SCL",    5:"M2SCK"},                 # 27
    {0:"I2SWCLK",   1:"NCE28",    2:"CTIM7",   3:"GPIO", 5:"M2MOSI",   6:"UART0TX"},               # 28
    {0:"ADCSE1",    1:"NCE29",    2:"CTIM9",   3:"GPIO", 4:"UART0CTS", 5:"UART1CTS",6:"UART0RX", 7:"PDMDATA"}, # 29
    {0:"ANATEST1",  1:"NCE30",    2:"CTIM11",  3:"GPIO", 4:"UART0TX",  5:"UART1RTS",7:"I2SDAT"},   # 30 BGA only
    {0:"ADCSE3",    1:"NCE31",    2:"CTIM13",  3:"GPIO", 4:"UART0RX",  5:"SCCCLK",  7:"UART1RTS"}, # 31 BGA only
    {0:"ADCSE4",    1:"NCE32",    2:"CTIM15",  3:"GPIO", 4:"SCCIO",    5:"EXTLF",   7:"UART1CTS"}, # 32 BGA only
    {0:"ADCSE5",    1:"NCE33",    2:"32KHZXT", 3:"GPIO", 5:"UART0CTS", 6:"CTIM23",  7:"SWO"},      # 33 BGA only
    {0:"ADCSE6",    1:"NCE34",    2:"UART1RTS",3:"GPIO", 4:"CMPRF2",   5:"UART0RTS",6:"UART0RX", 7:"PDMDATA"}, # 34 BGA only
    {0:"ADCSE7",    1:"NCE35",    2:"UART1TX", 3:"GPIO", 4:"I2SDAT",   5:"CTIM27",  6:"UART0RTS"}, # 35 BGA only
    {0:"TRIG1",     1:"NCE36",    2:"UART1RX", 3:"GPIO", 4:"32KHZXT",  5:"UART1CTS",6:"UART0CTS",7:"PDMDATA"}, # 36 BGA only (PSOURCE)
    {0:"TRIG2",     1:"NCE37",    2:"UART0RTS",3:"GPIO", 4:"SCCIO",    5:"UART1TX", 6:"PDMCLK",  7:"CTIM29"},  # 37 BGA only (PSINK)
    {0:"TRIG3",     1:"NCE38",    2:"UART0CTS",3:"GPIO", 5:"M3MOSI",   6:"UART1RX"},               # 38 BGA only
    {0:"UART0TX",   1:"UART1TX",  2:"CTIM25",  3:"GPIO", 4:"M4SCL",    5:"M4SCK"},                 # 39
    {0:"UART0RX",   1:"UART1RX",  2:"TRIG0",   3:"GPIO", 4:"M4SDAWIR3",5:"M4MISO"},                # 40
    {0:"NCE41",     2:"SWO",      3:"GPIO",    4:"I2SWCLK",5:"UART1RTS",6:"UART0TX",7:"UART0RTS"}, # 41 (PSINK)
    {0:"UART1TX",   1:"NCE42",    2:"CTIM16",  3:"GPIO", 4:"M3SCL",    5:"M3SCK"},                 # 42 BGA only
    {0:"UART1RX",   1:"NCE43",    2:"CTIM18",  3:"GPIO", 4:"M3SDAWIR3",5:"M3MISO"},                # 43 BGA only
    {0:"UART1RTS",  1:"NCE44",    2:"CTIM20",  3:"GPIO", 5:"M4MOSI",   6:"UART0TX"},               # 44
    {0:"UART1CTS",  1:"NCE45",    2:"CTIM22",  3:"GPIO", 4:"I2SDAT",   5:"PDMDATA", 6:"UART0RX", 7:"SWO"},     # 45 BGA only
    {0:"32KHZXT",   1:"NCE46",    2:"CTIM24",  3:"GPIO", 4:"SCCRST",   5:"PDMCLK",  6:"UART1TX", 7:"SWO"},     # 46 BGA only
    {0:"32KHZXT",   1:"NCE47",    2:"CTIM26",  3:"GPIO", 5:"M5MOSI",   6:"UART1RX"},               # 47
    {0:"UART0TX",   1:"NCE48",    2:"CTIM28",  3:"GPIO", 4:"M5SCL",    5:"M5SCK"},                 # 48
    {0:"UART0RX",   1:"NCE49",    2:"CTIM30",  3:"GPIO", 4:"M5SDAWIR3",5:"M5MISO"},                # 49
)

_OUTCFG = ("DIS", "PP", "OD", "TS")   # disabled, push-pull, open-drain, tristate


def _rd32(off):
    return machine.mem32[GPIO_BASE + off]


def GPIO_inspect():
    # Snapshot the three state register pairs once, then decode per pin.
    rda, rdb = _rd32(RDA), _rd32(RDB)
    wta, wtb = _rd32(WTA), _rd32(WTB)
    ena, enb = _rd32(ENA), _rd32(ENB)

    print("Apollo3 Blue GPIO @ 0x{:08X}".format(GPIO_BASE))
    print("pin sel function      dir       RD WT EN  notes")
    print("--- --- ------------- --------- -- -- --  -----")

    for pin in range(50):
        # PADREG byte for this pad
        padreg = _rd32(PADREGA + (pin // 4) * 4)
        print("padreg = {:>3}".format(padreg))
        pad    = (padreg >> ((pin % 4) * 8)) & 0xFF
        fncsel = pad & 0x07
        inpen  = (pad >> 4) & 1
        pull   = (pad >> 5) & 1
        pwrsw  = (pad >> 6) & 3

        # GPIOCFG nibble for this pin
        cfg    = (_rd32(CFGA + (pin // 8) * 4) >> ((pin % 8) * 4)) & 0xF
        print("CFG = {:>3}".format(cfg))
        rdzero = cfg & 1
        outcfg = (cfg >> 1) & 3

        # State bits: A-bank = pins 0-31, B-bank = pins 32-49
        b  = pin % 32
        rd = ((rdb if pin >= 32 else rda) >> b) & 1
        wt = ((wtb if pin >= 32 else wta) >> b) & 1
        en = ((enb if pin >= 32 else ena) >> b) & 1

        name = PIN_FUNC[pin].get(fncsel, "RSVD")

        # Direction / which logic values are applicable
        if fncsel == 3:                       # GPIO function
            if outcfg == 0:
                d = "IN" if inpen else "Hi-Z"
            else:
                d = "OUT-" + _OUTCFG[outcfg] + ("+IN" if inpen else "")
            rd_s = str(rd) if inpen else "-"
            wt_s = str(wt) if outcfg else "-"
            en_s = str(en) if outcfg == 3 else "-"
        else:                                 # peripheral function
            d    = "periph"
            rd_s = str(rd) if inpen else "-"  # live pad level if input buffer on
            wt_s = "-"
            en_s = "-"

        notes = []
        if pull:
            notes.append("PULL")
        if rdzero and fncsel == 3:
            notes.append("RDZERO")            # RD forced to 0 by GPIOCFG.INCFG
        if pin in (3, 36) and pwrsw == 1:
            notes.append("PWR=VDD")           # PSOURCE active
        elif pin in (37, 41) and pwrsw == 2:
            notes.append("PWR=VSS")           # PSINK active

        print("{:>3} {:>3} {:<13} {:<9} {:>2} {:>2} {:>2}  {}".format(
              pin, fncsel, name, d, rd_s, wt_s, en_s, " ".join(notes)))
 

if __name__ == '__main__':
    powered_up()