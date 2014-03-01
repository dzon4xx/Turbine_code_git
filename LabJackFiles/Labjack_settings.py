import u3, ue9
from LabJackFiles.LabJackPython import *      
try:
    d = ue9.UE9()
    labjack_class = ue9.UE9
    d.close()
except:

    d = u3.U3()
    labjack_class = u3.U3
    d.close()

class LabJack(labjack_class):

        def __init__(self, ):
            self.d = labjack_class()
            self.offset =   4

            self.counters_port = []
            self.valve_pulse_port = None

        def set_labjack(self):
            """ labjack setting for proper valve work."""

            ### Valve
            try: 
                divisor = 7
                AddRequest(self.d.handle,  LJ_ioPUT_CONFIG,  LJ_chTIMER_COUNTER_PIN_OFFSET, self.valve_pulse_port, 0, 0) 
                AddRequest(self.d.handle,  LJ_ioPUT_CONFIG,  LJ_chTIMER_CLOCK_BASE, LJ_tc48MHZ, 0, 0) 
                AddRequest(self.d.handle,  LJ_ioPUT_CONFIG,  LJ_chTIMER_CLOCK_DIVISOR, divisor, 0, 0)
        
                AddRequest(self.d.handle,  LJ_ioPUT_CONFIG,  LJ_chNUMBER_TIMERS_ENABLED, 1, 0, 0) 
                #Configure Timer0 as 8-bit PWM.  Frequency will be 1M/256 = 3906 Hz. 
                AddRequest(self.d.handle, LJ_ioPUT_TIMER_MODE, 0, LJ_tmPWM8, 0, 0) 
                AddRequest(self.d.handle, LJ_ioPUT_TIMER_VALUE, 0, 31777, 0, 0)
            except TypeError as e:
                print "-Labjack: [{e}] occured becasue Valve ports are not set in mpa file".format(**locals())

            
            try:
                for port in self.counters_port: 
                    AddRequest(self.d.handle, LJ_ioPUT_COUNTER_ENABLE, port - self.offset, 1, 0, 0)
                    AddRequest(self.d.handle, LJ_ioPUT_COUNTER_RESET, port - self.offset, 1, 0, 0)

            except TypeError as e:
                print "-Labjack: [{e}] occured becasue Counter ports are not set in mpa file".format(**locals())
            
            GoOne(self.d.handle)

        def read_AIN(self, port):

            AddRequest (self.d.handle, LJ_ioGET_AIN, port, 0, 0, 0);
            GoOne( self.d.handle )
            result = GetFirstResult (self.d.handle)
            return result[2]

        def set_DO(self, port, state):

            AddRequest (self.d.handle, LJ_ioPUT_DIGITAL_BIT, port, state, 0, 0);
            GoOne( self.d.handle )

        def reset_counter(self, counter_channel):

            AddRequest (self.d.handle, LJ_ioPUT_COUNTER_RESET, counter_channel-self.offset, 1, 0, 0);
            GoOne (self.d.handle);

        def exec_counter(self, counter_channel):

            return eGet(self.d.handle, LJ_ioGET_COUNTER, counter_channel-self.offset, 0, 0 )