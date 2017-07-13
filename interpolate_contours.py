# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 14:06:34 2017

@author: Paul
"""
import numpy as np
from scipy.interpolate import UnivariateSpline

def interpolate_contours(contour, coeff):
    '''
    Interpolating the contours of an image. It is done by using Univariatesplines
    with the curvilineat absciss. If contours are closed, the are doubled to catch
    correctly the first few and last few points.
    
    Parameters :
    ------------
    contour : (n,2)-ndarrays
        a unique contour obtained with measure.find_contours
    coeff : float
        the coefficient is used for interpolation. It determines how constrained
        the interpolation functions will be.

    Returns :
    ---------
    fx,fy : functions
        interpolated splines of the contour
    t : list of floats
        the curvilinear absciss
    
    Notes :
    -------
    fx and fy are used with the form fx(t), fy(t) to obtain all interpolated 
    points.
    '''

    x,y = [ kik[1] for kik in contour], [ kik[0] for kik in contour]
    number = len(contour) / 2
        
#==============================================================================
#       Doubling contours if the shape is closed.
#==============================================================================
    if all([contour[0][tu] == contour[-1][tu] for tu in [0,1]]):
        x_ext = x+x
        y_ext = y+y
        number = len(x_ext)/2
        t_start = number/4 #we consider the curvilinear absciss in the
        t_end = 3*number/4                                  #middle
        
#==============================================================================
#     else just taking the contour
#==============================================================================
    else :
        x_ext = x
        y_ext = y
        number = len(x_ext)/2
        t_start = 0
        t_end = -1               
            
#==============================================================================
#             contour interpolation, finding curvilinear absciss
#==============================================================================
    xd =np.diff(x_ext)
    yd =np.diff(y_ext)
    dist = np.sqrt(np.power(xd,2)+np.power(yd,2))
    u = np.cumsum(dist)
    u = np.hstack([[0],u])
    t = np.linspace(0,u.max(),number)
    xn = np.interp(t, u, x_ext)
    yn = np.interp(t, u, y_ext)

#==============================================================================
#             getting the splines
#==============================================================================
    fx = UnivariateSpline(t, xn, k=4, s = coeff*number)
    fy = UnivariateSpline(t, yn, k=4, s = coeff*number)

    return fx,fy,t[t_start:t_end]
