/*
#include <string.h>
#include <stdio.h>
#include "py/mpconfig.h"
#include "py/mphal.h"
#include "py/obj.h"
#include "modmachine.h"
*/

#if MICROPY_PY_MACHINE_BARE_METAL_FUNCS

#include "py/runtime.h"
#include "am_mcu_apollo.h"

mp_obj_t mp_machine_unique_id(void) {
    uint64_t chip_id;
    am_hal_mcuctrl_device_t sDevice;
    am_hal_mcuctrl_info_get(AM_HAL_MCUCTRL_INFO_DEVICEID, &sDevice);
    chip_id = ((uint64_t)sDevice.ui32ChipID0 << 32) + sDevice.ui32ChipID1;
    return mp_obj_new_bytes((byte *)&chip_id, 64);
}

mp_obj_t mp_machine_get_freq(void) {
    am_hal_clkgen_status_t sClkGenStatus;
    am_hal_clkgen_status_get(&sClkGenStatus);
    mp_obj_t tuple[] = {
        mp_obj_new_int(sClkGenStatus.ui32SysclkFreq),
    };
    return mp_obj_new_tuple(MP_ARRAY_SIZE(tuple), tuple);
}

void mp_machine_set_freq(size_t n_args, const mp_obj_t *args) {
    mp_raise_NotImplementedError(MP_ERROR_TEXT("machine.freq set not supported"));
}

void mp_machine_lightsleep(size_t n_args, const mp_obj_t *args) {
//  NVIC_DisableIRQ(UART0_IRQn);
    NVIC_DisableIRQ(STIMER_CMPR0_IRQn);
    NVIC_DisableIRQ(STIMER_CMPR1_IRQn);
    // configure powerdown / retain
    am_hal_pwrctrl_memory_deepsleep_powerdown(AM_HAL_PWRCTRL_MEM_CACHE);
    am_hal_pwrctrl_memory_deepsleep_powerdown(AM_HAL_PWRCTRL_MEM_FLASH_MAX);
    am_hal_pwrctrl_memory_deepsleep_powerdown(AM_HAL_PWRCTRL_MEM_SRAM_MAX);
    am_hal_pwrctrl_memory_deepsleep_retain(AM_HAL_PWRCTRL_MEM_SRAM_MAX);
    // deep sleep
    am_hal_sysctrl_sleep(AM_HAL_SYSCTRL_SLEEP_DEEP);
    // restore interrupts
//  NVIC_EnableIRQ(UART0_IRQn);
    NVIC_EnableIRQ(STIMER_CMPR0_IRQn);
    NVIC_EnableIRQ(STIMER_CMPR1_IRQn);
}

MP_NORETURN void mp_machine_deepsleep(size_t n_args, const mp_obj_t *args) {
    mp_raise_NotImplementedError(MP_ERROR_TEXT("machine.deepsleep not implemented"));
    for(;;){
        // no return
    }
}

#endif // MICROPY_PY_MACHINE_BARE_METAL_FUNCS
