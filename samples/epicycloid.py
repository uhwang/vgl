'''
  Epicycloid
  
  22/01/24
  
  x(t) = (a+b) cos(t) - b cos((a/b+1)t)
  y(t) = (a+b) sin(t) - b sin((a/b+1)t)
  
  Facts:
  (a) There are four curves which are closely related: 
      epicycloid, epitrochoid, hypocycloid, and the hypotrochoid. 
      They are all traced by a point P on a circle of radius b 
      which rolls around a fixed circle of radius a.
  (b) For an epicycloid, the circle of radius b rolls on 
      the outside of the circle of radius a. The point P is 
      on the edge of the circle of radius b.
  (c) If a = b: cardioid.
  (d) If a = 2b, nephroid.

  https://en.wikipedia.org/wiki/Epicycloid
  
'''
import math
import numpy as np

dur = 20
fps = 20

r1 = 3
r2 = r1*0.3
r3 = r2*0.15
max_freq  = 3 # Hz
t1 = 0
t2 = 2*np.pi*max_freq
dt = (t2-t1)/(dur*fps)
max_curve_points=int((t2-t1)/dt)

fpx = lambda r1, r2, t : (r1+r2)*np.cos(t) - r2*np.cos((r1/r2+1)*t)
fpy = lambda r1, r2, t : (r1+r2)*np.sin(t) - r2*np.sin((r1/r2+1)*t)

tt = np.arange(t1, t2, dt)
xx = np.array([fpx(r1, r2, t) for t in tt])
yy = np.array([fpy(r1, r2, t) for t in tt])

curve_trail_x =[]
curve_trail_y =[]

def movie_curve(t):
    global dev, curve_trail_x, curve_trail_y
    dev.fill_white()
    vgl.draw_tick_2d(dev)	
    vgl.draw_grid_2d(dev)
    vgl.draw_label_2d(dev)
    vgl.draw_frame(dev)
    
    # draw circle
    t3 = t1 + dt * t * fps
    dev.circle(0, 0, r1, lcol = vgl.color.BLACK, lthk = dev.frm.hgt()*0.005)
    
    p1x = r1*np.cos(t3) 
    p1y = r1*np.sin(t3)
    c2x = p1x + r2 * math.cos(t3)
    c2y = p1y + r2 * math.sin(t3)
    dev.circle(c2x, c2y, r2, lcol = vgl.color.BLUE, lthk = dev.frm.hgt()*0.005)
    
    t4 = r1/r2*t3
    p2x = c2x - r2 * math.cos(t3+t4)
    p2y = c2y - r2 * math.sin(t3+t4)
    
    curve_trail_x = [p2x]+curve_trail_x[:max_curve_points]
    curve_trail_y = [p2y]+curve_trail_y[:max_curve_points]
    dev.polyline(curve_trail_x, curve_trail_y, vgl.color.MAGENTA, dev.frm.hgt()*0.005)

    dev.circle(p2x, p2y, r3, lcol=None, lthk=None, fcol=vgl.color.RED)
    
def plot_curve(dev):
    vgl.draw_frame(dev)
    vgl.draw_tick_2d(dev)	
    vgl.draw_grid_2d(dev)
    vgl.draw_label_2d(dev)
    dev.polyline(xx,yy,vgl.color.BLUE, dev.frm.hgt()*0.005)
    
def save_curve_mov():
    global dev
    dev = vgl.DeviceCairo("", fmm.get_gbbox(), 200)
    dev.set_device(frm)
    frm.xaxis.label.size *= 2
    frm.yaxis.label.size *= 2
    dev_mov = vgl.DeviceCairoAnimation("epicycloid.mp4", dev, movie_curve, dur, fps)
    dev_mov.save_video()
    
import vgl
xmin,xmax,ymin,ymax=-7,7,-7,7
data = vgl.Data(xmin,xmax,ymin,ymax)
fmm = vgl.FrameManager()
frm = fmm.create(0,0,5,5, data)
frm.hide_header()

def save_curve_img():
    dev = vgl.DeviceCairo("Epicycloid.jpg", fmm.get_gbbox(), 130)
    dev.set_device(frm)
    plot_curve(dev)
    dev.close()

    dev = vgl.DeviceWindowsMetafile("Epicycloid.wmf", fmm.get_gbbox())
    dev.set_device(frm)
    plot_curve(dev)
    dev.close()
    

save_curve_mov()
save_curve_img()