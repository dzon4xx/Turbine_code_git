# -*- coding: utf-8 -*-
from copy import deepcopy
from collections import namedtuple
import Write_turbine_tree
from __init__ import *


#class Characteristic():

#    def __init__


class Devices_creator():

    def __init__(self, devices_file_path, ):

        self.name   =   "File Reader"
        self.turbine_tree_creator = Write_turbine_tree.Turbine_tree_creator()

        self.devices_file      = self.open_file(devices_file_path)

    def open_file(self, rel_path, mode= 'r'):
    
        try:       
            file_handle   = open( rel_path, mode)
            file_handle.readline()
            return (file_handle)

        except IOError: 
            print "Configuration file not found press any button to exit"
            exit = raw_input()
            sys.exit( 0 )
     
    def prepare_devices_to_launch(self, devices_data, classes_map ):
       
        devices_data                  = self.load_data(self.devices_file , devices_data)
        self.create_database()
        operating_devices_list        = self.map_devices_objects(devices_data, classes_map)
                
        return devices_data, operating_devices_list # list which are empty are not initialized

    def load_data(self, file, devices_data):

        def prepare_channels(device_attrs, device_name):

            def get_type_and_num(channel):

                try:
                    channel_type = channel[:3].lower()
                    if channel_type not in MAX_CHANNEL.keys():
                        print "Invalid channel type for device ID:{0} {1}".format(ident, device_name)
                        raise TypeError 

                    channel_number =  int(channel[3:])       
                    if channel_number not in range(0, MAX_CHANNEL[channel_type]):      
                        print "Invalid channel number for device ID:{0} {1}. It must be between 0 and {2}".format(ident, device_name, MAX_CHANNEL[channel_type])
                        raise TypeError 
                except:
                    print "-FILE READER: Cannot read channel: {0} for device: ID:{1}-{2}".format(channel, ident, device_name)

                return channel_type, channel_number

            ident       = device_attrs[ID]
            channels    = device_attrs[CHANNELS].split('|')
            channels_dict = {}

            for channel in channels:

                if ';' in channel:
                    channel = channel.split(';')
                    channel_type = channel[0][:3].lower()                    
                    channels_dict[channel_type] = []
                    for ch in channel:
                        channel_type, channel_number = get_type_and_num(ch)
                        channels_dict[channel_type].append(channel_number)
                else:
                    channel_type, channel_number = get_type_and_num(channel) 
                    channels_dict[channel_type] = channel_number

            return channels_dict

        def prepare_char(device_attrs, device_name):
           
            ident       = device_attrs[ID]
            char        = device_attrs[CHARACTERISTIC] 
               
            char  = char.split(';')
            prep_char = namedtuple('characteristic', 'x y')

            prep_char.x = [float(x) for x in char[0].split(',')]
            prep_char.y = [float(y) for y in char[1].split(',')]

            assert len(prep_char.x) == len(prep_char.y), 'Characteristic for ID:{0}-{1} not loaded because lenght of X and Y vectors not equal'.format(ident, device_name)


            return prep_char

        def prepare_settings(device_attrs, ident):
            
            type     = device_attrs[TYPE].lower()
            settings = device_attrs[SETTINGS].split(';')
            prep_settings = {} 

            for set in settings:
                set = set.split('=')
                prep_settings[set[0]] = set[1]

            return prep_settings


        for line in file:               # unpacks one line in file

            if line.startswith('#'):
                continue
            tab_line = line.split() 
            if tab_line == []:
                continue

            device_attrs = {}
            for attr_name, attr in zip(attributes, tab_line):

                try:
                    attr = int(attr)
                except: ValueError

                device_attrs[attr_name]           = attr

            
            device_name = device_attrs[NAME]
            pointId     = device_attrs[POINT]

            channels    = prepare_channels(device_attrs, device_name) 
            device_attrs[CHANNELS] = channels 
             
            try:                                
                char        = prepare_char(device_attrs, device_name)
                device_attrs[CHARACTERISTIC] = char
            except KeyError:
                print "-FILE READER: No characteristic for name:{0} in point {1}".format(device_name, pointId) 
            try:
                setting     = prepare_settings(device_attrs, device_name)
                device_attrs[SETTINGS] = setting 
            except KeyError:
                print "-FILE READER: No setting for name:{0} in point {1}".format(device_name, pointId) 
                        
            if pointId not in self.turbine_tree_creator.points_list:
                self.turbine_tree_creator.points_list.append(pointId)
                self.turbine_tree_creator.names_dict[pointId] = []
            if device_name not in self.turbine_tree_creator.names_dict[pointId]:
                self.turbine_tree_creator.names_dict[pointId].append(device_name)
            
            devices_data[device_name].append(device_attrs)
        file.close()
        return devices_data        

    def map_devices_objects(self, devices_data, classes_map):

        operating_devices = []            
        for device_type in classes_map:
            for device_data in devices_data[device_type]:
                if device_data[KIND] != "UNKNOWN":
                    operating_devices.append((classes_map[device_type](device_data)))
               
        return operating_devices

    def create_database(self):
       
        self.turbine_tree_creator.create_tree()
        self.turbine_tree_creator.points_list       = [] # when database is created resources should be released so input tree won't be created again while creating output tree
        self.turbine_tree_creator.type_names_dict   = {}