#!/bin/bash

cd $(dirname $0)
BASE=`pwd`
TARGET=${BASE}/build

which west || {
  echo "West command not found - please activate Zephyr environment"
  exit 1
}

cd $(dirname $(which west))
cd $(west topdir)

EXTRA_CFLAGS="-DMICROPY_CONFIG_ROM_LEVEL=MICROPY_CONFIG_ROM_LEVEL_EXTRA_FEATURES"
EXTRA_CFLAGS="${EXTRA_CFLAGS} -DMICROPY_PY_MACHINE_BARE_METAL_FUNCS=1"
EXTRA_CFLAGS="${EXTRA_CFLAGS} -DMICROPY_PY_MACHINE_BOARD_INCLUDEFILE=\\\"${BASE}/src/modmachine_bare_metal_funcs.c\\\""

west build -b apollo3_evb \
    -d $TARGET \
    $BASE/micropython/ports/zephyr/ \
    -DEXTRA_CONF_FILE=thread.conf \
    -DEXTRA_CONF_FILE=$BASE/evernode.conf \
    -DEXTRA_DTC_OVERLAY_FILE=$BASE/evernode.overlay \
    -DEXTRA_CFLAGS="$EXTRA_CFLAGS" \
    $*
