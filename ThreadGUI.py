# -*- coding: utf-8 -*-
"""
Created on Sat Feb 08 11:51:50 2014

@author: Patryk
"""
import sys
from copy import deepcopy
import numpy as np
import time
import File_reader
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from __init__ import *
        

class ManagerGUI(object):
    
    def __init__(self, GUI):
        self.GUI = GUI
        self.time = 0        

    def Prepare_devices(self):
        
        VALVE, THROTTLE, SERVO, RELAY, POTENTIOMETER, REV_COUNTER, FLOWMETER, THERMOMETER,  MANOMETER, EXHAUST_SENSOR, CURRENT_METER, VOLTAGE_METER, FREQUENCY_METER =  kinds_list

        classes_map     = { THERMOMETER : Device, 
                            MANOMETER: Device, 
                            FLOWMETER: Device, 
                            REV_COUNTER: Device, 
                            EXHAUST_SENSOR: Device,
                            CURRENT_METER: Device,
                            VOLTAGE_METER: Device,
                            FREQUENCY_METER: Device,        
                            VALVE : Device, 
                            THROTTLE: Device, 
                            RELAY:Device, 
                            SERVO: Device,
                            POTENTIOMETER: Device  
                            } 
                            
        Devices_creator =   File_reader.Devices_creator()

        load_devices_data, self.operating_devices  = Devices_creator.prepare_devices_to_launch(DEVICES_MAP_PATH, DEVICES_CHAR_PATH, devices_data, classes_map, create_db=False)
        
        return self.operating_devices
        
    def launch(self):       
        self.time  = self.time + sleep_time
        for device in self.operating_devices:
                            
            try:
                curve = self.GUI.dict_plot[device.kind + str(device.point)].curve
            except KeyError: continue
                
            label_value = self.GUI.dict_label_sensor[device.kind + str(device.point)].value
            label_radio = self.GUI.dict_label_sensor[device.kind + str(device.point)].radio
            device.time = self.time
            device.run(label_value, curve)
            if label_radio.isChecked():
                curve_main = self.GUI.dict_plot['curve_main']
                device.set_curve(curve_main)
                                                

class Device(object):
    
    def __init__(self, device_attrs):
        self.id             =   device_attrs[ID]
        self.point          =   'P' + str(device_attrs[POINT])
        self.name           =   device_attrs[NAME]
        self.direction      =   device_attrs[DIRECTION]
        self.type           =   device_attrs[TYPE]
        self.kind           =   device_attrs[KIND]

        self.dir            =   client.get_dir(PRESENT_DIR + [self.point, self.name] )
        self.x_list = []
        self.y_list = []
        self.time = 0 
        
    def run(self, label, curve):       
        value = client.get_dir_values(self.dir)
        if self.kind  == 'REV_COUNTER':     label.display(str(value[0]))
        else:                               label.setText(str(value[0]))
        self.x_list.append(self.time) 
        self.y_list.append(value[0])        
        self.set_curve(curve)
        
    def set_curve(self, curve):
        curve.setData(x=np.array(self.x_list), y=np.array(self.y_list))
              
        