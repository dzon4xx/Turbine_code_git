from Turbine import *
from File_read import File_handler

class Settings():
    DEUTZ           =   "Deutz_turbine"
    MITSHUBISHI     =   "Mitsubishi_turbine"
    kinds_list = ['VALVE', 'THROTTLE', 'SERVO', 'RELAY', 'POTENTIOMETER', 'REV_COUNTER', 'FLOWMETER', 
              'THERMOMETER', 'MANOMETER', 'EXHAUST_SENSOR', 'CURRENT_METER', 'VOLTAGE_METER', 'FREQUENCY_METER']
    def __init__ (self, turbine_name):

        self.turbine_name   =   turbine_name
        self.devices_path   =   ["DevicesData", turbine_name]
        self.db_history_dir =   [turbine_name, 'History']
        self.db_present_dir =   [turbine_name, 'Present', 'Points']
        
        self.atributes      =   self.__get_atributes()
 
        
    def __read_atributes(self, ):
        fh  =   File_handler()
        return fh.read_first_line()

    def get_classes_map(self, turbine_name):
        
        VALVE, THROTTLE, SERVO, RELAY, POTENTIOMETER, REV_COUNTER, FLOWMETER, THERMOMETER,  MANOMETER, EXHAUST_SENSOR, CURRENT_METER, VOLTAGE_METER, FREQUENCY_METER =  kinds_list
        
        if turbine_name == DEUTZ:

            classes_map = { THERMOMETER :Turbine.Measure_Device, 
                            MANOMETER: Turbine.Measure_Device, 
                            FLOWMETER: Turbine.Measure_Device, 
                            REV_COUNTER: Turbine.Rev_counter, 
                            EXHAUST_SENSOR: Turbine.Measure_Device,                                       
                            VALVE : Turbine.Gas_valve, 
                            THROTTLE: Turbine.Throttle, 
                            RELAY:Turbine.Switch_device, 
                            SERVO: Turbine.Wastegate,
                            POTENTIOMETER: Turbine.Starter_fan  
                            } 

        if turbine_name == MITSHUBISHI:
            
            classes_map = { THERMOMETER :Turbine.Measure_Device, 
                            MANOMETER: Turbine.Measure_Device,                            
                            CURRENT_METER: Turbine.Measure_Device,
                            VOLTAGE_METER: Turbine.Measure_Device,
                            FREQUENCY_METER: Turbine.Measure_Device,                                   
                            } 

    


