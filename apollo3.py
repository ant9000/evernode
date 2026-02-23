import machine
from micropython import const
from collections import OrderedDict

REGISTERS = OrderedDict()
REGISTERS["PWRCTRL"] = [
    (const(0x40021000), "SUPPLYSRC"       ), # Voltage Regulator Select Register
    (const(0x40021004), "SUPPLYSTATUS"    ), # Voltage Regulators status
    (const(0x40021008), "DEVPWREN"        ), # Device Power Enable
    (const(0x4002100C), "MEMPWDINSLEEP"   ), # Power-down SRAM banks in Deep Sleep mode
    (const(0x40021010), "MEMPWREN"        ), # Enables individual banks of the MEMORY array
    (const(0x40021014), "MEMPWRSTATUS"    ), # Mem Power ON Status
    (const(0x40021018), "DEVPWRSTATUS"    ), # Device Power ON Status
    (const(0x4002101C), "SRAMCTRL"        ), # SRAM Control register
    (const(0x40021020), "ADCSTATUS"       ), # Power Status Register for ADC Block
    (const(0x40021024), "MISC"            ), # Power Optimization Control Bits
    (const(0x40021028), "DEVPWREVENTEN"   ), # Event enable register to control which DEVP-WRSTATUS bits are routed to event input of CPU.
    (const(0x4002102C), "MEMPWREVENTEN"   ), # Event enable register to control which MEMP-WRSTATUS bits are routed to event input of CPU.
]
REGISTERS["MCUCTRL"] = [
    (const(0x40020000), "CHIPPN"          ), # Chip Information Register
    (const(0x40020004), "CHIPID0"         ), # Unique Chip ID 0
    (const(0x40020008), "CHIPID1"         ), # Unique Chip ID 1
    (const(0x4002000C), "CHIPREV"         ), # Chip Revision
    (const(0x40020010), "VENDORID"        ), # Unique Vendor ID
    (const(0x40020014), "SKU"             ), # Unique Chip SKU
    (const(0x40020018), "FEATUREENABLE"   ), # Feature Enable on Burst and BLE
    (const(0x40020020), "DEBUGGER"        ), # Debugger Control
    (const(0x40020100), "BODCTRL"         ), # BOD control Register
    (const(0x40020104), "ADCPWRDLY"       ), # ADC Power Up Delay Control
    (const(0x4002010C), "ADCCAL"          ), # ADC Calibration Control
    (const(0x40020110), "ADCBATTLOAD"     ), # ADC Battery Load Enable
    (const(0x40020118), "ADCTRIM"         ), # ADC Trims
    (const(0x4002011C), "ADCREFCOMP"      ), # ADC Referece Keeper and Comparator Control
    (const(0x40020120), "XTALCTRL"        ), # XTAL Oscillator Control
    (const(0x40020124), "XTALGENCTRL"     ), # XTAL Oscillator General Control
    (const(0x40020198), "MISCCTRL"        ), # Miscellaneous control register.
    (const(0x400201A0), "BOOTLOADER"      ), # Bootloader and secure boot functions
    (const(0x400201A4), "SHADOWVALID"     ), # Register to indicate whether the shadow registers have been successfully loaded from the Flash Information Space.
    (const(0x400201B0), "SCRATCH0"        ), # Scratch register that is not reset by any reset
    (const(0x400201B4), "SCRATCH1"        ), # Scratch register that is not reset by any reset
    (const(0x400201C0), "ICODEFAULTADDR"  ), # ICODE bus address which was present when a bus fault occurred.
    (const(0x400201C4), "DCODEFAULTADDR"  ), # DCODE bus address which was present when a bus fault occurred.
    (const(0x400201C8), "SYSFAULTADDR"    ), # System bus address which was present when a bus fault occurred.
    (const(0x400201CC), "FAULTSTATUS"     ), # Reflects the status of the bus decoders' fault detection. Any write to this register will clear all of the status bits within the register.
    (const(0x400201D0), "FAULTCAPTUREEN"  ), # Enable the fault capture registers
    (const(0x40020200), "DBGR1"           ), # Read-only debug register 1
    (const(0x40020204), "DBGR2"           ), # Read-only debug register 2
    (const(0x40020220), "PMUENABLE"       ), # Control bit to enable/disable the PMU
    (const(0x40020250), "TPIUCTRL"        ), # TPIU Control Register. Determines the clock enable and frequency for the M4's TPIU interface.
]
REGISTERS["CACHECTRL"] = [
	(const(0x40018000), "CACHECFG"        ), # Flash Cache Control Register"
	(const(0x40018004), "FLASHCFG"        ), # Flash Control Register"
	(const(0x40018008), "CTRL"            ), # Cache Control"
	(const(0x40018010), "NCR0START"       ), # Flash Cache Noncachable Region 0 Start"
	(const(0x40018014), "NCR0END"         ), # Flash Cache Noncachable Region 0 End"
	(const(0x40018018), "NCR1START"       ), # Flash Cache Noncachable Region 1 Start"
	(const(0x4001801C), "NCR1END"         ), # Flash Cache Noncachable Region 1 End"
	(const(0x40018040), "DMON0"           ), # Data Cache Total Accesses"
	(const(0x40018044), "DMON1"           ), # Data Cache Tag Lookups"
	(const(0x40018048), "DMON2"           ), # Data Cache Hits"
	(const(0x4001804C), "DMON3"           ), # Data Cache Line Hits"
	(const(0x40018050), "IMON0"           ), # Instruction Cache Total Accesses"
	(const(0x40018054), "IMON1"           ), # Instruction Cache Tag Lookups"
	(const(0x40018058), "IMON2"           ), # Instruction Cache Hits"
	(const(0x4001805C), "IMON3"           ), # Instruction Cache Line Hits"
]
REGISTERS["GPIO"] = [
    (const(0x40010000), "PADREGA"         ), # Pad Configuration Register A (Pads 3-0)
    (const(0x40010004), "PADREGB"         ), # Pad Configuration Register B (Pads 7-4)
    (const(0x40010008), "PADREGC"         ), # Pad Configuration Register C (Pads 11-8)
    (const(0x4001000C), "PADREGD"         ), # Pad Configuration Register D (Pads 15-12)
    (const(0x40010010), "PADREGE"         ), # Pad Configuration Register E (Pads 19-16)
    (const(0x40010014), "PADREGF"         ), # Pad Configuration Register F (Pads 23-20)
    (const(0x40010018), "PADREGG"         ), # Pad Configuration Register G (Pads 27-24)
    (const(0x4001001C), "PADREGH"         ), # Pad Configuration Register H (Pads 31-28)
    (const(0x40010020), "PADREGI"         ), # Pad Configuration Register I (Pads 35-32)
    (const(0x40010024), "PADREGJ"         ), # Pad Configuration Register J (Pads 39-36)
    (const(0x40010028), "PADREGK"         ), # Pad Configuration Register K (Pads 43-40)
    (const(0x4001002C), "PADREGL"         ), # Pad Configuration Register L (Pads 47-44)
    (const(0x40010030), "PADREGM"         ), # Pad Configuration Register M (Pads 49-48)
    (const(0x40010040), "CFGA"            ), # GPIO Configuration Register A (Pads 7-0)
    (const(0x40010044), "CFGB"            ), # GPIO Configuration Register B (Pads 15-8)
    (const(0x40010048), "CFGC"            ), # GPIO Configuration Register C (Pads 23-16)
    (const(0x4001004C), "CFGD"            ), # GPIO Configuration Register D (Pads 31-24)
    (const(0x40010050), "CFGE"            ), # GPIO Configuration Register E (Pads 39-32)
    (const(0x40010054), "CFGF"            ), # GPIO Configuration Register F (Pads 47-40)
    (const(0x40010058), "CFGG"            ), # GPIO Configuration Register G (Pads 49-48)
    (const(0x40010060), "PADKEY"          ), # Key Register for all pad configuration registers
    (const(0x40010080), "RDA"             ), # GPIO Input Register A (31-0)
    (const(0x40010084), "RDB"             ), # GPIO Input Register B (49-32)
    (const(0x40010088), "WTA"             ), # GPIO Output Register A (31-0)
    (const(0x4001008C), "WTB"             ), # GPIO Output Register B (49-32)
    (const(0x40010090), "WTSA"            ), # GPIO Output Register A Set (31-0)
    (const(0x40010094), "WTSB"            ), # GPIO Output Register B Set (49-32)
    (const(0x40010098), "WTCA"            ), # GPIO Output Register A Clear (31-0)
    (const(0x4001009C), "WTCB"            ), # GPIO Output Register B Clear (49-32)
    (const(0x400100A0), "ENA"             ), # GPIO Enable Register A (31-0)
    (const(0x400100A4), "ENB"             ), # GPIO Enable Register B (49-32)
    (const(0x400100A8), "ENSA"            ), # GPIO Enable Register A Set (31-0)
    (const(0x400100AC), "ENSB"            ), # GPIO Enable Register B Set (49-32)
    (const(0x400100B4), "ENCA"            ), # GPIO Enable Register A Clear (31-0)
    (const(0x400100B8), "ENCB"            ), # GPIO Enable Register B Clear (49-32)
    (const(0x400100BC), "STMRCAP"         ), # STIMER Capture Control
    (const(0x400100C0), "IOM0IRQ"         ), # IOM0 Flow Control IRQ Select
    (const(0x400100C4), "IOM1IRQ"         ), # IOM1 Flow Control IRQ Select
    (const(0x400100C8), "IOM2IRQ"         ), # IOM2 Flow Control IRQ Select
    (const(0x400100CC), "IOM3IRQ"         ), # IOM3 Flow Control IRQ Select
    (const(0x400100D0), "IOM4IRQ"         ), # IOM4 Flow Control IRQ Select
    (const(0x400100D4), "IOM5IRQ"         ), # IOM5 Flow Control IRQ Select
    (const(0x400100D8), "BLEIFIRQ"        ), # BLEIF Flow Control IRQ Select
    (const(0x400100DC), "GPIOOBS"         ), # GPIO Observation Mode Sample register
    (const(0x400100E0), "ALTPADCFGA"      ), # Alternate Pad Configuration reg0 (Pads 0-3)
    (const(0x400100E4), "ALTPADCFGB"      ), # Alternate Pad Configuration reg1 (Pads 4-7)
    (const(0x400100E8), "ALTPADCFGC"      ), # Alternate Pad Configuration reg2 (Pads 8-11)
    (const(0x400100EC), "ALTPADCFGD"      ), # Alternate Pad Configuration reg3 (Pads 12-15)
    (const(0x400100F0), "ALTPADCFGE"      ), # Alternate Pad Configuration reg4 (Pads 16-19)
    (const(0x400100F4), "ALTPADCFGF"      ), # Alternate Pad Configuration reg5 (Pads 20-23)
    (const(0x400100F8), "ALTPADCFGG"      ), # Alternate Pad Configuration reg6 (Pads 24-27)
    (const(0x400100FC), "ALTPADCFGH"      ), # Alternate Pad Configuration reg7 (Pads 28-31)
    (const(0x40010100), "ALTPADCFGI"      ), # Alternate Pad Configuration reg8 (Pads 32-35)
    (const(0x40010104), "ALTPADCFGJ"      ), # Alternate Pad Configuration reg9 (Pads 36-39)
    (const(0x40010108), "ALTPADCFGK"      ), # Alternate Pad Configuration reg10 (Pads 40-43)
    (const(0x4001010C), "ALTPADCFGL"      ), # Alternate Pad Configuration reg11 (Pads 44-47)
    (const(0x40010110), "ALTPADCFGM"      ), # Alternate Pad Configuration reg12 (Pads 48-49)
    (const(0x40010114), "SCDET"           ), # SCARD Card Detect select
    (const(0x40010118), "CTENCFG"         ), # Counter/Timer Enable Config
    (const(0x40010200), "INT0EN"          ), # GPIO Interrupt Registers 31-0: Enable
    (const(0x40010204), "INT0STAT"        ), # GPIO Interrupt Registers 31-0: Status
    (const(0x40010208), "INT0CLR"         ), # GPIO Interrupt Registers 31-0: Clear
    (const(0x4001020C), "INT0SET"         ), # GPIO Interrupt Registers 31-0: Set
    (const(0x40010210), "INT1EN"          ), # GPIO Interrupt Registers 49-32: Enable
    (const(0x40010214), "INT1STAT"        ), # GPIO Interrupt Registers 49-32: Status
    (const(0x40010218), "INT1CLR"         ), # GPIO Interrupt Registers 49-32: Clear
    (const(0x4001021C), "INT1SET"         ), # GPIO Interrupt Registers 49-32: Set
]
REGISTERS["CLKGEN"] = [
	(const(0x40004000), "CALXT"           ), # XT Oscillator Control"
	(const(0x40004004), "CALRC"           ), # RC Oscillator Control"
	(const(0x40004008), "ACALCTR"         ), # Autocalibration Counter"
	(const(0x4000400C), "OCTRL"           ), # Oscillator Control"
	(const(0x40004010), "CLKOUT"          ), # CLKOUT Frequency Select"
	(const(0x40004014), "CLKKEY"          ), # Key Register for Clock Control Register"
	(const(0x40004018), "CCTRL"           ), # HFRC Clock Control"
	(const(0x4000401C), "STATUS"          ), # Clock Generator Status"
	(const(0x40004020), "HFADJ"           ), # HFRC Adjustment"
	(const(0x40004028), "CLOCKENSTAT"     ), # Clock Enable Status"
	(const(0x4000402C), "CLOCKEN2STAT"    ), # Clock Enable Status"
	(const(0x40004030), "CLOCKEN3STAT"    ), # Clock Enable Status"
	(const(0x40004034), "FREQCTRL"        ), # HFRC Frequency Control register"
	(const(0x4000403C), "BLEBUCKTONADJ"   ), # BLE BUCK TON ADJUST"
	(const(0x40004100), "INTRPTEN"        ), # CLKGEN Interrupt Register: Enable"
	(const(0x40004104), "INTRPTSTAT"      ), # CLKGEN Interrupt Register: Status"
	(const(0x40004108), "INTRPTCLR"       ), # CLKGEN Interrupt Register: Clear"
	(const(0x4000410C), "INTRPTSET"       ), # CLKGEN Interrupt Register: Set"
]
REGISTERS["STIMER"] = [
	(const(0x40008140), "STCFG"           ), # ST Configuration"
	(const(0x40008144), "STTMR"           ), # System Timer Count (Real Time Counter)"
	(const(0x40008148), "CAPTURECONTROL"  ), # Capture Control"
	(const(0x40008150), "SCMPR0"          ), # Compare A"
	(const(0x40008154), "SCMPR1"          ), # Compare B"
	(const(0x40008158), "SCMPR2"          ), # Compare C"
	(const(0x4000815C), "SCMPR3"          ), # Compare D"
	(const(0x40008160), "SCMPR4"          ), # Compare E"
	(const(0x40008164), "SCMPR5"          ), # Compare F"
	(const(0x40008168), "SCMPR6"          ), # Compare G"
	(const(0x4000816C), "SCMPR7"          ), # Compare H"
	(const(0x400081E0), "SCAPT0"          ), # Capture A"
	(const(0x400081E4), "SCAPT1"          ), # Capture B"
	(const(0x400081E8), "SCAPT2"          ), # Capture C"
	(const(0x400081EC), "SCAPT3"          ), # Capture D"
	(const(0x400081F0), "SNVR0"           ), # System Timer NVRAM_A"
	(const(0x400081F4), "SNVR1"           ), # System Timer NVRAM_B"
	(const(0x400081F8), "SNVR2"           ), # System Timer NVRAM_C"
	(const(0x400081FC), "SNVR3"           ), # System Timer NVRAM_D"
	(const(0x40008300), "STMINTEN"        ), # STIMER Interrupts: Enable"
	(const(0x40008304), "STMINTSTAT"      ), # STIMER Interrupts: Status"
	(const(0x40008308), "STMINTCLR"       ), # STIMER Interrupts: Clear"
	(const(0x4000830C), "STMINTSET"       ), # STIMER Interrupts: Set"
]

def u32bit(v):
    s = f"{v:032b}"
    return " ".join([s[i:i+8] for i in range(0,32,8)])

if __name__ == "__main__":
    for section in REGISTERS:
        print(f"### {section} ###")
        for addr, name in REGISTERS[section]:
            value = machine.mem32[addr] & 0xffffffff
            print(f"\t{name:-15s}  {u32bit(value)} | 0x{value:08x}")
        print("")
