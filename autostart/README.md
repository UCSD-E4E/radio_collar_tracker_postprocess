# Operation

The autostart module should accomplish the following:
* When the switch is moved to the "on" position, execute the `~/xcode/run` script.
* Monitor the output of the `~/xcode/run` script to ensure that the collarTracker program is running correctly.
* When the switch is moved to the "off" position, send `SIGTERM` to the `~/xcode/run` script.
* Enable multiple runs without rebooting the system.

# Configuring the autostart code

To configure the autostart code, place the file `rctstart.sh` in the `/etc/init.d/` directory.  In the directory `/home/debian`, make the file `autostart`.

# Pinout:
PWR -> 3.3V

LED ->

SW1	->

GND	->
