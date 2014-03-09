# -*- coding: utf-8 -*-

################################NOTES_TO_MYSELF#############################################
#
#
#
#
#
#
#############################################################################


import time
import threading
import sys
import imp

from __init__ import *

import Threads_Manager
import File_reader
import Turbine
import Database_manage

class Start():

    def __init__( self ):
       pass

    def Get_devices_to_launch( self ):

        DEVICES_FILE_PATH           = "DevicesMaps\devices_map.txt"

        devices_data      = {       'THERMOMETER': [], 
                                    'MANOMETER': [], 
                                    'FLOWMETER': [], 
                                    'REV_COUNTER': [], 
                                    'EXHAUST_SENSOR': [],           
                                    'VALVE': [], 
                                    'THROTTLE': [], 
                                    'IGNITION': [] , 
                                    'STARTER_FAN': [] , 
                                    'WASTEGATE': [],
                                    'OIL_PUMP': [], 
                            }

        classes_map         = {     'THERMOMETER' :Turbine.Measure_Device, 
                                    'MANOMETER': Turbine.Measure_Device, 
                                    'FLOWMETER': Turbine.Measure_Device, 
                                    'REV_COUNTER': Turbine.Rev_counter, 
                                    'EXHAUST_SENSOR': Turbine.Measure_Device,        
                                    'VALVE' : Turbine.Gas_valve, 
                                    'THROTTLE': Turbine.Throttle, 
                                    'IGNITION':Turbine.Switch_device, 
                                    'WASTEGATE': Turbine.Wastegate, 
                                    'OIL_PUMP': Turbine.Switch_device,  
                                }                

        Devices_creator =   File_reader.Devices_creator(DEVICES_FILE_PATH,)

        devices_data, devices_instances  = Devices_creator.prepare_devices_to_launch( devices_data, classes_map )

        Turbine.d.set_labjack(devices_data)
        return devices_instances

    def Start_threads( self, devices_instances, recorder ):

        launcher    = Threads_Manager.Measure_and_control()
        commander   = Threads_Manager.Command()

        measure_control_thread  =   threading.Thread(target = launcher.launch, args=(operating_devices, recorder, ) )
        #command_thread          =   threading.Thread(target = commander.simple_command, args=(exporter, )) # LAter on we can add start commands
       
        measure_control_thread.start()      
        #command_thread.start()


starter = Start()
operating_devices = starter.Get_devices_to_launch()
recorder = Database_manage.Record() 
#exporter = Database_manage.Export( ["Turbine", "History"], operating_devices )   # sending history start_dir_list

starter.Start_threads( operating_devices, recorder )





