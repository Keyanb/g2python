# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 14:15:29 2012
Data Container
This class is responsible for creating and providing access to data
@author: bram
"""
import time
import os, errno

class data():
    def __init__(self):
        print "Data Structure initialized"
        
    def set_file_name(self,sample,wire,name):
        # should be called to initialize the file
        # creates a file in a foler labeled with the date, sample and wire
        # name of the file should be provided by calling function
        date = time.strftime('%d-%m-%y',time.localtime())
        
        def mkdir_p(path):
            try:
                os.makedirs(path)
            except OSError as exc:
                if exc.errno == errno.EEXIST:
                    pass
                else: raise

        path = 'C:\\Users\\bram\\Documents\\Data\\' + date + '\\' + sample +'\\' + wire + '\\'
    
        if os.path.isfile(path+'rampup.dat'):
            print 'Warning! File already exists'
            path = path + '1'
    
        mkdir_p(path)
        self.file = open (path + name, 'w')
        
    def set_headers(self,headers):
        # headers should be provided as a list
        
        n = len(headers)
        
        
    
        