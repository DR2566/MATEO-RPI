try:
    import time, datetime
    from bme280 import BME280
    from smbus import SMBus
    import requests
    import board
    import busio
    import adafruit_ads1x15.ads1015 as ADS
    from adafruit_ads1x15.analog_in import AnalogIn
except Exception as e:
    print('some of the modules are not installed')
class TEST:
    def __init__(self):

        try:
            self.ads_val = AnalogIn(self.ads, ADS.P0)    # variable for output channel of uv sensor
            self.ads_ref = AnalogIn(self.ads, ADS.P1)    # variable for reference channel of UV sensor
            self.i2c = busio.I2C(board.SCL, board.SDA)   # Create the I2C bus for UV
            self.ads = ADS.ADS1015(self.i2c)             # variable to access ads1115
        except Exception:
            self.uv = 'error'

        try:
            self.bus = SMBus(1)
            self.bme = BME280(i2c_dev=self.bus)
        except Exception:
            self.temp = 'error'    
            self.press = 'error'       
            self.humid = 'error'    

        self.iter_num = 2
        self.sleep_time = 200/1000
        # Constants for UV sensor:
        self.UV_IN_MIN = 0.96
        self.UV_IN_MAX = 2.8
        self.UV_OUT_MIN = 0.0
        self.UV_OUT_MAX = 15.0

    def get_temp(self):
        if self.temp != 'error':
            try:
                temps_list = []
                for i in range(self.iter_num):
                    temp = self.bme.get_temperature()
                    if i != 0:
                        temps_list.append(temp)
                    time.sleep(self.sleep_time)
                temp = round(get_avg(temps_list),2)
                return temp
            except Exception as e:
                return 'error'

        
    def get_press(self):
        if self.press != 'error':
            try:
                press_list = []
                for i in range(self.iter_num):
                    press = self.bme.get_pressure()
                    if i != 0:
                        press_list.append(press)
                    time.sleep(self.sleep_time)
                press = round(get_avg(press_list),2)
                return press
            except Exception as e:
                return 'error'

    def get_humid(self):
        if self.humid != 'error':
            try:
                humid_list = []
                for i in range(self.iter_num):
                    humid = self.bme.get_humidity()
                    if i != 0:
                        humid_list.append(humid)
                    time.sleep(self.sleep_time)
                humid = round(get_avg(humid_list),2)
                return humid
            except Exception as e:
                return 'error'
    
    def get_uv(self):
        if self.uv != 'error':
            try:
                uv_list = []
                for i in range(self.iter_num):
                    uv = self.v2mw()
                    if i !=0:
                        uv_list.append(uv)
                    time.sleep(self.sleep_time)
                uv = round(get_avg(uv_list),2)
                return uv
            except Exception as e:
                return 'error'
    
    def v2mw(self): 
        return (self.ads_val.voltage*3.3/self.ads_ref.voltage - self.UV_IN_MIN) * (self.UV_OUT_MAX - self.UV_OUT_MIN) / (self.UV_IN_MAX - self.UV_IN_MIN) + self.UV_OUT_MIN
        
    def test_everything(self):   
        self.get_uv()
        self.get_temp()
        self.get_press()
        self.get_humid()
        return [{"Uv": self.uv, "Temperature": self.temp, "Pressure": self.press, "Humidity": self.humid}]

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