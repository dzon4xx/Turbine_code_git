# -*- coding: utf-8 -*-
from Nikitta import SiloReaderWriter

file_handle     = open( "DevicesMaps\devices_map.txt" )
attributes      = file_handle.readline().split()
file_handle.close()
 
ID                  = attributes[0]
POINT	            = attributes[1] 
NAME	            = attributes[2]
DIRECTION	        = attributes[3]
TYPE	            = attributes[4]
KIND	            = attributes[5]
CHANNELS	        = attributes[6]
CHANNELS_DESCRIPTION= attributes[7]
SETTINGS            = attributes[8]
CHARACTERISTIC      = attributes[9]
#channels types
DIO =   'dio'
AIN =   'ain'
DAC =   'dac'
TIO =   'tio'
CIO =   'cio'
#devices types
DIGITAL_PULSE = 'digital_pulse'
DIGITAL       = 'digital'
ANALOG        = 'ANALOG'

#Devices names
REV_COUNTER   = 'rev_counter'

#Settings
DIV     = 'div'
BASE    = 'base'
MODE    = 'mode'
VALUE   = 'value'
RES     = 'res'
RANGE   = 'range'
   



MAX_CHANNEL = {DIO: 22, AIN: 13, DAC: 2, TIO: 7, CIO: 2}



client = SiloReaderWriter.SiloReaderWriter()  
sleep_time      = client.sleep_time
avarage_time    = 0.1