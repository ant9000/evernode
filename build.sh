#!/bin/bash

cd $(dirname $0)
BASE=`pwd`

EXTRA_CFLAGS="-DMICROPY_CONFIG_ROM_LEVEL=MICROPY_CONFIG_ROM_LEVEL_EXTRA_FEATURES"
EXTRA_CFLAGS="$EXTRA_CFLAGS -DMICROPY_PY_MACHINE_DISABLE_IRQ_ENABLE_IRQ=1"

exec ./west.sh build -b apollo3_evb \
    $BASE/micropython/ports/zephyr/ \
    --extra-conf thread.conf \
    --extra-conf $BASE/evernode.conf \
    --extra-dtc-overlay $BASE/evernode.overlay \
    -DEXTRA_CFLAGS="$EXTRA_CFLAGS" \
    -DUSER_C_MODULES=${BASE}/modules/ \
    $*
