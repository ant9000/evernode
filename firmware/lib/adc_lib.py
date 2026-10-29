# adc_lib.py
from machine import ADC, Pin, mem32
from zephyr_pm import *
import time

def adc_read_values():
	GPIO47  = Pin(("gpio32_63", 15), Pin.OUT)  # EN-IO
	pm_busy_set("adc0")
	time.sleep(0.1)
	Vpanel = ADC(("adc0", 6))
	Vcap = ADC(("adc0", 7))
	numMeas = 50
	myDelay = 0.0001
	
	try:
		Vpanel_curr = 0
		Vcap_curr = 0
		GPIO47.on()  # activate EN-IO
		time.sleep(0.102) # need stabilization of voltages when switching on EN-IO
		for i in range(numMeas):
			Vpanel_curr += (Vpanel.read_uv()-3000) # offset compensation
			Vcap_curr += (Vcap.read_uv()-3000)     # offset compensation
			time.sleep(myDelay)
		time.sleep(0.1)
			
		Vpanel_val = Vpanel_curr/(numMeas*333) # linearity compensation
		Vcap_val = Vcap_curr/(numMeas*333)     # linearity compensation
		GPIO47.off()  # deactivate EN-IO
		pm_busy_clear("adc0")
		return Vpanel_val, Vcap_val
	except Exception as e:
		GPIO47.off()  # deactivate EN-IO
		print("adc_lib adc_read_values() Error: ", e)
		return None, None

if __name__ == '__main__':
    Vp, Vc = adc_read_values()
    print ("adc6 (VPanel) = {:.0f}; adc7 (VCap) = {:.0f}".format(Vp, Vc))
    time.sleep(1)
