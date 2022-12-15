import time, datetime
from bme280 import BME280
from smbus import SMBus
import requests
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

class TEST:
    def __init__(self):
        self.bus = SMBus(1)
        self.i2c = busio.I2C(board.SCL, board.SDA)   # Create the I2C bus for UV
        self.bme = BME280(i2c_dev=self.bus)
        self.ads = ADS.ADS1015(self.i2c)             # variable to access ads1115
        self.ads_val = AnalogIn(self.ads, ADS.P0)    # variable for output channel of uv sensor
        self.ads_ref = AnalogIn(self.ads, ADS.P1)    # variable for reference channel of UV sensor
        self.iter_num = 5
        self.current_temp = None
        self.current_press = None
        self.current_humid = None
        self.current_uv = None
        # Constants for UV sensor:
        self.UV_IN_MIN = 0.96
        self.UV_IN_MAX = 2.8
        self.UV_OUT_MIN = 0.0
        self.UV_OUT_MAX = 15.0

    def get_temp(self):
        temps_list = []
        for i in range(self.iter_num):
            temp = self.bme.get_temperature()
            if i != 0:
                temps_list.append(temp)
            time.sleep(1)
        self.current_temp = round(get_avg(temps_list),2)
        return self.current_temp
        
    def get_press(self):
        press_list = []
        for i in range(self.iter_num):
            press = self.bme.get_pressure()
            if i != 0:
                press_list.append(press)
            time.sleep(1)
        self.current_press = round(get_avg(press_list),2)
        return self.current_press

    def get_humid(self):
        humid_list = []
        for i in range(self.iter_num):
            humid = self.bme.get_humidity()
            if i != 0:
                humid_list.append(humid)
            time.sleep(1)
        self.current_humid = round(get_avg(humid_list),2)
        return self.current_humid
    
    def get_uv(self):
        uv_list = []
        for i in range(self.iter_num):
            uv = self.v2mw()
            if i !=0:
                uv_list.append(uv)
            time.sleep(1)
        self.current_uv = round(get_avg(uv_list),2)
        return self.current_uv
    
    def v2mw(self): 
        return (self.ads_val.voltage*3.3/self.ads_ref.voltage - self.UV_IN_MIN) * (self.UV_OUT_MAX - self.UV_OUT_MIN) / (self.UV_IN_MAX - self.UV_IN_MIN) + self.UV_OUT_MIN
        
    def test_everything(self):   
        return self.get_uv(), self.get_temp(), self.get_press(), self.get_humid()

def get_avg(list_num):
    return sum(list_num) / len(list_num)
def convert_float(float_num): # we want to change "." separator substitude to "," for excel
    int_str = str(float_num)
    new_int = ""
    for letter in int_str:
        if letter == ".":
            new_int += ","
        else:
            new_int += letter
    return new_int

# testing = TEST()
# print(testing.test_everything())
