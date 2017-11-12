#!/usr/bin/python
import smbus
import time
import serial 
import struct

 
DEVICE     = 0x23 
 
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_1 = 0x20

THRESHOLD_VALUE = 500
CONSECUTIVE_READS = 10
CONSECUTIVE_THRESHOLD_CLEAR = 3
MAX_DOSAGE = 240.0


bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

#Converts 2 bytes into decimal 
def convertToNumber(data):
    return ((data[1] + (256 * data[0])) / 1.2)

#Reads ambient light values from sensor 
def readLight(addr=DEVICE):
    data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_1)
    return convertToNumber(data)

#Sends an dosage via the Serial bus based on the given value.
#Checks that the dosage for the value, is available to give. 
def send_dosage(val, dosage_left):
    result = 0
    dosage = lux_to_dosage(val)
    if (dosage_left - dosage) > 0:
        result = send_val(dosage)
        if result < 0:
            print 'Meds Now empty, reset!'
    else:
        print 'Desired Dosage is %s and remaining doesage is %s. Cannot send dosage, reset!' % (dosage, dosage_left)
    return result

#Sends a value as a string to the serial BUS 
def send_val(val):
    ser = serial.Serial('/dev/ttyACM0', 9600)
    ser.write(str(val))
    response_val = ser.readline()
    ser.close()
    return float(response_val)

#Converst lux values to dosage
def lux_to_dosage(lux):
    if lux >= 500 and lux < 1000:
        return 30
    elif lux >= 1000 and lux < 1500:
        return 60
    elif lux >= 1500 and lux < 2000:
        return 90
    else: 
        return 120

#Main loop: Reads light values from the sensor
#If the the value if greater than a configured max it is added to an average
#Once 10 semi-consecutive values greater than such a max are seen, a dosage is administered.
def main():
    dosage_left = MAX_DOSAGE
    sum_over_threshold = 0.0
    values_over_threshold = 0.0
    under_threshold = 0

    while True:
        light_val = readLight()
        if light_val > THRESHOLD_VALUE:
            under_threshold = 0
            sum_over_threshold += light_val
            values_over_threshold += 1.0
            if values_over_threshold == CONSECUTIVE_READS:
                avg = sum_over_threshold/values_over_threshold
                print 'read values over threshold with average ', avg
                dosage_left = send_dosage(avg, dosage_left)
                sum_over_threshold = 0.0
                values_over_threshold = 0.0
        else:
            under_threshold += 1
            if under_threshold == CONSECUTIVE_THRESHOLD_CLEAR:
                sum_over_threshold = 0.0
                values_over_threshold = 0.0 
        #Sensor takes about 120ms to read, so we sleep for 130ms to be safe 
        time.sleep(0.130)
   
if __name__=="__main__":
    main()
