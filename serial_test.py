#!/usr/bin/python
import smbus
import time
import serial 
import struct

# Define some constants from the datasheet
 
DEVICE     = 0x23 # Default device I2C address
 
POWER_DOWN = 0x00 # No active state
POWER_ON   = 0x01 # Power on
RESET      = 0x07 # Reset data register value
 
# Start measurement at 4lx resolution. Time typically 16ms.
CONTINUOUS_LOW_RES_MODE = 0x13
# Start measurement at 1lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_1 = 0x10
# Start measurement at 0.5lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_2 = 0x11
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_1 = 0x20
# Start measurement at 0.5lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_2 = 0x21
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_LOW_RES_MODE = 0x23

THRESHOLD_VALUE = 500
CONSECUTIVE_READS = 10
CONSECUTIVE_THRESHOLD_CLEAR = 3
MAX_DOSAGE = 240.0


#bus = smbus.SMBus(0) # Rev 1 Pi uses 0
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

 
def convertToNumber(data):
    # Simple function to convert 2 bytes of data
    # into a decimal number
    return ((data[1] + (256 * data[0])) / 1.2)
 
def readLight(addr=DEVICE):
    data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_1)
    return convertToNumber(data)


def send_dosage(val, dosage_left):
    result = 0
    dosage = lux_to_dosage(val)
    if (dosage_left - dosage) > 0:
        result = send_val(dosage)
        if result < 0:
            print 'Meds Now empty, reset!'
    else:
        print 'Desired Dosage is %s and remaining doesage is %s. Cannot send dosage, reset!' % (dosage, dosage_left)

def send_val(val):
    ser = serial.Serial('/dev/ttyACM0', 9600)
    ser.write(str(val))
    print 'sending ', val
    response_val = ser.readline()
    print 'read ', response_val
    ser.close()
    return float(response_val)



print 'send with response ', send_val(120)
