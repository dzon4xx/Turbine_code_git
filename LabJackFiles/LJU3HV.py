import u3 #imports the library provided by the produce

#print u3.openAllU3()#future module for multiple device operation 

d = u3.U3() #start the single device with all the defaults
#d.debug=True
d.getCalibrationData()#calibration of measuring device

ConfigList=[]
for b in range (0,13):
    ConfigList.append(b)

def ConfigurationFile (Directory=None):
    
    '''
    Desc: Creates the configuration file in given directory or in the one of the driver    
    Ex: 
    >>> LJU3HV.ConfigurationFile ('C:\Users\Dom\Desktop)    
    '''
    
    Check=None#remains None if the file is not open
    if Directory==None:
        
        try:
            ConfigFile=open ('config.txt','w')
            Check=1
        except IOError:
            print 'The file was not open in the default directory'
    else: 
        
        try:
            ConfigFile=open(Directory+'\config.txt','w')
            Check=1
        except IOError:
            print 'The file was not open in the specified directory'
    
    if Check is not None:#if the file was not open the operation will not procede
        
        for LineNum in range (0,4):
            ConfigFile.write('AIN%d\tMode:AI\tNegChan:SE\tLongSettle:F\tQuickSample:F\tProperty:Temp%d\tUnit:C\tP_min:0\tP_max:10\tV_min[V]:-10.3\tV_max[V]:10.3\t|\n' %(LineNum,LineNum))#separate style for AIN0-3
        for LineNum in range (4,8):
            ConfigFile.write('FIO%d\tMode:AI\tNegChan:SE\tLongSettle:F\tQuickSample:F\tProperty:Temp%d\tUnit:C\tP_min:0\tP_max:10\tV_min[V]:0\tV_max[V]:2.44\tDig:L\t|\n' %(LineNum,LineNum))#FIO4-7
        for LineNum in range (8,10):
            ConfigFile.write('AO%d\tProperty:Valve%d\tUnit:Percents\tP_min:0\tP_max:100\tP_current:0\tV_min[V]:0\tV_max[V]:5\tBits:8\t|\n' %(LineNum-8, LineNum-8))#in 16bit mode 0(no value) yields 5 V
        ConfigFile.write('PinOffset:4\tTimersEnabled:0\tClockBase[MHZ]:48\tDivisorPresent:T\tDivisor:1\t|\n') #1st step of DIO configuration
        for LineNum in range (10,12):
            ConfigFile.write('Timer%d\tUpadateReset:F\tValue:0\tMode:0\t|Counter%d\tEnabled:F\t|\n' %(LineNum-10,LineNum-10))

        ConfigFile.close()

def ReadConfiguration(Directory=None):
    
    '''  
    Desc: Reads the configuration file in given directory or inthe one of the driver and outputs the list of configuration data
    
    Ex: 
    >>> LJU3HV.ReadConfiguration ('C:\Users\Dom\Desktop')
    
    [
     ['AIN0', 'Mode:AI', 'NegChan:SE', 'LongSettle:F', 'QuickSample:F', 'Property:Temp0', 'Unit:C', 'P_min:0', 'P_max:10', 'V_min[V]:-10.3', 'V_max[V]:10.3', '|\n'], 
     ['AIN1', 'Mode:AI', 'NegChan:SE', 'LongSettle:F', 'QuickSample:F', 'Property:Temp1', 'Unit:C', 'P_min:0', 'P_max:10', 'V_min[V]:-10.3', 'V_max[V]:10.3', '|\n'],
     ['AIN2', 'Mode:AI', 'NegChan:SE', 'LongSettle:F', 'QuickSample:F', 'Property:Temp2', 'Unit:C', 'P_min:0', 'P_max:10', 'V_min[V]:-10.3', 'V_max[V]:10.3', '|\n'],
     ['AIN3', 'Mode:AI', 'NegChan:SE', 'LongSettle:F', 'QuickSample:F', 'Property:Temp3', 'Unit:C', 'P_min:0', 'P_max:10', 'V_min[V]:-10.3', 'V_max[V]:10.3', '|\n'],
     ['FIO4', 'Mode:AI', 'NegChan:SE', 'LongSettle:F', 'QuickSample:F', 'Property:Temp4', 'Unit:C', 'P_min:0', 'P_max:10', 'V_min[V]:0', 'V_max[V]:2.44', 'Dig:L', '|\n'],
     ['FIO5', 'Mode:AI', 'NegChan:SE', 'LongSettle:F', 'QuickSample:F', 'Property:Temp5', 'Unit:C', 'P_min:0', 'P_max:10', 'V_min[V]:0', 'V_max[V]:2.44', 'Dig:L', '|\n'],
     ['FIO6', 'Mode:AI', 'NegChan:SE', 'LongSettle:F', 'QuickSample:F', 'Property:Temp6', 'Unit:C', 'P_min:0', 'P_max:10', 'V_min[V]:0', 'V_max[V]:2.44', 'Dig:L', '|\n'],
     ['FIO7', 'Mode:AI', 'NegChan:SE', 'LongSettle:F', 'QuickSample:F', 'Property:Temp7', 'Unit:C', 'P_min:0', 'P_max:10', 'V_min[V]:0', 'V_max[V]:2.44', 'Dig:L', '|\n'], 
     ['AO0', 'Property:Valve0', 'Unit:', 'P_min:0', 'P_max:100', 'P_current:0', 'V_min[V]:0', 'V_max[V]:5', 'Bits:8', '|\n'],
     ['AO1', 'Property:Valve1', 'Unit:', 'P_min:0', 'P_max:100', 'P_current:0', 'V_min[V]:0', 'V_max[V]:5', 'Bits:8', '|\n'],
     ['PinOffset:4', 'TimersEnabled:0', 'ClockBase[MHZ]:48', 'DivisorPresent:T', 'Divisor:1', '|\n'], 
     ['Timer0', 'UpadateReset:F', 'Value:0', 'Mode:0', '|Counter0', 'Enabled:F', 'Reset:F', '|\n'], 
     ['Timer1', 'UpadateReset:F', 'Value:0', 'Mode:0', '|Counter1', 'Enabled:F', 'Reset:F', '|\n']
    ]
    ''' 
    
    Check=None
    if Directory==None:
        
        try:
            ConfigFile=open ('config.txt','r')
            Check=1
        except IOError:
            print 'The file was not found in the default directory'
            
    else: 
        try:
            ConfigFile=open(Directory+'\config.txt','r')
            Check=1
        except IOError:
            print 'The file was not found in the specified directory'
    
    if Check is not None:#the same chedking procedure as in ConfigurationFile()
        
        for b in range (0,13):
            ConfigLine=ConfigFile.readline()#reading the configuration data
            ConfigList[b]=ConfigLine.split('\t')#addition of elements to the ConfigList
    
        ConfigFile.close()
    
    return ConfigList
        

def ReadAnalogInputAll(ConfigList=[]):
    
    '''
    Desc: Basing on the configuration file reads the voltage of all pins set as analog input.
    Subsequently converts the voltage to units of the particular property and returns the database (list of dictionaries) with all results and description
    
    Ex: 
    >>> LJU3HV.ReadAnalogInputAll(ConfigList=LJU3HV.ReadConfiguration())

    [
     {'V_max': 1.5, 'Pin': 0, 'V_min': 0.5, 'P_actual': 47.941696839407086, 'P_min': 30.0, 'P_max': 50.0, 'V_actual': 1.3970848419703543, 'Remarks': 'Proper scaling', 'Property': 'Pressure1', 'NegChan': 'SE', 'Unit': 'P'}, 
     {'V_max': 10.3, 'Pin': 1, 'V_min': -10.3, 'P_actual': 5.683407634677529, 'P_min': 0.0, 'P_max': 10.0, 'V_actual': 1.407819727435708, 'Remarks': 'Proper scaling', 'Property': 'Temp', 'NegChan': 'SE', 'Unit': 'C'}, 
     {'V_max': -1.2, 'Pin': 2, 'V_min': -1.6, 'P_actual': -19.0, 'P_min': -20.0, 'P_max': -19.0, 'V_actual': 1.397304239217192, 'Remarks': 'Scale exceeded, the value signed to the highest possible', 'Property': 'FanPower', 'NegChan': 'SE', 'Unit': 'W'}, 
     {'V_max': 10.3, 'Pin': 3, 'V_min': -10.3, 'P_actual': 5.678479240741581, 'P_min': 0.0, 'P_max': 10.0, 'V_actual': 1.3976672359276563, 'Remarks': 'Proper scaling', 'Property': 'Temp', 'NegChan': 'SE', 'Unit': 'C'}, 
     {'V_max': 2.44, 'Pin': 4, 'V_min': 0.0, 'P_actual': 1.5265470357291155, 'P_min': 0.0, 'P_max': 10.0, 'V_actual': 0.3724774767179042, 'Remarks': 'Proper scaling', 'Property': 'Temp', 'NegChan': 'SE', 'Unit': 'C'}, 
     {'Pin': 'Pin 5 is not an AIN'}, 
     {'V_max': 2.44, 'Pin': 6, 'V_min': 0.0, 'P_actual': 1.3394892171834458, 'P_min': 0.0, 'P_max': 10.0, 'V_actual': 0.3268353689927608, 'Remarks': 'Proper scaling', 'Property': 'Temp', 'NegChan': 'SE', 'Unit': 'C'}, 
     {'V_max': 2.44, 'Pin': 7, 'V_min': 0.0, 'P_actual': 1.4354794135424078, 'P_min': 0.0, 'P_max': 10.0, 'V_actual': 0.35025697690434754, 'Remarks': 'Proper scaling', 'Property': 'Temp', 'NegChan': 'SE', 'Unit': 'C'}
    ]    
    '''
    
    ainValues =[]
    ResultsList=[]
    
    fioAn=0
    for b in range (0,8):    
        
        if ConfigList[b][1] =='Mode:AI':#if the pin is to be analog input
            fioAn+=2**b
            
    d.configIO(FIOAnalog = fioAn)#bringing appropriate terminal to AIN
    
    for b in range (0,8):
        
        Results=[]
                 
        #checking the nagetive channel for AIN terminals
        if ConfigList[b][1] =='Mode:AI':
            
            if ConfigList[b][2] =='NegChan:SE':
                NegChanInt=31
                Results.append('SE')
            elif ConfigList[b][2] =='NegChan:SR':
                NegChanInt=32
                Results.append('SR')
                
            else:
                NegChanInt =int(ConfigList[b][2][8])
                Results.append(NegChanInt)
                            
            #checking if LongSetting should be activated
            LongSet =False #default value 
            if ConfigList[b][3][11]=='T': #ConfigList [b][3][11]=='F' by default
                LongSet =True
            else:
                pass
                                    
            #checking if Quick Sampling should be activated - same as above
            QSample =False
            if ConfigList[b][4][12]=='T':
                QSample=True
            else:
                pass
            
            #measurement of the voltage according to the settings
            ainValues.append(d.getAIN(posChannel=b, negChannel=NegChanInt, longSettle=LongSet, quickSample=QSample))
            
            #preparing the file to be returned
            Results.append(ainValues[b])
            Results.append(b)
            
            PropertyList=ConfigList[b][5].split(':') #splitting 'Property:'
            Results.append(PropertyList[1])#adding the second element to the dictionary
            
            UnitList=ConfigList[b][6].split(':') #splitting 'Unit:'
            Results.append(UnitList[1])#adding the second element to the dictionary
                        
            P_minList=ConfigList[b][7].split(':')
            P_min=float(P_minList[1])# to number
            Results.append(P_min)#the same as above for P_min (but number conversion)
                        
            P_maxList=ConfigList[b][8].split(':')
            P_max=float(P_maxList[1])# to number
            Results.append(P_max)#the same as above for P_max
            
            V_minList=ConfigList[b][9].split(':')
            V_min=float(V_minList[1])# to number
            Results.append(V_min)#the same as above for V_min
                        
            V_maxList=ConfigList[b][10].split(':')
            V_max=float(V_maxList[1])# to number
            Results.append(V_max)#the same as above for V_max
                        
            #scaling
            Scale_P=P_max-P_min
            Scale_V=V_max-V_min
            ActualValue= P_min +(ainValues[b]-V_min)/Scale_V*Scale_P
            
            #checking if P_min<ActualValue<P_max; otherwise changing
            if ActualValue>P_max:
                ActualValue=P_max
                Results.append(ActualValue)
                Results.append('Scale exceeded, the value signed to the highest possible')
            
            elif ActualValue <P_min:
                ActualValue=P_min
                Results.append(ActualValue)
                Results.append('Scale exceeded, the value signed to the lowest possible')
            
            else: 
                 Results.append(ActualValue)
                 Results.append('Proper scaling')
           
            ResultsKeys=['NegChan', 'V_actual', 'Pin', 'Property', 'Unit', 'P_min', 'P_max','V_min', 'V_max', 'P_actual', 'Remarks']
            print "Value on pin %d is  %0.4f V" % (b, ainValues[b])
            print ('\n')
        
        else:
            Results.append('Pin %d is not an AIN' %(b))
            ResultsKeys =['Pin']
            ainValues.append(b)
            print "No analog input"
        
        #making the dictionary
        ResultsList.append(dict(zip(ResultsKeys, Results)))
        
    return ResultsList
    

def ReadAnalogInputOne(ConfigList=[], CheckedProperty=None):
    
    '''
    Desc: Basing on the configuration file reads the voltage of ONE pin to which the signal of measured
    property is conected. Then returns the wanted magnitude.
    
    Ex: 
    >>> LJU3HV.ReadAnalogInputOne(ConfigList=LJU3HV.ReadConfiguration(), CheckedProperty='Pressure')
    
    47.941696839407086
    '''
    ActualValue=None   
    fioAn=0
    if CheckedProperty is not None:
        
        for b in range (0,8):
        
            PropertyList=ConfigList[b][5].split(':') #splitting 'Property:'
        
            if PropertyList[1] ==CheckedProperty:
            
                fioAn+=2**b# in order to bring pin to AIN
                if ConfigList[b][1] =='Mode:AI':
                    
                    d.configIO(FIOAnalog = fioAn)#bringing the pin to AIN
                    
                    if ConfigList[b][2] =='NegChan:SE':#checking the negative channel
                        NegChanInt=31
                        
                    elif ConfigList[b][2] =='NegChan:SR':
                        NegChanInt=32               
                    
                    else:
                        NegChanInt =int(ConfigList[b][2][8])
                    
                    #Long Settling - as in ReadAnalogInputALL
                    LongSet =False 
                    if ConfigList[b][3][11]=='T':
                         LongSet =True
                    else:
                        pass
                                    
                    #Quick Sample
                    QSample =False#
                    if ConfigList[b][4][12]=='T':
                        QSample=True
                    else:
                        pass
                    
                    #measurement of the voltage according to the settings
                    ainValue=d.getAIN(posChannel=b, negChannel=NegChanInt, longSettle=LongSet, quickSample=QSample)
                                        
                    #data needed for scaling
                    P_minList=ConfigList[b][7].split(':')
                    P_min=float(P_minList[1])# to number
                    
                    P_maxList=ConfigList[b][8].split(':')
                    P_max=float(P_maxList[1])# to number
                    
                    V_minList=ConfigList[b][9].split(':')
                    V_min=float(V_minList[1])# to number
                                    
                    V_maxList=ConfigList[b][10].split(':')
                    V_max=float(V_maxList[1])# to number
                                    
                    #scaling
                    Scale_P=P_max-P_min
                    Scale_V=V_max-V_min
                    ActualValue= P_min +(ainValue-V_min)/Scale_V*Scale_P#minimal voltage is 0 ainValues-0=ainValues
                    
                    #checking if P_min<ActualValue<P_max
                    if ActualValue>P_max:
                        ActualValue=P_max
                        print 'Scale exceeded, the value signed to the highest possible'
                        
                    elif ActualValue <P_min:
                        ActualValue=P_min
                        print 'Scale exceeded, the value signed to the lowest possible'
                    else:
                        print 'Proper scaling'
                
                else:
                    print 'The pin number %d set for reading property %s is not an anlog one' (b, CheckedProperty)
        
    return ActualValue


def ReadTemp(inK=False):
    
    if inK is True:
        temp=d.getTemperature()
    
    else:
        temp= d.getTemperature()-273.15
    
    return temp
    
    
def AnalogOutput(ConfigList=[]):
    
    '''
    Desc: Sets voltage on DAC0 and DAC1 as configured - the voltage is evaluated basing on
    P_current, P_max, P_min, V_max, V_min -> linear calculation.
    
    Ex: 
    >>> LJU3HV.AnalogOutput(ConfigList=LJU3HV.ReadConfiguration())
    """ where LJU3HV.ReadConfiguration()[8]==['AO0', 'Property:Valve', 'Unit:', 'P_min:0', 'P_max:100', 'P_current:50', 'V_min[V]:0', 'V_max[V]:5', 'Bits:8', '|\n'])"""
    
    VoltageLevel= V_min+ (P_current-P_min)/(P_max-P_min)*(V_max-V_min)=0+(50-0)/(100-0)*(5-0)2.5
    The voltage on DAC0 is set to 2.5 V.
    '''
    
    VoltageMinList=[]
    VoltageMaxList=[]
    P_minList=[]
    P_maxList=[]
    P_realList=[]
    
    for b in range (0,2):
                          
        P_minList.append(ConfigList[b+8][3].split(':'))#trick with splitting and the convertion to number
        P_min=float(P_minList[b][1])
            
        P_maxList.append(ConfigList[b+8][4].split(':'))
        P_max=float(P_maxList[b][1])
        
        P_realList.append(ConfigList[b+8][5].split(':'))
        P_real=float(P_realList[b][1])
            
        VoltageMinList.append(ConfigList[b+8][6].split(':'))
        VoltageMin=float(VoltageMinList[b][1])
            
        VoltageMaxList.append(ConfigList[b+8][7].split(':'))
        VoltageMax=float(VoltageMaxList[b][1])
        
        #voltage scale validation
        if VoltageMax >5:
            print 'The proposed maximal voltage on DAC %d is greater than 5 V\nThe voltage cannot be set' %(b)
            break #The loop must be broken
        else:
            pass
        
        if VoltageMax <0:
            print 'The proposed maximal voltage on DAC %d is less than 0 V\nThe voltage cannot be set' %(b)
            break
        else:
            pass
        
        if VoltageMin >5:
            print 'The proposed minimal voltage on DAC %d is greater than 5 V\nThe voltage cannot be set' %(b)
            break
        else:
            pass
        
        if VoltageMin <0:
            print 'The proposed minimal voltage on DAC %d is less than 0 V\nThe voltage cannot be set' %(b)
            break
        else:
            pass
            
        VoltageLevel= VoltageMin + (P_real-P_min)/(P_max-P_min)*(VoltageMax-VoltageMin)
        
        #checking whether P is within the range, if not the value must be reassigned
        if P_real > P_max:
            print 'The set value corresponding to DAC %d is greater than the maximal one\nThe voltage was set to Vmax' % (b)
            VoltageLevel=VoltageMax
        else:
            pass
        
        if P_real < P_min:
            print 'The set value corresponding to DAC %d is smaller than the minimal one\nThe voltage was set to Vmin' % (b)
            VoltageLevel=VoltageMin
        else:
            pass
                
        if ConfigList[b+8][8]=='Bits:16':
            #Because of the error            
            if VoltageLevel==0:
                d.getFeedback(u3.DAC8(Dac=b, Value=d.voltageToDACBits(volts=VoltageLevel, dacNumber=b, is16Bits=False)))
            else:
                d.getFeedback(u3.DAC16(Dac=b, Value=d.voltageToDACBits(volts=VoltageLevel, dacNumber=b, is16Bits=True)))
        elif ConfigList[b+8][8]=='Bits:8':
            d.getFeedback(u3.DAC8(Dac=b, Value=d.voltageToDACBits(volts=VoltageLevel, dacNumber=b, is16Bits=False)))
        else:
            pass
        
        
def AnalogOutputOneValue(ConfigList=[], PropertyChanged=None, PropertyValue=None):
        
    '''
    Desc: Sets voltage on a particular pin with particular property to the configured level.
    The voltage is evaluated basing on PropertyValue, P_max, P_min, V_max, V_min - linear calculation.
    
    Ex: 
    >>> LJU3HV.AnalogOutputOneValue(LJU3HV.ReadConfiguration(),
    PropertyChanged=FirstValve, PropertyValue=80)
    """ the following element of LJU3HV.ReadConfiguration() is considered: ['AO0', 'Property:FirstValve', 'Unit:', 'P_min:50', 'P_max:100', 'P_current:50', 'V_min[V]:0', 'V_max[V]:5', 'Bits:8', '|\n'])"""
    
    VoltageLevel= V_min+ (PropertyValue-P_min)/(P_max-P_min)*(V_max-V_min)=0+(80-50)/(100-50)*(5-0)=3.0
    The voltage on DAC0 is set to 3.0 V
    
    !!!Please note that DAC0 was chosen because of the folowing list elements : 'AO0', 'Property:FirstValve'
    and that the value of property is given by the user, not read from the file!!!.
    '''
    
    if PropertyChanged is not None:       
        
        for b in range (0,2):
            
            PropertyList=ConfigList[b+8][1].split(':')
            if PropertyList[1] ==PropertyChanged:
                
                #PropertyValue =float(PropertyValue)                
                if PropertyValue is not None:
                    
                    P_minList=ConfigList[b+8][3].split(':')#trick with splitting
                    P_min=float(P_minList[1])
                    
                    P_maxList=ConfigList[b+8][4].split(':')#trick with splitting
                    P_max=float(P_maxList[1])
                    
                    VoltageMinList=ConfigList[b+8][6].split(':')
                    VoltageMin=float(VoltageMinList[1])
                    
                    VoltageMaxList=ConfigList[b+8][7].split(':')
                    VoltageMax=float(VoltageMaxList[1])
                    
                    #voltage scale validation
                    if VoltageMax >5:
                        print 'The proposed maximal voltage on DAC %d is greater than 5 V\nThe voltage cannot be set' %(b)
                        break #The loop must be broken
                    else:
                        pass
        
                    if VoltageMax <0:
                        print 'The proposed maximal voltage on DAC %d is less than 0 V\nThe voltage cannot be set' %(b)
                        break
                    else:
                        pass
        
                    if VoltageMin >5:
                        print 'The proposed minimal voltage on DAC %d is greater than 5 V\nThe voltage cannot be set' %(b)
                        break
                    else:
                        pass
        
                    if VoltageMin <0:
                        print 'The proposed minimal voltage on DAC %d is less than 0 V\nThe voltage cannot be set' %(b)
                        break
                    else:
                        pass
                    
                    VoltageLevel= VoltageMin+ (PropertyValue-P_min)/(P_max-P_min)*(VoltageMax-VoltageMin)
                    print VoltageLevel
                    
                    #checking if P is within the range, if not the value must be reassigned
                    if PropertyValue > P_max:
                        print 'The  given value corresponding to DAC %d is greater than the maximal one\nThe voltage was set to Vmax' % (b)
                        VoltageLevel=VoltageMax
                    else:
                        pass
        
                    if PropertyValue < P_min:
                        print 'The set value corresponding to DAC %d is smaller than the minimal one\nThe voltage was set to Vmin' % (b)
                        VoltageLevel=VoltageMin
                    else:
                        pass
                
                    if ConfigList[b+8][8]=='Bits:16':
                        d.getFeedback(u3.DAC16(Dac=b, Value=d.voltageToDACBits(volts=VoltageLevel, dacNumber=b, is16Bits=True)))
                    elif ConfigList[b+8][8]=='Bits:8':
                        d.getFeedback(u3.DAC8(Dac=b, Value=d.voltageToDACBits(volts=VoltageLevel, dacNumber=b, is16Bits=False)))
                    else:
                        pass
                    
                else:
                    print ('Please set some value')
                                
    else:
        print ('Not configured properly')


def AnalogOutputOnePercentage(ConfigList=[], PropertyChanged=None, PercentsVoltageAvailable=None):
    
    '''
    Desc: Sets voltage on a particular pin with particular property to the configured level.
    The voltage is evaluated basing on  P_max, P_min, V_max, V_min and PercentsVoltageAvailable- linear calculation.
    
    Ex: 
    >>> LJU3HV.AnalogOutput(ConfigList=LJU3HV.ReadConfiguration(), PropertyChanged=FirstValve, PercentsVoltageAvailable=30)
    """ the following element of LJU3HV.ReadConfiguration() is considered: ['AO0', 'Property:FirstValve', 'Unit:', 'P_min:50', 'P_max:100', 'P_current:50', 'V_min[V]:1', 'V_max[V]:3', 'Bits:8', '|\n'])"""
    
    VoltageLevel= V_min+ PercentsVoltageAvailable/100*(VoltageMax-VoltageMin)=1+80/100*(3-1)*=2.6
    The voltage on DAC0 is set to 2.6 V
    
    !!!Please note that DAC0 was chosen because of the folowing list elements : 'AO0', 'Property:FirstValve'!!!
    '''
        
    if PropertyChanged is not None:       
        
        for b in range (0,2):
            
            PropertyList=ConfigList[b+8][1].split(':')
            if PropertyList[1] ==PropertyChanged:
                
                #PropertyValue =float(PropertyValue)                
                if PercentsVoltageAvailable is not None:
                    
                    VoltageMinList=ConfigList[b+8][6].split(':')
                    VoltageMin=float(VoltageMinList[1])
                    
                    VoltageMaxList=ConfigList[b+8][7].split(':')
                    VoltageMax=float(VoltageMaxList[1])
                    
                    #voltage scale validation
                    if VoltageMax >5:
                        print 'The proposed maximal voltage on DAC %d is greater than 5 V\nThe voltage cannot be set' %(b)
                        break #The loop must be broken
                    else:
                        pass
        
                    if VoltageMax <0:
                        print 'The proposed maximal voltage on DAC %d is less than 0 V\nThe voltage cannot be set' %(b)
                        break
                    else:
                        pass
        
                    if VoltageMin >5:
                        print 'The proposed minimal voltage on DAC %d is greater than 5 V\nThe voltage cannot be set' %(b)
                        break
                    else:
                        pass
        
                    if VoltageMin <0:
                        print 'The proposed minimal voltage on DAC %d is less than 0 V\nThe voltage cannot be set' %(b)
                        break
                    else:
                        pass                    
                    
                    VoltageLevel= VoltageMin+ float(PercentsVoltageAvailable)/100*(VoltageMax-VoltageMin)
                   
                
                    if ConfigList[b+8][8]=='Bits:16':
                        d.getFeedback(u3.DAC16(Dac=b, Value=d.voltageToDACBits(volts=VoltageLevel, dacNumber=b, is16Bits=True)))
                    elif ConfigList[b+8][8]=='Bits:8':
                        d.getFeedback(u3.DAC8(Dac=b, Value=d.voltageToDACBits(volts=VoltageLevel, dacNumber=b, is16Bits=False)))
                    else:
                        pass
                    
                else:
                    print ('Please set some value')
                                
    else:
        print ('Not configured properly')


def AnalogOutputOneGiveVoltageProperty (ConfigList=[], PropertyChanged=None, Voltage=None):
        
    '''
    Desc: Sets voltage on a particular pin with particular property to the configured level.
    The pin is identified with the property given in the configuration file, while the voltage is set from the keyboard.
    
    Ex: 
    >>> LJU3HV.AnalogOutput(ConfigList=LJU3HV.ReadConfiguration(), PropertyChanged=FirstValve, Voltage=2.50)
    """ the following element of LJU3HV.ReadConfiguration() is considered: ['AO0', 'Property:FirstValve', 'Unit:', 'P_min:50', 'P_max:100', 'P_current:50', 'V_min[V]:1', 'V_max[V]:3', 'Bits:8', '|\n'])"""
    
    The voltage on DAC0 is set to 2.5 V
    
    '''
    
    if PropertyChanged is not None:       
        
        for b in range (0,2):
            
            PropertyList=ConfigList[b+8][1].split(':')
            if PropertyList[1] ==PropertyChanged:
                
                #PropertyValue =float(PropertyValue)                
                if Voltage is not None:
                    
                    VoltageLevel= Voltage
                    
                    #voltage scale validation
                    if Voltage >5:
                        print 'The proposed voltage on pin DAC %d is greater than 5 V\nThe voltage cannot be set' %(b)
                        break #The loop must be broken
                    else:
                        pass
        
                    if Voltage <0:
                        print 'The proposed voltage on pin DAC %d is less than 0 V\nThe voltage cannot be set' %(b)
                        break
                    else:
                        pass
                    if ConfigList[b+8][8]=='Bits:16':
                        d.getFeedback(u3.DAC16(Dac=b, Value=d.voltageToDACBits(volts=VoltageLevel, dacNumber=b, is16Bits=True)))
                    elif ConfigList[b+8][8]=='Bits:8':
                        d.getFeedback(u3.DAC8(Dac=b, Value=d.voltageToDACBits(volts=VoltageLevel, dacNumber=b, is16Bits=False)))
                    else:
                        pass
                    
                else:
                    print ('Please set some value')
                                
    else:
        print ('Not configured properly')


def AnalogOutputOneGiveVoltagePin (Pin=None, Voltage=None, Bits=None):
        
    '''
    Desc: Sets voltage on a particular pin with particular property to the configured level.
    All pin, volatge and resolution are set from the keyboard.
    
    Ex: 
    >>> LJU3HV.AnalogOutput(Pin=1, Voltage=1.57, Bits=8)
    
    The voltage on DAC1 is set to 1.57 V
    
    '''
    
    if Pin is None:
        print 'No pin is given'
    else:
        pass
    
    if Voltage is not None:
                    
                    
        #voltage scale validation
        if Voltage >5:
            print 'The proposed voltage on pin DAC %d is greater than 5 V\nThe voltage was set to 5' %(Pin)
            Voltage=5
        else:
            pass
        
        if Voltage <0:
            print 'The proposed voltage on pin DAC %d is less than 0 V\nThe voltage was set to 0' %(Pin)
            Voltage =0
        else:
            pass
        VoltageLevel=Voltage
        
        if Bits==16:
            d.getFeedback(u3.DAC16(Dac=Pin, Value=d.voltageToDACBits(volts=VoltageLevel, dacNumber=Pin, is16Bits=True)))
        elif Bits==8:
            d.getFeedback(u3.DAC8(Dac=Pin, Value=d.voltageToDACBits(volts=VoltageLevel, dacNumber=Pin, is16Bits=False)))
        else:
            print 'The number of bits should be either 8 or 16'
                    
    else:print ('Please set some value')
        

def AnalogOutputOneGiveVoltagePin16bits (Pin=None, Voltage=None):
        
    '''
    Desc: Sets voltage on a particular pin with particular property to the configured level.
    All pin and voltage are set from the keyboard. The resolution is 16 bits.
    
    Ex: 
    >>> LJU3HV.AnalogOutput(Pin=1, Voltage=2.06)
    
    The voltage on DAC1 is set to 2.06 V
    
    '''
    
    if Pin is None:
        print 'No pin is given'
    else:
        pass
    
    if Voltage is not None:
                    
                    
        #voltage scale validation
        if Voltage >5:
            print 'The proposed voltage on pin DAC %d is greater than 5 V\nThe voltage was set to 5' %(Pin)
            Voltage=5
        else:
            pass
        
        if Voltage <0:
            print 'The proposed voltage on pin DAC %d is less than 0 V\nThe voltage was set to 0' %(Pin)
            Voltage =0
        else:
            pass
        VoltageLevel=Voltage
        
        d.getFeedback(u3.DAC16(Dac=Pin, Value=d.voltageToDACBits(volts=VoltageLevel, dacNumber=Pin, is16Bits=True)))
                    
    else:print ('Please set some value')


def AnalogOutputOneGiveVoltagePin8bits (Pin=None, Voltage=None):
        
    '''
    Desc: Sets voltage on a particular pin with particular property to the configured level.
    All pin and voltage are set from the keyboard. The resolution is 8 bits.
    
    Ex: 
    >>> LJU3HV.AnalogOutput(Pin=0, Voltage=2.06)
    
    The voltage on DAC0 is set to 2.06 V
    
    '''
    
    if Pin is None:
        print 'No pin is given'
    else:
        pass
    
    if Voltage is not None:
                    
                    
        #voltage scale validation
        if Voltage >5:
            print 'The proposed voltage on pin DAC %d is greater than 5 V\nThe voltage was set to 5' %(Pin)
            Voltage=5
        else:
            pass
        
        if Voltage <0:
            print 'The proposed voltage on pin DAC %d is less than 0 V\nThe voltage was set to 0' %(Pin)
            Voltage =0
        else:
            pass
        VoltageLevel=Voltage
        
        d.getFeedback(u3.DAC8(Dac=Pin, Value=d.voltageToDACBits(volts=VoltageLevel, dacNumber=Pin, is16Bits=False)))
                    
    else:print ('Please set some value')
        
        
def TimersCountersSettings(ConfigList=[]):
    
    '''
    Desc: The function responsible for setting pins to be timers, counter, digital input and ouput.
    The argument for this function can be changed.
    
    PinOffset:4	TimersEnabled:0	ClockBase[MHZ]:48	DivisorPresent:T	Divisor:1	|
    Timer0	UpadateReset:F	Value:0	Mode:0	|Counter0	Enabled:F	Reset:F	|
    Timer1	UpadateReset:F	Value:0	Mode:0	|Counter1	Enabled:F	Reset:F	|
    
    For more information please check sections 2.8 an 2.9 of LabJack U3 User's guide
    
    Ex: 
    >>> LJU3HV.AnalogOutput(ConfigList=LJU3HV.ReadConfiguration ('C:\Users\Dom\Desktop\config.txt'))  
    '''
    
    fioAn=255
    EC0=None
    EC1=None
    TimerReset=False
    Base=None
    TimerValue=0
    TimerMode=0
    
    TimerResults=[]
    TimerResultsList=[]
    
    for b in range (4,8):    
        
        if ConfigList[b][1] !='Mode:AI':
            fioAn-=2**b
            
       
    if fioAn!=255:
        
        OffsetList=ConfigList[10][0].split(':')#checking what the pinoffset is
        Offset=int(OffsetList[1])
         
        TimersEnabledList=ConfigList[10][1].split(':')#checking what the pinoffset is
        TimersEnabled=int(TimersEnabledList[1])
        
        if ConfigList[11][5] =='Enabled:T':#enabling of counter 0
            EC0=True
        if ConfigList[12][5] =='Enabled:T':#enabling of counter 1
            EC1=True
        
               
        d.configIO(FIOAnalog=fioAn,TimerCounterPinOffset = Offset, EnableCounter1 = EC1, EnableCounter0 = EC0, NumberOfTimersEnabled = TimersEnabled)
        
        ClockBaseList=ConfigList[10][2].split(':')#checking what the base clock
        
        #default for TimerClockDivisor
        DivisorList=ConfigList[10][4].split(':')
        Divisor=int(DivisorList[1])
        
        
        if ConfigList[10][3]=='DivisorPresent:F':
            
            Divisor =None
            
            if ClockBaseList[1]=='4':# for 1MHZ
                Base=0
            elif ClockBaseList[1]=='12':# for 1MHZ
                Base=1
            if ClockBaseList[1]=='48':# for 1MHZ
                Base=2
        
        elif ConfigList[10][3]=='DivisorPresent:T':
            
            if ClockBaseList[1]=='1':# for 1MHZ
                Base=3
            elif ClockBaseList[1]=='4':# for 1MHZ
                Base=4
            elif ClockBaseList[1]=='12':# for 1MHZ
                Base=5
            if ClockBaseList[1]=='48':# for 1MHZ
                Base=6
        # setting of the clockbase and the possible divisor
        
        
        if Base is not None:
            
            
            d.configTimerClock(TimerClockBase = Base, TimerClockDivisor = Divisor)
        
            for b in range (0,2):
            
                if ConfigList[b+11][1]=='UpdateReset:T':
                    TimerReset=True
                else:
                        pass
                TimerResults.append(Base)
                TimerResults.append(Divisor)
    
                TimerValueList=ConfigList[b+11][2].split(':')
                TimerValue=int(TimerValueList[1])
                TimerResults.append(TimerValue)
            
                TimerModeList=ConfigList[b+11][3].split(':')
                TimerMode=int(TimerModeList[1])
                TimerResults.append(TimerMode)
            
                if b< TimersEnabled:
                    
                    TimerKeys=['Base', 'Divisor', 'TimerValue', 'TimerMode', 'Timer', 'Read']
                    TimerResults.append(b)
                    
                    print 'Output of timer %d is' %(b)
                    print d.getFeedback(u3.Timer(timer = b, UpdateReset = TimerReset, Value=TimerValue, Mode = TimerMode))                    
                    TimerResults.append(d.getFeedback(u3.Timer(timer = b, UpdateReset = TimerReset, Value=TimerValue, Mode = TimerMode)))
                    
                else:
                    TimerKeys=['Timer', 'Read']
                    TimerResults= [b, 'No reading']
                    
                    print 'Timer %d is not enabled' %(b)
                
                TimerResultsList.append(dict(zip(TimerKeys, TimerResults)))
                
        else: print 'Wrong clock cofiguration'
    
    return TimerResultsList
        

def ResetCounter (Counter=None):
    
    '''
    Desc: Performs a reset of the chosen counter 
    !!! Before using it make sure than the counter is really enabled!!!
       
    Ex: 
    >>> LJU3HV.ResetCounter(0)
    
    Conter 0 was reset
    '''
    
    if Counter is not None:
        d.getFeedback(u3.Counter(counter = Counter, Reset = True))
    else:
        print 'No counter specified'


def ResetCounter0 ():
    
    '''
    Desc: Performs a reset of counter0 
    !!! Before using it make sure than the counter is really enabled!!!
     
    Ex: 
    >>> LJU3HV.ResetCounter0()
    
    Conter 0 was reset
    '''
    
    d.getFeedback(u3.Counter0( Reset = True)) 
        

def ResetCounter1 ():
    
    '''
    Desc: Performs a reset of counter1 
    !!! Before using it make sure than the counter is really enabled!!!
      
    Ex: 
    >>> LJU3HV.ResetCounter1()
    
    Conter 1 was reset
    '''
    
    d.getFeedback(u3.Counter1( Reset = True))
    
    
def ReadCounter (Counter=None):
    
    '''
    Desc: Reads the chosen counter 
    !!! Before using it make sure than the counter is really enabled!!!
       
    Ex: 
    >>> LJU3HV.ResetCounter(0)
    []
    '''
    CounterResult=None
    if Counter is not None:
        CounterResult=d.getFeedback(u3.Counter(counter = Counter, Reset = True))
    else:
        print 'No counter specified'
    
    return CounterResult


def ReadCounter0 ():
    
    '''
    Desc: Reads counter0 
    !!! Before using it make sure than the counter is really enabled!!!
     
    Ex: 
    >>> LJU3HV.ResetCounter0()
    []
    Conter 0 was reset
    '''
    
    return d.getFeedback(u3.Counter0( Reset = True)) 
        

def ReadCounter1 ():
    
    '''
    Desc: Read counter1 
    !!! Before using it make sure than the counter is really enabled!!!
      
    Ex: 
    >>> LJU3HV.ResetCounter1()
    []
    '''
    
    return d.getFeedback(u3.Counter1( Reset = True))

        
def DigitalInputOutputAll(ConfigList=[]):
        
    '''
    Desc: The function that sets FIO pins (4-7) to be either digital input or output. In the latter
    case both high (3.4 V)or low (0 V) can be specified in the configuration file. The function returns
    a list of states of all the aforementioned pins: 
    
    0 - digital input LOW, 1 - digital input HIGH 
    and 2 - the particular pin is not digital input 
    
    !!! Remember not to use this function for the pins AIN0-3!!!
    
       
    Ex: 
    >>> LJU3HV.DigitalInputOutputAll(LJU3HV.ReadConfiguration ('C:\Users\Dom\Desktop))
    
    """
    FIO4	Mode:DI	NegChan:SE	LongSettle:F	QuickSample:F	Property:Temp4	Unit:C	P_min:0	P_max:10	V_min[V]:0	V_max[V]:2.44	Dig:L	|
    FIO5	Mode:AI	NegChan:SE	LongSettle:F	QuickSample:F	Property:out1	Unit:C	P_min:0	P_max:10	V_min[V]:0	V_max[V]:2.44	Dig:L	|
    FIO6	Mode:DO	NegChan:SE	LongSettle:F	QuickSample:F	Property:Temp6	Unit:C	P_min:0	P_max:10	V_min[V]:0	V_max[V]:2.44	Dig:H	|
    FIO7	Mode:DO	NegChan:SE	LongSettle:F	QuickSample:F	Property:Temp7	Unit:C	P_min:0	P_max:10	V_min[V]:0	V_max[V]:2.44	Dig:H	|
    """ 
    
    [0,2,2,2]
    '''
   
    fioAn=255
    DIResults=[2,2,2,2]    
    
    for b in range (4,8):    
        
        if ConfigList[b][1] !='Mode:AI':
            fioAn-=2**b
        
    d.configIO(FIOAnalog = fioAn)

    for b in range (4,8):
        
        if ConfigList[b][1]=='Mode:DI':
            
            d.getFeedback(u3.BitDirWrite(b, 0))
            
            if d.getFeedback(u3.BitStateRead(b))==[1]:
                DIResults[b-4]=1
            
            elif d.getFeedback(u3.BitStateRead(b))==[0]:
                DIResults[b-4]=0
            
            else:
                pass# 2 given by the defaults means it is not digtal input
        
        elif ConfigList[b][1]=='Mode:DO':
            
            print ConfigList[b][11]
            
            d.getFeedback(u3.BitDirWrite(b, 1))
            
            if ConfigList[b][11]=='Dig:L':
                d.getFeedback(u3.BitStateWrite(b, 0))
            
            if ConfigList[b][11]=='Dig:H':
                d.getFeedback(u3.BitStateWrite(b, 1))    

    return DIResults        


def DigitalOutputOnePin(Pin=None, LowHigh=None):
        
    '''
    Desc: Sets on pin (FIO4-7) to be digital output. In such a case either high (3.4 V)
    or low (0 V) should be specified.
    !!! Remember not to use this function for pin AIN0-3!!!
        
    Ex: 
    >>> LJU3HV.DigitalInputOutputOnePin(Pin=5, LowHigh='H')
    
    Pin 5 was set to high digital output(3.4 V)
    '''
   
    if Pin is not None:
        
        d.configIO(FIOAnalog = (255-2**Pin))

        d.getFeedback(u3.BitDirWrite(Pin, 1))
        
        if LowHigh=='H':
            d.getFeedback(u3.BitStateWrite(Pin, 1))
        
        elif LowHigh=='L':
            d.getFeedback(u3.BitStateWrite(Pin, 0))
        
        else:
            print ('For digital output set if it is about to be high or low')
    else:
        print 'No pin specified'


def DigitalInputOnePin(Pin=None):
        
    '''
    Desc: Sets on pin (FIO4-7) to be digital input. Returns 1 for digital high and 0 for
    digital low.
        
    Ex: 
    >>> LJU3HV.DigitalInputOnePin(Pin=5)
    1
    
    Pin 5 is a digital inout connected to high signal
    '''
    
    LogicState=None    
    if Pin is not None:
        
        d.configIO(FIOAnalog = (255-2**Pin))
        
        d.getFeedback(u3.BitDirWrite(Pin, 0))
        
        if d.getFeedback(u3.BitStateRead(Pin))==[1]:
            LogicState=1
            
        elif d.getFeedback(u3.BitStateRead(Pin))==[0]:
            LogicState=0
            
        else:
            print 'Something went wrong - it is neither low nor high'
        
    else:
        print 'No pin specified'
        
    return LogicState
            

def DigitalOutputOneProperty(ConfigList=[], Property=None, LowHigh=None):
        
    '''
    Desc: Sets on pin (FIO4-7) to be digital output. In such a case either high (3.4 V)
    or low (0 V) should be specified.
    !!! Remember not to use this function for AIN0-3!!!
        
    Ex: 
    >>> LJU3HV.DigitalInputOutputOnePin(ConfigList=LJU3HV.ReadConfiguration(), Property='AirTemp',  LowHigh='H')
    
    """the following element of LJU3HV.ReadConfiguration() is considered:
    ['FIO5', 'Mode:AI', 'NegChan:SE', 'LongSettle:F', 'QuickSample:F', 'Property:AirTemp', 'Unit:C', 'P_min:0', 'P_max:10', 'V_min[V]:0', 'V_max[V]:2.44', 'Dig:L', '|\n']"""
    
    Pin 5 was set to high digital output(3.4 V) notwithstanding that according to the configuration
    file this pin was about to be analog input. However the only relevant information taken from the
    aforementioned file is the name of the property.
    '''
    
    Checker = None    
    for b in range (4,8):
        
        PropertyList=ConfigList[b][5].split(':')
        if Property == PropertyList[1]:
            
            d.configIO(FIOAnalog = (255-2**b))
            
            Checker = PropertyList[1]
            d.getFeedback(u3.BitDirWrite(b, 1))
                
            if LowHigh=='H':
                d.getFeedback(u3.BitStateWrite(b, 1))
            elif LowHigh=='L':
                d.getFeedback(u3.BitStateWrite(b, 0))
            else:
                print ('For digital output set if it is about to be high or low')
        
    if Checker is None:
        print 'No property chosen at all'


def DigitalInputOneProperty(ConfigList=[], Property=None):
        
    '''
    Desc: Sets on pin (FIO4-7) to be digital input. Returns 1 for digital high and 0 for
    digital low.
    !!! Remember not to use this function for AIN0-3!!!
        
    Ex: 
    >>> LJU3HV.DigitalInputOutputOnePin(ConfigList=LJU3HV.ReadConfiguration(), Property='AirTemp')
    """the following element of LJU3HV.ReadConfiguration() is considered:
    ['FIO5', 'Mode:AI', 'NegChan:SE', 'LongSettle:F', 'QuickSample:F', 'Property:AirTemp', 'Unit:C', 'P_min:0', 'P_max:10', 'V_min[V]:0', 'V_max[V]:2.44', 'Dig:L', '|\n']"""
    
    1
    '''
    
    a=None
    Checker = None    
    for b in range (4,8):
        
        PropertyList=ConfigList[b][5].split(':')
        if Property == PropertyList[1]:
            
            d.configIO(FIOAnalog = (255-2**b))
            
            Checker = PropertyList[1]
            d.getFeedback(u3.BitDirWrite(b, 0))
                
            if d.getFeedback(u3.BitStateRead(b))==[1]:
                State=1
            
            elif d.getFeedback(u3.BitStateRead(b))==[0]:
                State=0
                
            else:
                print 'Something went wrong - it is neither low nor high'
        
    if Checker is None:
        print 'No property chosen at all'
    
    return State


    

    
     

            
        
    
    
        
    
   
    
       
        

