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

    
def draw(dev):
    dev.set_device(frm)
    vgl.draw_axis(dev)
    dev.circle(0, 0, r1, lcol = vgl.color.BLACK, lthk = 0.005)
    dev.polyline(xx,yy,vgl.color.BLUE, 0.005)
    dev.close()
    
import vgl
xmin,xmax,ymin,ymax=-7,7,-7,7
data = vgl.Data(xmin,xmax,ymin,ymax)
fmm = vgl.FrameManager()
frm = fmm.create(0,0,5,5, data)
frm.show_all_major_grid()
frm.xaxis.label.size *= 1.7
frm.yaxis.label.size *= 1.7
gbox = fmm.get_gbbox()

def save():
    import chkfld
    
    chkfld.create_folder("./epicycloid")
    
    dev_wmf = vgl.DeviceWMF("./epicycloid/epicycloid.wmf", gbox)
    dev_emf = vgl.DeviceEMF("./epicycloid/epicycloid.emf", gbox)
    dev_pdf = vgl.DevicePDF("./epicycloid/epicycloid.pdf", gbox)
    dev_svg = vgl.DeviceSVG("./epicycloid/epicycloid.svg", gbox, 200)
    dev_ppt = vgl.DevicePPT("./epicycloid/epicycloid.pptx",gbox)
    dev_img = vgl.DeviceIMG("./epicycloid/epicycloid.png", gbox, 200)
    
    draw(dev_wmf)
    draw(dev_emf)
    draw(dev_pdf)
    draw(dev_svg)
    draw(dev_ppt)
    draw(dev_img)
    
if __name__ == "__main__":
    save()
