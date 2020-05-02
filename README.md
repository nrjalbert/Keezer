RPi Keezer Project
---
This project added 2 bathroom scales for measuring volume of corny kegs. <br>
The amounts are displayed on python flask web page. <br>
The web page allows the scales to calculate the tare weight for accurate measurement.

Requirements:<br>
Raspberry Pi<br>
2x HX711 load cell amplifier<br>
2x Bathroom scales<br>
Ethernet cable<br>
Soldering iron<br>
Various jumper wires<br>

I used the ethernet cable to run the wires from the 2 scales into the GPIO connections.  4 wires for each scale connected to the load cell going into the GPIO.

The scales are wired using a wheatstone bridge going into the HX711 load cell, see diagrams included.

Note-the scales are not directly on the bottom of the chest freezer to preserve the electronics.

Great resource: https://tutorials-raspberrypi.com/digital-raspberry-pi-scale-weight-sensor-hx711/
