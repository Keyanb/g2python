# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 16:46:03 2013

Live data collector
This program is responsible for the collection of all the data and feeding it
into the GUI. It runs in a separate thread.

@author: keyan
"""

import threading

class data_aquisition(threading.Thread):
     """ A thread for collecting the data and such. We should have a way of 
     the GUI to change settings mid-run
    """