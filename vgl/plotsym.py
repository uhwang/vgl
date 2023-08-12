'''

    plotsym.py

    8/12/2023

'''

from . import color
from . import symbol

def plot_circle_symbol(
                dev, 
                xs, 
                ys, 
                size=0.008,
                lcol=color.BLACK,
                lthk=0.002,
                fill=True,
                fcol=color.RED,
                skip=1):

    sym = symbol.Circle(size, dev.frm.hgt(), lcol, lthk, fill, fcol)
    
    nsym = len(xs)
    i = 0
    
    while i < nsym:
        x, y = xs[i], ys[i]
        dev.symbol(x,y, sym)
        i += skip
    
def plot_gradient_symbol(
                dev, 
                xs, 
                ys, 
                size=0.008,
                lcol=color.BLACK,
                lthk=0.002,
                fill=True,
                fcol=color.RED,
                skip=1):

    sym = symbol.Gradient(size, dev.frm.hgt(), lcol, lthk, fill, fcol)
    
    nsym = len(xs)
    i = 0
    
    while i < nsym:
        x, y = xs[i], ys[i]
        dev.symbol(x,y, sym)
        i += skip
        
def plot_rtriangle_symbol(
                dev, 
                xs, 
                ys, 
                size=0.008,
                lcol=color.BLACK,
                lthk=0.002,
                fill=True,
                fcol=color.RED,
                skip=1):

    sym = symbol.RightTriangle(size, dev.frm.hgt(), lcol, lthk, fill, fcol)
    
    nsym = len(xs)
    i = 0
    
    while i < nsym:
        x, y = xs[i], ys[i]
        dev.symbol(x,y, sym)
        i += skip
        
def plot_ltriangle_symbol(
                dev, 
                xs, 
                ys, 
                size=0.008,
                lcol=color.BLACK,
                lthk=0.002,
                fill=True,
                fcol=color.RED,
                skip=1):

    sym = symbol.LeftTriangle(size, dev.frm.hgt(), lcol, lthk, fill, fcol)
    
    nsym = len(xs)
    i = 0
    
    while i < nsym:
        x, y = xs[i], ys[i]
        dev.symbol(x,y, sym)
        i += skip
        
def plot_diamond_symbol(
                dev, 
                xs, 
                ys, 
                size=0.008,
                lcol=color.BLACK,
                lthk=0.002,
                fill=True,
                fcol=color.RED,
                skip=1):

    sym = symbol.Diamond(size, dev.frm.hgt(), lcol, lthk, fill, fcol)
    
    nsym = len(xs)
    i = 0
    
    while i < nsym:
        x, y = xs[i], ys[i]
        dev.symbol(x,y, sym)
        i += skip
        
def plot_square_symbol(
                dev, 
                xs, 
                ys, 
                size=0.008,
                lcol=color.BLACK,
                lthk=0.002,
                fill=True,
                fcol=color.RED,
                skip=1):

    sym = symbol.Square(size, dev.frm.hgt(), lcol, lthk, fill, fcol)
    
    nsym = len(xs)
    i = 0
    
    while i < nsym:
        x, y = xs[i], ys[i]
        dev.symbol(x,y, sym)
        i += skip
        
