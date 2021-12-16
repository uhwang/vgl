import math
import random
import vgl
import coltbl

xmin,xmax,ymin,ymax=-10,10,-10,10
data = vgl.Data(xmin,xmax,ymin,ymax)
fmm = vgl.FrameManager()
frm = fmm.create(0,0,3,3, data)
radius = 10

def draw_fcircle0(dev, x, y, rad):
    dev.circle(x, y, rad, vgl.color.BLACK, 0.001*dev.frm.hgt())
    
    if rad > 0.2:
        rad1 = rad*0.5
        draw_fcircle0(dev, x-rad1, y, rad1)
        draw_fcircle0(dev, x+rad1, y, rad1)

def draw_fcircle1(dev, x, y, rad):
    dev.circle(x, y, rad, vgl.color.BLACK, 0.001*dev.frm.hgt())
    
    if rad > 0.2:
        rad1 = rad*0.5
        draw_fcircle1(dev, x-rad1, y-rad1, rad1)
        draw_fcircle1(dev, x-rad1, y+rad1, rad1)
        draw_fcircle1(dev, x+rad1, y-rad1, rad1)
        draw_fcircle1(dev, x+rad1, y+rad1, rad1)
        
def save_wmf(fname, draw_fcircle, radius, gbbox):
    dev = vgl.DeviceWindowsMetafile(fname, gbbox)
    dev.set_device(frm)
    #vgl.drawfrm.draw_axis(dev, dev.frm.data)
    vgl.drawtick.draw_tick_2d(dev)	
    vgl.drawfrm.draw_grid(dev, dev.frm.data, 1)
    vgl.drawlabel.draw_label_2d(dev)
    draw_fcircle(dev, 0, 0, radius)
    dev.close()
    
def save_cairo(fname, draw_fcircle, radius, gbox, dpi):
    dev = vgl.DeviceCairo(fname, gbox, dpi)
    dev.fill_white()
    dev.set_device(frm)
    #vgl.drawfrm.draw_axis(dev, dev.frm.data)
    vgl.drawtick.draw_tick_2d(dev)	
    vgl.drawfrm.draw_grid(dev, dev.frm.data, 1)
    vgl.drawlabel.draw_label_2d(dev)
    draw_fcircle(dev, 0, 0, radius)
    dev.close()

save_cairo("fcircle0.png", draw_fcircle0, radius, fmm.get_gbbox(), 200)
save_wmf  ("fcircle0.wmf", draw_fcircle0, radius, fmm.get_gbbox())        
save_cairo("fcircle1.png", draw_fcircle1, radius, fmm.get_gbbox(), 200)
save_wmf  ("fcircle1.wmf", draw_fcircle1, radius, fmm.get_gbbox())        