# -*- coding: utf-8 -*-
"""
Created on Fri Feb 07 20:32:44 2014

@author: Patryk
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy as np
import pyqtgraph as pg

from __init__ import *


class PlotsTab(QDialog):

    def __init__(self, dict_plot):
        self.dict_plot = dict_plot        
        self.layout = QGridLayout()        
        checkBox_temp_layout = QGridLayout()
        checkBox_pres_layout = QGridLayout()
        
        self.dict_plot['T' + str(0)] = PlotLabel('temp', 0) 
        self.dict_plot['P' + str(0)] = PlotLabel('pres', 0)              
        self.layout.addLayout(checkBox_temp_layout, 0, 0, 3, 1)
        self.layout.addLayout(checkBox_pres_layout, 3, 0, 3, 1)
        
        nt = 4 
        for point in range(nt):
            point += 1
            self.dict_plot['T' + str(point)] = PlotLabel('temp', point)            
            
            checkBox_temp_layout.addWidget(self.dict_plot['T' + str(point)].checkBox)
            
            self.layout.addWidget(self.dict_plot['T' + str(point)].plot, 0, point, 3, 2)
                
            self.connect(self.dict_plot['T' + str(point)].checkBox, SIGNAL("toggled(bool)"), self.dict_plot['T' + str(point)].check)
        
        self.dict_plot['P' + str(1)] = PlotLabel('pres', 1)
        self.layout.addWidget(self.dict_plot['P' + str(1)].plot, 3, 1, 3, 2)
        checkBox_pres_layout.addWidget(self.dict_plot['P' + str(1)].checkBox)
        self.connect(self.dict_plot['P' + str(1)].checkBox, SIGNAL("toggled(bool)"), self.dict_plot['P' + str(1)].check)
        
        self.dict_plot['P' + str(2)] = PlotLabel('pres', 2)
        self.layout.addWidget(self.dict_plot['P' + str(2)].plot, 3, 2, 3, 2)
        checkBox_pres_layout.addWidget(self.dict_plot['P' + str(2)].checkBox)
        self.connect(self.dict_plot['P' + str(2)].checkBox, SIGNAL("toggled(bool)"), self.dict_plot['P' + str(2)].check)
        
        self.dict_plot['F' + str(1)] = PlotLabel('flow', 1)
        self.layout.addWidget(self.dict_plot['F' + str(1)].plot, 3, 3, 3, 2)
        checkBox_pres_layout.addWidget(self.dict_plot['F' + str(1)].checkBox)
        self.connect(self.dict_plot['F' + str(1)].checkBox, SIGNAL("toggled(bool)"), self.dict_plot['F' + str(1)].check)
        
        self.dict_plot['F' + str(2)] = PlotLabel('flow', 2)
        self.layout.addWidget(self.dict_plot['F' + str(2)].plot, 3, 4, 3, 2) 
        checkBox_pres_layout.addWidget(self.dict_plot['F' + str(2)].checkBox)
        self.connect(self.dict_plot['F' + str(2)].checkBox, SIGNAL("toggled(bool)"), self.dict_plot['F' + str(2)].check)                
                                  
class PlotLabel (QDialog):
    
    def __init__(self, name, point):
        self.name = name
        self.plot = pg.PlotWidget(name= self.name +'_'+ str(point))
        self.checkBox = QCheckBox(self.name +'_'+ str(point))
        self.checkBox.setChecked(True)
        
        self.curve = self.set_curve()
        
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
        self.plot.setLabel('left', title, units= unit)
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
        
        