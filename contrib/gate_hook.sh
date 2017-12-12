#!/usr/bin/env bash

set -ex

GATE_DEST=$BASE/new
DEVSTACK_PATH=$GATE_DEST/devstack

$BASE/new/devstack-gate/devstack-vm-gate.sh
