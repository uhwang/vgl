'''
    directrix   y = -f
    focal point F = (0, F)
    a point     P = (x,y)
    |PF|^2 = |Pf|^2*np
    
    y=1/vf x**2

'''
import numpy as np
import vgl

data = vgl.data.Data(-6,6,-3,8)
fmm = vgl.frame.FrameManager()
frm = fmm.create(0,0,5,5, data)
gbox = fmm.get_gbbox()

f = -1
npnt = 100
x = np.linspace(data.xmin+1, data.xmax-1, npnt)
y = -1/(4*f)*x**2
fy = lambda x,f: -1/(4*f)*x**2
x1 = -4
y1 = fy(x1,f)
xx = (x1, x1, 0)
yy = (f, y1, -f)

def draw(dev):
    dev.set_device(frm)
    vgl.draw_axis(dev)
    dev.polyline(x, y, vgl.color.RED, 0.002)
    dev.line(-5, f, 5, f, vgl.color.BLACK, 0.001)
    dev.line(0, -1, 0, 6, vgl.color.BLACK, 0.001)
    dev.circle(x1,f, 0.1, fcol=vgl.color.GREEN) 
    dev.circle(0,-f, 0.1, fcol=vgl.color.GREEN) 
    dev.polyline(xx, yy, vgl.color.MAGENTA, 0.002)
    dev.circle(xx[1], yy[1], 0.1, fcol=vgl.color.BLACK)
    dev.close()
    
def save():
    import chkfld
    
    if not chkfld.create_folder("./parabola"):
        return
    
    dev_wmf = vgl.DeviceWMF("./parabola/parabola.wmf", gbox)
    dev_emf = vgl.DeviceEMF("./parabola/parabola.emf", gbox)
    dev_pdf = vgl.DevicePDF("./parabola/parabola.pdf", gbox)
    dev_svg = vgl.DeviceSVG("./parabola/parabola.svg", gbox, 200)
    dev_ppt = vgl.DevicePPT("./parabola/parabola.pptx",gbox)
    dev_img = vgl.DeviceIMG("./parabola/parabola.jpg", gbox, 200)
    
    draw(dev_wmf)
    draw(dev_emf)
    draw(dev_pdf)
    draw(dev_svg)
    draw(dev_ppt)
    draw(dev_img)
    
if __name__ == "__main__":
    save()
