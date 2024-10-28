###########################

AbsEncoderAS5048Aspi4wire_ReubenTeensy

Code to read angles from the Absolute Magnetic Rotary Encoder AMS 5048A over 4-wire-SPI
connected to a Teensy 3.2 or 4.1.

https://ams.com/en/as5048a, Digikey PN's: AS5048A-AB-1.0-ND and AS5048A-EK-AB-STM1.1-ND

Reuben Brewer, Ph.D.

reuben.brewer@gmail.com

www.reubotics.com

Apache 2 License

Software Revision D, 10/27/2024

Verified working on:

Teensy 3.2 and 4.1.

1. Although some people claim to have 3-wire-SPI working, I could only get 4-wire working.

2. To receive the angular data from the Teensy, you must connect it to a computer via an
FTDI TTL-232RG-VREG3V3-WE cable and run "test_program_for_SerialJSONstreamer_ReubenPython3Class.py"

###########################
