# -*- coding: utf-8 -*-
from copy import deepcopy
from collections import namedtuple
import Write_turbine_tree
from __init__ import *


#class Characteristic():

#    def __init__


class Devices_creator():

    def __init__(self, input_file_path, output_file_path, *args):

        self.name   =   "File Reader"
        self.turbine_tree_creator = Write_turbine_tree.Turbine_tree_creator()

        self.input_file             = self.open_file(input_file_path)
        self.output_file            = self.open_file(output_file_path)
        self.characteristics_file   = self.open_file(args[0])

    def open_file(self, rel_path, mode= 'r'):
    
        try:       
            file_handle   = open( rel_path, mode)
            ids         = file_handle.readline()                  # reads point ID line which is healpfull for user orientation but not for code runing
            return (file_handle)

        except IOError: 
            print "Configuration file not found press any button to exit"
            exit = raw_input()
            sys.exit( 0 )
     
    def prepare_devices_to_launch(self, file, devices_data, classes_map, *args):

        self.test_string = ("*"*10 + "VALIDITY OF {0} READ" + 10*"*").format((file.name.split('_')[0]).upper()) 
        print self.test_string
        
        devices_data                  = self.read_devices_data(file, devices_data)
        self.create_database()
        
        if args:
            char_file = args[0]
            devices_char            = self.read_devices_characteristics(char_file)
            operating_devices_list        = self.map_devices_objects(devices_data, classes_map, devices_char)
        else:
            operating_devices_list        = self.map_devices_objects(devices_data, classes_map)
                
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

                    device_attrs['point']       = int(pointId)
                    device_attrs['kind']        = data[0]  
                    device_attrs['channels']    = data[1:]
                    one_type_devices_attrs.append(deepcopy(device_attrs))  

                    if pointId not in self.turbine_tree_creator.points_list:
                        self.turbine_tree_creator.points_list.append(pointId)
                        self.turbine_tree_creator.type_names_dict[pointId] = []
                    if device_attrs['kind'] not in self.turbine_tree_creator.type_names_dict[pointId]:
                        self.turbine_tree_creator.type_names_dict[pointId].append(device_type)
                    

            
            devices_data[device_type] = one_type_devices_attrs
        
        return devices_data

    def read_devices_characteristics(self, char_file):

        char_dict = {}
        char_dict['MANOMETER']          = []
        char_dict['THERMOCOUPLE']       = []

        char = namedtuple('characteristic', 'x y')
        char.x = [0.472, 2.36]
        char.y = [0, 4]
        char_dict['MANOMETER'].append({'I':char})
        char1 = namedtuple('characteristic', 'x y')
        char1.x = [0, 3]
        char1.y = [0, 4]
        char_dict['MANOMETER'].append({'B':char1})
        char_dict['THERMOCOUPLE'].append({'K':None})
        
        return char_dict

    def map_devices_objects(self, devices_data, classes_map, *args):
        print "\n-{0}: Devices data from file: \n{1}".format(self.name, devices_data) 

        operating_devices = []            
        for device_type in classes_map:
                    
            for device_attrs in devices_data[device_type]:
                point       = device_attrs['point']    # device_type means device name, device Id means device type number
                kind        = device_attrs['kind']
                dir         = ['Turbine', 'Points', 'P'+str(point), device_type]

                channel_list = []
                for channel in device_attrs['channels']:
                    channel_list.append(int(channel))

                if args:
                    devices_char = args[0]
                    if device_type in devices_char.keys():
                        for kind_char_dict in devices_char[device_type]:
                            if kind in kind_char_dict.keys():
                                char = kind_char_dict[kind]
                                operating_devices.append((classes_map[device_type](device_type, point, kind, channel_list, dir, char)))

                    else:
                        print "\n-{0}: Device {1} kind {2} in point {3} not loaded because characteristic not given".format(self.name, device_type, kind, point)

                else:
                    operating_devices.append((classes_map[device_type](device_type, point, kind, channel_list, dir)))

        
        
        print "\n-Devices to launch:\n{0}\n{1}\n\n".format(operating_devices, '*'*len(self.test_string) )
        return operating_devices


    def create_database(self):
       
        self.turbine_tree_creator.create_tree()
        self.turbine_tree_creator.points_list       = [] # when database is created resources should be released so input tree won't be created again while creating output tree
        self.turbine_tree_creator.type_names_dict   = {}