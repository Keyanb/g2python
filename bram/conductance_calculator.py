# -*- coding: utf-8 -*-
"""
Convert to conductance
Just a couple functions which will
be used to convert readings into conductance
data.

@author: keyan
"""

def twopointcond(voltage,v_o=49.0):
    uV = voltage * 1000000.0
    sense = 4982.8
    if uV !=0:
        Rs = (v_o/uV)*(sense)-sense
        Gs = (1/Rs)/(7.748E-5)
    else:
        Gs = 0
    return Gs
    
def fourpointcond(voltage1,voltage2):
    Gs = ((voltage1/4982.8)/(voltage2))/(7.748E-5) # (I/V)/Quantum
    
    return Gs