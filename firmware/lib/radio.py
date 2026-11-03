from machine import Pin, SPI
import zephyr_pm, time
from lora import AsyncSX1262

class Radio(AsyncSX1262):
    def __init__(self, lora_cfg):
        pinset = {
                'busy':       Pin(("gpio0_31", 16)),
                'reset':      Pin(("gpio0_31", 17)),
                'chipselect': Pin(("gpio0_31", 11)),
                'dio':        Pin(("gpio0_31", 15)),
                'rf_switch':  Pin(("gpio0_31", 18), Pin.OUT),
                'power':      Pin(("gpio32_63", 14), Pin.OUT),
        }
        self.pinset = pinset

        pinset['power'](0)
        pinset['reset'](0)
        time.sleep_ms(5)
        pinset['reset'](1)
        time.sleep_ms(10)
        zephyr_pm.pm_resume("spi1")

        class EvernodeAntennaSwitch:
            def tx(self, tx_arg):
                pinset['rf_switch'].on()
            def rx(self):
                pinset['rf_switch'].on()
            def idle(self):
                pinset['rf_switch'].off()

        spi = SPI("spi1", baudrate=10_000_000, polarity=0, phase=0)
        ant_sw = EvernodeAntennaSwitch()
        error = None
        for i in range(3):
            try:
                error = None
                super().__init__(
                    spi=spi,
                    cs=pinset["chipselect"],
                    busy=pinset["busy"],
                    dio1=pinset["dio"],
                    reset=pinset["reset"],
                    dio3_tcxo_millivolts=1800,
                    dio3_tcxo_start_time_us=2000,
                    ant_sw=ant_sw,
                )
                break
            except Exception as e:
                error = e
        if error:
            raise error

        # use DC-DC instead of LDO
        self._cmd("BB", 0x96, 0x01)
        # set PA ramp value to 200 us
        self._ramp_val = 0x04
        self.configure(lora_cfg)

    def _get_pa_tx_params(self, output_power, tx_ant):
        # Given an output power level in dB, return a 2-tuple:
        # - First item is the 3 arguments for SetPaConfig command
        # - Second item is the power level argument value for SetTxParams command.
        #
        # DS 13.1.14.1 "PA Optimal Settings" gives optimally efficient
        # values for output power +22, +20, +17, +14 dBm and "these changes make
        # the use of nominal power either sub-optimal or unachievable" (hence it
        # recommends setting +22dBm nominal TX Power for all these).
        #
        # However the modem supports output power as low as -9dBm, and there's
        # no explanation in the datasheet of how to best set other output power
        # levels.
        #
        # Semtech's own driver (sx126x.c in LoRaMac-node) only ever executes
        # SetPaConfig with the values shown in the datasheet for +22dBm, and
        # then executes SetTxParams with power set to the nominal value in
        # dBm.
        #
        # If the caller requests an "Optimal" value, use the datasheet values.
        # Otherwise use the nearest optimal choice.
        output_power = min(max(int(output_power), -9), 22)

        DEFAULT = (0x4, 0x7, 0x0, 0x1)
        OPTIMAL = {
            22: (DEFAULT, 22),
            20: ((0x3, 0x5, 0x0, 0x1), 22),
            17: ((0x2, 0x3, 0x0, 0x1), 22),
            14: ((0x2, 0x2, 0x0, 0x1), 22),
        }
        if output_power in OPTIMAL:
            # Datasheet optimal values
            return OPTIMAL[output_power]
        else:
            pa_level = 22  # default
            for level in sorted(OPTIMAL.keys()):
                if output_power <= level:
                    pa_level = level
                    break
            return (OPTIMAL[pa_level][0], output_power & 0xFF)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.off()

    def off(self):
        try:
            self.sleep()
        except:
            pass
        zephyr_pm.pm_busy_clear("spi1")
        zephyr_pm.pm_suspend("spi1")
        for key in self.pinset:
            if key != 'power':
                self.pinset[key].init(0)
        self.pinset['power'](1)

    def sleep(self):
        error = None
        for i in range(3):
            try:
                error = None
                super().sleep()
                break
            except Exception as e:
                error = e
        if error:
            raise error
