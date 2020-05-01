import RPi.GPIO as GPIO
import time
import sys
from hx711 import HX711
import subprocess
from flask import Flask
#setup GPIO Pins
GPIO.setmode(GPIO.BCM)         #Set GPIO pin numbering
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Enable input and pull up resistors

#Raspberry Pi pin configuration:
RST = None
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0
lKeg = 0.0
#create the scale objects, hx is right and hx1 is left and configure the measurement options
hx = HX711(5, 6)
hx1 = HX711(23,24)
hx.set_reading_format("LSB", "MSB")
hx1.set_reading_format("LSB", "MSB")
rKeg = 0
lKeg = 0

#cleanup gpio
def cleanAndExit():
    print ("Cleaning...")
    GPIO.cleanup()
    print ("Bye!")
    sys.exit()

def scaleConfig():
    #set the refence unit for both scales
    hx.set_reference_unit(-27)
    hx.reset()
    hx.tare()
    hx1.set_reference_unit(-27)
    hx1.reset()
    hx1.tare()
    #cleanAndExit()

def currentKegVol():
    global rKeg
    global lKeg
    #grab the current weight
    val = hx.get_weight(1)
    val1 = hx1.get_weight(1)
    hx.power_down()
    hx.power_up()
    hx1.power_down()
    hx1.power_up()
    #calculate the percent of beer left
    #left keg
    new_val1 = val1 - 3960
    lKeg = float(100*new_val1)/17360
    lKeg = int(round(lKeg))
    #right keg
    new_val = val - 3960
    rKeg = float(100*new_val)/17360
    rKeg = int(round(rKeg))
    #display 0 if keg is empty or reporting less than 0
    if lKeg <= 0:
        lKeg = 0
    if rKeg <= 0:
        rKeg = 0
    #cleanAndExit()

main_page = """
<!DOCTYPE html>
<html>
<body>

<h2>Jalbert's Keezer</h2>
    <a href="/refresh"><input type="button" value="Refresh"></a>
    <a href="/calibrate"><input type="button" value="Calibrate"></a> 
    

 
</body>
</html>
"""
app = Flask(__name__)

@app.route('/')
def index():
    return main_page

@app.route('/calibrate')
def calibrate():
    scaleConfig()
    print("Calibrated")
    return main_page

@app.route('/refresh')
def currentVolume():
    currentKegVol()
    curr = "<table><tr><th>Left Keg:</th><th>Right Keg:</th></tr><tr><td>Pumpkin</td><td>IPA</td></tr><tr><td>"+str(lKeg)+"</td><td>"+str(rKeg)+"</td></tr></table>"
    return main_page + curr


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
















