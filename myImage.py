# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 17:56:30 2017

@author: Paul
"""
import os,sys
sys.path.append('C:\Users\Paul\Documents\These\codes')

from scipy import ndimage as nd
from skimage import io,exposure,measure
import PIL
import numpy as np
from scipy.signal import argrelextrema
from Savitzjy_goulay import savitzky_golay
from remove_small_objects import remove_small_objects
from my_tools_img_proc import finddata


def find_segparam(img, gamma):
    y,x = exposure.histogram(img)
    x = x[1:-1]
    y = y[1:-1]

    idmax=argrelextrema(savitzky_golay(y,51,2), np.greater)[0]

    xSorted = [x1 for (y1,x1) in sorted(zip(y[idmax],x[idmax]))]
    xMin = min(xSorted[-1],xSorted[-2])
    xMax = max(xSorted[-1],xSorted[-2])
    
    segParam = [x1 for (y1,x1) in sorted(zip(y[xMin:xMax],x[xMin:xMax]))][0]
    return segParam    
    

class myImage(object):
    def __init__(self,filename,dimension):
        self.filename=filename
        self.ini = io.imread(filename)
        self.img = self.ini[:dimension]
        self.isPrepared = False
        self.segparam = 0
        self.pR = 1
        self.size = np.size(self.img)
        self.char = {}
        
    def set_segparam(self,segparam):
        '''
        Set the segmentation paramter to an arbitrary value. If given, the code
        will not try to find it and take this one instead.
        '''
        self.segparam = segparam
        
        
    def preparerMedian(self,param = 6,
                       size = (2,2), 
                       method = 'find',
                       obj_size = 80,
                       gamma=False):
                           
        self.median = nd.filters.median_filter(self.img, size = size)
        
        if self.segparam == 0 and method == 'find':
            self.segparam = find_segparam(self.median,gamma = gamma)
        elif self.segparam == 0 and method == 'fit':
            pass
        elif self.segparam != 0:
            pass
        else:
            print('Method unknown, it should be either \'fit\' or \'find\' ')
        tmp = remove_small_objects(self.median>self.segparam,obj_size)
        self.ready = np.logical_not(remove_small_objects(np.logical_not(tmp),obj_size))
        self.isPrepared = True        
        
    def getChar(self):
        if not self.isPrepared:
            self.preparerMedian()
            print(u'Image en préparation automatique, attention aux paramètres')
        self.char['taux'] = 100*np.sum(self.ready)/float(self.size)
        self.char['temp'],self.char['time'] = finddata(self.filename)
        self.char['perimeter']=measure.perimeter(self.ready)
        