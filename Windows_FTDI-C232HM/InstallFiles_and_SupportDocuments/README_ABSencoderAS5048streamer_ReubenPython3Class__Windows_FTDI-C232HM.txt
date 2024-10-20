###########################

AbsEncoderAS5048Aspi4wire_ReubenPython3Class__Windows_FTDI-C232HM

Code to read angles from the Absolute Magnetic Rotary Encoder AMS 5048A over 4-wire-SPI
via the FTDI USB to MPSSE Serial Cable (either C232-HM-DDHSL-0 for 3.3V-VCC or C232HM-EDHSL-0 for 5V-VCC).

https://ams.com/en/as5048a, Digikey PN's: AS5048A-AB-1.0-ND and AS5048A-EK-AB-STM1.1-ND

https://ftdichip.com/products/c232hm-ddhsl-0-2/

Reuben Brewer, Ph.D.

reuben.brewer@gmail.com

www.reubotics.com

Apache 2 License

Software Revision C, 10/19/2024

Verified working on:

Python 3.12.

Windows 10, 11 64-bit

Notes:

1. In Windows (with the FTDI USB to MPSSE Serial Cable), the only python module that successfully worked with the AS5048A (in 4-wire-SPI mode) was the "pyftdi" module.
However, this required switching to the libusb-win32 driver, and no-matter-what, the values seem off by an exact factor of 2 (not sure why, multiplied by 2 to correct this).
Failed to get the AS5048A working following "https://iosoft.blog/2018/12/05/ftdi-python-part-3/" with "ftd2xx", "pylibftdi".
Failed to get the AS5048A working following "https://stackoverflow.com/questions/58477347/ftdi-libmpsse-spi" with "ftd2xx".

2. In Windows, the default driver for the FTDI USB to MPSSE Serial Cable does not work with this code.
Instead, Zadig (https://zadig.akeo.ie/) must be used to replace the default driver with the libusb-32 driver (https://sourceforge.net/projects/libusb-win32/).
Please see the screenshots "Driver_OriginalBroken.png" and "Driver_AfterReplacingDriverWithLIBUSB-WIN32_Working.png".

3. FTDI USB to MPSSE Serial Cable (either C232-HM-DDHSL-0 for 3.3V-VCC or C232HM-EDHSL-0 for 5V-VCC)
can ONLY BE SPI-MASTER (NOT SLAVE).

4. I could only get 4-wire-SPI working, not 3-wire SPI.

###########################

########################### Python module installation instructions, all OS's

AbsEncoderAS5048Aspi4wire_ReubenPython3Class_Windows_FTDI-C232HM.py, ListOfModuleDependencies_All:['keyboard', 'pyftdi.ftdi', 'pyftdi.spi', 'pyftdi.usbtools']

pip install pyftdi #Home-page: http://github.com/eblot/pyftdi, as of 10/19/24 currently at Version: 0.55.4

###########################
