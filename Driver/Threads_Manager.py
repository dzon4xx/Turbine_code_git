import threading
# -*- coding: utf-8 -*-

import Turbine_devices
import Database_manage

class Measure_and_control():

    def __init__(self,):        
        pass

    def launch(self, operating_devices):
        print "MEASURE_AND_CONTROL: START"
        db_manager    =   Database_manage.Database_manager()
        db_manager.set_devices_present_dir(operating_devices) 
        db_manager.set_devices_history_dir(operating_devices)
            

        for device in operating_devices:           
            device_run = threading.Thread( target = device.run, args=( ) )
            device_run.start()

        
              
        record_thread = threading.Thread( target = db_manager.record, args= (operating_devices, ) )
        #record_thread.start()


class Command():
    """ Finally the aim of the class will be to interface with GUI """
    def __init__( self ):       
        self.name = "Command Thread: "
                                       
    def simple_command( self ):
        print "-COMMAND: START"
        
        ### na razie ustawiamy na sztywno ktore punkty zapisujemy.
        export_points_list = ['0', '1', '2', '3', '4'] 
        while True:
            print "\n{0} -Type command".format(self.name)
            command             =   raw_input()
            print self.name + "-Your command is {0}".format(command) 
            if command == "s":
                print self.name + "Saving history to file"
                header, data = exporter.get_export_data( export_points_list )
                exporter.save_export_data( "test.txt" , header, data)

               

           
            
