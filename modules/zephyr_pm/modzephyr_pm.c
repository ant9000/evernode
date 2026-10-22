// Include MicroPython API.
#include "py/runtime.h"

#include <zephyr/device.h>
#include <zephyr/pm/device.h>
#include <zephyr/pm/device_runtime.h>
#include "zephyr_device.h"

static mp_obj_t zephyr_pm_pm_suspend(mp_obj_t name) {
    const struct device *dev = zephyr_device_find(name);
    int retval;

    if (dev == NULL) {
        mp_raise_ValueError(MP_ERROR_TEXT("unknown device"));
        return mp_obj_new_int(-ENODEV);
    }

    bool busy = pm_device_is_busy(dev);
    if (!busy) {
        retval = pm_device_action_run(dev, PM_DEVICE_ACTION_SUSPEND);
    } else {
        retval = -EBUSY;
    }

    return mp_obj_new_int(retval);
}
static MP_DEFINE_CONST_FUN_OBJ_1(zephyr_pm_pm_suspend_obj, zephyr_pm_pm_suspend);

static mp_obj_t zephyr_pm_pm_resume(mp_obj_t name) {
    const struct device *dev = zephyr_device_find(name);
    int retval;

    if (dev == NULL) {
        mp_raise_ValueError(MP_ERROR_TEXT("unknown device"));
        return mp_obj_new_int(-ENODEV);
    }

    retval = pm_device_action_run(dev, PM_DEVICE_ACTION_RESUME);

    return mp_obj_new_int(retval);
}
static MP_DEFINE_CONST_FUN_OBJ_1(zephyr_pm_pm_resume_obj, zephyr_pm_pm_resume);

static mp_obj_t zephyr_pm_pm_busy_set(mp_obj_t name) {
    const struct device *dev = zephyr_device_find(name);

    if (dev == NULL) {
        mp_raise_ValueError(MP_ERROR_TEXT("unknown device"));
        return mp_obj_new_int(-ENODEV);
    }

    pm_device_busy_set(dev);
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(zephyr_pm_pm_busy_set_obj, zephyr_pm_pm_busy_set);

static mp_obj_t zephyr_pm_pm_busy_clear(mp_obj_t name) {
    const struct device *dev = zephyr_device_find(name);

    if (dev == NULL) {
        mp_raise_ValueError(MP_ERROR_TEXT("unknown device"));
        return mp_obj_new_int(-ENODEV);
    }

    pm_device_busy_clear(dev);
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(zephyr_pm_pm_busy_clear_obj, zephyr_pm_pm_busy_clear);

static mp_obj_t zephyr_pm_pm_is_busy(mp_obj_t name) {
    const struct device *dev = zephyr_device_find(name);
    bool busy;

    if (dev == NULL) {
        mp_raise_ValueError(MP_ERROR_TEXT("unknown device"));
        return mp_obj_new_int(-ENODEV);
    }

    busy = pm_device_is_busy(dev);
    return mp_obj_new_bool(busy);
}
static MP_DEFINE_CONST_FUN_OBJ_1(zephyr_pm_pm_is_busy_obj, zephyr_pm_pm_is_busy);

static const mp_rom_map_elem_t zephyr_pm_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_zephyr_pm) },
    { MP_ROM_QSTR(MP_QSTR_pm_suspend), MP_ROM_PTR(&zephyr_pm_pm_suspend_obj) },
    { MP_ROM_QSTR(MP_QSTR_pm_resume), MP_ROM_PTR(&zephyr_pm_pm_resume_obj) },
    { MP_ROM_QSTR(MP_QSTR_pm_busy_set), MP_ROM_PTR(&zephyr_pm_pm_busy_set_obj) },
    { MP_ROM_QSTR(MP_QSTR_pm_busy_clear), MP_ROM_PTR(&zephyr_pm_pm_busy_clear_obj) },
    { MP_ROM_QSTR(MP_QSTR_pm_is_busy), MP_ROM_PTR(&zephyr_pm_pm_is_busy_obj) },
};
static MP_DEFINE_CONST_DICT(zephyr_pm_globals, zephyr_pm_globals_table);

const mp_obj_module_t zephyr_pm = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t *)&zephyr_pm_globals,
};

MP_REGISTER_MODULE(MP_QSTR_zephyr_pm, zephyr_pm);
