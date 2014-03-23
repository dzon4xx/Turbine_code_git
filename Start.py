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
import File_read
import Turbine
import Database_manage

class Start():

    def __init__( self ):
       pass

    def Get_devices_to_launch( self, turbine_name ):
        #turbine_settings = Settings(turbine_name)
        VALVE, THROTTLE, SERVO, RELAY, POTENTIOMETER, REV_COUNTER, FLOWMETER, THERMOMETER,  MANOMETER, EXHAUST_SENSOR, CURRENT_METER, VOLTAGE_METER, FREQUENCY_METER =  kinds_list

        classes_map     = { THERMOMETER :Turbine.Measure_Device, 
                            MANOMETER: Turbine.Measure_Device, 
                            FLOWMETER: Turbine.Measure_Device, 
                            REV_COUNTER: Turbine.Rev_counter, 
                            EXHAUST_SENSOR: Turbine.Measure_Device,
                            CURRENT_METER: Turbine.Measure_Device,
                            VOLTAGE_METER: Turbine.Measure_Device,
                            FREQUENCY_METER: Turbine.Measure_Device,        
                            VALVE : Turbine.Gas_valve, 
                            THROTTLE: Turbine.Throttle, 
                            RELAY:Turbine.Switch_device, 
                            SERVO: Turbine.Wastegate,
                            POTENTIOMETER: Turbine.Starter_fan  
                            } 
                    
        Devices_creator =   File_read.Devices_creator()
        loaded_devices_data, devices_instances  = Devices_creator.prepare_devices_to_launch(devices_data, DEVICES_MAP_PATH, DEVICES_CHAR_PATH ,  classes_map )

        Turbine.d.set_labjack(loaded_devices_data)
        return devices_instances

    def Start_threads( self, devices_instances, recorder, exporter):

        launcher    = Threads_Manager.Measure_and_control()
        commander   = Threads_Manager.Command()

        measure_control_thread  =   threading.Thread(target = launcher.launch, args=(operating_devices, recorder, ) )
        command_thread          =   threading.Thread(target = commander.simple_command, args=(exporter, )) # LAter on we can add start commands
       
        measure_control_thread.start()      
        #command_thread.start()


#turbine_name = "Deutz_turbine"
turbine_name = "Mitsubishi_turbine"

starter = Start()

operating_devices = starter.Get_devices_to_launch(turbine_name)
recorder = Database_manage.Record() 
#exporter = Database_manage.Export( history_dir, operating_devices )   # sending history start_dir_list
exporter = None
starter.Start_threads( operating_devices, recorder, exporter)





