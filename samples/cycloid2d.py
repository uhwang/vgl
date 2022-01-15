'''
  2D Cycloid
  
  22/01/14
  
  OP = OQ + QC + CP

  OP : a vector from origin to a point on a circle
  OQ : a vector from origin to a point on the x-axis 
  QC : a vector from OQ to the center of a circle
  CP : a vector from the center of a circle to 

  Draw the circle as t
    OQ = at
    circle (at, radius)
    
  Find P as t
    Cx - a sin(t)
    Cy - a cos(t)
'''
import math
import numpy as np

dur = 20
fps = 20

r1 = 1
max_freq  = 1.5 # 2 Hz
t1 = 0
t2 = 2*np.pi*max_freq
dt = (t2-t1)/(dur*fps)
max_cycloid_points=int((t2-t1)/dt)

# x = a (t-sin(t))
# y = a (1-cos(t))
fpx = lambda a,t : a*(t-math.sin(t))
fpy = lambda a,t : a*(1-math.cos(t))

tt = np.arange(t1, t2, dt)
x = np.array([fpx(r1, t) for t in tt])
y = np.array([fpy(r1, t) for t in tt])

cycloid_trail_x =[]
cycloid_trail_y =[]

def movie_cycloid(t):
    global dev, cycloid_trail_x, cycloid_trail_y
    dev.fill_white()
    vgl.drawtick.draw_tick_2d(dev)	
    vgl.drawfrm.draw_grid(dev, dev.frm.data, 1)
    vgl.drawlabel.draw_label_2d(dev)
    
    # draw circle
    t3 = t1 + dt * t * fps
    cx = r1 * t3
    cy = r1
    dev.circle(cx, cy, r1, lcol = vgl.color.BLACK, lthk = dev.frm.hgt()*0.005)
    
    px = cx - r1 * math.sin(t3)
    py = cy - r1 * math.cos(t3)
    
    cycloid_trail_x = [px]+cycloid_trail_x[:max_cycloid_points]
    cycloid_trail_y = [py]+cycloid_trail_y[:max_cycloid_points]
    dev.polyline(cycloid_trail_x, cycloid_trail_y, vgl.color.BLUE, dev.frm.hgt()*0.005)

    r2 = r1 * 0.15
    dev.circle(px, py, r2, lcol=None, lthk=None, fcol=vgl.color.RED)
    
def plot_cycloid(dev):
    vgl.drawtick.draw_tick_2d(dev)	
    vgl.drawfrm.draw_grid(dev, dev.frm.data, 1)
    vgl.drawlabel.draw_label_2d(dev)
    dev.polyline(x,y,vgl.color.BLUE, dev.frm.hgt()*0.005)
    
    
import vgl
xmin,xmax,ymin,ymax=0,10,-5,5
data = vgl.Data(xmin,xmax,ymin,ymax)
fmm = vgl.FrameManager()
frm = fmm.create(0,0,3,3, data)

def save_cycloid_img():
    dev = vgl.DeviceCairo("cycloid.jpg", fmm.get_gbbox(), 150)
    dev.set_device(frm)
    plot_cycloid(dev)
    dev.close()

def save_cycloid_mov():
    global dev
    dev = vgl.DeviceCairo("", fmm.get_gbbox(), 150)
    frm.xaxis.xlabel.size *= 2
    frm.yaxis.ylabel.size *= 2
    dev.set_device(frm)
    dev_mov = vgl.DeviceCairoAnimation("cycloid.mp4", dev, movie_cycloid, dur, fps = fps)
    dev_mov.save_video()

save_cycloid_img()
save_cycloid_mov()