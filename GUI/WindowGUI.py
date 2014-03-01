# -*- coding: utf-8 -*-
"""
Created on Fri Feb 07 20:32:44 2014

@author: Patryk
"""

import sys, os
from time import sleep

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy as np
import pyqtgraph as pg

from TabPlotsGUI import PlotsTab
from ThreadGUI import ManagerGUI
from __init__ import *


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.dict_plot = {}
        self.tabWidget = QTabWidget()
        self.TurbineWidget = QWidget()
        self.PlotsWidget = QWidget()
        self.tabWidget.addTab(self.TurbineWidget, 'Turbine')
        self.tabWidget.addTab(self.PlotsWidget, 'Plots')

        self.TurbineWidget.setLayout(self.TurbineTab())
        
        self.PlotsTab = PlotsTab(self.dict_plot)
        self.PlotsWidget.setLayout(self.PlotsTab.layout) 
        
        layout = QVBoxLayout()
        layout.addWidget(self.tabWidget)
        self.setLayout(layout)
        self.setWindowTitle("Gas Turbine Project")
        
        self.manager = ManagerGUI(self)
        self.manager.prepare_operating_divaces()
        
        self.timer = QTimer()
        self.timer_auto = QTimer()
        self.connect(self.timer, SIGNAL("timeout()"), self.manager.launch)
        print "\n-GUI thread start"  
        self.timer.start(sleep_time*1000) 
               
        
    def TurbineTab(self):  
        addressText = QTextEdit() #to delete
        
        button = QPushButton()
        button.setText('Hej')
            
        layout_main = QGridLayout()
              
        layout_main.addLayout(self.TitleLayout(), 0, 0)
        layout_main.addLayout(self.SensorLabelLayout(), 0, 4, 4, 2, Qt.AlignTop)
        layout_main.addLayout(self.SliderLayout(), 1, 0, 2, 1)
        layout_main.addLayout(self.SchemeLayout(), 0, 1, 3, 3, Qt.AlignCenter)
        layout_main.addLayout(self.ButtonLayout(), 3, 0, 1, 4, Qt.AlignRight)
        
        return layout_main
        
        
    def TitleLayout (self):
        layout_title = QGridLayout()
        
        label_logo = QLabel('KNE')
        self.image_logo = QPixmap('images/kne.png')
        width = self.image_logo.width() * 0.04
        height = self.image_logo.height() * 0.04
        image = self.image_logo.scaled(width, height, Qt.KeepAspectRatio)        
        label_logo.setPixmap(image)  
        
        layout_title.addWidget(label_logo, 0, 0, Qt.AlignLeft)    
        
        return layout_title        
        
        
    def SensorLabelLayout (self):
        self.dict_label_sensor = {}
        box_radio = QGroupBox('Box')
    
        nt = 5
        for point in range(nt):
            self.dict_label_sensor['label_T' + str(point)] = SensorLabel('ST' + str(point), 'C')
            
        np = 3
        for point in range(np):
            self.dict_label_sensor['label_P' + str(point)] = SensorLabel('SP' + str(point), 'bar')
            
        nf = 2
        for point in range(nf):
            self.dict_label_sensor['label_F' + str(point + 1)] = SensorLabel('SF' + str(point + 1), 'm3/h')
            self.dict_label_sensor['label_V' + str(point + 1)] = SensorLabel('SV' + str(point + 1), 'RMP', mode = 'LCD')
        
        name_layout = QLabel("SENSORS")
        self.layout_sensors = QGridLayout()
        self.layout_sensors.addWidget(name_layout, 0, 0, 1, 6, Qt.AlignCenter)
        self.layout_sensors.addWidget(box_radio, 0, 0, 1, 1, Qt.AlignCenter)        
        for point in range(nt):
            self.layout_sensors.addWidget(self.dict_label_sensor['label_T' + str(point)].radio, point + 1, 0)
            self.layout_sensors.addWidget(self.dict_label_sensor['label_T' + str(point)].name, point + 1, 1)
            self.layout_sensors.addWidget(self.dict_label_sensor['label_T' + str(point)].value, point + 1, 2)
            self.layout_sensors.addWidget(self.dict_label_sensor['label_T' + str(point)].unit, point + 1, 3)
            
        for point in range(np):
            self.layout_sensors.addWidget(self.dict_label_sensor['label_P' + str(point)].radio, point + 1, 4)
            self.layout_sensors.addWidget(self.dict_label_sensor['label_P' + str(point)].name, point + 1, 5)
            self.layout_sensors.addWidget(self.dict_label_sensor['label_P' + str(point)].value, point + 1, 6)
            self.layout_sensors.addWidget(self.dict_label_sensor['label_P' + str(point)].unit, point + 1, 7)
            
        for point in range(nf):
            self.layout_sensors.addWidget(self.dict_label_sensor['label_F' + str(point + 1)].radio, point + 4, 4)
            self.layout_sensors.addWidget(self.dict_label_sensor['label_F' + str(point + 1)].name, point + 4, 5)
            self.layout_sensors.addWidget(self.dict_label_sensor['label_F' + str(point + 1)].value, point + 4, 6)
            self.layout_sensors.addWidget(self.dict_label_sensor['label_F' + str(point + 1)].unit, point + 4, 7)
            self.layout_sensors.addWidget(self.dict_label_sensor['label_V' + str(point + 1)].radio, point + 6, 4)
            self.layout_sensors.addWidget(self.dict_label_sensor['label_V' + str(point + 1)].name, point + 6, 5)
            self.layout_sensors.addWidget(self.dict_label_sensor['label_V' + str(point + 1)].value, point + 6, 6)
            self.layout_sensors.addWidget(self.dict_label_sensor['label_V' + str(point + 1)].unit, point + 6, 7)
        
        plot_main = pg.PlotWidget(name= 'Main plot')
        self.layout_sensors.addWidget(plot_main, 8, 0, 1, 8)
        self.dict_plot['curve_main'] = self.set_curve(plot_main)
            
        return self.layout_sensors
        
    def set_curve(self, plot):
        plot.setLabel('left', 'Checked')
        plot.setLabel('bottom', 'Time', units='s')
        plot.setXRange(0, 10)
        plot.setYRange(0, 10)
        curve = plot.plot()
        curve.setPen((200,200,100))
        return curve 
        
        
    def SliderLayout (self):
        self.layout_sliders = QGridLayout()
        
        name1_slider_throttle = QLabel('Air')
        name2_slider_throttle = QLabel('Throttle')        
        self.value_slider_throttle = QLCDNumber()
        self.value_slider_throttle.setFixedHeight(30)
        self.value_slider_throttle.setFixedWidth(50)
        self.value_slider_throttle.setNumDigits(2)
        self.slider_air_throttle = QSlider(Qt.Vertical)
        
        name1_slider_valve = QLabel('Gas')
        name2_slider_valve = QLabel('Valve')        
        self.value_slider_valve = QLCDNumber()
        self.value_slider_valve.setFixedHeight(30)
        self.value_slider_valve.setFixedWidth(50)
        self.value_slider_valve.setNumDigits(2)
        self.slider_gas_valve = QSlider(Qt.Vertical)
        
        self.layout_sliders.addWidget(name1_slider_throttle, 0, 0, Qt.AlignCenter)
        self.layout_sliders.addWidget(name2_slider_throttle, 1, 0, Qt.AlignCenter)
        self.layout_sliders.addWidget(self.slider_air_throttle, 2, 0)
        self.layout_sliders.addWidget(self.value_slider_throttle, 3, 0)
        self.layout_sliders.addWidget(name1_slider_valve, 0, 1, Qt.AlignCenter)
        self.layout_sliders.addWidget(name2_slider_valve, 1, 1, Qt.AlignCenter)
        self.layout_sliders.addWidget(self.slider_gas_valve, 2, 1)
        self.layout_sliders.addWidget(self.value_slider_valve, 3, 1)
        
        self.connect(self.slider_air_throttle, SIGNAL("valueChanged(int)"), self.set_position_slider_throttle)
        self.connect(self.slider_gas_valve, SIGNAL("valueChanged(int)"), self.set_position_slider_valve)
        
        return self.layout_sliders
        
    def set_position_slider_throttle(self):
        value = self.slider_air_throttle.value()
        self.value_slider_throttle.display(value)
        
    def set_position_slider_valve(self):
        value = self.slider_gas_valve.value()
        self.value_slider_valve.display(value)
        
        
    def SchemeLayout (self):
        self.layout_scheme = QGridLayout()
        label_name = QLabel("Gas Turbine Remote Control") 
        label_scheme = QLabel('scheme')
        self.image_scheme = QPixmap('images/scheme.png')
        width = self.image_scheme.width() * 0.9
        height = self.image_scheme.height() * 0.9
        image = self.image_scheme.scaled(width, height, Qt.KeepAspectRatio)        
        label_scheme.setPixmap(image)
        
        self.dial_waste_gate = QDial()
        self.dial_waste_gate.setRange(0, 100)
        self.dial_waste_gate.setFixedHeight(80)
        
        self.bar_waste_gate = QProgressBar()
        self.bar_waste_gate.setFixedWidth(150)
        self.bar_waste_gate.setFixedHeight(25)
        self.bar_waste_gate.setValue(0)
            
        self.layout_scheme.addWidget(label_name, 0, 0, 1, 20, Qt.AlignCenter)
        self.layout_scheme.addWidget(label_scheme, 1, 0, 20, 20)
        self.layout_scheme.addWidget(self.bar_waste_gate, 5, 15, 3, 6)
        self.layout_scheme.addWidget(self.dial_waste_gate, 8, 15)
        
        self.dict_switch = {}
        n_switch = 4
        self.dict_switch['switch_1'] = SwitchLabel(self.layout_scheme, p1 = 16, p2 = 1)
        self.dict_switch['switch_2'] = SwitchLabel(self.layout_scheme, p1 = 16, p2 = 5)
        self.dict_switch['switch_3'] = SwitchLabel(self.layout_scheme, p1 = 20, p2 = 8)
        self.dict_switch['switch_4'] = SwitchLabel(self.layout_scheme, p1 = 4, p2 = 13)

        self.connect(self.dial_waste_gate, SIGNAL("valueChanged(int)"), self.set_position_dial)
        for i in range(n_switch):
            i += 1
            self.connect(self.dict_switch['switch_' + str(i)].switch, SIGNAL("toggled(bool)"), self.dict_switch['switch_' + str(i)].check)
        
        return self.layout_scheme
          
                
    def set_position_dial(self):
        value = self.dial_waste_gate.value()
        self.bar_waste_gate.setValue(value)
        
        
    def ButtonLayout (self):
        layout_buttons = QGridLayout()
        dict_buttons = {}
        list_name = ['Start', 'Auto', 'Manual', 'Stop']

        #color = QColor(Qt.green).dark(120)
        #palette = QPalette(color)
        #button_start.palette()
        i = 0
        for name in list_name:
            i+=1
            dict_buttons[name] = QPushButton(name)
            dict_buttons[name].setFixedHeight(70)
            dict_buttons[name].setFixedWidth(100)
            layout_buttons.addWidget(dict_buttons[name], 0, i)
            self.connect(dict_buttons[name], SIGNAL('clicked()'), eval('self.' + name + 'Button'))
        
        return layout_buttons
        
    def StartButton (self):
        self.timer_auto.blockSignals(True)
        self.dict_switch['switch_1'].switch.setChecked(True)
        self.dict_switch['switch_2'].switch.setChecked(True)
        self.dict_switch['switch_3'].switch.setChecked(True)
        self.dict_switch['switch_4'].switch.setChecked(True)
        self.slider_air_throttle.setValue(0)
        self.slider_gas_valve.setValue(10)
        self.dial_waste_gate.setValue(0)
                
    def AutoButton (self):
        self.dict_switch['switch_3'].switch.setChecked(True)
        self.dict_switch['switch_4'].switch.setChecked(True)
        self.slider_gas_valve.setValue(10)
        self.dial_waste_gate.setValue(0)
        
        self.timer_auto = QTimer()
        self.connect(self.timer_auto, SIGNAL("timeout()"), self.auto_slider_throttle)
        self.timer_auto.start(sleep_time*100)  
        
    def ManualButton(self):
        self.timer_auto.blockSignals(True)
        
    def StopButton (self):
        self.timer_auto.blockSignals(True)
        self.dict_switch['switch_1'].switch.setChecked(True)
        self.dict_switch['switch_2'].switch.setChecked(True)
        self.dict_switch['switch_3'].switch.setChecked(True)
        self.dict_switch['switch_4'].switch.setChecked(False)
        self.slider_air_throttle.setValue(0)
        self.slider_gas_valve.setValue(0)
        self.dial_waste_gate.setValue(0)
        
        
    def auto_slider_throttle(self):
        self.dict_switch['switch_3'].switch.setChecked(True)
        self.dict_switch['switch_4'].switch.setChecked(True)
        if self.slider_air_throttle.value() < 60:
            self.dict_switch['switch_1'].switch.setChecked(True)
            self.dict_switch['switch_2'].switch.setChecked(True)
            self.dial_waste_gate.setValue(0)
            position_throttle = self.slider_air_throttle.value()
            position_throttle += 1
            self.slider_air_throttle.setValue(position_throttle)
        elif self.slider_air_throttle.value() >= 60 and self.slider_air_throttle.value() < 99:
            self.dict_switch['switch_1'].switch.setChecked(False)
            self.dict_switch['switch_2'].switch.setChecked(False)
            self.dial_waste_gate.setValue(0)
            position_throttle = self.slider_air_throttle.value()
            position_throttle += 1
            self.slider_air_throttle.setValue(position_throttle)
        elif self.slider_air_throttle.value() == 99:
            self.dict_switch['switch_1'].switch.setChecked(False)
            self.dict_switch['switch_2'].switch.setChecked(False)
            possition_dial = self.dial_waste_gate.value()
            possition_dial += 1
            self.dial_waste_gate.setValue(possition_dial)
        
        
class SensorLabel (QDialog):
    
    def __init__(self, name, unit, mode = 'normal'):
        self.name = QLabel(name)
        self.unit = QLabel(unit)
        hej = QGroupBox() #to delete       
        self.radio = QRadioButton()
        
        if mode == 'LCD':
            self.value = QLCDNumber()
            self.value.setFixedHeight(30)
            self.value.setFixedWidth(50)
            self.value.setNumDigits(4)
        else:
            self.value = QLineEdit()
            self.value.setFixedWidth(100)
            self.value.setText(str(0))
            
            
class SwitchLabel (QDialog):
    
    def __init__(self, layout_scheme, p1 = 0, p2 = 0):
        
        self.switch = QCheckBox()        
        self.label_diodeRed = QLabel('diodeRed')
        self.image_diodeRed = QPixmap('images/diodeRed.png')
        width = self.image_diodeRed.width() * 0.6
        height = self.image_diodeRed.height() * 0.6
        image_diodeRed = self.image_diodeRed.scaled(width, height, Qt.KeepAspectRatio)        
        self.label_diodeRed.setPixmap(image_diodeRed)
        
        self.label_diodeGreen = QLabel('diodeGreen')
        self.image_diodeGreen = QPixmap('images/diodeGreen.png')
        image_diodeGreen = self.image_diodeGreen.scaled(width, height, Qt.KeepAspectRatio)        
        self.label_diodeGreen.setPixmap(image_diodeGreen)
        self.label_diodeGreen.hide()
        
        layout_scheme.addWidget(self.label_diodeRed, p1, p2)
        layout_scheme.addWidget(self.label_diodeGreen, p1, p2)        
        layout_scheme.addWidget(self.switch, p1, p2 + 1)
        
    
    def check(self):
        if self.switch.isChecked():
            self.label_diodeGreen.show()
        else:
            self.label_diodeGreen.hide()
            
            


app = QApplication(sys.argv)

form = Form()
form.show()
app.exec_()