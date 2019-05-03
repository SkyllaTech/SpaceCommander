#! /usr/bin/env python3

from generated.python.spacecommands import Device

device = Device('/dev/ttyUSB0')

device.ping()

print(device.echo('a'.encode('ascii')))

print(device.times2(1040))

print(device.sqrt(2))
