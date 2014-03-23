# -*- coding: utf-8 -*-
from copy import deepcopy
from collections import namedtuple
import Write_turbine_tree
import xlrd
import csv
from __init__ import *

class Devices_creator():

    def __init__(self,):

        self.name   =   "File_Reader"       
        self.turbine_tree_creator = Write_turbine_tree.Turbine_tree_creator()
            
    def prepare_devices_to_launch(self, devices_data, devices_file_path, devices_char_path, classes_map, create_db=True):

        def open_file( rel_path, mode= 'r'):
    
            try:       
                file_handle   = open( rel_path, mode)
                file_handle.readline()
                return (file_handle)

            except IOError: 
                print "Configuration file not found press any button to exit"
                exit = raw_input()
                sys.exit( 0 )

        def load_characteristics(devices_char_path,):

            class characteristic():

                def __init__(self, raw_char):

                    self.x_value, self.x_unit = raw_char['x'][0:2]
                    self.y_value, self.y_unit = raw_char['y'][0:2]
                    self.x  =   [float(x) for x in raw_char['x'][2:]]
                    self.y  =   [float(y) for y in raw_char['y'][2:]]
           
            char_file = open_file(devices_char_path)
            raw_char = {}
            characteristics = {}
            for line in char_file:               # unpacks one line in file

                if line.startswith('#'):
                    continue
                tab_line = line.split() 
                if tab_line == []:
                    continue
                elif tab_line[0] == '&':
                                      
                    if raw_char:
                        char = characteristic(raw_char)
                        characteristics[ident] = char
                    raw_char = {}
                    ident, point, name  =   tab_line[1:] 
                    
                else:
                    cord = tab_line[0]
                    raw_char[cord] = tab_line[1:]
                    print tab_line

                
            char_file.close()
            return characteristics     

        def load_data(devices_file_path, devices_data, characteristics):

            def prepare_channels(device_attrs, device_name):

                def get_type_and_num(channel):

                    try:
                        channel_type = channel[:3]
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
                        channel_type = channel[0][:3]                    
                        channels_dict[channel_type] = []
                        for ch in channel:
                            channel_type, channel_number = get_type_and_num(ch)
                            channels_dict[channel_type].append(channel_number)
                    else:
                        channel_type, channel_number = get_type_and_num(channel) 
                        channels_dict[channel_type] = channel_number

                return channels_dict

            def prepare_settings(device_attrs, ident):
            
                type     = device_attrs[TYPE]
                settings = device_attrs[SETTINGS].split(';')
                prep_settings = {} 

                for set in settings:
                    set = set.split('=')
                    prep_settings[set[0]] = set[1]

                return prep_settings

            def generate_attribute_dict(line):

                device_attrs = {}
                for attr_name, attr in zip(ATTRIBUTES, tab_line):

                    device_attrs[attr_name] = attr

                return device_attrs

            def append_database(pointId, device_name):

                if pointId not in self.turbine_tree_creator.points_list:
                    self.turbine_tree_creator.points_list.append(pointId)
                    self.turbine_tree_creator.names_dict[pointId] = []
                if device_name not in self.turbine_tree_creator.names_dict[pointId]:
                    self.turbine_tree_creator.names_dict[pointId].append(device_name)
                    
            device_file = open_file(devices_file_path)
            for line in device_file:               # unpacks one line in file

                if line.startswith('#'):
                    continue
                tab_line = line.split() 
                if tab_line == []:
                    continue

                device_attrs = generate_attribute_dict(line)
                if device_attrs[ENABLE] == 0:
                    continue
                            
                device_name = device_attrs[NAME]
                device_kind = device_attrs[KIND]
                pointId     = device_attrs[POINT]

                channels    = prepare_channels(device_attrs, device_name) 
                device_attrs[CHANNELS] = channels 
             
                if device_attrs[CHARACTERISTIC]=='1':
                    ident       =   device_attrs[ID]                               
                    char        =   characteristics[ident]
                    device_attrs[CHARACTERISTIC] = char

                if device_attrs.has_key(SETTINGS):
                    setting     = prepare_settings(device_attrs, device_name)
                    device_attrs[SETTINGS] = setting 
                        
                append_database(pointId, device_name)
                devices_data[device_kind].append(device_attrs)
                          
            device_file.close()
            return devices_data
                
        def map_devices_objects(devices_data, classes_map):

            operating_devices = []            
            for device_type in classes_map:
                for device_attrs in devices_data[device_type]:
                    operating_devices.append((classes_map[device_type](device_attrs)))            
            return operating_devices

        def create_database():       
                self.turbine_tree_creator.create_tree()
        
        #create_csv_file()
        characteristics             = load_characteristics(devices_char_path, )
        devices_data                = load_data(devices_file_path, devices_data, characteristics)
        if create_db:
            create_database()
        operating_devices      = map_devices_objects(devices_data, classes_map)
                        
        return devices_data, operating_devices # list which are empty are not initialized

class File_handler():
    TXT = "txt"
    CSV = "csv"
    XLS = "xls"
    def __init__(self, start_path_list):
        pass
        
    def convert_to_path(self, path_list):

        path = "\\".join(path_list)
        return path     

    def create_csv_file(self, path, file_name, sheet_index, ):

       # path = DEVICES_PATH + [".".join([MAP, XLS])]
        #path = "\\".join(path)
        path = '\\'.join(path + [".".join([file_name, XLS])])
        with xlrd.open_workbook(path) as wb:
            sh = wb.sheet_by_index(sheet_index)  # or wb.sheet_by_name('name_of_the_sheet_here')
            path = DEVICES_PATH + [".".join([MAP, CSV])]
            path = "\\".join(path)
            with open(path, 'wb') as f:
                c = csv.writer(f)
                for r in range(sh.nrows):
                    c.writerow(sh.row_values(r))

    def read_first_line(self, path):

        file    = open( path  )
        line    = file.readline().split()
        file.close()


def prepare_devices_to_launch( classes_map, create_db=True):

    file_handler    =   File_handler(DEVICES_PATH)
    #data_loader     =   Data_loader()
    
    file_handler.create_csv_file(DEVICES_PATH, MAP, 0)


    


