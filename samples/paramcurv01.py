import math
import numpy as np

dur = 20
fps = 20

max_freq  = 1
r1 = 1
t1 = 0
t2 = 2*np.pi*max_freq
dt = (t2-t1)/(dur*fps)
max_cycloid_points=int((t2-t1)/dt)

fpx = lambda a,t : a*(math.sin(t))
fpy = lambda a,t : a*(math.sin(2*t))

tt = np.arange(t1, t2+dt, dt)
x = np.array([fpx(r1, t) for t in tt])
y = np.array([fpy(r1, t) for t in tt])

def plot_paramcurve(dev):
    vgl.draw_frame(dev, frm)
    vgl.draw_tick_2d(dev)	
    vgl.draw_grid_2d(dev)
    vgl.draw_label_2d(dev)
    dev.polyline(x,y,vgl.color.BLUE, dev.frm.hgt()*0.002)
    
import vgl
xmin,xmax,ymin,ymax=-1.5,1.5,-1.5, 1.5
data = vgl.Data(xmin,xmax,ymin,ymax)
fmm = vgl.FrameManager()
frm = fmm.create(0,0,5,5, data)
frm.hide_header()
#frm.hide_xmajor_tick()

def save_img():
    dev = vgl.DeviceCairo("paramcurv01.jpg", fmm.get_gbbox(), 300)
    dev.set_device(frm)
    plot_paramcurve(dev)
    dev.close()

    dev = vgl.DeviceWindowsMetafile("paramcurv01.wmf", fmm.get_gbbox())
    dev.set_device(frm)
    plot_paramcurve(dev)
    dev.close()
    
save_img()