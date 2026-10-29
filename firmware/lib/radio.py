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
                    lora_cfg=lora_cfg,
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

    def __del__(self):
        self.sleep()
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
