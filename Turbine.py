import sys
import random
import math
import time
import random
import threading
from copy import deepcopy
    
import Nikitta

from LabJackFiles.Labjack_settings import LabJack
from __init__ import *


d = LabJack()

class Device(object):

    def __init__(self, point, kind, channels, dir ):

        self.channel        =   channels[0]
        self.point          =   point
        self.kind           =   kind
        self.device_type    =   dir[-1]     
        self.dir            =   client.get_dir(dir)
        self.history_dir    =   None

        self.record_id      =   0
        self.value          =   client.get_attr( self.dir, 'value' ) 

    def show(self):        
        print "kind {2} value: {1} point: {0} channel: {3}  \n".format(self.point, self.value, self.kind, self.channel )


class Measure_Device(Device):

    def run(self, caller):

        sum_value = 0.
        sum_iter = 0
        start = time.time()

        while True:
            try:
                caller.convert
                analog_measure_device = True
            except AttributeError:
                analog_measure_device = False
            
            

            if analog_measure_device:
                voltage         =   d.read_AIN(self.channel)
                self.value      =   round(caller.convert(voltage), 3)
                sum_value = sum_value + self.value
                sum_iter +=1

            else:
                self.value      =   round(caller.get_frequency(), 3)
                value_table.append(self.value)
                sum_value = sum_value + self.value
                sum_iter +=1
                
            if time.time()-start > sleep_time:
                mean_value =  sum_value/sum_iter
                sum_value = 0.
                sum_iter = 0
                                 
                client.set_value(self.dir, 'value', self.value)
                start = time.time()
            
         
class Thermocouple(Measure_Device):
            
    def convert(self, voltage):

        if self.kind == 'K': return voltage#TCVoltsToTemp(6004, (voltage-1.4) , d.getTemperature())-273.15
        if self.kind == 'M': return random.randint(1, 10)
        else: return 0
                        
class Flowmeter(Measure_Device):
            
    def convert(self, voltage):

        if self.kind == 'gas': return voltage+5
        if self.kind == 'air': return voltage+10
        else: return 0

class Manometer(Measure_Device):
            
    def convert(self, voltage):

        if self.kind == 'M': return voltage#TCVoltsToTemp(6004, (voltage-1.4) , d.getTemperature())-273.15
        else: return 0

class Exhaust_sensor(Measure_Device):
            
    def convert(self, voltage):

        if self.kind == 'E': return voltage#TCVoltsToTemp(6004, (voltage-1.4) , d.getTemperature())-273.15
        else: return 0

class Rev_counter(Measure_Device):

    def __init__(self, point, kind, channels, dir):

        Measure_Device.__init__(self, point, kind, channels, dir)
        self.channel = channels[0]
        d.counters_port.append(channels[0])

        self.frequency  =   deepcopy(self.value)

    def get_frequency(self):

        self.reset_counter()
        start = time.time()
        d.exec_counter(self.channel)
        time.sleep(0.3)
        count = d.exec_counter(self.channel)
        self.frequency = count/(time.time()-start)
        return self.frequency
             
    def reset_counter(self):
        'Resets internal labjack hardware counter'
        d.reset_counter(self.channel)
        self.count = 0 
        
          
     
class Control_device(Device):
    'Class defining run method of controled devices'
    def run(self, caller):
        while True:
            new_value = client.get_attr( self.dir, 'value' )         ## later on must check if percent is (0%, 100%) range
            if new_value != self.value:
                caller.set_value(new_value, caller)
                self.value = new_value  
                      
       
class Regulated_device(Control_device):
    'Class defining atribute position for regulated devices. Handles apropriate method for setting value based on who is caller'
    def __init__(self, point, kind, channels, dir):
        Device.__init__(self, point, kind, channels, dir)
        self.position       =   deepcopy(self.value)

    def set_value(self, new_value, caller):
        if caller.kind == 'G':
            caller.set_valve(new_value)

class Gas_valve(Regulated_device):
    
    def __init__(self, point, kind, channels, dir):
        Regulated_device.__init__(self, point, kind, channels, dir)

        self.clock_port     =   channels[0]
        d.valve_pulse_port  =   channels[0]
        self.dir_port       =   channels[1]
        self.enable_port    =   channels[2]

        self.cycle_time     =   1.05
        
        self.enable( False )

    def enable(self, execute):
        """Enable or disable valve"""        
        d.set_DO(self.enable_port, execute)

    def open(self, execute):
        """ Open or close valve """            
        d.set_DO(self.dir_port, execute)
       
    def close_valve(self):
        """Completely close valve"""
        self.enable(True)
        self.open(False)
        time.sleep(1.2*self.cycle_time) # multiplication to be sure that valve is closed.
        self.enable(False)

        self.position   =   0
        
        return self.position

    def set_valve(self, end_position):

        """Sets valve for specific position"""
        end_position = int(end_position)

        if end_position < 0 or end_position > 100 or self.position==end_position:
            raise Exception("V-position must be set between 0 and 100")
              
        work_time = self.cycle_time*(float((math.fabs(end_position-self.position)))/100)
        print "V-work_time: ", work_time
        self.enable(True)

        if end_position > self.position:
            print "V-Valve is opening"
            self.open(True)
        if end_position < self.position:
            print "V-Valve is closing"
            self.open(False)
        time.sleep(work_time)               ## DANGEROUS CODE Delays all code        
        print "V-Valve position {0}".format(self.position)
        self.enable(False)

        self.position   =   end_position
                           
class Throttle(Regulated_device):

    def __init__(self, point, kind, channels, dir):
        Regulated_device.__init__(self, point, kind, channels, dir)

class Wastegate(Regulated_device):
        
    def __init__(self, point, kind, channels, dir):
        Regulated_device.__init__(self, point, kind, channels, dir)


class Switch_device(Control_device):
    'Class defining atribute state for Switch devices. Handles change of state'
    def __init__(self, point, kind, channels, dir):
        Device.__init__(self, point, kind, channels, dir)
        self.state  =   deepcopy(self.value)

    def set_value(self, new_state, caller):
        d.set_DO(self.channel, new_state)
        self.state = new_state

        print "-new state of {0} is {1}".format(caller.kind, new_state)
                                               
class Oil_pump(Switch_device):

    def __init__(self, point, kind, channels, dir):
        Switch_device.__init__(self, point, kind, channels, dir)

class Ignition(Switch_device):

    def __init__(self, point, kind, channels, dir):
        Switch_device.__init__(self, point, kind, channels, dir)




    
        