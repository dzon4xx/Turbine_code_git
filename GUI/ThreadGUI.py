# -*- coding: utf-8 -*-
"""
Created on Sat Feb 08 11:51:50 2014

@author: Patryk
"""
import sys
from copy import deepcopy
import numpy as np
import time
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Settings import *
import Driver.File_read as File_read
#from Driver.File_read import File_handler, Data_parser
        

class ManagerGUI(object):
    
    def __init__(self, GUI):

        self.GUI = GUI
        self.time = 0        
        self.operating_devices = []

    def _Prepare_devices(self):
        
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

    def load_devices(self, ):
        
        data_parser     = File_read.Data_parser()
        file_handler    = File_read.File_handler()
     
        gui_path_list   =   DEVICES_PATH + [DEVICES_GUI]      
        gui_file        =   file_handler.open_file(gui_path_list, 'csv', 'r')       
        devices_data    =   data_parser.load_gui_data(gui_file)
        
        for device_attrs in devices_data:
            self.operating_devices.append(Gui_device(device_attrs))

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
                                                

class Gui_device(object):
    display_length = 100
    def __init__(self, device_attrs):
        self.id             =   device_attrs[ID]
        self.point          =   'P' + str(device_attrs[POINT])
        self.name           =   device_attrs[NAME]
        self.direction      =   device_attrs[DIRECTION]
        self.type           =   device_attrs[TYPE]
        self.kind           =   device_attrs[KIND]

        self.dir            =   client.get_dir(DB_PRESENT_DIR + [self.point, self.name] )

        self.x_list         = [0 for i in range(Gui_device.display_length)]
        self.y_list         = [0 for i in range(Gui_device.display_length)]
        self.time           = 0 
        
    def run(self, label, curve):       
        value = client.get_dir_values(self.dir)

        label.setText(str(value[0]))
        self.x_list.insert(0, self.time)
        self.x_list.pop()
        self.y_list.insert(0, value[0])
        self.y_list.pop()  
     
        self.set_curve(curve)
        
    def set_curve(self, curve):
        curve.setData(x=np.array(self.x_list), y=np.array(self.y_list))
              
        