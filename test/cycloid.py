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

fpx = lambda a,t : a*(t-math.sin(t))
fpy = lambda a,t : a*(1-math.cos(t))

tt = np.arange(t1, t2, dt)
x = np.array([fpx(r1, t) for t in tt])
y = np.array([fpy(r1, t) for t in tt])

def draw(dev):
    dev.set_device(frm, extend=vgl.device._FIT_EXTEND_X)
    vgl.draw_frame(dev)
    vgl.draw_axis(dev)
    dev.polyline(x,y,vgl.color.BLUE, dev.frm.hgt()*0.005)
    dev.close()
    
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
    
    if not chkfld.create_folder("./cycloid"):
        return
        
    dev_img = vgl.DeviceIMG("./cycloid/cycloid.jpg", fmm.get_gbbox(), 300)
    dev_wmf = vgl.DeviceWMF("./cycloid/cycloid.wmf", fmm.get_gbbox())
    dev_emf = vgl.DeviceEMF("./cycloid/cycloid.emf", fmm.get_gbbox())
    dev_pdf = vgl.DevicePDF("./cycloid/cycloid.pdf", fmm.get_gbbox())
    dev_svg = vgl.DeviceSVG("./cycloid/cycloid.svg", fmm.get_gbbox(), 300)
    dev_ppt = vgl.DevicePPT("./cycloid/cycloid.pptx",fmm.get_gbbox())
    
    draw(dev_img)
    draw(dev_wmf)
    draw(dev_emf)
    draw(dev_pdf)
    draw(dev_svg)
    draw(dev_ppt)
    
if __name__ == "__main__":
    save()