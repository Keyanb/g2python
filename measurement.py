# -*- coding: utf-8 -*-
"""
Created on Thu Jun 07 12:11:52 2012

@author: BRAM
"""
import SRS830
import DAC488
import lakeshore332
import time

t_start = time.time()
frequency = 108.25 # hz
amplitude = 5.0 # V
time_constant = 100.0 #ms
lockin = SRS830.device('GPIB1::8')
gate = DAC488.device('GPIB1::10')
temp = lakeshore332.device('GPIB1::12')

gate.set_range(1,3)

def read(gateVoltage):
    t = time.time() - t_start
    t = float(t)
    x_value = lockin.read_input(1)
    x = float(x_value)
    # gate = gate
    temperature = float(temp.read('b'))
    conductance = calc_conduct(x)
    return [gateVoltage, conductance, x, temperature, t]
    
def calc_conduct(voltage):
    v_o = 47.8
    uV = voltage * 1000000.0
    sense = 4982.8
    if uV !=0:
        Rs = (v_o/uV)*(sense)-sense
        Gs = (1/Rs)/(7.748E-5)
    else:
        Gs = 0
    
    return Gs

def setNextGate(gate_voltage):
    gate.set_voltage(1,gate_voltage)

            