# -*- coding: utf-8 -*-
"""
Created on Sat Feb 08 11:51:50 2014

@author: Patryk
"""
from __init__ import *
import sys
from copy import deepcopy
import numpy as np
import time
from PyQt4.QtCore import *
from PyQt4.QtGui import *
        

class ManagerGUI(object):
    
    def __init__(self, GUI):
        self.GUI = GUI
        self.time = 0        
        
        self.INPUT_file_path     = "DevicesMaps\input_devices_map.txt"
        self.OUTPUT_file_path    = "DevicesMaps\output_devices_map.txt"

        self.INPUT_devices_data = {'T': {}, 'P': {}, 'F': {}, 'RPM': {}, 'EXH': {}}
        self.INPUT_devices_instances = {'T': {}, 'P': {}, 'F': {}, 'RPM': {}, 'EXH': {}}        # stores clases instancies
        self.INPUT_classes_map = {'T' : Device, 'F': Device, 'RPM': Device, 'P': Device, 'EXH': Device } 

    def prepare_operating_divaces(self):
        creator = Devices_creator(self.INPUT_file_path, self.OUTPUT_file_path)       
        devices_data = creator.read_devices_data(creator.input_file, self.INPUT_devices_data)
        self.operating_devices   = creator.map_devices_objects(devices_data, self.INPUT_devices_instances, self.INPUT_classes_map)
        print "-Operating divaces prepared"
        
    def launch(self):       
        self.time  = self.time + sleep_time
        for device_type in self.operating_devices:
            
            dict_point = self.operating_devices[device_type]
            
            for point in dict_point:
                try:
                    curve = self.GUI.dict_plot[device_type + point].curve
                except KeyError: continue
                    
                label_value = self.GUI.dict_label_sensor['label_' + device_type + point].value
                label_radio = self.GUI.dict_label_sensor['label_' + device_type + point].radio
                device = dict_point[point]
                device.time = self.time
                device.run(label_value, curve)
                if label_radio.isChecked():
                    curve_main = self.GUI.dict_plot['curve_main']
                    device.set_curve(curve_main)
                                         
        

class Devices_creator(object):
    
    def __init__(self, input_file_path, output_file_path):
        self.input_file      = self.open_file(input_file_path)
        self.output_file     = self.open_file(output_file_path)
        
    def open_file(self, rel_path, mode = 'r'):
        
        try:       
            file_handle   = open( rel_path, mode)
            ids         = file_handle.readline()
            return (file_handle)

        except IOError: 
            print "Configuration file not found press any button to exit"
            exit = raw_input()
            sys.exit( 0 )
            
    def read_devices_data(self, file, devices_data):
        for line in file:                      
            line = line.split() 
            if line != []:    
                device_type = line[0]       
                del line[0]               

                device_attrs   =   {'point': None, 'channels': None, 'kind': None}
                one_type_devices_attrs = []

            for pointId, data in enumerate(line):

                if data != '0':

                    data = data.split(',')
                    device_attrs['point']   = int(pointId)
                    device_attrs['kind']    = data[0]  
                    device_attrs['channels']  = data[1:]
                    one_type_devices_attrs.append(deepcopy(device_attrs))  
         
            devices_data[device_type] = one_type_devices_attrs
        
        return devices_data
        
    def map_devices_objects(self, devices_data, device_instances, classes_map):

        for device_type in classes_map: 
            dict_point = {}
            for device_attrs in devices_data[device_type]:
                point       = device_attrs['point']    # device_type means device name, device Id means device type number
                kind        = device_attrs['kind']
                channel_list = []
                for channel in device_attrs['channels']:
                    channel_list.append(int(channel))
                dir         = ['Turbine', 'Points', 'P'+str(point), device_type]
                dict_point[str(point)] = classes_map[device_type](point, kind, channel_list, dir)
            
            device_instances[device_type] = dict_point       

        return device_instances
        

class Device(object):
    
    def __init__(self, point, kind, channel_list, dir):
        self.point = point
        self.dir = dir
        self.kind = kind
        self.channel_list = channel_list
        self.x_list = []
        self.y_list = []
        self.time = 0     
        #self.device_type = device_type
        
    def run(self, label, curve):       
        value_dir = client.get_dir(self.dir)
        value = client.get_dir_values(value_dir)
        label.setText(str(value[0]))
        self.x_list.append(self.time) 
        self.y_list.append(value[0])        
        self.set_curve(curve)
        
    def set_curve(self, curve):
        curve.setData(x=np.array(self.x_list), y=np.array(self.y_list))
        

        
        