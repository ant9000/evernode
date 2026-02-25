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

west build -b apollo3_evb \
    -d $TARGET \
    $BASE/micropython/ports/zephyr/ \
    --extra-conf thread.conf \
    --extra-conf $BASE/evernode.conf \
    --extra-dtc-overlay $BASE/evernode.overlay \
    -DEXTRA_CFLAGS="$EXTRA_CFLAGS" \
    $*
