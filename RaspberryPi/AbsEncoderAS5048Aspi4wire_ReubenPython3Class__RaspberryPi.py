'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision C, 10/19/2024

Verified working on: Python 3.12 for Raspberry Pi Buster.
'''

##########################################
import os
import sys
import time
import traceback
import spi #https://github.com/lthiery/SPI-Py
##########################################

'''
Official Rpi documentation of SPI: https://www.raspberrypi.org/documentation/hardware/raspberrypi/spi/README.md

Operating in 4-wire mode: 
https://pinout.xyz/pinout/spi
RPi Pin 4 (5V) to AS5048 5V, currently using a red wire
RPi Pin 6 (GND) to AS5048 GND, currently using a black wire
RPi Pin 19 (SPI0 MOSI) to AS5048 MOSI, currently using a yellow wire with black stripes
RPi Pin 21 (SPI0 MISO) to AS5048 MISO, currently using a yellow wire
RPi Pin 23 (SPIO SCLK) to AS5048 SCK, currently using a blue wire
RPi Pin 24 (SPI0 CE0) to AS5048 CSn, currently using a green wire

To list all spi ports: "ls -l /dev/spidev*"
http://abyz.me.uk/rpi/pigpio/piscope.html
wget abyz.me.uk/rpi/pigpio/piscope.tar
tar xvf piscope.tar
cd PISCOPE
make hf
make install
To run: "piscope &"

To show loaded modules: cat /etc/modules   https://www.raspberrypi.org/forums/viewtopic.php?t=74463
In /dev, you'll see spidev0.0 and spidev0.1

To check if SPI modules are loaded: lsmod | grep "spi"

To check is SPI is enabled, go to /boot/config.txt and check for the line dtparam=spi=on
'''

##########################################################################################################
##########################################################################################################
##########################################################################################################
if __name__ == '__main__':

	print("AbsEncoderAS5048Aspi4wire_ReubenPython3Class__RaspberryPi.py")

	##########################################################################################################
	##########################################################################################################
	try:

    	device_0 =  spi.openSPI(device="/dev/spidev0.0",mode=1,speed=1953000) #SPI device 0 using the CE0 pin for chip select
		data_out = (0xFF, 0xFF)

		LoopCounter = 0
		##########################################################################################################
		while True:
			LoopCounter = LoopCounter + 1

			AngleBytes = spi.transfer(device_0, data_out)
			AngleByte_MSB = AngleBytes[0]
			AngleByte_LSB = AngleBytes[1]

			# The data are sent and read with MSB first.
			# Have to remove the 16th and 15th bits. All of the LSB bits are used, the lower 6-bits of the MSB are used.
			AngleInt = (((AngleByte_MSB & 0b00111111) << 8) | (AngleByte_LSB & 0b11111111))  # 0x3F = 0b00111111, & 0x3FFF.
			#AngleInt = ((AngleByte_MSB << 8) | AngleByte_LSB) & 0x3FFF
			
			AngleFloatDegrees = 360.0*(AngleInt/16383.0) #0x3FFF = 16383 = 2^14-1 = max value
			print("LoopCounter: " + str(LoopCounter) + \
			", Rx-Bytes: " + str(AngleBytes) + \
			", INT: " + str(AngleInt) + \
			", DEG: " + str(AngleFloatDegrees))

		    time.sleep(0.030)

		##########################################################################################################

	##########################################################################################################
	##########################################################################################################

	##########################################################################################################
	##########################################################################################################
	except:
		exceptions = sys.exc_info()[0]
		print("AbsEncoderAS5048Aspi4wire_ReubenPython3Class__RaspberryPi.py, exceptions: %s" % exceptions)
		traceback.print_exc()

	##########################################################################################################
	##########################################################################################################

	##########################################################################################################
	##########################################################################################################
	spi.closeSPI(device_0)
	print(AbsEncoderAS5048Aspi4wire_ReubenPython3Class__RaspberryPi)
	##########################################################################################################
	##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################