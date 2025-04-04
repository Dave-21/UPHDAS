# MIT License
# 
# Original author: Zoltan Szarvas
# https://github.com/szazo/DHT11_Python
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


#!/usr/bin/python3
import time
import sys
import RPi.GPIO as GPIO
import get_config as gc
import error_Handler as ERR

# DHTxx sensor result returned by DHT.read() method'
class DHTResult:
    

    ERR_NO_ERROR = 0
    ERR_MISSING_DATA = 1
    ERR_CRC = 2
    ERR_NOT_FOUND = 3

    error_code = ERR_NO_ERROR
    temperature = -1
    humidity = -1     

    def __init__(self, error_code, temperature, humidity):
        self.error_code = error_code
        self.temperature = temperature
        self.humidity = humidity
                                

    def is_valid(self):
        return self.error_code == DHTResult.ERR_NO_ERROR
        
    
    
# DHTxx sensor reader class for Raspberry'
class DHT:
    
    __pin = 0
    __isDht11 = True

    def __init__(self, pin, isDht11):
        self.__pin = pin
        self.__isDht11 = isDht11

    def read(self):
        GPIO.setup(self.__pin, GPIO.OUT)

        # send initial high
        self.__send_and_sleep(GPIO.HIGH, 0.05)

        # pull down to low
        self.__send_and_sleep(GPIO.LOW, 0.02)

        # change to input using pull up
        GPIO.setup(self.__pin, GPIO.IN, GPIO.PUD_UP)

        # collect data into an array
        data = self.__collect_input()

        # parse lengths of all data pull up periods
        pull_up_lengths = self.__parse_data_pull_up_lengths(data)
        
        if len(pull_up_lengths) == 0:
            return DHTResult(DHTResult.ERR_NOT_FOUND, 0, 0)

        # if bit count mismatch, return error (4 byte data + 1 byte checksum)
        if len(pull_up_lengths) != 40:
            return DHTResult(DHTResult.ERR_MISSING_DATA, 0, 0)

        # calculate bits from lengths of the pull up periods
        bits = self.__calculate_bits(pull_up_lengths)

        # we have the bits, calculate bytes
        the_bytes = self.__bits_to_bytes(bits)

        # calculate checksum and check
        checksum = self.__calculate_checksum(the_bytes)
        if the_bytes[4] != checksum:
            return DHTResult(DHTResult.ERR_CRC, 0, 0)

        # ok, we have valid data
        # The meaning of the return sensor values
        # the_bytes[0]: humidity int
        # the_bytes[1]: humidity decimal
        # the_bytes[2]: temperature int
        # the_bytes[3]: temperature decimal
        temperature = -1
        humidity = -1
        if(self.__isDht11):
            # DHT11
            temperature = the_bytes[2] + float(the_bytes[3]) / 10
            humidity = the_bytes[0] + float(the_bytes[1]) / 10
        else:
            #DHT22
            temperature = (the_bytes[2] * 256 + float(the_bytes[3])) / 10
            humidity = (the_bytes[0] * 256 + float(the_bytes[1])) / 10
            c = (float)(((the_bytes[2]&0x7F)<< 8)+the_bytes[3])/10
            
            if ( c > 125 ):
                c = the_bytes[2]
                
            if (the_bytes[2] & 0x80):
                c = -c;
            
            temperature = c
            humidity = ((the_bytes[0]<<8)+the_bytes[1])/10.00

        return DHTResult(DHTResult.ERR_NO_ERROR, temperature, humidity)
                                                          

    def __send_and_sleep(self, output, sleep):
        GPIO.output(self.__pin, output)
        time.sleep(sleep)

    def __collect_input(self):
        # collect the data while unchanged found
        unchanged_count = 0

        # this is used to determine where is the end of the data
        max_unchanged_count = 100

        last = -1
        data = []
        while True:
            current = GPIO.input(self.__pin)
            data.append(current)
            if last != current:
                unchanged_count = 0
                last = current
            else:
                unchanged_count += 1
                if unchanged_count > max_unchanged_count:
                    break

        return data

    def __parse_data_pull_up_lengths(self, data):
        STATE_INIT_PULL_DOWN = 1
        STATE_INIT_PULL_UP = 2
        STATE_DATA_FIRST_PULL_DOWN = 3
        STATE_DATA_PULL_UP = 4
        STATE_DATA_PULL_DOWN = 5

        state = STATE_INIT_PULL_DOWN

        lengths = [] # will contain the lengths of data pull up periods
        current_length = 0 # will contain the length of the previous period

        for i in range(len(data)):

            current = data[i]
            current_length += 1

            if state == STATE_INIT_PULL_DOWN:
                if current == GPIO.LOW:
                    # ok, we got the initial pull down
                    state = STATE_INIT_PULL_UP
                    continue
                else:
                    continue
            if state == STATE_INIT_PULL_UP:
                if current == GPIO.HIGH:
                    # ok, we got the initial pull up
                    state = STATE_DATA_FIRST_PULL_DOWN
                    continue
                else:
                    continue
            if state == STATE_DATA_FIRST_PULL_DOWN:
                if current == GPIO.LOW:
                    # we have the initial pull down, the next will be the data pull up
                    state = STATE_DATA_PULL_UP
                    continue
                else:
                    continue
            if state == STATE_DATA_PULL_UP:
                if current == GPIO.HIGH:
                    # data pulled up, the length of this pull up will determine whether it is 0 or 1
                    current_length = 0
                    state = STATE_DATA_PULL_DOWN
                    continue
                else:
                    continue
            if state == STATE_DATA_PULL_DOWN:
                if current == GPIO.LOW:
                    # pulled down, we store the length of the previous pull up period
                    lengths.append(current_length)
                    state = STATE_DATA_PULL_UP
                    continue
                else:
                    continue

        return lengths

    def __calculate_bits(self, pull_up_lengths):
        # find shortest and longest period
        shortest_pull_up = 1000
        longest_pull_up = 0

        for i in range(0, len(pull_up_lengths)):
            length = pull_up_lengths[i]
            if length < shortest_pull_up:
                shortest_pull_up = length
            if length > longest_pull_up:
                longest_pull_up = length

        # use the halfway to determine whether the period it is long or short
        halfway = shortest_pull_up + (longest_pull_up - shortest_pull_up) / 2
        bits = []

        for i in range(0, len(pull_up_lengths)):
            bit = False
            if pull_up_lengths[i] > halfway:
                bit = True
            bits.append(bit)

        return bits

    def __bits_to_bytes(self, bits):
        the_bytes = []
        byte = 0

        for i in range(0, len(bits)):
            byte = byte << 1
            if (bits[i]):
                byte = byte | 1
            else:
                byte = byte | 0
            if ((i + 1) % 8 == 0):
                the_bytes.append(byte)
                byte = 0

        return the_bytes

    def __calculate_checksum(self, the_bytes):
        return the_bytes[0] + the_bytes[1] + the_bytes[2] + the_bytes[3] & 255
        
        
        
        
        
        
        
        
        
        
"""        
        
# Parse command line parameters
if len(sys.argv) == 3:
    sensor = sys.argv[1]
    if sensor not in ("11", "22", "2302"):
        print('Sensor "{}" is not valid. Use 11, 22 or 2302'.format(sensor))
        exit(1)
    isDht11 = sensor == "11"
    try:
        pin = int(sys.argv[2])
        if (pin < 2 or pin > 27):
            raise ValueError
    except:
        print('Gpio {} is not valid'.format(pin))
        exit(1)
else:
    print('usage: dht.py [11|22|2302] [gpio#]')
    exit(1)       
"""        

def get_temperature():

    cfg = gc.load_config().get("temperature")

    sensor = str(cfg.get("sensor_type", '22'))
    pin = cfg.get("gpio_pin", 4)



    try:
        if (pin < 2 or pin > 27):
            raise ValueError
    except:
        ERR.raiseError("02001", 'Temperature sensor gpio pin {} is not valid'.format(pin), False)
        return None

    if sensor not in ("11", "22", "2302"):
        ERR.raiseError("02002", 'Temperature sensor type "{}" is not valid. Use 11, 22 or 2302', False)
        return None
            
            
            
    isDht11 = sensor == "11"
    
    
    # initialize GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    # read data
    MAX_ATTEMPTS = 15
    MAX_NOT_FOUND_ATTEMPTS = 3
    dht = DHT(pin, isDht11)
    result = dht.read()
    not_found_attempts = 0

    # make some attempts, because someone may not be successful
    for x in range(0, MAX_ATTEMPTS):
        if result.is_valid() or not_found_attempts == MAX_NOT_FOUND_ATTEMPTS:
            break
        else:
            time.sleep(2)
            result = dht.read()
            if result.error_code == DHTResult.ERR_NOT_FOUND:
                not_found_attempts += 1
            else:
                not_found_attempts = 0

                
    # print result
    if result.is_valid():
        output = [result.temperature, result.humidity]
    else:
        ERR.raiseError("02003", "Temperature sensor failed to get reading. Is the sensor connected? Is the pin number correct?", False)
        return None
        
    # clean the gpio
    GPIO.cleanup()
    
    return output


