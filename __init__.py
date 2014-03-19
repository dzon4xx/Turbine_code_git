# -*- coding: utf-8 -*-
from Nikitta import SiloReaderWriter
debug = 'DEBUG'
#Mitsubishi turbine
#DEVICES_FILE_PATH           = "DevicesMaps\devices_map.txt"
#DEVICES_CHAR_PATH           = "DevicesMaps\devices_characteristics.txt"

#Deutz turbine
DEVICES_FILE_PATH           = "DevicesMaps\devices_map_deutze.txt"
DEVICES_CHAR_PATH           = "DevicesMaps\devices_characteristics_deutze.txt"

file_handle     = open( DEVICES_FILE_PATH )
ATTRIBUTES      = file_handle.readline().split()
file_handle.close()

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
                      "LABJACK_TEMP_SENSOR", "MANOMETER", "THERMOMETER"]
GAS_VALVE, WASTEGATE, MAIN_THROTTLE, AUXILARY_THROTTLE, STARTER_FAN, IGNITION, OIL_PUMP, REV_COUNTER_1ST, REV_COUNTER_2ND, FLOWMETER_AIR, FLOWMETER_GAS, MANOMETER_INTROL, MANOMETER_BOTLAND, THERMOCOUPLE_K, LABJACK_TEMP_SENSOR, MANOMETER, THERMOMETER = devices_names_list	

    


#channels types
DIO, AIN, DAC, TIO, CIO, NOT = ['DIO', 'AIN', 'DAC', 'TIO', 'CIO', 'NOT']
#devices types
DIGITAL_PULSE, DIGITAL, ANALOG = ['DIGITAL_PULSE', 'DIGITAL', 'ANALOG']

#Settings
MODE, VALUE, VOFFSET, GAIN, SAVE_TIME     =  'mode', 'value', 'voffset', 'gain', 'save_time'

   
MAX_CHANNEL = {DIO: 22, AIN: 13, DAC: 2, TIO: 7, CIO: 2, NOT: 1}



client = SiloReaderWriter.SiloReaderWriter()  
sleep_time      = client.sleep_time
avarage_time    = 0.1
