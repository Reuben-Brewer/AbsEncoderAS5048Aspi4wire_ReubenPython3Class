###########################

AbsEncoderAS5048Aspi4wire_ReubenPython3Class__RaspberryPi

Code to read angles from the Absolute Magnetic Rotary Encoder AMS 5048A over 4-wire-SPI
connected directly to a Raspberry Pi 4B.

https://ams.com/en/as5048a, Digikey PN's: AS5048A-AB-1.0-ND and AS5048A-EK-AB-STM1.1-ND

Reuben Brewer, Ph.D.

reuben.brewer@gmail.com

www.reubotics.com

Apache 2 License

Software Revision C, 10/19/2024

Verified working on:

Python 3.12.

Windows 10, 11 64-bit

Raspberry Pi Buster

Notes:

1. In Raspberry Pi, the only python module that successfully worked with the AS5048A 4-wire-SPI was "SPI-Py" (https://github.com/lthiery/SPI-Py).

The standard "spidev" DID NOT WORK. There are some software modules for GPIO-bit-banging to be an SPI Slave, but haven't tried them:

https://www.raspberrypi.org/forums/viewtopic.php?t=230392

https://www.raspberrypi.org/forums/viewtopic.php?t=250788

SOMEONE HAS IMPLEMENTED A GPIO-SPI-SLAVE-MODE FOR PI:

https://github.com/anetczuk/SpiSlave

2. If using the standard drivers/pins, the Raspberry Pi can ONLY BE SPI-MASTER (NOT SLAVE)
(https://www.raspberrypi.org/forums/viewtopic.php?t=230392 and https://www.raspberrypi.org/forums/viewtopic.php?t=250788)

3. Although some people claim to have 3-wire-SPI working in Raspberry Pi, I could only get 4-wire working.

###########################

########################### Python module installation instructions, all OS's

AbsEncoderAS5048Aspi4wire_ReubenPython3Class__RaspberryPi.py, ListOfModuleDependencies_All:['spi']

###########################
