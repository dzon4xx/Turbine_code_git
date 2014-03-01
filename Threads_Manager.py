import time
import threading
from __init__ import *
# -*- coding: utf-8 -*-

import Turbine
import Database_manage

class Measure_and_control():

    def __init__(self,):        
        pass

    def launch(self, operating_devices, recorder,):
        print "\n-Measure and control thread start"
        
        for device in operating_devices:
            device_run = threading.Thread( target = device.run, args=(device, ) )
            device_run.start()

        start = time.time()       
        while True:
            
            if time.time()-start > sleep_time:                      
                recorder.add_record(operating_devices)
                start = time.time()


class Command():
    """ Finally the aim of the class will be to interface with GUI """
    def __init__( self ):       
        self.name = "Command Thread: "
                                       
    def simple_command( self, exporter ):
        print "-Command thread start"
        
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

               

           
            
