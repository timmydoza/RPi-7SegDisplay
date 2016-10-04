# RPi_7SegDisplay

RPi_7SegDisplay is a python package for displaying messages on an eight-digit seven-segment display connected to a Raspberry Pi.  

## Installation
`pip install RPi_7SegDisplay`

RPi_7SegDisplay depends upon the RPi.GPIO library, which should already be installed if you are using Raspbian.

## Usage
Note: RPi_7SegDisplay accepts BCM numbers when initializing the GPIO pins.  See: https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/#pin-numbering
```
import RPi_7SegDisplay as display

data_pin=2
clock_pin=3
latch_pin=4

display.init(data_pin, clock_pin, latch_pin)

display.show('12345678')
```
