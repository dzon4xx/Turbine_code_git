# -*- coding: utf-8 -*-


import time
import threading
import sys
import imp

from copy import deepcopy
from multiprocessing import Process

from Settings import *

import Driver.Threads_Manager as Threads_Manager
import Driver.File_read as File_read
import Driver.Data_parse as Data_parse
import Driver.Turbine_devices   as Turbine_devices
import Driver.Labjack_settings as LabJack_settings

import GUI.WindowGUI as WindowGUI

import Control.Control_manager as Control_manager



class Start():

        def __init__( self, turbine_name ):

           self.file_handler        = File_read.File_handler(  )              
           self.data_parser         = Data_parse.Data_parser(  )
           self.d                   = LabJack_settings.LabJack()

        def load_settings( self, create_db=True ):

            self.__create_settings_files()        

            empty_devices_data, classes_map = self.data_parser.get_classes_map()
            devices_char                    = self.__load_characteristics()       
            loaded_devices_data             = self.__load_devices_data(empty_devices_data, devices_char)
            devices_instances              = self.data_parser.map_devices_objects(loaded_devices_data, classes_map, self.d)
            self.d.set_labjack(loaded_devices_data)

            return devices_instances, loaded_devices_data

        def start_driver( self, operating_devices):

            launcher    = Threads_Manager.Measure_and_control()
            commander   = Threads_Manager.Command()

            measure_control_thread  =   threading.Thread(target = launcher.launch, args=(operating_devices, ) )
            command_thread          =   threading.Thread(target = commander.simple_command, args=( )) # LAter on we can add start commands
       
            measure_control_thread.start()      
            #command_thread.start()

        def __create_settings_files(self,):

            settings_result_files   =   [DEVICES_MAP, DEVICES_CHAR, DEVICES_GUI]
            self.file_handler.create_csv_files(settings_result_files)

        def __load_characteristics(self, ):
            char_path_list  =  DEVICES_PATH + [DEVICES_CHAR] 
            char_file   =   self.file_handler.open_file(char_path_list, 'csv', 'r')
            return self.data_parser.load_characteristics( char_file )

        def __load_devices_data(self, empty_devices_data, characteristics):

            map_path_list  =  DEVICES_PATH + [DEVICES_MAP]      
            map_file   =   self.file_handler.open_file(map_path_list, 'csv', 'r')

            return self.data_parser.load_driver_data(map_file, empty_devices_data, characteristics) 

if __name__ == '__main__': 

    starter = Start("Mitsubishi_turbine")
    operating_devices, loaded_devices_data = starter.load_settings()    
    starter.start_driver( operating_devices )
    WindowGUI.start_gui_process( )
    Control_manager.start_control( loaded_devices_data )









