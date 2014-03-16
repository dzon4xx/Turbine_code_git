import math
import time
import numpy as np

from scipy import interpolate 
from copy import deepcopy
    
import Nikitta

from Labjack_settings import LabJack

from LabJackFiles.LabJackPython import TCVoltsToTemp, LJ_ttK 
from __init__ import *

d = LabJack()
class Device(object):

    def __init__(self, device_attrs ):

        self.id             =   device_attrs[ID]
        self.point          =   device_attrs[POINT]
        self.name           =   device_attrs[NAME]
        self.direction      =   device_attrs[DIRECTION]
        self.type           =   device_attrs[TYPE]
        self.kind           =   device_attrs[KIND]
        dir                 =   ['Turbine', 'Points', 'P'+str(self.point), self.kind] 
        self.dir            =   client.get_dir(dir)

        self.history_dir    =   None

        self.record_id      =   0
        self.value          =   client.get_attr( self.dir, 'value' ) 

    def show(self, value, sum_iter):        
        print "{2} value: {1} point: {0} iter: {3} \n".format(self.point, value, self.name, sum_iter )

class Measure_Device(Device):

    def __init__(self, device_attrs):

        Device.__init__(self, device_attrs)        
        self.device_attrs = device_attrs           
          
    def run(self):

        def get_convert_function(device_attrs):

            def interpol_char(char):

                x = np.array(char.x) 
                y = np.array(char.y)

                if len(char.x) == 2:
                    interpol_fun =  interpolate.interp1d(x, y, kind='linear')
                if len(char.x) > 2 and len(char.x) < 6:
                    k = len(char.x)-1
                    interpol_fun = interpolate.InterpolatedUnivariateSpline(x, y, k)
                if len(char.x) > 6:
                    k = 5                       
                    interpol_fun = interpolate.InterpolatedUnivariateSpline(x, y)

                return interpol_fun

            def thermocouple_conv():

                voltage = 0
                def convert(voltage):
                    #print "temp in convert: ",               
                    return TCVoltsToTemp(LJ_ttK, voltage , 292  )-273.15
                return convert

            if device_attrs[CHARACTERISTIC] != 0:
                char            =   device_attrs[CHARACTERISTIC]
                convert         =   interpol_char(char)
                return convert
            elif self.name == (THERMOCOUPLE_K): 
                convert    =   thermocouple_conv()
                return convert

            elif self.type == DIGITAL:
                def convert(value):
                    return value
                return convert

        def get_read_function(device_attrs):

            if self.type == ANALOG:
                self.channel    =   device_attrs[CHANNELS][AIN]  ## this line may slow down code
                try:
                    voffset     =   float(device_attrs[SETTINGS][VOFFSET])
                    gain        =   int(device_attrs[SETTINGS][GAIN])
                except KeyError:
                    voffset = 0
                    gain = 1
                                
                def read_value():                   
                    voltage = d.read_AIN(self.channel)
                    return (voltage-voffset)/gain
                return read_value

            elif self.kind == REV_COUNTER:   
                def read_value():
                    return self.get_frequency()
                return read_value

            elif self.name == LABJACK_TEMP_SENSOR:
                def read_value():
                    val = d.read_temp()
                    return val
                return read_value
        
        def sum_readings(sum_value, sum_iter):

            self.value  =   read()                
            sum_value = sum_value + self.value
            sum_iter += 1
            #time.sleep(avarage_time)
            return sum_value, sum_iter
         
        read       = get_read_function(self.device_attrs)
        convert    = get_convert_function(self.device_attrs)
        sum_value = 0.
        sum_iter = 0
        start = time.time()
        save_time    = float(self.device_attrs[SETTINGS][SAVE_TIME])    
             
        while True:                       
            sum_value, sum_iter = sum_readings(sum_value, sum_iter)

            if time.time()-start > save_time:

                mean_value =  sum_value/sum_iter
                conv_mean_value  =  convert(mean_value)
                conv_mean_value =   round(conv_mean_value, 3)
                self.show(conv_mean_value, sum_iter)
                sum_value = 0.
                sum_iter = 0
                                                             
                client.set_value(self.dir, 'value', mean_value)
                start = time.time()
                    
class Rev_counter(Measure_Device):

    def __init__(self, device_attrs):

        Device.__init__(self, device_attrs)
        self.device_attrs = device_attrs
        self.channel    =   device_attrs[CHANNELS][CIO]
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
    def run(self):
        while True:
            new_value = client.get_attr( self.dir, 'value' )         ## later on must check if percent is (0%, 100%) range
            if new_value != self.value:
                self.set_value(new_value)
                self.value = deepcopy(new_value)
                            
class Regulated_device(Control_device):
    'Class defining atribute position for regulated devices. Handles apropriate method for setting value based on who is caller'
    def __init__(self, device_attrs):
        Device.__init__(self, device_attrs)
        self.position       =   deepcopy(self.value)

        if self.kind == VALVE: 
            self.set_value  =  self.set_valve 
        elif self.kind == THROTTLE:
            self.set_value = self.set_throttle
        elif self.kind == SERVO:
            self.set_value = self.set_wastegate
        elif self.kind == POTENTIOMETER: 
             self.set_value  = self.set_starter_fan
           
class Gas_valve(Regulated_device):
    
    def __init__(self, device_attrs):
        Regulated_device.__init__(self, device_attrs)

        self.clock_port     =   device_attrs[CHANNELS][TIO]
        self.dir_port       =   device_attrs[CHANNELS][DIO][0]
        self.enable_port    =   device_attrs[CHANNELS][DIO][1]

        self.cycle_time     =   float(device_attrs[SETTINGS]['cycle_time']) # wyciagnac na zewnatrz
        
        self.enable( False )

    def enable(self, execute):
        """Enable or disable valve"""        
        d.set_DO(self.enable_port, execute)

    def close(self, direction):
        """ Open or close valve """            
        d.set_DO(self.dir_port, direction)
       
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
            raise Exception("[ERROR] {0}: position must be set between 0 and 100".format(self.name))
            #constrain 
              
        work_time = self.cycle_time*(float((math.fabs(end_position-self.position)))/100)
        print "{0}: work time: {1} ".format(self.name, work_time) 
        self.enable(True)

        if end_position > self.position:
            self.close(False)
        if end_position < self.position:
            self.close(True)
        time.sleep(work_time)               ## DANGEROUS CODE Delays all code
        self.enable(False)

        self.position   =   end_position        
        print "{0}: position {1}".format(self.name, self.position)

class Throttle(Regulated_device):

    def __init__(self, device_attrs):
        Regulated_device.__init__(self, device_attrs)
        self.PWM_channel    =   device_attrs[CHANNELS][TIO]
        self.angle_channel  =   device_attrs[CHANNELS][AIN]  
        
    def set_throttle(self, end_position):

        def voltage_to_angle(voltage):
 
            angle_max   =   90
            voltage_max =   4.3
            angle    =   float(voltage/voltage_max)*angle_max
            return angle

        def open(direction):

            open_pwm    =   7500
            close_pwm   =   65000
            if direction:
                d.set_PWM(self.PWM_channel, open_pwm)
            else:
                d.set_PWM(self.PWM_channel, close_pwm)

        if end_position != 0. and end_position != 1.:
            raise Exception("[ERROR] {0}: Throttle can be only set as 1 - open or 0 - closed".format(self.name))

        if end_position > self.position:            
            open(True)
            print "{0}: opened".format(self.name)
        else:            
            open(False)
            print "{0}: closing".format(self.name)
                                   
class Wastegate(Regulated_device):

        def __init__(self, device_attrs):
            Regulated_device.__init__(self, device_attrs)
            self.PWM_channel    =   device_attrs[CHANNELS][TIO]
            self.baseValue      =   65535
            self.freq           =   325.516 # from osciloskope

            self.PWM_minus45    =   0.001*self.freq*self.baseValue
            self.PWM_plus45     =   0.002*self.freq*self.baseValue
            self.min_angle      =   -90
            self.max_angle      =   +90     
            self.angle          =     0
     
        def set_wastegate(self, angle):

            if angle < self.min_angle or angle > self.max_angle:
                raise Exception("[ERROR] {0}: Wastegate can be only set between {1} and {2} degrees".format(self.name, self.min_angle, self.max_angle))

            else:

                PWM = self.baseValue - (self.PWM_minus45 + ((self.PWM_plus45-self.PWM_minus45)/(self.max_angle-self.min_angle))*(angle-self.min_angle))                    
                d.set_PWM(self.PWM_channel, PWM)
                self.angle = angle
                print "{0}: set to {1}".format(self.name, angle)

class Starter_fan(Regulated_device):

    def __init__(self, device_attrs):
        Regulated_device.__init__(self, device_attrs)
        self.switch_channel =   device_attrs[CHANNELS][DIO]
        self.DAC_channel    =   device_attrs[CHANNELS][DAC]

    def set_starter_fan(self, power):
        
        if power < 0 or power > 100:
            raise Exception("[ERROR] {0}:  can be only set between 0 and 100 POWER %".format(self.name))

        elif power > 0:
            d.set_DO(self.switch_channel, 1)
            voltage = 0.05*power
            d.set_AO(self.DAC_channel, voltage)
        else:
            d.set_DO(self.switch_channel, 0)
            d.set_AO(self.DAC_channel, 0)
 
class Switch_device(Control_device):
    'Class defining atribute state for Switch devices. Handles change of state'
    def __init__(self, device_attrs,):
        Device.__init__(self, device_attrs,)
        self.channel    =   device_attrs[CHANNELS][DIO]
        self.state  =   deepcopy(self.value)
        d.set_DO(self.channel, self.state )

    def set_value(self, new_state):
        d.set_DO(self.channel, new_state)
        self.state = new_state
        print "{0}: state is {1}".format(self.name, new_state)
                                               









    
        