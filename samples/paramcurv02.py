import math
import numpy as np

dur = 20
fps = 20

a = 1
b = 2
kx = 2
ky = 3
max_freq  = 1
r1 = 1
t1 = 0
t2 = 2*np.pi*max_freq
dt = (t2-t1)/(dur*fps)
max_cycloid_points=int((t2-t1)/dt)

fpx = lambda a,kx,t : a*(math.sin(kx*t))
fpy = lambda b,ky,t : b*(math.sin(ky*t))

tt = np.arange(t1, t2+dt, dt)
x = np.array([fpx(r1, kx, t) for t in tt])
y = np.array([fpy(r1, ky, t) for t in tt])

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
    dev = vgl.DeviceCairo("paramcurv02.jpg", fmm.get_gbbox(), 300)
    dev.set_device(frm)
    plot_paramcurve(dev)
    dev.close()

    dev = vgl.DeviceWindowsMetafile("paramcurv02.wmf", fmm.get_gbbox())
    dev.set_device(frm)
    plot_paramcurve(dev)
    dev.close()
    
save_img()