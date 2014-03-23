# -*- coding: utf-8 -*-
from Nikitta import SiloReaderWriter
TXT = "txt"
CSV = "csv"
XLS = "xls"
#Mitsubishi turbine
DEVICES_PATH       =   ["DevicesData", "Mitsubishi_turbine"]
HISTORY_DIR        =   ['Mitsubishi_turbine', 'History']
PRESENT_DIR        =   ['Mitsubishi_turbine', 'Present', 'Points']  

#Deutz turbine
#DEVICES_PATH        = ['DevicesData', 'Deutz_turbine']
#HISTORY_DIR =   ['Deutz_turbine', 'History']
#PRESENT_DIR =   ['Deutz_turbine', 'Present', 'Points']
  
OPERATING           = "operating_devices"
MAP                 = "devices_map"
CHAR                = "devices_characteristics"
DEVICES_MAP_PATH    = '\\'.join(DEVICES_PATH+[".".join([MAP, TXT])])
DEVICES_CHAR_PATH   = '\\'.join(DEVICES_PATH+[".".join([CHAR, TXT])])


map_file     = open( DEVICES_MAP_PATH  )
ATTRIBUTES   = map_file.readline().split()
map_file.close()

#devices attributes
ID, ENABLE, POINT, NAME, DIRECTION, TYPE, KIND, CHANNELS, CHANNELS_DESCRIPTION, SETTINGS, CHARACTERISTIC = ATTRIBUTES     


#Devices kinds
kinds_list = ['VALVE', 'THROTTLE', 'SERVO', 'RELAY', 'POTENTIOMETER', 'REV_COUNTER', 'FLOWMETER', 
              'THERMOMETER', 'MANOMETER', 'EXHAUST_SENSOR', 'CURRENT_METER', 'VOLTAGE_METER', 'FREQUENCY_METER']
VALVE, THROTTLE, SERVO, RELAY, POTENTIOMETER, REV_COUNTER, FLOWMETER, THERMOMETER,  MANOMETER, EXHAUST_SENSOR, CURRENT_METER, VOLTAGE_METER, FREQUENCY_METER =  kinds_list 

UNITS_DICT = {FLOWMETER: 'm3/h',
              THERMOMETER: 'K',
              MANOMETER: ''}
devices_data = { kind: [] for kind in kinds_list }
#Devices names

devices_names_list = ["GAS_VALVE", "WASTEGATE", "MAIN_THROTTLE", "AUXILARY_THROTTLE", "STARTER_FAN", 
                      "IGNITION", "OIL_PUMP", "REV_COUNTER_1ST", "REV_COUNTER_2ND", "FLOWMETER_AIR", 
                      "FLOWMETER_GAS", "MANOMETER_INTROL", "MANOMETER_BOTLAND", "THERMOCOUPLE_K", 
                      "LABJACK_TEMP_SENSOR",]

GAS_VALVE, WASTEGATE, MAIN_THROTTLE, AUXILARY_THROTTLE, STARTER_FAN, IGNITION, OIL_PUMP, REV_COUNTER_1ST, REV_COUNTER_2ND, FLOWMETER_AIR, FLOWMETER_GAS, MANOMETER_INTROL, MANOMETER_BOTLAND, THERMOCOUPLE_K, LABJACK_TEMP_SENSOR, = devices_names_list	
    
#channels types
DIO, AIN, DAC, TIO, CIO, NOT = ['DIO', 'AIN', 'DAC', 'TIO', 'CIO', 'NOT']
#devices types
DIGITAL_PULSE, DIGITAL, ANALOG = ['DIGITAL_PULSE', 'DIGITAL', 'ANALOG']

#Settings
MODE, VALUE, VOFFSET, GAIN, SAVE_TIME     =  'mode', 'value', 'voffset', 'gain', 'save_time'
  
MAX_CHANNEL = {DIO: 22, AIN: 13, DAC: 2, TIO: 7, CIO: 2, NOT: 1}

#start dirs

client = SiloReaderWriter.SiloReaderWriter()  
sleep_time      = client.sleep_time
avarage_time    = 0.1

