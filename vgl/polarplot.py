'''

    ploarplot.py
    
    7/28/2023

'''
import numpy as np
from . import color
from . import linepat

def polarplot(dev, theta, rho, lcol=color.cornflowerblue, lthk=0.004, lpat=linepat._PAT_SOLID, fcol=None):

    dev.frm.to_polar(0,np.max(rho))
    size = len(theta)
    x = np.empty(size, dtype='float32')
    y = np.empty(size, dtype='float32')
    
    for i, (t, r) in enumerate(zip(theta, rho)):
        x[i] = r*np.cos(t)
        y[i] = r*np.sin(t)
        
    if isinstance(fcol, color.Color):
        dev.polygon(x,y, lcol, lthk*dev.frm.hgt(), lpat, fcol)
    else:
        dev.polyline(x,y, lcol, lthk*dev.frm.hgt(), lpat)
