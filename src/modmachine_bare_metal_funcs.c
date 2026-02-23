#if MICROPY_PY_MACHINE_BARE_METAL_FUNCS

#include "py/runtime.h"
#include <zephyr/device.h>
#include <zephyr/drivers/uart.h>
#include <zephyr/drivers/pinctrl.h>
#include <zephyr/pm/device.h>
#include <soc.h>

// lifted from zephyr/drivers/serial/uart_pl011_ambiq.h
#include "uart_pl011_registers.h"
typedef struct {
    bool bValid;
    uint32_t regILPR;
    uint32_t regIBRD;
    uint32_t regFBRD;
    uint32_t regLCRH;
    uint32_t regCR;
    uint32_t regIFLS;
    uint32_t regIER;
} uart_register_state_t;
static uart_register_state_t sRegState[AM_REG_UART_NUM_MODULES];

static int uart_ambiq_pm_action(const struct device *dev, enum pm_device_action action)
{
    int key;

    /*Uart module number*/
    uint32_t ui32Module = ((uint32_t)get_uart(dev) == UART0_BASE) ? 0 : 1;

    /*Uart Power module*/
    am_hal_pwrctrl_periph_e eUARTPowerModule =
        ((am_hal_pwrctrl_periph_e)(AM_HAL_PWRCTRL_PERIPH_UART0 + ui32Module));

    /*Uart register status*/
    uart_register_state_t *pRegisterStatus = &sRegState[ui32Module];

    /* Decode the requested power state and update UART operation accordingly.*/
    switch (action) {

    /* Turn on the UART. */
    case PM_DEVICE_ACTION_RESUME:

        /* Make sure we don't try to restore an invalid state.*/
        if (!pRegisterStatus->bValid) {
            return -EPERM;
        }

        /*The resume and suspend actions may be executed back-to-back,
         * so we add a busy wait here for stabilization.
         */
        k_busy_wait(100);

        /* Enable power control.*/
        am_hal_pwrctrl_periph_enable(eUARTPowerModule);

        /* Restore UART registers*/
        key = irq_lock();

        UARTn(ui32Module)->ILPR = pRegisterStatus->regILPR;
        UARTn(ui32Module)->IBRD = pRegisterStatus->regIBRD;
        UARTn(ui32Module)->FBRD = pRegisterStatus->regFBRD;
        UARTn(ui32Module)->LCRH = pRegisterStatus->regLCRH;
        UARTn(ui32Module)->CR = pRegisterStatus->regCR;
        UARTn(ui32Module)->IFLS = pRegisterStatus->regIFLS;
        UARTn(ui32Module)->IER = pRegisterStatus->regIER;
        pRegisterStatus->bValid = false;

        irq_unlock(key);

        return 0;
    case PM_DEVICE_ACTION_SUSPEND:

        while ((get_uart(dev)->fr & PL011_FR_BUSY) != 0) {
        }

        /* Preserve UART registers*/
        key = irq_lock();

        pRegisterStatus->regILPR = UARTn(ui32Module)->ILPR;
        pRegisterStatus->regIBRD = UARTn(ui32Module)->IBRD;
        pRegisterStatus->regFBRD = UARTn(ui32Module)->FBRD;
        pRegisterStatus->regLCRH = UARTn(ui32Module)->LCRH;
        pRegisterStatus->regCR = UARTn(ui32Module)->CR;
        pRegisterStatus->regIFLS = UARTn(ui32Module)->IFLS;
        pRegisterStatus->regIER = UARTn(ui32Module)->IER;
        pRegisterStatus->bValid = true;

        irq_unlock(key);

        /* Clear all interrupts before sleeping as having a pending UART
         * interrupt burns power.
         */
        UARTn(ui32Module)->IEC = 0xFFFFFFFF;

        /* If the user is going to sleep, certain bits of the CR register
         * need to be 0 to be low power and have the UART shut off.
         * Since the user either wishes to retain state which takes place
         * above or the user does not wish to retain state, it is acceptable
         * to set the entire CR register to 0.
         */
        UARTn(ui32Module)->CR = 0;

        /* Disable power control.*/
        am_hal_pwrctrl_periph_disable(eUARTPowerModule);
        return 0;
    default:
        return -ENOTSUP;
    }
}
// <--

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

    uint32_t status, enabled;
    for(am_hal_pwrctrl_periph_e i=1; i<AM_HAL_PWRCTRL_PERIPH_MAX; i++) {
        status = am_hal_pwrctrl_periph_enabled(i, &enabled);
        printf("Periph %d: status=%08x, enabled=%d\n", i, status, enabled);
    }

    uint32_t timers = am_hal_stimer_int_enable_get();
    am_hal_stimer_int_disable(timers);
    am_hal_stimer_int_clear(timers);

    const struct device *dev = DEVICE_DT_GET(DT_CHOSEN(zephyr_console));
    if (dev == NULL) {
        mp_raise_OSError(ENOENT);
        // ignored
        return;
    }
    int err = uart_ambiq_pm_action(dev, PM_DEVICE_ACTION_SUSPEND);
    if (err != AM_HAL_STATUS_SUCCESS) {
        printf("ERROR: cannot set console to sleep (status=%d)\n", err);
        return;
    }

    // configure powerdown / retain
    am_hal_pwrctrl_memory_deepsleep_powerdown(AM_HAL_PWRCTRL_MEM_CACHE);
    am_hal_pwrctrl_memory_deepsleep_powerdown(AM_HAL_PWRCTRL_MEM_FLASH_MAX);
    am_hal_pwrctrl_memory_deepsleep_powerdown(AM_HAL_PWRCTRL_MEM_SRAM_MAX);
    am_hal_pwrctrl_memory_deepsleep_retain(AM_HAL_PWRCTRL_MEM_SRAM_MAX);
    // deep sleep
    am_hal_sysctrl_sleep(AM_HAL_SYSCTRL_SLEEP_DEEP);

    err = uart_ambiq_pm_action(dev, PM_DEVICE_ACTION_RESUME);
    if (err != AM_HAL_STATUS_SUCCESS) {
        printf("ERROR: cannot restore console from sleep (status=%d)\n", err);
        return;
    }

    am_hal_stimer_int_enable(timers);
}

MP_NORETURN void mp_machine_deepsleep(size_t n_args, const mp_obj_t *args) {
    mp_raise_NotImplementedError(MP_ERROR_TEXT("machine.deepsleep not implemented"));
    for(;;){
        // no return
    }
}

#endif // MICROPY_PY_MACHINE_BARE_METAL_FUNCS
