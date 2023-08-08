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
import vgl

xmin,xmax,ymin,ymax=-7,7,-7,7
data = vgl.Data(xmin,xmax,ymin,ymax)
fmm = vgl.FrameManager()
frm = fmm.create(0,0,5,5, data)
frm.show_all_major_grid()
frm.xaxis.label.size *= 1.7
frm.yaxis.label.size *= 1.7

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

curve_trail_x =[]
curve_trail_y =[]

def draw(t):
    global dev, curve_trail_x, curve_trail_y
    dev.fill_white()
    vgl.draw_axis(dev)
    vgl.draw_frame(dev)
    
    # draw circle
    t3 = t1 + dt * t * fps
    dev.circle(0, 0, r1, lcol = vgl.color.BLACK, lthk = 0.005)
    
    p1x = r1*np.cos(t3) 
    p1y = r1*np.sin(t3)
    c2x = p1x + r2 * math.cos(t3)
    c2y = p1y + r2 * math.sin(t3)
    dev.circle(c2x, c2y, r2, lcol = vgl.color.BLUE, lthk = 0.005)
    
    t4 = r1/r2*t3
    p2x = c2x - r2 * math.cos(t3+t4)
    p2y = c2y - r2 * math.sin(t3+t4)
    
    curve_trail_x = [p2x]+curve_trail_x[:max_curve_points]
    curve_trail_y = [p2y]+curve_trail_y[:max_curve_points]
    dev.polyline(curve_trail_x, curve_trail_y, vgl.color.MAGENTA, 0.005)

    dev.circle(p2x, p2y, r3, lcol=None, lthk=None, fcol=vgl.color.RED)
    
def save_curve_mov():
    global dev, curve_trail_x, curve_trail_y
    curve_trail_x =[]
    curve_trail_y =[]
    dev = vgl.DeviceCairo("", fmm.get_gbbox(), 200)
    dev.set_device(frm)
    dev_mov = vgl.DeviceCairoAnimation("./epicycloid-mov/epicycloid.mp4", dev, draw, dur, fps)
    dev_mov.save_video()

def save_curve_gif():
    global dev, curve_trail_x, curve_trail_y
    curve_trail_x =[]
    curve_trail_y =[]
    dev= vgl.DeviceCairo("", fmm.get_gbbox(), 70)
    dev.set_device(frm)
    dev_mov = vgl.DeviceCairoAnimation("./epicycloid-mov/epicycloid.gif", dev, draw, dur, fps)
    dev_mov.save_gif()
    
def save():
    import chkfld
    
    chkfld.create_folder("./epicycloid-mov")
    
    save_curve_mov()
    
if __name__ == "__main__":
    save() 