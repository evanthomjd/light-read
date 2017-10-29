#!/usr/bin/python
import smbus
import time
 
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

THRESHOLD_VALUE = 100
CONSECUTIVE_READS = 10
CONSECUTIVE_THRESHOLD_CLEAR = 3


#bus = smbus.SMBus(0) # Rev 1 Pi uses 0
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1
 
def convertToNumber(data):
    # Simple function to convert 2 bytes of data
    # into a decimal number
    return ((data[1] + (256 * data[0])) / 1.2)
 
def readLight(addr=DEVICE):
    data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_1)
    return convertToNumber(data)
 
def main():
    sum_over_threshold = 0.0
    values_over_threshold = 0.0
    under_threshold = 0

    while True:
        light_val = readLight()
        print 'light value ', light_val
        if light_val > THRESHOLD_VALUE:
            under_threshold = 0
            sum_over_threshold += light_val
            values_over_threshold += 1.0
            if values_over_threshold == CONSECUTIVE_READS:
                print 'read values over threshold with average ', (sum_over_threshold/values_over_threshold) 
                sum_over_threshold = 0.0
                values_over_threshold = 0.0
        else:
            under_threshold += 1
            if under_threshold == CONSECUTIVE_THRESHOLD_CLEAR:
                sum_over_threshold = 0.0
                values_over_threshold = 0.0 
        time.sleep(0.130)
   
if __name__=="__main__":
    main()
