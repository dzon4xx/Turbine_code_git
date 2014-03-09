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
        dir                 =   ['Turbine', 'Points', 'P'+str(self.point), self.name] 
        self.dir            =   client.get_dir(dir)

        self.history_dir    =   None

        self.record_id      =   0
        self.value          =   client.get_attr( self.dir, 'value' ) 

    def show(self, value):        
        print "kind {2} value: {1} point: {0} channel: {3}  \n".format(self.point, value, self.kind, self.channel )

class Measure_Device(Device):

    def __init__(self, device_attrs):
        Device.__init__(self, device_attrs)
        self.channel    =   device_attrs[CHANNELS][AIN]
        try:
            char            =   device_attrs[CHARACTERISTIC]
            self.convert    =   self.interpol_char(char)
        except KeyError:
            if self.kind == 'K': 
                self.convert    =   self.thermo_conv()

    def run(self, caller):

        sum_value = 0.
        sum_iter = 0
        start = time.time()

        if caller.type == ANALOG:
            analog_measure_device = True
        else:
            analog_measure_device = False
             
        while True:
                                      
            if analog_measure_device:
                self.value          =   d.read_AIN(self.channel)                
            else:
                self.value          =   caller.get_frequency()

            sum_value = sum_value + self.value
            sum_iter += 1
            time.sleep(avarage_time)    

            if time.time()-start > sleep_time:

                mean_value =  sum_value/sum_iter

                if analog_measure_device:
                    conv_mean_value  =   caller.convert(mean_value)

                conv_mean_value =   round(conv_mean_value, 3)
                self.show(conv_mean_value )
                sum_value = 0.
                sum_iter = 0
                                                             
                client.set_value(self.dir, 'value', conv_mean_value)
                start = time.time()

    def interpol_char(self, char):

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

    def thermo_conv(self):
        voltage = 0
        def convert(voltage):               
            return TCVoltsToTemp(LJ_ttK, voltage , 294)-273.15

                    
class Rev_counter(Measure_Device):

    def __init__(self, device_attrs):

        Measure_Device.__init__(self, device_attrs)
        self.channel    =   device_attrs[CHANNELS]
        d.counters_port.append(self.channel)

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
    def __init__(self, device_attrs):
        Device.__init__(self, device_attrs)
        self.position       =   deepcopy(self.value)

    def set_value(self, new_value, caller):
        if caller.kind == 'G':
            caller.set_valve(new_value)

class Gas_valve(Regulated_device):
    
    def __init__(self, device_attrs):
        Regulated_device.__init__(self, device_attrs)

        self.clock_port     =   device_attrs[CHANNELS][DIO][0]
        self.dir_port       =   device_attrs[CHANNELS][DIO][1]
        self.enable_port    =   device_attrs[CHANNELS][DIO][2]

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

       def __init__(self, d, angle_channel, freq, pwm_mode):

            self.freq           =     float(freq)
            self.angle_channel  =     angle_channel   
            self.angle          =     self.voltage_to_angle(d.readRegister(self.angle_channel))
            self.baseValue      =     65535
            self.pwm_mode       =     pwm_mode
            self.d              =     d
            self.set_labjack(d )


       def voltage_to_angle(self, voltage):
 
            angle_max   =   90
            voltage_max =   4.3

            angle    =   float(voltage/voltage_max)*angle_max
            return angle

class Wastegate(Regulated_device):

        def __init__(self, d):

            self.baseValue      =     65535
            self.freq           =     325.516 # from osciloskope

            #self.PWM_zero      =     0.0015*self.freq*self.baseValue
            self.PWM_minus45    =   0.001*self.freq*self.baseValue
            self.PWM_plus45     =   0.002*self.freq*self.baseValue
            self.min_angle      =   -90
            self.max_angle      =   +90
     
            self.position       =     0
     
            self.d              =     d
            self.set_labjack( d )

        def set_angle(self, d, angle):

            if angle < self.min_angle or angle > self.max_angle:
                print "Angle must be between -45deg and 45deg"
                raise ValueError

            else:

                PWM = self.baseValue - (self.PWM_minus45 + ((self.PWM_plus45-self.PWM_minus45)/(self.max_angle-self.min_angle))*(angle-self.min_angle))
                    
                AddRequest(d.handle, LJ_ioPUT_TIMER_VALUE, 0, PWM, 0, 0)  
                GoOne(d.handle)
                return PWM


class Switch_device(Control_device):
    'Class defining atribute state for Switch devices. Handles change of state'
    def __init__(self, device_attrs,):
        Device.__init__(self, device_attrs,)
        self.state  =   deepcopy(self.value)

    def set_value(self, new_state, caller):
        d.set_DO(self.channel, new_state)
        self.state = new_state

        print "-new state of {0} is {1}".format(caller.kind, new_state)
                                               




    
        