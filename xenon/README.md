# Particle Xenon code
This is a collection of lighting experiments using a handful of Xenon's which were converted to use CircuitPython.

I followed these instructions to convert a Xenon

 1. Purchased a Particle Debugger https://store.particle.io/products/particle-debugger
 2. Download the Particle Workbench https://www.particle.io/workbench/
 3. Downloaded the Xenon boot loader https://github.com/adafruit/Adafruit_nRF52_Bootloader/releases/download/0.4.0/particle_xenon_bootloader-0.4.0.zip
 4. Download the latest CircuitPython (6.1.0) uf2 loader: https://circuitpython.org/board/particle_xenon/
 5. Connect the debugger and Xenon to USB ports on the laptop
 6. Run the openocd tool from the Workbench directory to burn in the bootloader
```
   bin/openocd -f interface/cmsis-dap.cfg -f target/nrf52-particle.cfg \
	-c "adapter_khz 1000" \
	-c "init" \
	-c "program /Users/mthomas/Dev/particle_xenon_bootloader-0.4.0_s140_6.1.1.hex 0x000000 verify reset" \
	-c "exit"
```
 7. Copy in the CircuitPython u2f file to the /Volumes/XENON drive, reset
 8. Download the CircuitPython bundle from here: https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/download/20210127/adafruit-circuitpython-bundle-6.x-mpy-20210127.zip
 9. Copy the following libs into the /Volumes/CIRCUITPY/lib directory
	1. neopixel.mpy
	2. adafruit_ble
	3. adafruit_bluefruit_connect
 10. Copy the code.py code into /Volumes/CIRCUITPY/ directory
 11. Connect to the USB terminal of the Xenon 
```
screen /dev/tty.usbmodem143101
```
 12. Download the Bluefruit Connect App for your phone
 13. Connect to the Xenon e.g. "CIRCUITPY8917"

## Related Materials
These were the materials used to create the set of steps above

 1. [Using CircuitPython with a Particle Xenon](https://docs.particle.io/tutorials/learn-more/xenon-circuit-python/)

