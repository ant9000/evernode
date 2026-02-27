// Include MicroPython API.
#include "py/runtime.h"

#include <zephyr/device.h>
#include <zephyr/pm/device.h>
#include <zephyr/pm/device_runtime.h>
#include "zephyr_device.h"

static mp_obj_t zephyr_pm_pm_toggle(mp_obj_t name) {
    const struct device *dev = zephyr_device_find(name);
    enum pm_device_state pm_state;
    int retval;

    if (dev == NULL) {
        mp_raise_ValueError(MP_ERROR_TEXT("unknown device"));
        return mp_obj_new_int(-ENODEV);
    }

    if (!pm_device_runtime_is_enabled(dev)) {
        mp_raise_ValueError(MP_ERROR_TEXT("device does not have runtime power management"));
        return mp_obj_new_int(-ENOTSUP);
    }

    (void)pm_device_state_get(dev, &pm_state);

    if (pm_state == PM_DEVICE_STATE_ACTIVE) {
        retval = pm_device_runtime_put(dev);
    } else {
        retval = pm_device_runtime_get(dev);
    }

    return mp_obj_new_int(retval);
}
static MP_DEFINE_CONST_FUN_OBJ_1(zephyr_pm_pm_toggle_obj, zephyr_pm_pm_toggle);

static const mp_rom_map_elem_t zephyr_pm_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_zephyr_pm) },
    { MP_ROM_QSTR(MP_QSTR_pm_toggle), MP_ROM_PTR(&zephyr_pm_pm_toggle_obj) },
};
static MP_DEFINE_CONST_DICT(zephyr_pm_globals, zephyr_pm_globals_table);

const mp_obj_module_t zephyr_pm = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t *)&zephyr_pm_globals,
};

MP_REGISTER_MODULE(MP_QSTR_zephyr_pm, zephyr_pm);
