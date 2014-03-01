# -*- coding: utf-8 -*-
from copy import deepcopy

import Write_turbine_tree
from __init__ import *


class Devices_creator():

    def __init__(self, input_file_path, output_file_path):

        self.turbine_tree_creator = Write_turbine_tree.Turbine_tree_creator()

        self.input_file      = self.open_file(input_file_path)
        self.output_file     = self.open_file(output_file_path)

    def open_file(self, rel_path, mode= 'r'):
    
        try:       
            file_handle   = open( rel_path, mode)
            ids         = file_handle.readline()                  # reads point ID line which is healpfull for user orientation but not for code runing
            return (file_handle)

        except IOError: 
            print "Configuration file not found press any button to exit"
            exit = raw_input()
            sys.exit( 0 )
     
    def prepare_devices_to_launch(self, file, devices_data, device_instances, classes_map):

        self.test_string = ("*"*10 + "VALIDITY OF {0} READ" + 10*"*").format((file.name.split('_')[0]).upper()) 
        print self.test_string
                              
        devices_data            = self.read_devices_data(file, devices_data)

        self.create_database()
        
        device_instances_dict   = self.map_devices_objects(devices_data, device_instances, classes_map)
   
        operating_devices_list  = self.get_operating_devices_list(devices_data, device_instances_dict) 
          
        return operating_devices_list # list which are empty are not initialized

    def read_devices_data(self, file, devices_data):
            
        for line in file:               # unpacks one line in file

            if line == '\n':            # if line is empty
                del line
                continue
                                     
            line = line.split()         # splits the line into list
            device_type = line[0]       # first position in line is fevice type. for example T is thermocouple F is flowmeter etc.
   
            del line[0]                 

            device_attrs   =   {'point': None, 'channels': None, 'kind': None}
            one_type_devices_attrs = [] # list of all devices of one type atributes dictionaries. for example list of all thermocouples atributes dictionaries

            for pointId, data in enumerate(line):

                if data != '0':

                    data = data.split(',')

                    if pointId not in self.turbine_tree_creator.points_list:
                        self.turbine_tree_creator.points_list.append(pointId)
                        self.turbine_tree_creator.type_names_dict[pointId] = []
                    if data[0] not in self.turbine_tree_creator.type_names_dict[pointId]:
                        self.turbine_tree_creator.type_names_dict[pointId].append(device_type)
                    
                    device_attrs['point']       = int(pointId)
                    device_attrs['kind']        = data[0]  
                    device_attrs['channels']    = data[1:]
                    one_type_devices_attrs.append(deepcopy(device_attrs))  
         
            devices_data[device_type] = one_type_devices_attrs
        
        return devices_data

    def map_devices_objects(self, devices_data, device_instances, classes_map):

        for device_type in classes_map:        
            for device_attrs in devices_data[device_type]:
                point       = device_attrs['point']    # device_type means device name, device Id means device type number
                kind        = device_attrs['kind']
                channel_list = []
                for channel in device_attrs['channels']:
                    channel_list.append(int(channel))
                dir         = ['Turbine', 'Points', 'P'+str(point), device_type]


                device_instances[device_type].append((classes_map[device_type](point, kind, channel_list, dir)))
        
        return device_instances

    def get_operating_devices_list(self, devices_data, device_instances):

        print "-Devices data from file: \n{0}".format(devices_data) 
        print "\n-Devices to launch:\n{0}\n{1}\n\n".format(device_instances, '*'*len(self.test_string) )
        operating_devices = []                
        for device in device_instances:                             ### This code may be redundant             
            if device_instances[device] != []:
                for deviceId in range( len(device_instances[device] ) ):
                    operating_device = device_instances[device][deviceId]
                    operating_devices.append( operating_device )
        return operating_devices

    def create_database(self):
       
        self.turbine_tree_creator.create_tree()
        self.turbine_tree_creator.points_list       = [] # when database is created resources should be released so input tree won't be created again while creating output tree
        self.turbine_tree_creator.type_names_dict   = {}