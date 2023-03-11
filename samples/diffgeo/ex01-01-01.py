'''
  Diff Geo
  
  03/11/2023
  
  a unit circle at a center (0,0)
  a line pass a point (-1,0) and (0,t)
  (x,y) is a path on a circle and meets the line 
  parameterize x,y according to t
  
  x = cos(th))
  y = sin(th))
  th = th1 + th2
  th1 = th2
  th1 = atan(t/1)
  
  x = cos(2atan(t)
  y = sin(2atan(t)
  
'''

import math
import numpy as np
import vgl

dur = 20
fps = 30
cx,cy=0,0
rr = 1.0
r1 = rr * 0.025
t_min,t_max  = -1,1
max_tcircle_points=dur*fps
dt = (t_max-t_min)/max_tcircle_points
tcircle_trail_x =[]
tcircle_trail_y =[]

fx = lambda r,t : r*np.cos(2*np.arctan(t/r))
fy = lambda r,t : r*np.sin(2*np.arctan(t/r))

def movie_tcircle(t):
    global dev, tcircle_trail_x, tcircle_trail_y, it
    dev.fill_white()
    vgl.draw_axis(dev)
    
    # draw circle
    dev.circle(cx, cy, rr, lcol = vgl.color.BLACK, 
                           lthk = dev.frm.hgt()*0.003, 
                           lpat = vgl.linepat.get_dash(0.008))
    
    tc = t_min + t*dt*fps
    px = fx(rr, tc)
    py = fy(rr, tc)
    
    dev.line(-rr, cy, px, py, vgl.color.GREEN, dev.frm.hgt()*0.003)
    dev.line(-rr, cy, cx, cy, vgl.color.RED, dev.frm.hgt()*0.003)
    dev.line(cx, cy, px, py, vgl.color.RED, dev.frm.hgt()*0.003)
    
    tcircle_trail_x = [px]+tcircle_trail_x[:max_tcircle_points]
    tcircle_trail_y = [py]+tcircle_trail_y[:max_tcircle_points]
    dev.polyline(tcircle_trail_x, tcircle_trail_y, vgl.color.BLUE, dev.frm.hgt()*0.005)

    dev.circle(-rr, cy, r1, lcol=None, lthk=None, fcol=vgl.color.BLACK)
    dev.circle(px, py, r1, lcol=None, lthk=None, fcol=vgl.color.BLACK)
    
xmin,xmax,ymin,ymax=-rr*1.2,rr*1.2,-rr*1.2,rr*1.2
data = vgl.Data(xmin,xmax,ymin,ymax)
fmm = vgl.FrameManager()
frm = fmm.create(0,0,4,4, data)
frm.show_all_major_grid()
    
def save_tcircle_mov():
    global dev
    dev = vgl.DeviceCairo("", fmm.get_gbbox(), 300)
    dev.set_device(frm, extend=vgl.device._FIT_EXTEND_X)
    dev_mov = vgl.DeviceCairoAnimation("tcircle.mp4", dev, movie_tcircle, dur, fps)
    dev_mov.save_video()

#save_img()
import time
start_time = time.clock()
save_tcircle_mov()
print(time.clock() - start_time, "seconds")
#write_tec()
