# -*- coding: utf-8 -*-
"""
Created on Fri Feb 07 20:32:44 2014

@author: Patryk
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy as np
import pyqtgraph as pg

#from __init__ import *


class PlotsTab(QDialog):

    def __init__(self, dict_plot, operating_devices):
        self.dict_plot = dict_plot  
        self.operating_devices = operating_devices
        self.layout = QGridLayout()
        layout_plot_up = QGridLayout()
        layout_plot_down = QGridLayout()        
        layout_checkBox_up = QGridLayout()
        layout_checkBox_down = QGridLayout()
        
        label_logo = QLabel('KNE')
        self.image_logo = QPixmap('GUI/images/kne.png')
        width = self.image_logo.width() * 0.11
        height = self.image_logo.height() * 0.11
        image = self.image_logo.scaled(width, height, Qt.KeepAspectRatio)        
        label_logo.setPixmap(image)
        
        label_logo2 = QLabel('KNE')       
        label_logo2.setPixmap(image)
        
        layout_plot_up.addWidget(label_logo, 0, 0, Qt.AlignLeft)
        layout_plot_down.addWidget(label_logo2, 0, 0, Qt.AlignLeft)
                    
        self.layout.addLayout(layout_checkBox_up, 0, 0, 3, 1)
        self.layout.addLayout(layout_checkBox_down, 3, 0, 3, 1)
        self.layout.addLayout(layout_plot_up, 0, 1, 3, 4)
        self.layout.addLayout(layout_plot_down, 3, 1, 3, 4)
        
        
        p2 = 0
        layout_plot     =   layout_plot_up
        layout_checkBox =   layout_checkBox_up
        
        for device in self.operating_devices:
            if device.point == '0':
                self.dict_plot[device.kind + '0'] = PlotLabel(device.kind, 0) 
            if device.direction == "INPUT" and device.point != '0':
                if p2 == 4:
                    layout_plot     =   layout_plot_down
                    layout_checkBox =   layout_checkBox_down
                    p2 = 0
                self.dict_plot[device.kind + device.point] = PlotLabel(device.kind, device.point)
                layout_checkBox.addWidget(self.dict_plot[device.kind + str(device.point)].checkBox)
                layout_plot.addWidget(self.dict_plot[device.kind + str(device.point)].plot, 0, p2, 3, 2)
                p2 += 1
        
                     
class PlotLabel (QDialog):
    
    def __init__(self, name, point):
        self.name = name
        self.plot = pg.PlotWidget(name= self.name +'_'+ str(point))
        self.checkBox = QCheckBox(self.name +' '+ str(point))
        self.checkBox.setChecked(True)
        
        self.curve = self.set_curve()
        self.connect(self.checkBox, SIGNAL("toggled(bool)"), self.check)
        
    def set_curve(self):
        if self.name == 'temp':
            title = 'Temperature'
            unit = 'C'
        if self.name == 'pres' :
            title = 'Pressure'
            unit = 'bar'
        if self.name == 'flow':
            title = 'Flow'
            unit = 'm3/h'
        self.plot.setLabel('left', self.name, units= 'C')
        self.plot.setLabel('bottom', 'Time', units='s')
        self.plot.setXRange(0, 10)
        self.plot.setYRange(0, 10)
        curve = self.plot.plot()
        curve.setPen((200,200,100))
        return curve
                
    def check(self):
        if self.checkBox.isChecked():
            self.plot.show()
        else:
            self.plot.hide()
        
        