# -*- coding: utf-8 -*-
"""
Convert to conductance
Just a couple functions which will
be used to convert readings into conductance
data.

@author: keyan
"""

def twopoint(voltage,v_o=49.0):
    uV = voltage * 1000000.0
    sense = 4982.8
    if uV !=0:
        Rs = (v_o/uV)*(sense)-sense
        Gs = (1/Rs)/(7.748E-5)
    else:
        Gs = 0
    return Gs
    
def fourpoint(voltage1,voltage2):
    Gs = ((voltage1/4982.8)/(voltage2))/(7.748E-5) # (I/V)/Quantum
    
    return Gs
    
def microfourpoint(voltage2):
    Gs = (0.000001/(voltage2))/(7.748E-5) # (I/V)/Quantum
    
    return Gs
    
def microtwopoint(voltage1):
    Gs = (0.000001/(voltage1))/(7.748E-5) # (I/V)/Quantum
    
    return Gs