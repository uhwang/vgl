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
fps = 30

r1 = 1
max_freq  = 3 # 2 Hz
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
    vgl.draw_axis(dev)
    
    # draw circle
    t3 = t1 + dt * t * fps
    cx = r1 * t3
    cy = r1
    dev.circle(cx, cy, r1, lcol = vgl.color.BLACK, lthk = dev.frm.hgt()*0.005)
    
    px = cx - r1 * math.sin(t3)
    py = cy - r1 * math.cos(t3)
    
    dev.line(cx, cy, px, py, vgl.color.GREEN, dev.frm.hgt()*0.003)
    
    cycloid_trail_x = [px]+cycloid_trail_x[:max_cycloid_points]
    cycloid_trail_y = [py]+cycloid_trail_y[:max_cycloid_points]
    dev.polyline(cycloid_trail_x, cycloid_trail_y, vgl.color.BLUE, dev.frm.hgt()*0.005)

    r2 = r1 * 0.15
    dev.circle(px, py, r2, lcol=None, lthk=None, fcol=vgl.color.RED)
    
def plot_cycloid(dev):
    vgl.draw_axis(dev)
    dev.polyline(x,y,vgl.color.BLUE, dev.frm.hgt()*0.005)
    
import vgl
#xmin,xmax,ymin,ymax=0,20,-2,5
xmin,xmax,ymin,ymax=-1,20,-1,5
data = vgl.Data(xmin,xmax,ymin,ymax)
fmm = vgl.FrameManager()
frm = fmm.create(0,0,6,2.5, data)
frm.show_xgrid()
frm.show_ymajor_grid()

def write_tec():
    fp = open("cycloid2d.tec", "wt")
    
    fp.write("variables = x,y\nzone t=\"cycloid\", i = %d\n"%x.size)
    
    for x1, y1 in zip(x,y):
        fp.write("%f %f\n"%(x1, y1))
    fp.close()
    
def save_cycloid_img(dev):
    dev.set_device(frm)
    plot_cycloid(dev)

def save_cycloid_mov():
    global dev
    dev = vgl.DeviceCairo("", fmm.get_gbbox(), 300)
    dev.set_device(frm, extend=vgl.device._FIT_EXTEND_X)
    frm.xaxis.label.size *= 2
    frm.yaxis.label.size *= 2
    dev_mov = vgl.DeviceCairoAnimation("cycloid.mp4", dev, movie_cycloid, dur, fps)
    dev_mov.save_video()

def save_img():
    dev = vgl.DeviceCairo("cycloid.jpg", fmm.get_gbbox(), 300)
    dev.set_device(frm)
    save_cycloid_img(dev)
    dev.close()

    dev = vgl.DeviceWindowsMetafile("cycloid.wmf", fmm.get_gbbox())
    dev.set_device(frm)
    save_cycloid_img(dev)
    dev.close()
    
#save_img()
import time
start_time = time.clock()
save_cycloid_mov()
print(time.clock() - start_time, "seconds")
#write_tec()