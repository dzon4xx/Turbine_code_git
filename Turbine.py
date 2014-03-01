import os
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


### NOTES To myself
# line 163 and 139!!


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
        self.value          =   0

    def run(self, other):

        voltage         =   d.read_AIN(self.channel)
        self.value      =   round(other.convert(voltage), 3)
        
        #self.show()
                                             
        client.set_value(self.dir, 'value', self.value)        
         
    def show(self):        
        print "kind {2} temp: {1} point: {0} channel: {3}  \n".format(self.point, self.value, self.kind, self.channel )
 
class Thermocouple(Device):
            
    def convert(self, voltage):

        if self.kind == 'K': return voltage#TCVoltsToTemp(6004, (voltage-1.4) , d.getTemperature())-273.15
        if self.kind == 'M': return random.randint(1, 10)
        else: return 0
                        
class Flowmeter(Device):
            
    def convert(self, voltage):

        if self.kind == 'gas': return voltage+5
        if self.kind == 'air': return voltage+10
        else: return 0

class Manometer(Device):
            
    def convert(self, voltage):

        if self.kind == 'M': return voltage#TCVoltsToTemp(6004, (voltage-1.4) , d.getTemperature())-273.15
        else: return 0

class Exhaust_sensor(Device):
            
    def convert(self, voltage):

        if self.kind == 'E': return voltage#TCVoltsToTemp(6004, (voltage-1.4) , d.getTemperature())-273.15
        else: return 0

class Rev_counter(Device):

    def __init__(self, point, kind, channels, dir):

        Device.__init__(self, point, kind, channels, dir)
        self.channel = channels[0]
        d.counters_port.append(channels[0])

    def run(self, other):

        self.reset_counter()
        start = time.time()
        d.exec_counter(self.channel)
        time.sleep(0.3)
        count = d.exec_counter(self.channel)
        value = count/(time.time()-start)


        client.set_value(self.dir, 'value', self.value )        
       
    def reset_counter(self):
        'Resets internal labjack hardware counter'
        d.reset_counter(self.channel)
        self.count = 0   
                                    
class Gas_valve(Device):
    
    def __init__(self, point, kind, channels, dir):
        #super(Valve, self).__init__(self, point, kind, channels, dir)
        self.clock_port     =   channels[0]
        d.valve_pulse_port  =   channels[0]
        self.dir_port       =   channels[1]
        self.enable_port    =   channels[2]

        self.point          =   point
        self.kind           =   kind
        self.device_type    =   dir[-1]       
        self.dir            =   client.get_dir(dir)
        self.history_dir    =   None

        self.record_id      =   0
        self.value          =   0

        self.cycle_time     =   1.05
        self.position       =   client.get_attr( self.dir, 'value' ) ### Position must be known with the initlialization

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
        self.position   =   end_position
        print "V-Valve position {0}".format(self.position)
        self.enable(False)
                           
    def run (self, other):

        percent = client.get_attr( self.dir, 'value' )         ## later on must check if percent is (0%, 100%) range
        if percent != self.position:
            #set_valve = threading.Thread(target = self.set_valve, args =(percent,) )
            self.set_valve(end_position)

class Throttle():
    def __init__(self, point, kind, channels, dir):
        pass
    def run(self):
        pass

class Switch_device(Device):

    def __init__(self, point, kind, channels, dir):
        Device.__init__(self, point, kind, channels, dir)
        self.state = 0
    def run (self, other):

        new_state = client.get_attr( self.dir, 'value' )         ## later on must check if percent is (0%, 100%) range
        if new_state != self.state:
            d.set_DO(self.channel, new_state)
            self.state = deepcopy(new_state)

class Oil_pump(Switch_device):

    def __init__(self, point, kind, channels, dir):
        Switch_device.__init__(self, point, kind, channels, dir)


class Ignition(Switch_device):

    def __init__(self, point, kind, channels, dir):
        Switch_device.__init__(self, point, kind, channels, dir)


class Wastegate():
        
    def run(self):
        pass


    
        