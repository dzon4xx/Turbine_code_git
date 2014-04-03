# -*- coding: utf-8 -*-
from copy import deepcopy

import Turbine_devices as Turbine

import Database_manage

from Settings import *



class Characteristic():

    def __init__(self, raw_char):

        self.x_value, self.x_unit = raw_char['x'][0:2]
        self.y_value, self.y_unit = raw_char['y'][0:2]
        self.x  =   [float(x) for x in raw_char['x'][2:]]
        self.y  =   [float(y) for y in raw_char['y'][2:]]

class Characteristics_loader():

    def __init__(self, ):
        pass

    def load_characteristics(self, char_file):
                   
        raw_char = {}
        characteristics = {}
        for line in char_file:               # unpacks one line in file

            if line.startswith('#'):
                continue
            line = line.rstrip('\n')
            line = line.strip(",")
            tab_line = line.split(',') 
            if tab_line == []:
                continue
            elif tab_line[0] == '&':
                                      
                if raw_char:
                    char = Characteristic(raw_char)
                    characteristics[ident] = char
                raw_char = {}
                ident, point, name  =   tab_line[1:] 
                    
            else:
                cord = tab_line[0]
                raw_char[cord] = tab_line[1:]
                print tab_line                
        char_file.close()
        return characteristics   

class Data_parser():

    def __init__ (self):
        self.database_manager = Database_manage.Database_manager()

    def load_file_data(self, file):

        ATTRIBUTES = file.readline()
        ATTRIBUTES = ATTRIBUTES.rstrip('\n')
        ATTRIBUTES = ATTRIBUTES.split(',')

        if file.name() == DEVICES_MAP:
            self.load_devices_data()


        file.close()

    def load_characteristics(self, char_file):
        
        ATTRIBUTES = char_file.readline()
        ATTRIBUTES = ATTRIBUTES.rstrip('\n')
        ATTRIBUTES = ATTRIBUTES.split(',')
                   
        raw_char = {}
        characteristics = {}
        for line in char_file:               # unpacks one line in file

            if line.startswith('#'):
                continue
            line = line.rstrip('\n')
            line = line.strip(",")
            tab_line = line.split(',') 
            if tab_line == []:
                continue
            elif tab_line[0] == '&':
                                      
                if raw_char:
                    char = Characteristic(raw_char)
                    characteristics[ident] = char
                raw_char = {}
                ident, point, name  =   tab_line[1:] 
                    
            else:
                cord = tab_line[0]
                raw_char[cord] = tab_line[1:]
                print tab_line
                
        char_file.close()
        return characteristics     

    def load_driver_data(self, map_file, devices_data, characteristics):

        def prepare_channels(channels, device_name):

            

            def get_type_and_num(channel):
                try:                   
                    channel_type = channel[:3]
                    if channel_type not in MAX_CHANNEL.keys():
                        print "Invalid channel type for device ID:{0} {1}".format(ident, device_name)
                        raise TypeError 

                    channel_number =  int(channel[-1])       
                    if channel_number not in range(0, MAX_CHANNEL[channel_type]):      
                        print "Invalid channel number for device ID:{0} {1}. It must be between 0 and {2}".format(ident, device_name, MAX_CHANNEL[channel_type])
                        raise TypeError 
                except:
                    print "-FILE READER: Cannot read channel: {0} for device: ID:{1}-{2}".format(channel, ident, device_name)

                return channel_type, channel_number

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

        def prepare_settings(settings, ident):
            
            #type     = device_attrs[TYPE]
            
            prep_settings = {} 

            for set in settings:
                set = set.split('=')
                prep_settings[set[0]] = set[1]

            return prep_settings

        def append_database(pointId, device_name):

            if pointId not in self.database_manager.points_list:
                self.database_manager.points_list.append(pointId)
                self.database_manager.names_dict[pointId] = []
            if device_name not in self.database_manager.names_dict[pointId]:
               self.database_manager.names_dict[pointId].append(device_name)
        
        ATTRIBUTES = map_file.readline()
        ATTRIBUTES = ATTRIBUTES.rstrip('\n')
        ATTRIBUTES = ATTRIBUTES.split(',')

        for line in map_file:               # unpacks one line in file

            tab_line = line.split(',') 
            if tab_line == []:
                continue

            device_attrs = self.__generate_attribute_dict(ATTRIBUTES, tab_line)
            if device_attrs[ENABLED] == '0':
                continue
                            
            device_name = device_attrs[NAME]
            device_kind = device_attrs[KIND]
            pointId     = device_attrs[POINT]
            ident       = device_attrs[ID]

            channels    = device_attrs[CHANNELS].split('|')
            channels    = prepare_channels(channels, device_name) 
            device_attrs[CHANNELS] = channels 
             
            if device_attrs[CHARACTERISTIC]=='1':                             
                char        =   characteristics[ident]
                device_attrs[CHARACTERISTIC] = char

            if device_attrs.has_key(SETTINGS):
                settings    = device_attrs[SETTINGS].split(';')
                settings    = prepare_settings(settings, device_name)
                device_attrs[SETTINGS] = settings 
                        
            append_database(pointId, device_name)
            devices_data[device_kind].append(device_attrs)

        self.database_manager.create_tree()              
        map_file.close()
        return devices_data

    def load_gui_data(self, gui_file):

        ATTRIBUTES = gui_file.readline()
        ATTRIBUTES = ATTRIBUTES.rstrip('\n')
        ATTRIBUTES = ATTRIBUTES.split(',')
        devices_data = []
        for line in gui_file:               # unpacks one line in file

            line = line.rstrip('\n')
            tab_line = line.split(',') 
            if tab_line == []:
                continue

            device_attrs = self.__generate_attribute_dict(ATTRIBUTES, tab_line)
            if device_attrs[ENABLED] == '0':
                continue

            devices_data.append(device_attrs)

        gui_file.close()

        return devices_data

    def get_classes_map(self):
        
        all_classes_map = { THERMOMETER :Turbine.Measure_device, 
                MANOMETER: Turbine.Measure_device, 
                FLOWMETER: Turbine.Measure_device, 
                REV_COUNTER: Turbine.Rev_counter, 
                EXHAUST_SENSOR: Turbine.Measure_device,                                       
                VALVE : Turbine.Gas_valve, 
                THROTTLE: Turbine.Throttle, 
                RELAY:Turbine.Switch_device, 
                SERVO: Turbine.Servo,
                POTENTIOMETER: Turbine.Starter_fan,
                CURRENT_METER: Turbine.Measure_device,
                VOLTAGE_METER: Turbine.Measure_device,
                FREQUENCY_METER: Turbine.Measure_device,    
                }
        
        if turbine_name == MITSHUBISHI:

            kinds_list  =   VALVE, THROTTLE, SERVO, RELAY, POTENTIOMETER, REV_COUNTER, FLOWMETER, THERMOMETER,  MANOMETER, EXHAUST_SENSOR

            classes_map =  {kind:all_classes_map[kind] for kind in kinds_list}
            empty_devices_data = {kind: [] for kind in kinds_list }

        elif turbine_name == DEUTZ:

            kinds_list  =  THERMOMETER,  MANOMETER, CURRENT_METER, VOLTAGE_METER, FREQUENCY_METER

            classes_map =  {kind:all_classes_map[kind] for kind in kinds_list}
            empty_devices_data = {kind: [] for kind in kinds_list }

        return empty_devices_data, classes_map 
                
    def map_devices_objects(self, devices_data, classes_map, d):

        operating_devices = []            
        for device_type in classes_map:
            for device_attrs in devices_data[device_type]:
                operating_devices.append((classes_map[device_type](device_attrs, d)))            
        return operating_devices

    def __generate_attribute_dict(self, atributes, tab_line):

            device_attrs = {}
            for attr_name, attr in zip(atributes, tab_line):

                device_attrs[attr_name] = attr.strip()

            return device_attrs











    


