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

cmd=$1
if [ -z "$cmd" ]; then
  exec west --help
fi
shift

exec west $cmd -d $TARGET $*
