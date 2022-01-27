'''
  Hypotrochoid
  
  22/01/24
  
  r1 : radius of outer circle
  r2 : radius of inner circle
  
  x(t) = (r1-r2)*cos(t) + d*cos((r1/r2-1)*t)
  y(t) = (r1-r2)*sin(t) - d*sin((r1/r2-1)*t)
  
  https://en.wikipedia.org/wiki/Hypotrochoid
  
'''
import math
import numpy as np

dur = 20
fps = 20

r1 = 4
#r2 = r1*0.25
r2 = 1
r3 = r2*0.15
max_freq  = 1 # Hz
t1 = 0
t2 = 2*np.pi*max_freq
dt = (t2-t1)/(dur*fps)
max_curve_points=int((t2-t1)/dt)

fpx = lambda r1, r2, d, t : (r1-r2)*np.cos(t) + d*np.cos((r1/r2-1)*t)
fpy = lambda r1, r2, d, t : (r1-r2)*np.sin(t) - d*np.sin((r1/r2-1)*t)

tt = np.arange(t1, t2+dt, dt)
dd = r2
xx = np.array([fpx(r1, r2, dd, t) for t in tt])
yy = np.array([fpy(r1, r2, dd, t) for t in tt])

curve_trail_x =[]
curve_trail_y =[]

def movie_curve(t):
    global dev, curve_trail_x, curve_trail_y, tt
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
    c2x = p1x - r2 * math.cos(t3)
    c2y = p1y - r2 * math.sin(t3)
    dev.circle(c2x, c2y, r2, lcol = vgl.color.BLUE, lthk = dev.frm.hgt()*0.005)
    
    '''
    r1 * th = r2 * (th + al)
    al + th = r1/r2 * th
    al = (r1/r2 - 1)*th
    '''    
    t4 = (r1/r2-1)*t3
    p2x = c2x + r2 * math.cos(t4)
    p2y = c2y - r2 * math.sin(t4)
    
    curve_trail_x = [p2x]+curve_trail_x[:max_curve_points]
    curve_trail_y = [p2y]+curve_trail_y[:max_curve_points]
    dev.polyline(curve_trail_x, curve_trail_y, vgl.color.MAGENTA, dev.frm.hgt()*0.005)

    dev.line(c2x, c2y, p2x, p2y, lcol=vgl.color.CUSTOM4, lthk=dev.frm.hgt()*0.003)
    dev.circle(p2x, p2y, r3, lcol=None, lthk=None, fcol=vgl.color.RED)
    
    tt.polyline = dev.lpolyline
    tt.polygon = dev.lpolygon
    tt.str = 'R=%1.0f, r=%1.0f, k=%1.0f'%(r1, r2, r1/r2)
    vgl.text.write_text(dev, tt)
    
def plot_curve(dev):
    vgl.draw_frame(dev)
    vgl.draw_tick_2d(dev)	
    vgl.draw_grid_2d(dev)
    vgl.draw_label_2d(dev)
    dev.polyline(xx,yy,vgl.color.BLUE, dev.frm.hgt()*0.005)
  
def save_curve_mov():
    global dev
    dev = vgl.DeviceCairo("", fmm.get_gbbox(), 200)
    #dev = vgl.DeviceCairo("", fmm.get_gbbox(), 40)
    dev.set_device(frm)
    frm.xaxis.label.size *= 2
    frm.yaxis.label.size *= 2
    dev_mov = vgl.DeviceCairoAnimation("hypocycloid.mp4", dev, movie_curve, dur, fps)
    dev_mov.save_video()
    #dev_mov = vgl.DeviceCairoAnimation("hypocycloid .gif", dev, movie_curve, dur, fps)
    #dev_mov.save_gif()
    
import vgl
xmin,xmax,ymin,ymax=-7,7,-7,7
data = vgl.Data(xmin,xmax,ymin,ymax)
fmm = vgl.FrameManager()
frm = fmm.create(0,0,5,5, data)
frm.hide_header()
tt = vgl.text.Text(2.5, 4.2)
tt.lthk = 0.003
tt.size = 0.03
tt.lcol = vgl.color.BLACK
tt.hn()

def save_curve_img():
    dev = vgl.DeviceCairo("hypocycloid.jpg", fmm.get_gbbox(), 130)
    dev.set_device(frm)
    plot_curve(dev)
    dev.close()

    #dev = vgl.DeviceWindowsMetafile("hypocycloid.wmf", fmm.get_gbbox())
    #dev.set_device(frm)
    #plot_curve(dev)
    #dev.close()
    

save_curve_mov()
#save_curve_img()