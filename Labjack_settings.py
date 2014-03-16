import u3, ue9
from LabJackFiles.LabJackPython import * 
from __init__ import * 
     
try:
    d = ue9.UE9()
    labjack_class = ue9.UE9
    print "temp is:", d.getTemperature()
except:
    d = u3.U3()
    labjack_class = u3.U3

class LabJack(labjack_class):

        def __init__(self,):
            pass

        def set_labjack(self, devices_data):
            """ labjack setting for proper valve work."""
            mode_map  = {'PWM8': LJ_tmPWM8, 'PWM16': LJ_tmPWM16, 'freq_out': LJ_tmFREQOUT}
            read_resolution =   12
                                                     
            def set_timers_counters(devices_data):

                def set_timer(settings, channel):
                    value   = float(settings[VALUE])
                    mode    = mode_map[settings[MODE]]
                                
                    AddRequest(d.handle, LJ_ioPUT_TIMER_MODE, channel, mode, 0, 0) 
                    AddRequest(d.handle, LJ_ioPUT_TIMER_VALUE, channel, value , 0, 0)

                def set_counter(counter_num):

                    AddRequest(d.handle, LJ_ioPUT_COUNTER_ENABLE, counter_num, 1, 0, 0)
                    AddRequest(d.handle, LJ_ioPUT_COUNTER_RESET, counter_num, 1, 0, 0)

                timers_quantity = 0
                for one_kind_device_data in devices_data.itervalues():
                    for device_data in one_kind_device_data:

                        if device_data[TYPE] == DIGITAL_PULSE:
                            channel =   device_data[CHANNELS][TIO]
                            set_timer(device_data[SETTINGS], channel)
                            timers_quantity += 1

                        if device_data[KIND] == REV_COUNTER:
                            counter_num = device_data[CHANNELS][CIO]
                            set_counter(counter_num)

                return timers_quantity

            def main_settings():
                AddRequest(d.handle, LJ_ioPUT_CONFIG,  LJ_chTIMER_CLOCK_BASE, LJ_tc12MHZ_DIV, 0, 0) 
                AddRequest(d.handle, LJ_ioPUT_CONFIG, LJ_chTIMER_COUNTER_PIN_OFFSET, 0, 0, 0)   ## ofset domyslnie zerowy
                AddRequest(d.handle, LJ_ioPUT_CONFIG,  LJ_chNUMBER_TIMERS_ENABLED, timers_quantity, 0, 0)     ## Na podstawie ilosci urzadzen PWM ustawiamy ilosc timerow
                AddRequest(d.handle, LJ_ioPUT_CONFIG,  LJ_chTIMER_CLOCK_DIVISOR, 9, 0, 0)       #Ustawienie dzielnika dla zegara
                AddRequest(d.handle, LJ_ioPUT_CONFIG, LJ_chAIN_RESOLUTION, read_resolution, 0,0)             #Ustawienie rozdzielczosci odczytu analogowego np. 18bit
                AddRequest(d.handle, LJ_ioPUT_AIN_RANGE, 0, LJ_rgUNI5V, 0, 0)                   #Ustawienie zakresu odczytu np 0-5V

            ePut(d.handle, LJ_ioPIN_CONFIGURATION_RESET, 0, 0, 0)
            timers_quantity =   set_timers_counters(devices_data)            
            main_settings()
            GoOne(d.handle)
            print "LABJACK SETTER: Labjack setup complete!"

        def read_AIN(self, channel):

            AddRequest (d.handle, LJ_ioGET_AIN, channel, 0, 0, 0)
            GoOne( d.handle )
            result = GetFirstResult (d.handle)
            return result[2]

        def read_temp(self, ):
            return d.getTemperature()

        def set_DO(self, channel, state):

            AddRequest (d.handle, LJ_ioPUT_DIGITAL_BIT, channel, state, 0, 0)
            GoOne( d.handle )

        def set_AO(self, channel, voltage):
            ePut (d.handle, LJ_ioPUT_DAC, channel, voltage, 0)

        def reset_counter(self, counter_num):

            AddRequest (d.handle, LJ_ioPUT_COUNTER_RESET, counter_num, 1, 0, 0)
            GoOne (d.handle)

        def exec_counter(self, counter_num):
      
            return eGet(d.handle, LJ_ioGET_COUNTER, counter_num, 0, 0 )

        def set_PWM(self, channel, value):

            AddRequest(d.handle, LJ_ioPUT_TIMER_VALUE, channel, value , 0, 0)
            GoOne(d.handle)
