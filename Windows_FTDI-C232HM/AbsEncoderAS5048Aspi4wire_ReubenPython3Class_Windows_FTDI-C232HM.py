# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision C, 10/19/2024

Verified working on: Python 3.12 for Windows 10, 11 64-bit.
'''

'''
Pinout:
"C232HM" = FTDI USB to MPSSE Serial Cable (either C232-HM-DDHSL-0 for 3.3V-VCC or C232HM-EDHSL-0 for 5V-VCC)

C232HM Pin 1 (Red), VCC/5V <==> AS5048 5V
C232HM Pin 2 (Orange), TCK (SPI Clock) <==> AS5048 SCK
C232HM Pin 3 (Yellow), TDO (SPI Data Output) <==> AS5048 MOSI
C232HM Pin 4 (Green), TDI (SPI Data Input) <==> AS5048 MISO
C232HM Pin 5 (Brown), TDI (SPI Data Chip Select) <==> AS5048 CSn
C232HM Pin 10 (Black), GND <==> AS5048 GND
'''

'''
Useful Links:

Discussion of parity bit: https://electronics.stackexchange.com/questions/349216/why-bother-with-even-parity

https://eblot.github.io/pyftdi/installation.html
https://eblot.github.io/pyftdi/api/spi.html

Example communication with a remote SPI device using full-duplex mode

SOMEONE HAD A SIMILAR PROBLEM
https://community.st.com/s/question/0D50X00009XkfHYSAZ/possible-hardware-bug-full-duplex-spi-incorrectly-reads-last-bit-of-each-incoming-byte

SIMILAR PROBLEM 2
https://forum.micropython.org/viewtopic.php?t=3045
'''

##########################################
import os
import sys
import time
import keyboard
import traceback
##########################################

##########################################
#pip install pyftdi. Home-page: http://github.com/eblot/pyftdi, as of 10/19/24 currently at Version: 0.55.4
from pyftdi.ftdi import Ftdi
from pyftdi.spi import *
from pyftdi.usbtools import *
##########################################

##########################################
import platform
if platform.system() == "Windows":
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
##########################################

##########################################################################################################
##########################################################################################################
def ExitProgram_Callback(OptionalArugment = 0):
    global EXIT_PROGRAM_FLAG

    print("ExitProgram_Callback event fired!")

    EXIT_PROGRAM_FLAG = 1
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def InitializeSPI():

    global SPI_Object
    global SPI_Slave
    global FTDI_USBmpsseConverterSerialNumber

    try:
        ##########################################################################################################
        # Instantiate a SPI controller. We need want to use A*BUS4 for /CS,
        # so at least 2 /CS lines should be reserved for SPI, the remaining IO are available as GPIOs.
        SPI_Object = SpiController(cs_count=2)
        ##########################################################################################################

        ##########################################################################################################
        MyUSBtools = UsbTools()

        LocatedUSB = MyUSBtools.find_all([[0x0403, 0x6014]]) #Using libusb-win32: USB\VID_0403&PID_6014\FT0NF9GG
        print("LocatedUSB: " + str(LocatedUSB))
        ##########################################################################################################

        ##########################################################################################################
        '''
        Configure the first interface (IF/1) of the FTDI device as a SPI master
        URL scheme: https://eblot.github.io/pyftdi/urlscheme.html
        ftdi://[vendor[:product[:index|:serial]]]/interface,
        '''

        SPI_Object.configure("ftdi://ftdi:232h:" + FTDI_USBmpsseConverterSerialNumber + "/1") #"e.g. "ftdi://ftdi:232h:FT0NF9GG/1"
        ##########################################################################################################

        ##########################################################################################################
        '''
        Get a port to a SPI slave w/ /CS on A*BUS4 and SPI mode 0 @ 10MHz
        
        FTDI hardware does not support cpha=1 (mode 1 and mode 3). As stated in Application Node 114:
        “It is recommended that designers review the SPI Slave data sheet to determine the SPI mode implementation.
        FTDI device can only support mode 0 and mode 2 due to the limitation of MPSSE engine.”
    
        SPI sample tests expect:
                MX25L1606E device on /CS 0, SPI mode 0
                ADXL345 device on /CS 1, SPI mode 2
                RFDA2125 device on /CS 2, SPI mode 0
        '''

        SPI_Slave = SPI_Object.get_port(cs=0, freq=1953000, mode=0) #10e6
        ##########################################################################################################

    except:
        exceptions = sys.exc_info()[0]
        print("InitializeSPI, exceptions: %s" % exceptions)
        traceback.print_exc()

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ReadSPI(PrintDebuggingFlag = 0):

    try:
        global SPI_Object
        global SPI_Slave
        global AngleFloatDegrees

        ##########################################################################################################
        '''
        #DROPTAIL = 1 MAKES IT GO FULL-RANGE (INSTEAD OF STOPPING AT 180), BUT THE ANGLE DOESN'T MATCH THE PI
        #(WITH THE STATOR TAPED TO THE ROTOR, THE PI SAID IT WAS 335DEG, AND C232HM SAYS 347.5DEEG)
        #ONCE YOU CHANGE DROPTAIL, YOU HAVE TO POWER-CYCLE THE USB CHIP TO CHANGE THE DROPTAIL VALUE
        '''

        AngleBytes = SPI_Slave.exchange(SPI_WriteBuffer, readlen=2, start=True, stop=True, duplex=True, droptail=0) #For 4-Wire-SPI
        ##########################################################################################################

        ##########################################################################################################
        AngleByte_MSB = AngleBytes[0]
        AngleByte_LSB = AngleBytes[1]

        '''
        The data are sent and read with MSB first.
        All of the LSB bits are used, and the lower 6-bits of the MSB are used (so have to remove the 16th and 15th bits). 
        The values seem-off by exactly a factor of 2 (no idea why), so we're multiplying by 2 below. 
        '''

        AngleInt = 2.0*( ( (AngleByte_MSB & 0b00111111) << 8) | (AngleByte_LSB & 0b11111111) )  #0x3F = 0b00111111, & 0x3FFF.

        AngleFloatDegrees = 360.0 * (AngleInt / 16383.0)  # 0x3FFF = 16383 = 2^14-1 = max value
        ##########################################################################################################

        ##########################################################################################################
        if PrintDebuggingFlag == 1:
            print("LoopCounter: " + str(LoopCounter) + \
                  #", Rx-Bytes: " + str(AngleBytes) + \
                  ", Rx-Byte Low: " + str(AngleByte_LSB) + \
                  ", Rx-Byte High: " + str(AngleByte_MSB) + \
                  ", INT: " + str(AngleInt) + \
                  ", DEG: " + str(AngleFloatDegrees))
        ##########################################################################################################

    except:
        exceptions = sys.exc_info()[0]
        print("ReadSPI, exceptions: %s" % exceptions)
        traceback.print_exc()

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
if __name__ == '__main__':

    global EXIT_PROGRAM_FLAG
    EXIT_PROGRAM_FLAG = 0

    global AngleFloatDegrees
    AngleFloatDegrees = -11111.0

    ##########################################################################################################
    global SPI_Object
    global SPI_Slave

    global SPI_WriteBuffer
    SPI_WriteBuffer = [0xFF, 0xFF]
    ##########################################################################################################

    ##########################################################################################################
    keyboard.on_press_key("esc", ExitProgram_Callback)
    keyboard.on_press_key("q", ExitProgram_Callback)
    ##########################################################################################################

    ##########################################################################################################
    global FTDI_USBmpsseConverterSerialNumber
    FTDI_USBmpsseConverterSerialNumber = "FT0NF9GG" #Unicorn, change this to your unique device!

    InitializeSPI()
    ##########################################################################################################

    ##########################################################################################################
    LoopCounter = 0
    while(EXIT_PROGRAM_FLAG == 0):

        ReadSPI(PrintDebuggingFlag=1)

        LoopCounter = LoopCounter + 1
        time.sleep(0.030)
    ##########################################################################################################

##########################################################################################################
##########################################################################################################