# ex_polygon.py
#
#	Ref: Math Adventures with Python by Peter Farell 
#
#import pygame 
#from pygame.locals import *
import numpy as np
import vgl

data = vgl.Data(-4,4,-4,4)
fmm = vgl.FrameManager()
frm = fmm.create(0,0,4,4, data)
frm.show_all_major_grid()
plist = []

def create_polygon_list():
    plist.append(vgl.geom.Polygon(-2, 2,4,1.5,vgl.color.BLACK, 0.007))
    plist.append(vgl.geom.Polygon( 2, 2,5,1.5,vgl.color.PURPLE, 0.007, lpat = vgl.linepat._PAT_DASH))
    plist.append(vgl.geom.Polygon( 2,-2,6,1.5,vgl.color.PURPLE, 0.007, fcol=vgl.color.GREEN))
    plist.append(vgl.geom.Polygon(-2,-2,7,1.5,vgl.color.PURPLE, 0.007, fcol=vgl.color.GREEN, lpat = vgl.linepat._PAT_DASH))
    plist.append(vgl.geom.Polygon( 0, 0,3,1,vgl.color.BLACK, 0.007, vgl.color.CYAN))
    
def draw_shape(dev):
    vgl.drawaxis.draw_axis(dev)
    
    for p in plist:
        dev.polygon(p.get_xs(), p.get_ys(), 
                    p.lcol, p.lthk*dev.frm.hgt(), 
                    p.fcol, lpat=p.get_line_pattern())                    
def save_wmf(fname, frm, gbbox):
    dev_wmf = vgl.DeviceWindowsMetafile(fname, gbbox)
    dev_wmf.set_device(frm)
    draw_shape(dev_wmf)
    dev_wmf.close()
	
def save_img(fname, frm, gbox, dpi):
    dev_img = vgl.DeviceCairo(fname, gbox, dpi)
    dev_img.set_device(frm)
    draw_shape(dev_img)
    dev_img.close()

create_polygon_list()
gbox = fmm.get_gbbox()
save_wmf("poly2.wmf", frm, gbox)
save_img("poly2.jpg", frm, gbox, 200)                    