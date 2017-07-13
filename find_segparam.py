# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 14:30:03 2017

@author: Paul
"""
import sys
sys.path.append('C:\Users\Paul\Documents\These\codes\git\sem-proc')
import numpy as np
from scipy.optimize import curve_fit
from scipy.signal import argrelextrema
from Savitzjy_goulay import savitzky_golay
from skimage import io,exposure


def find_segparam(img, gamma=False,fit=False):
    y,x = exposure.histogram(img)
    x = x[1:-1] #remove saturation
    y = y[1:-1] #remove saturation

    idmax=argrelextrema(savitzky_golay(y,51,2), np.greater)[0] #find local maxima
    idmax = [k for k in idmax if y[k]>max(y)/100.] #remove maxima on flat parts of the histogram

    if len(idmax)==1 or fit:
        segParam = fitSegparam(x,y)
    else:   
        xSorted = [x1 for (y1,x1) in sorted(zip(y[idmax],x[idmax]))] #two highest maxima
        xMin = min(xSorted[-1],xSorted[-2])
        xMax = max(xSorted[-1],xSorted[-2])
        
        segParam = x[np.where(y[xMin:xMax]==min(y[xMin:xMax]))] #minimum between the two.
    return segParam    
    
def gaussian(x, amp, cen, wid):
    return amp * np.exp(-(x-cen)**2 /wid)

def func(x, amp0, cen0, wid0, amp1, cen1, wid1):
    return gaussian(x, amp0, cen0, wid0)+ gaussian(x, amp1, cen1, wid1)

def fitSegparam(x,y):
    '''
    This proceudre is used when only one maximum is found.
    It happens sometimes during the dewetting, but also when no holes are found
    If the signal is well modelled by a single gaussian, the layer is considered
    as uniform.
    '''
    #first, check if fit with one gaussian is ok
    if fitSingleGaussian(x,y) <=0.01:
        segParam = 1
    else:
    #if not, wee need to fit two gaussians
        init_vals = [max(y), x[len(x)/2], 20, 1,x[-1],20]      
        best_vals, covar = curve_fit(func, x, y, p0=init_vals)
#    fit = func(x,*best_vals)

        centre1 = min(best_vals[1],best_vals[4])
        centre2 = max(best_vals[1],best_vals[4])
        borne1 = np.where(x - centre1 == min(abs(x - centre1)))
        borne2 = np.where(x - centre2 == min(abs(x - centre2)))
        x = x[borne1:borne2]
        segParam = x[np.where(gaussian(x,*best_vals[3:])-gaussian(x,*best_vals[:3])\
                ==min(abs(gaussian(x,*best_vals[3:])-gaussian(x,*best_vals[:3]))))]
    return segParam
    
def fitSingleGaussian(x,y):
    init_vals = [max(y), x[len(x)/2], 20]
    gauss_vals, covar = curve_fit(gaussian, x, y, p0=init_vals)
    default = np.sqrt(np.sum((gaussian(x,*gauss_vals)-y)**2.))
    error = default/float(np.sum(y))
    return error