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

cycloid_trail_x =[]
cycloid_trail_y =[]

def draw(t):
    global dev, cycloid_trail_x, cycloid_trail_y
    dev.fill_white()
    vgl.draw_frame(dev)
    vgl.draw_axis(dev)
    
    # draw circle
    t3 = t1 + dt * t * fps
    cx = r1 * t3
    cy = r1
    dev.circle(cx, cy, r1, lcol = vgl.color.BLACK, lthk = 0.005)
    
    px = cx - r1 * math.sin(t3)
    py = cy - r1 * math.cos(t3)
    dev.line(cx, cy, px, py, vgl.color.GREEN, 0.003)
    
    cycloid_trail_x = [px]+cycloid_trail_x[:max_cycloid_points]
    cycloid_trail_y = [py]+cycloid_trail_y[:max_cycloid_points]
    dev.polyline(cycloid_trail_x, cycloid_trail_y, vgl.color.BLUE, 0.005)

    r2 = r1 * 0.1
    dev.circle(px, py, r2, fcol=vgl.color.RED)
    
import vgl
xmin,xmax,ymin,ymax=-1,20,-1,5
data = vgl.Data(xmin,xmax,ymin,ymax)
fmm = vgl.FrameManager()
frm = fmm.create(1,1,6,2, data)
frm.show_all_major_grid()
frm.show_xminor_grid()
frm.xaxis.label.size *= 2
frm.yaxis.label.size *= 2
    
def save():
    import chkfld
    global dev
    
    chkfld.create_folder("./cycloid-mov")   

    dev = vgl.DeviceCairo("", fmm.get_gbbox(), 200)
    dev.set_device(frm, extend=vgl.device._FIT_EXTEND_X)
    dev_mov = vgl.DeviceCairoAnimation("./cycloid-mov/cycloid.mp4", dev, draw, dur, fps)
    dev_mov.save_video()

if __name__ == "__main__":
    save()
