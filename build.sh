#!/bin/bash

cd $(dirname $0)
BASE=`pwd`

EXTRA_CFLAGS="-DCONFIG_MICROPY_CONFIG_ROM_LEVEL_EXTRA_FEATURES"

exec ./west.sh build -b apollo3_evb \
    $BASE/micropython/ports/zephyr/ \
    --extra-conf thread.conf \
    --extra-conf $BASE/evernode.conf \
    --extra-dtc-overlay $BASE/evernode.overlay \
    -DEXTRA_CFLAGS="$EXTRA_CFLAGS" \
    -DUSER_C_MODULES=${BASE}/modules/ \
    $*
