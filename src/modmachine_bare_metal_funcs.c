#if MICROPY_PY_MACHINE_BARE_METAL_FUNCS

#include "py/runtime.h"
#include <zephyr/device.h>
#include <zephyr/drivers/uart.h>
#include <zephyr/drivers/pinctrl.h>
#include <zephyr/pm/pm.h>
#include <zephyr/pm/device.h>
#include <soc.h>

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
    // Check if no argument is provided
    if (n_args == 0) {
        mp_raise_ValueError(MP_ERROR_TEXT("value must be provided"));
    }
    mp_int_t milliseconds = mp_obj_get_int(args[0]);

    const struct device *console = DEVICE_DT_GET(DT_CHOSEN(zephyr_console));
    if (console != NULL) {
        pm_device_busy_clear(console);
        pm_device_action_run(console, PM_DEVICE_ACTION_SUSPEND);
    }

    // Reset the semaphore before sleeping to ensure clean state
    k_sem_reset(&lightsleep_wake_sem);

    // Use semaphore with timeout instead of k_sleep to allow GPIO wake
    k_sem_take(&lightsleep_wake_sem, K_MSEC(milliseconds));

    if (console != NULL) {
        pm_device_action_run(console, PM_DEVICE_ACTION_RESUME);
        pm_device_busy_set(console);
    }
}

MP_NORETURN void mp_machine_deepsleep(size_t n_args, const mp_obj_t *args) {
    mp_raise_NotImplementedError(MP_ERROR_TEXT("machine.deepsleep not implemented"));
    for(;;){
        // no return
    }
}

#endif // MICROPY_PY_MACHINE_BARE_METAL_FUNCS
