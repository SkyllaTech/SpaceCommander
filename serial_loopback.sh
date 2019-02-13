#!/bin/bash

set -e
set -x

socat -d -d pty,raw,echo=0 pty,raw,echo=0
