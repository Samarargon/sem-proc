# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 14:44:40 2017

@author: Paul
"""
from skimage import exposure
import matplotlib.pyplot as plt

def histo_plot(img, output = False, new = True):
    '''
    Uses expo.histogram to plot graylevel histogram. Returns x, y if output = True.
    '''
    hi = exposure.histogram(img)
    if new:
        plt.figure()
    plt.plot(hi[1],hi[0])
    if output:
        return hi[1],hi[0]