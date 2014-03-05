import math
import time
import numpy as np

from scipy import interpolate 
from copy import deepcopy
    
import Nikitta

from LabJackFiles.Labjack_settings import LabJack
from LabJackFiles.LabJackPython import TCVoltsToTemp
from __init__ import *


d = LabJack()

class Device(object):

    def __init__(self, type, point, kind, channels, dir ):

        self.type           =   type
        self.point          =   point
        self.kind           =   kind
        self.channel        =   channels[0]             
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

            analog_measure_device = self.check_caller_type(caller)
                                      
            if analog_measure_device:
                self.value          =   d.read_AIN(self.channel)                
            else:
                self.value          =   caller.get_frequency()

            sum_value = sum_value + self.value
            sum_iter +=1
            time.sleep(avarage_time)    

            if time.time()-start > sleep_time:

                mean_value =  sum_value/sum_iter

                if analog_measure_device:
                    conv_mean_value  =   caller.convert(mean_value)

                conv_mean_value =   round(conv_mean_value, 3)
                #self.show()
                sum_value = 0.
                sum_iter = 0
                                                             
                client.set_value(self.dir, 'value', conv_mean_value)
                start = time.time()
       
    def check_caller_type(self, caller):

        if hasattr( caller, 'convert'):               
            analog_measure_device = True
        else:
            analog_measure_device = False
            
        return analog_measure_device
                  
class Thermocouple(Measure_Device):

    def __init__(self, type, point, kind, channels, dir, char):
        Device.__init__(self, type, point, kind, channels, dir)
        self.gen_conv_fun()
            
    def gen_conv_fun(self, ):

        if self.kind == 'K': self.convert = lambda voltage: voltage#TCVoltsToTemp(6004, (voltage-1.4) , d.getTemperature())-273.15
        if self.kind == 'M': self.convert = lambda voltage: 0

                        
class Flowmeter(Measure_Device):
    
    def __init__(self, type, point, kind, channels, dir, char):
        Device.__init__(self, type, point, kind, channels, dir)
        self.gen_conv_fun()

            
    def gen_conv_fun(self, ):

        if self.kind == 'gas': self.convert = lambda voltage: 0
        if self.kind == 'air': 
            y = np.array([8, 10, 15, 30, 60, 120, 250, 370, 480])           
            x = np.array([1.2390, 1.3644, 1.5241, 1.8748, 2.3710, 2.9998, 3.7494, 4.1695, 4.4578])
            self.convert = interpolate.InterpolatedUnivariateSpline(x, y)

class Manometer(Measure_Device):
    
    def __init__(self, type, point, kind, channels, dir, char):
        Device.__init__(self, type, point, kind, channels, dir)
        self.gen_conv_fun(char)
            
    def gen_conv_fun(self, char):

        if self.kind == 'I':
            x = np.array(char.x) 
            y = np.array(char.y)                       
            self.convert = interpolate.interp1d(x, y, kind='linear')

                    
        elif self.kind == 'B': self.convert = lambda voltage: 0


class Exhaust_sensor(Measure_Device):
            
    def convert(self, voltage):

        if self.kind == 'E': return voltage#TCVoltsToTemp(6004, (voltage-1.4) , d.getTemperature())-273.15
        else: return 0

class Rev_counter(Measure_Device):

    def __init__(self, type, point, kind, channels, dir):

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
    def __init__(self, type, point, kind, channels, dir):
        Device.__init__(self, type, point, kind, channels, dir)
        self.position       =   deepcopy(self.value)

    def set_value(self, new_value, caller):
        if caller.kind == 'G':
            caller.set_valve(new_value)

class Gas_valve(Regulated_device):
    
    def __init__(self, type, point, kind, channels, dir):
        Regulated_device.__init__(self, point, kind, channels, dir)

        self.clock_port     =   channels[0]
        d.valve_pulse_port  =   channels[0]
        self.dir_port       =   channels[1]
        self.enable_port    =   channels[2]

        self.cycle_time     =   1.05 # wyciagnac na zewnatrz
        
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
        # open loop
        """Sets valve for specific position"""
        end_position = int(end_position)

        if end_position < 0 or end_position > 100:
            raise Exception("V-position must be set between 0 and 100")
            #constrain 
              
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
    pass

class Wastegate(Regulated_device):
    pass


class Switch_device(Control_device):
    'Class defining atribute state for Switch devices. Handles change of state'
    def __init__(self, type, point, kind, channels, dir,):
        Device.__init__(self, type, point, kind, channels, dir,)
        self.state  =   deepcopy(self.value)

    def set_value(self, new_state, caller):
        d.set_DO(self.channel, new_state)
        self.state = new_state

        print "-new state of {0} is {1}".format(caller.kind, new_state)
                                               
class Oil_pump(Switch_device):
    pass

class Ignition(Switch_device):
    pass




    
        