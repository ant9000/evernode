#rtc_lib.py
from machine import I2C, Pin, lightsleep
import time

NightSleep = True
#NightSleep = False
BatIntSleep = True
#BatIntSleep = False
BpolSleep = True
#BpolSleep = False
AlarmSleep = True
#AlarmSleep = False

DEV = "i2c5"
ADDR = 0x69

bus = I2C(DEV)

def rtc_restore():
    print("  RTC restore")
    try:
        bus.writeto_mem(ADDR, 0x0f, b'\x00')
        bus.writeto_mem(ADDR, 0x10, b'\x17')
        wake = bus.readfrom_mem(ADDR, 0x0f, 1)
        print ("after restore wake = ", wake)
        bus.writeto_mem(ADDR, 0x11, b'\x1C')
        bus.writeto_mem(ADDR, 0x12, b'\xe0')
        bus.writeto_mem(ADDR, 0x14, b'\x46')  # XT calibration
    except Exception as e:
        print("    ERROR rtc_lib rtc_restore() i2c error: ", e)


def rtc_sleep(night, batint, bpol, alarm):
    try:
    # night = True -> nightsleep, otherwise daysleep;
    # nRSTlow = True -> nRST low in sleep, otherwise nRST HiZ in sleep (default)
    #batint = True -> wake on panel voltagefalling
        bus.writeto_mem(ADDR, 0x1f, b'\x9d')  #configuration key reg to enable write on the output control reg
        bus.writeto_mem(ADDR, 0x30, b'\x0C')
        if batint:
            if alarm:
                bus.writeto_mem(ADDR, 0x12, b'\xf7') # write 0xf7 in reg 0x12 to enable AIE, EXTI, WDI and BATINT
            else:
                bus.writeto_mem(ADDR, 0x12, b'\xf3') # write 0xf3 in reg 0x12 to enable EXTI, WDI and BATINT
            if bpol: bus.writeto_mem(ADDR, 0x3f, b'\x40') # set BPOL bit (0x40) in reg 0x3F to enable raising interrupt on VBat pin, otherwise is falling interrupt
        else:
            if alarm:
                bus.writeto_mem(ADDR, 0x12, b'\xe7') # write 0xe7 in reg 0x12 to enable AIE, EXTI and WDId BATINT
            else:
                bus.writeto_mem(ADDR, 0x12, b'\xe3') # write 0xe3 in reg 0x12 to enable EXTI and WDI

        bus.writeto_mem(ADDR, 0x11, b'\x18') # PSW OUT2S = 0x6 -> SLEEP function for PSW pin

    # write 0xa1 in reg 0x1f (conf key) and write 0x04 in reg 0x1c
        bus.writeto_mem(ADDR, 0x1f, b'\xa1')  #configuration key reg to enable write on the oscillator control reg
        bus.writeto_mem(ADDR, 0x1c, b'\x04')  # PWGT = 1
        if night:
            bus.writeto_mem(ADDR, 0x10, b'\x0F') # write 0x0F in reg 0x10 to enable all interrupt clear
        else:
            bus.writeto_mem(ADDR, 0x10, b'\x1F') # write 0x1F in reg 0x10 to enable all interrupt clear
        val = bus.readfrom_mem(ADDR, 0x0f, 1) # read 0x0f reg to clear interrupts
        bus.writeto_mem(ADDR, 0x17, b'\xC0')  # SLRES=1 nRST maintained at asserted value
        # now it should go in rtc-sleep with switch off of the processor. The code hereafter is for debug only
        time.sleep(500)
        val = bus.readfrom_mem(ADDR, 0x17, 1)
        val2 = bus.readfrom_mem(ADDR, 0x0f, 1)
        print(f'[{0x17:02x}] SLP {val.hex()} [{0x0f:02x}] STATUS {val2.hex()}')
        bus.writeto_mem(ADDR, 0x17, b'\xC0')  # SLRES=1 nRST maintained at asserted value
        time.sleep(500)
        val = bus.readfrom_mem(ADDR, 0x17, 1)
        val2 = bus.readfrom_mem(ADDR, 0x0f, 1)
        print(f'[{0x17:02x}] SLP {val.hex()} [{0x0f:02x}] STATUS {val2.hex()}')
        bus.writeto_mem(ADDR, 0x17, b'\xC0')  # SLRES=1 nRST maintained at asserted value
        time.sleep(500)
        val = bus.readfrom_mem(ADDR, 0x17, 1)
        val2 = bus.readfrom_mem(ADDR, 0x0f, 1)
        print(f'[{0x17:02x}] SLP {val.hex()} [{0x0f:02x}] STATUS {val2.hex()}')
        bus.writeto_mem(ADDR, 0x17, b'\xC0')  # SLRES=1 nRST maintained at asserted value
        time.sleep(500)
        val = bus.readfrom_mem(ADDR, 0x17, 1)
        val2 = bus.readfrom_mem(ADDR, 0x0f, 1)
        print(f'[{0x17:02x}] SLP {val.hex()} [{0x0f:02x}] STATUS {val2.hex()}')
        bus.writeto_mem(ADDR, 0x17, b'\xC0')  # SLRES=1 nRST maintained at asserted value
        time.sleep(500)
        val = bus.readfrom_mem(ADDR, 0x17, 1)
        val2 = bus.readfrom_mem(ADDR, 0x0f, 1)
        print(f'[{0x17:02x}] SLP {val.hex()} [{0x0f:02x}] STATUS {val2.hex()}')
        bus.writeto_mem(ADDR, 0x17, b'\xC0')  # SLRES=1 nRST maintained at asserted value
        time.sleep(500)
        val = bus.readfrom_mem(ADDR, 0x17, 1)
        val2 = bus.readfrom_mem(ADDR, 0x0f, 1)
        print(f'[{0x17:02x}] SLP {val.hex()} [{0x0f:02x}] STATUS {val2.hex()}')
        bus.writeto_mem(ADDR, 0x17, b'\xC0')  # SLRES=1 nRST maintained at asserted value
        time.sleep(500)
        val = bus.readfrom_mem(ADDR, 0x17, 1)
        val2 = bus.readfrom_mem(ADDR, 0x0f, 1)
        print(f'[{0x17:02x}] SLP {val.hex()} [{0x0f:02x}] STATUS {val2.hex()}')
        time.sleep(3)
        tempo = 0
        print(f"Error {tempo}")
        time.sleep(3)
        val = bus.readfrom_mem(ADDR, 0x17, 1)
        print(f'[{0x17:02x}] {val.hex()}')
        tempo=tempo+1
        print(f"Error {tempo}")
        time.sleep(3)
        val = bus.readfrom_mem(ADDR, 0x17, 1)
        print(f'[{0x17:02x}] {val.hex()}')
        tempo=tempo+1
        print(f"Error {tempo}")
    except Exception as e:
        print(f"    ERROR rtc_lib rtc_sleep() i2c error: ", e)


def wake_reason():
    try:
        time.sleep(0.001)
        return bus.readfrom_mem(ADDR, 0x0f, 1)
    except Exception as e:
        print("    ERROR rtc_lib wake_reason() i2c error: ", e)

def wake_pol_reason():
    try:
        time.sleep(0.001)
        return bus.readfrom_mem(ADDR, 0x3f, 1)
    except Exception as e:
        print("    ERROR rtc_lib wake_pol_reason() i2c error: ", e)

# AM18X5 Standard I2C address is 0x69
RTC_I2C_ADDR = 0x69

# Registers
REG_HUNDREDTHS     = 0x00
REG_SECONDS        = 0x01
REG_MINUTES        = 0x02
REG_HOURS          = 0x03
REG_DATE           = 0x04
REG_MONTH          = 0x05
REG_YEAR           = 0x06
REG_WEEKDAY        = 0x07

# Alarm Registers
REG_ALM_HUNDREDTHS = 0x08
REG_ALM_SECONDS    = 0x09
REG_ALM_MINUTES    = 0x0A
REG_ALM_HOURS      = 0x0B
REG_ALM_DATE       = 0x0C
REG_ALM_MONTH      = 0x0D
REG_ALM_WEEKDAY    = 0x0E

# Control & Status Registers
REG_STATUS         = 0x0F
REG_CTRL_1         = 0x10
REG_CTRL_2         = 0x11
REG_INT_MASK       = 0x12
REG_TIMER_CTRL     = 0x18

# Constants & Mask bits
CTRL_1_WRTC        = 0x01  # Write RTC bit (bit 0) - Must be set to write counter registers
INT_MASK_AIE       = 0x04  # Alarm Interrupt Enable bit (bit 2)

# Initialize I2C5 under Zephyr
# Make sure SCL and SDA have correct pull-ups as required by AM18X5
i2c = I2C(DEV)

def tm_to_epoch(tm):
    """
    Converts a time tuple (year, month, date, hour, minute, second)
    to epoch seconds (seconds since Jan 1, 2000).
    """
    year, month, day, hour, minute, second = tm[0], tm[1], tm[2], tm[3], tm[4], tm[5]

    # Days in each month (index 1 to 12)
    days_in_months = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # Helper to check if a year is a leap year
    def is_leap(y):
        return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)

    days = 0
    # Process years from 2000 up to target year
    for y in range(2000, year):
        days += 366 if is_leap(y) else 365

    # Process months of target year
    for m in range(1, month):
        if m == 2 and is_leap(year):
            days += 29
        else:
            days += days_in_months[m]

    # Add days, hours, minutes, and seconds
    days += (day - 1)
    total_seconds = (((days * 24 + hour) * 60) + minute) * 60 + second
    return total_seconds

def epoch_to_tm(epoch_sec):
    """
    Converts epoch seconds (since Jan 1, 2000) back to a time tuple
    (year, month, date, hour, minute, second).
    """
    # 946684800 is the Unix epoch offset for Year 2000 (Jan 1, 2000 is 0 in Y2K epoch)
    # We will compute relative to the year 2000
    days_in_months = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    def is_leap(y):
        return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)

    # Extract time of day
    seconds = epoch_sec % 60
    minutes_rem = epoch_sec // 60
    minute = minutes_rem % 60
    hours_rem = minutes_rem // 60
    hour = hours_rem % 24
    days = hours_rem // 24

    # Determine Year
    year = 2000
    while True:
        year_days = 366 if is_leap(year) else 365
        if days >= year_days:
            days -= year_days
            year += 1
        else:
            break

    # Determine Month and Day
    month = 1
    while True:
        dim = 29 if (month == 2 and is_leap(year)) else days_in_months[month]
        if days >= dim:
            days -= dim
            month += 1
        else:
            break
    day = days + 1

    return (year, month, day, hour, minute, seconds)

def bcd_to_dec(bcd):
    """Convert binary coded decimal (BCD) to decimal."""
    return (bcd_to_tens := (bcd >> 4) * 10) + (bcd & 0x0F)

def dec_to_bcd(dec):
    """Convert decimal to binary coded decimal (BCD)."""
    return ((dec // 10) << 4) | (dec % 10)

def rtc_write_reg(reg, value):
    """Writes a single byte value to a specified register."""
    i2c.writeto_mem(RTC_I2C_ADDR, reg, bytes([value]))

def rtc_read_reg(reg):
    """Reads a single byte value from a specified register."""
    return i2c.readfrom_mem(RTC_I2C_ADDR, reg, 1)[0]

def set_write_enable(enabled):
    """
    Enables/Disables writing to RTC registers using the WRTC (Write RTC) bit
    in Control Register 1. Required for modifying date/time counters.
    """
    current_ctrl = rtc_read_reg(REG_CTRL_1)
    if enabled:
        new_ctrl = current_ctrl | CTRL_1_WRTC
    else:
        new_ctrl = current_ctrl & ~CTRL_1_WRTC
    rtc_write_reg(REG_CTRL_1, new_ctrl)

def rtc_inspect():
    """
    Reads all configuration, control, status, interrupt, and oscillator registers
    of the Artasie-AM18X5, parses every bit, and prints them in a comprehensive,
    human-readable format referenced directly to the Ambiq Datasheet.
    """
    print("\n" + "="*80)
    print("                AMBIQ ARTASIE-AM18X5 RTC HARDWARE INSPECTION")
    print("="*80)

    # 1. Read block of key status, configuration, and control registers (0x0F to 0x20)
    # We will read 18 bytes starting from REG_STATUS (0x0F) up to REG_TRICKLE (0x20)
    try:
        reg_data = i2c.readfrom_mem(RTC_I2C_ADDR, 0x0F, 18)
    except Exception as e:
        print("    ERROR rtc_lib rtc_inspect()  i2c error: ", e)
        return

    # Helper mapping array offsets to registers
    # index 0: 0x0F (Status)
    # index 1: 0x10 (Control 1)
    # index 2: 0x11 (Control 2)
    # index 3: 0x12 (Interrupt Mask)
    # index 5: 0x14 (XT Calibration)
    # index 9: 0x18 (Timer Control)
    # index 12: 0x1B (Watchdog)
    # index 14: 0x1D (Oscillator Status)
    # index 17: 0x20 (Trickle Charger)

    # Also read Identity Register 0x28 separately
    try:
        chip_id = i2c.readfrom_mem(RTC_I2C_ADDR, 0x28, 1)[0]
    except:
        chip_id = 0x00

    # ==========================================================================
    # CHIP IDENTITY
    # ==========================================================================
    print(f"[{0x28:#04x}] IDENTITY REGISTER:")
    print(f"  * Core ID Code : {chip_id:#04x} (Expected: 0x18 for AM1805/15, 0x08 for AM0805/15)")
    print("-"*80)

    # ==========================================================================
    # 0x0F: STATUS REGISTER
    # ==========================================================================
    status = reg_data[0]
    print(f"[{0x0F:#04x}] STATUS REGISTER: {status:#010b} ({status:#04x})")
    print(f"  * [Bit 7] CB   (Century bit)             : {(status >> 7) & 1} (1 = Year overflowed from 99 to 00)")
    print(f"  * [Bit 6] BAT  (Battery Switch Flag)     : {(status >> 6) & 1} (1 = Device currently or previously powered by VBAT)")
    print(f"  * [Bit 5] WDT  (Watchdog Timer Flag)     : {(status >> 5) & 1} (1 = Watchdog timer met/expired)")
    print(f"  * [Bit 4] BL   (Battery Low Flag)        : {(status >> 4) & 1} (1 = VBAT dropped below analog threshold BREF)")
    print(f"  * [Bit 3] TIM  (Countdown Timer Flag)    : {(status >> 3) & 1} (1 = Countdown timer reached 0)")
    print(f"  * [Bit 2] ALM  (Alarm Match Flag)        : {(status >> 2) & 1} (1 = RTC counters matched programming target)")
    print(f"  * [Bit 1] EX2  (External Interrupt 2 WDI): {(status >> 1) & 1} (1 = Interrupt triggered on WDI pin)")
    print(f"  * [Bit 0] EX1  (External Interrupt 1 EXTI): {status & 1} (1 = Interrupt triggered on EXTI pin)")
    print("-"*80)

    # ==========================================================================
    # 0x10: CONTROL 1 REGISTER
    # ==========================================================================
    ctrl1 = reg_data[1]
    print(f"[{0x10:#04x}] CONTROL 1 REGISTER: {ctrl1:#010b} ({ctrl1:#04x})")
    print(f"  * [Bit 7] STOP   (Stop Clock Engine)     : {(ctrl1 >> 7) & 1} (1 = Counter clocking stopped; 0 = Normal clocking)")
    print(f"  * [Bit 6] 12/24  (Time Format Mode)      : {(ctrl1 >> 6) & 1} (1 = 12hr AM/PM mode; 0 = 24hr military mode)")
    print(f"  * [Bit 5] OUTB   (nIRQ2 Pin Static Value): {(ctrl1 >> 5) & 1} (Value on nIRQ2 pin when not configured as interrupt)")
    print(f"  * [Bit 4] OUT    (nIRQ Pin Static Value) : {(ctrl1 >> 4) & 1} (Value on nIRQ pin when not configured as interrupt)")
    print(f"  * [Bit 3] RSP    (nRST Pin Polarity)     : {(ctrl1 >> 3) & 1} (1 = Active high reset; 0 = Active low reset)")
    print(f"  * [Bit 2] ARST   (Auto Reset Enable)     : {(ctrl1 >> 2) & 1} (1 = Auto-clear control register interrupt indicators on read)")
    print(f"  * [Bit 1] PWR2   (nIRQ2 Pull-down En)    : {(ctrl1 >> 1) & 1} (1 = Enable weak pull-down on nIRQ2 pin)")
    print(f"  * [Bit 0] WRTC   (Write RTC Enable)      : {ctrl1 & 1} (1 = Counter modifications enabled; 0 = Counter locked/read-only)")
    print("-"*80)

    # ==========================================================================
    # 0x11: CONTROL 2 REGISTER
    # ==========================================================================
    ctrl2 = reg_data[2]
    out2s_modes = {
        0: "000: Standard nIRQ2 status mode (OUTB bit driven)",
        1: "001: Square-wave FOUT configuration",
        2: "010: Countdown Timer Output Pulse",
        3: "011: Alarm output pulse (250ms active-low trigger)",
        4: "100: Inverse configuration of Alarm output pulse",
        5: "101: Inverse of Countdown Timer Output Pulse",
        6: "110: Analog comparator relative status out",
        7: "111: Read/Write external dynamic RAM bank select (XADA)"
    }
    out2s = (ctrl2 >> 2) & 0x07
    print(f"[{0x11:#04x}] CONTROL 2 REGISTER: {ctrl2:#010b} ({ctrl2:#04x})")
    print(f"  * [Bits 4-2] OUT2S (nIRQ2 Signal Routing): {out2s_modes.get(out2s, 'Unknown Configuration')}")
    print(f"  * [Bits 1-0] OUT1S (nIRQ Signal Routing) : {ctrl2 & 0x03:02b} (00: nIRQ standard (OUT bit driven) | 01: FOUT clock | 10: Alarm pulse | 11: Main interrupt output)")
    print("-"*80)

    # ==========================================================================
    # 0x12: INTERRUPT MASK REGISTER
    # ==========================================================================
    intmask = reg_data[3]
    print(f"[{0x12:#04x}] INTERRUPT MASK REGISTER: {intmask:#010b} ({intmask:#04x})")
    print(f"  * [Bit 7] CEB  (Century Enable Flag)     : {(intmask >> 7) & 1} (1 = Set CB status bit on year overflow)")
    print(f"  * [Bits 6-5] IM (Interrupt Pulsed Modes) : {(intmask >> 5) & 0x03:02b} (00=Level mode, 01=3.8ms pulse, 10=15ms pulse, 11=Sec pulsed trigger)")
    print(f"  * [Bit 4] BLIE (Battery Low Interrupt En): {(intmask >> 4) & 1} (1 = Assert interrupt line when battery crosses BREF threshold)")
    print(f"  * [Bit 3] TIE  (Timer Interrupt Enable)  : {(intmask >> 2) & 1} (1 = Assert interrupt line when countdown timer reaches zero)")
    print(f"  * [Bit 2] AIE  (Alarm Interrupt Enable)  : {(intmask >> 2) & 1} (1 = Assert interrupt line on Alarm match target events)")
    print(f"  * [Bit 1] EX2E (EXT2 Interrupt Enable)   : {(intmask >> 1) & 1} (1 = Assert interrupt line on WDI input transition)")
    print(f"  * [Bit 0] EX1E (EXT1 Interrupt Enable)   : {intmask & 1} (1 = Assert interrupt line on EXTI input transition)")
    print("-"*80)

    # ==========================================================================
    # 0x14: OSCILLATOR CALIBRATION REGISTER
    # ==========================================================================
    calib = reg_data[5]
    print(f"[{0x14:#04x}] OSCILLATOR CALIBRATION REG: {calib:#010b} ({calib:#04x})")
    print(f"  * [Bit 7] CMDX   (Calibration Comm Type) : {(calib >> 7) & 1} (0 = Adjust calibration pulses, 1 = Auto-calibration clock select)")
    print(f"  * [Bits 6-0] OFSTX (Calibration Offset)  : BCD Offset value code = {calib & 0x7F} (Applies ± correction factor to matching source XT/RC clock)")
    print("-"*80)

    # ==========================================================================
    # 0x18: TIMER CONTROL REGISTER
    # ==========================================================================
    t_ctrl = reg_data[9]
    rpt_modes = {
        0: "000: Alarm Disabled",
        1: "001: Once per Year Match (Exact Month, Day, Hour, Min, Sec)",
        2: "010: Once per Month Match (Exact Day, Hour, Min, Sec)",
        3: "011: Once per Week Match (Exact Weekday, Hour, Min, Sec)",
        4: "100: Once per Day Match (Exact Hour, Min, Sec)",
        5: "101: Once per Hour Match (Exact Min, Sec)",
        6: "110: Once per Minute Match (Exact Sec)",
        7: "111: Once per Second Match (Exact Hundredths)"
    }
    rpt = (t_ctrl >> 2) & 0x07
    print(f"[{0x18:#04x}] TIMER CONTROL REGISTER: {t_ctrl:#010b} ({t_ctrl:#04x})")
    print(f"  * [Bit 7] TE     (Countdown Timer En)    : {(t_ctrl >> 7) & 1} (1 = Countdown timer logic active)")
    print(f"  * [Bits 6-5] TM  (Timer Interrupt Mode)  : {(t_ctrl >> 5) & 0x03:02b} (Controls routing output on system pin configurations)")
    print(f"  * [Bits 4-2] RPT (Alarm Repeat Code)     : {rpt_modes.get(rpt, 'Unknown configuration')}")
    print(f"  * [Bits 1-0] TFS (Countdown Timer Clock) : {t_ctrl & 0x03:02b} (00=1/256Hz, 01=64Hz, 10=1Hz, 11=1/60Hz (1 minute clock source))")
    print("-"*80)

    # ==========================================================================
    # 0x1B: WATCHDOG REGISTER
    # ==========================================================================
    wdt = reg_data[12]
    print(f"[{0x1B:#04x}] WATCHDOG REGISTER: {wdt:#010b} ({wdt:#04x})")
    print(f"  * [Bit 7] WDS  (Watchdog pin steering)   : {(wdt >> 7) & 1} (1 = Trigger reset pulse through nRST; 0 = Trigger pulse through nIRQ)")
    print(f"  * [Bits 6-2] BND (Watchdog match limit)  : {(wdt >> 2) & 0x1F} (Timeout value configured)")
    print(f"  * [Bits 1-0] WRB (Watchdog clock source) : {wdt & 0x03:02b} (00=Disabled, 01=1/16Hz (16s cycle), 10=1Hz (1s cycle), 11=1/4Hz (4s cycle))")
    print("-"*80)

    # ==========================================================================
    # 0x1D: OSCILLATOR STATUS REGISTER
    # ==========================================================================
    osc = reg_data[14]
    acal_modes = {
        0: "00: Disabled (No auto-calibration is active)",
        1: "01: Enabled, 1024 seconds calibration cycles (~17 minutes)",
        2: "10: Enabled, 512 seconds calibration cycles (~8.5 minutes)",
        3: "11: Enabled, XT autocalibration mode is managed by external trigger"
    }
    acal = (osc >> 5) & 0x03
    print(f"[{0x1D:#04x}] OSCILLATOR STATUS REGISTER: {osc:#010b} ({osc:#04x})")
    print(f"  * [Bit 7] OMD  (Oscillator Mode Control) : {(osc >> 7) & 1} (1 = External Crystal source active; 0 = RC Oscillator mode in use)")
    print(f"  * [Bit 6] LOMD (Locked-Osc mode indicator) : {(osc >> 6) & 1} (1 = Locked active crystal mode in place)")
    print(f"  * [Bits 5-4] ACAL (Auto-calibration En)  : {acal_modes.get(acal, 'N/A')}")
    print(f"  * [Bit 3] OF   (Oscillator Failure bit)  : {(osc >> 3) & 1} (1 = System clock stopped, reset to clear)")
    print(f"  * [Bit 2] ACFAIL (Auto-calibration fail) : {(osc >> 2) & 1} (1 = System failed tracking automated crystal calibrators)")
    print(f"  * [Bit 1] XSO  (Crystal Oscillator Status): {(osc >> 1) & 1} (1 = Crystal oscillator active and valid)")
    print(f"  * [Bit 0] OFIE (Osc Switchover Interrupt): {osc & 1} (1 = Generate hardware interrupt on dynamic clock source auto-switchover)")
    print("-"*80)

    # ==========================================================================
    # 0x20: TRICKLE CHARGER REGISTER
    # ==========================================================================
    trickle = reg_data[17]
    diode_options = "Standard Diode (0.6V Drop)" if (trickle & 0x0C) == 0x08 else "Schottky Diode (0.2V Drop)" if (trickle & 0x0C) == 0x04 else "Disabled"
    res_opts = {0: "No connection", 1: "3 kOhm Resistor", 2: "6 kOhm Resistor", 3: "11 kOhm Resistor"}
    resis = trickle & 0x03
    print(f"[{0x20:#04x}] TRICKLE CHARGER CONFIGURATION: {trickle:#010b} ({trickle:#04x})")
    print(f"  * Trickle Charger Power Path state       : {'ENABLED' if (trickle >> 4) == 0x0A else 'DISABLED'}")
    print(f"  * Power Path protection Diode type       : {diode_options}")
    print(f"  * Current-limiting Resistor path         : {res_opts.get(resis)}")
    print("="*80 + "\n")

# ==============================================================================
# 1) Set Calendar and Date
# ==============================================================================
def rtc_setDate(year, month, date, hour, minute, second, weekday=0):
    """
    Sets the calendar date and time.
    :param year: 2-digit year format (00-99 representing 2000-2099)
    :param month: 1-12
    :param date: 1-31 (Day of the month)
    :param hour: 0-23 (24h format default)
    :param minute: 0-59
    :param second: 0-59
    :param weekday: 0-6 (0=Sunday or customized)
    """
    try:
        set_write_enable(True)

    # Write the values sequentially or structure them to prevent roll-overs
        rtc_write_reg(REG_HUNDREDTHS, 0x00) # Reset hundredths
        rtc_write_reg(REG_SECONDS, dec_to_bcd(second))
        rtc_write_reg(REG_MINUTES, dec_to_bcd(minute))
        rtc_write_reg(REG_HOURS, dec_to_bcd(hour))
        rtc_write_reg(REG_DATE, dec_to_bcd(date))
        rtc_write_reg(REG_MONTH, dec_to_bcd(month))
        rtc_write_reg(REG_YEAR, dec_to_bcd(year % 100))
        rtc_write_reg(REG_WEEKDAY, dec_to_bcd(weekday))

        set_write_enable(False)
        print(f"RTC Date & Time Set: 20{year:02d}-{month:02d}-{date:02d} {hour:02d}:{minute:02d}:{second:02d}")
    except Exception as e:
        print("    ERROR rtc_lib rtc_setDate() i2c error: ", e)


# ==============================================================================
# 2) Retrieve RTC Calendar and Date
# ==============================================================================
def rtc_getDate():
    """
    Retrieves the RTC calendar and date.
    Returns: A dictionary representing the current calendar date.
    """
    try:
        # Read consecutive registers 0x00 through 0x07 in one block
        data = i2c.readfrom_mem(RTC_I2C_ADDR, REG_HUNDREDTHS, 8)

        seconds  = bcd_to_dec(data[1] & 0x7F)
        minutes  = bcd_to_dec(data[2] & 0x7F)
        hours    = bcd_to_dec(data[3] & 0x3F) # standard 24h mode mapping
        date     = bcd_to_dec(data[4] & 0x3F)
        month    = bcd_to_dec(data[5] & 0x1F)
        year     = bcd_to_dec(data[6]) + 2000
        weekday  = bcd_to_dec(data[7] & 0x07)

        # Return formatted date mappings
        time_info = {
            'year': year,
            'month': month,
            'date': date,
            'hour': hours,
            'minute': minutes,
            'second': seconds,
            'weekday': weekday
        }
    except Exception as e:
        print("    ERROR rtc_lib rtc_getDate() i2c error: ", e)
        time_info = {
            'year': 0,
            'month': 0,
            'date': 0,
            'hour': 0,
            'minute': 0,
            'second': 0,
            'weekday': 0
        }
    return time_info

# ==============================================================================
# 3) Program Alarm on a Future Date and Time
# ==============================================================================
def rtc_setAlarmDate(year, month, date, hour, minute, second):
    """
    Sets a singular static alarm at a precise future date and time coordinate.
    Also clears old alarm flags and activates the Alarm Interrupt Enable (AIE).
    """
    try:
        set_write_enable(True)

    # Configure precise matching levels in AM18X5 alarm registers
    # In AM18X5, writing matching BCD blocks to Alarm registers will cause a
    # match when the main counters match these register values.
        rtc_write_reg(REG_ALM_HUNDREDTHS, 0x00)
        rtc_write_reg(REG_ALM_SECONDS, dec_to_bcd(second))
        rtc_write_reg(REG_ALM_MINUTES, dec_to_bcd(minute))
        rtc_write_reg(REG_ALM_HOURS, dec_to_bcd(hour))
        rtc_write_reg(REG_ALM_DATE, dec_to_bcd(date))
        rtc_write_reg(REG_ALM_MONTH, dec_to_bcd(month))

    # Configure Timer Control (0x18) to trigger match once per year (or exact date match)
    # The default alarm repeating mode for precise matches requires setting internal RPT bits.
    # Setting alarm repetition mode (RPT) configuration to match up to Month/Date/Hour/Min/Sec:
    # Set RPT = 1 (match Month, Day, Hour, Min, Sec and hundredths)
        curr_timer_ctrl = rtc_read_reg(REG_TIMER_CTRL)
    # RPT bits are typically bits 5:2 in register 0x18. Setting RPT = 0x01 (Alarm once per year)
        new_timer_ctrl = (curr_timer_ctrl & 0xE3) | (0x01 << 2)
        rtc_write_reg(REG_TIMER_CTRL, new_timer_ctrl)

    # Clear any stale alarm flags in the Status register (0x0F)
        status_reg = rtc_read_reg(REG_STATUS)
        rtc_write_reg(REG_STATUS, status_reg & ~0x04) # Write 0 to clear ALM bit (bit 2)

    # Enable Alarm Interrupt Enable (AIE) inside the Interrupt Mask register (0x12)
#    int_mask = rtc_read_reg(REG_INT_MASK)
#    rtc_write_reg(REG_INT_MASK, int_mask | INT_MASK_AIE)

        set_write_enable(False)
        print(f"Alarm successfully programmed for: 20{year:02d}-{month:02d}-{date:02d} {hour:02d}:{minute:02d}:{second:02d}")
    except Exception as e:
        print("    ERROR rtc_lib rtc_setAlarmDate() i2c error: ", e)

# ==============================================================================
# 4) Program Alarm from N Seconds from Now
# ==============================================================================
def rtc_setAlarmTime(seconds_from_now):
    """
    Sets an alarm relative to the current platform clock 'X' seconds in the future.
    """
    # 1. Retrieve current RTC datetime state
    now = rtc_getDate()

    # Pack values into tuple
    time_tuple = (now['year'], now['month'], now['date'], now['hour'], now['minute'], now['second'])

    # 2. Add relative target delta using custom conversion
    current_epoch = tm_to_epoch(time_tuple)
    alarm_epoch = current_epoch + seconds_from_now # to compensate for the switch off and boot time

    # Convert seconds back to tuple
    alarm_tuple = epoch_to_tm(alarm_epoch)

    # Extract calculated future offsets
    alarm_year   = alarm_tuple[0]
    alarm_month  = alarm_tuple[1]
    alarm_date   = alarm_tuple[2]
    alarm_hour   = alarm_tuple[3]
    alarm_minute = alarm_tuple[4]
    alarm_sec    = alarm_tuple[5]

    # 3. Apply coordinates to static Alarm sequence caller
    rtc_setAlarmDate(alarm_year, alarm_month, alarm_date, alarm_hour, alarm_minute, alarm_sec)
# ==============================================================================
# Verification Loop / Test
# ==============================================================================
if __name__ == '__main__':
    # Set current time to July 20, 2026, 14:30:00 (Monday = 1)
#    rtc_setDate(year=26, month=7, date=20, hour=14, minute=30, second=0, weekday=1)

    # Allow 1 second clock pulse
#    time.sleep(1)

    # Check updated date
#    current_time = rtc_getDate()
#    print("Now retrieved from RTC: {year:04d}-{month:02d}-{date:02d} {hour:02d}:{minute:02d}:{second:02d} (Weekday: {weekday})".format(**current_time))

    # Program alarm to trigger 15 seconds from now
    print("rtc_lib: Nightsleep for 20s")
    time.sleep(2)
    rtc_setAlarmTime(20)
#    rtc_setAlarmDate(2026, 7, 20, 13, 40, 10)

    print(f"rtc_sleep with: NightSleep: {NightSleep}, BatIntSleep: {BatIntSleep}, BpolSleep: {BpolSleep}")
    rtc_sleep(NightSleep, BatIntSleep, BpolSleep, AlarmSleep)
