![pattern](https://github.com/uhwang/vgl/assets/43251090/d193910a-86cf-44c6-8ff1-04a222cfb31b)
```Python
# pattern.py
import numpy as np
import vgl

xx = np.linspace(-4,4, 100, endpoint=True)
y1 = 0.5*xx
y2 = 0.5*xx+1
y3 = 0.5*xx+2
y4 = 0.5*xx+3
y5 = 0.5*xx+4
y6 = 0.5*xx+5

xmin, xmax, ymin, ymax = xx.min(), xx.max(), y1.min(), y6.max()

fmm = vgl.FrameManager()
frm = fmm.create(1,1,4,5, vgl.Data(xmin,xmax,ymin,ymax))

def plot(dev):
    dev.set_device(frm)
    dev.polyline(xx,y1, lcol=vgl.color.BLUE,lthk=0.003)
    dev.polyline(xx,y2, lcol=vgl.color.BLUE,lthk=0.003, lpat=vgl.linepat.get_stock_dash())
    dev.polyline(xx,y3, lcol=vgl.color.BLUE,lthk=0.003, lpat=vgl.linepat.get_stock_dashdot())
    dev.polyline(xx,y4, lcol=vgl.color.BLUE,lthk=0.003, lpat=vgl.linepat.get_stock_dot())
    dev.polyline(xx,y5, lcol=vgl.color.BLUE,lthk=0.003, lpat=vgl.linepat.get_stock_longdash())
    dev.polyline(xx,y6, lcol=vgl.color.BLUE,lthk=0.003, lpat=vgl.linepat.get_stock_dashdotdot())
    
    vgl.draw_axis(dev)
    dev.close()
    
def save():
    import chkfld
    
    if not chkfld.create_folder("./pattern"):
        return
            
    dev_img = vgl.DeviceIMG("./pattern/pattern.jpg", fmm.get_gbbox(), 300)
    dev_pdf = vgl.DevicePDF("./pattern/pattern.pdf", fmm.get_gbbox())
    dev_wmf = vgl.DeviceWMF("./pattern/pattern.wmf", fmm.get_gbbox())
    dev_emf = vgl.DeviceEMF("./pattern/pattern.emf", fmm.get_gbbox())
    dev_svg = vgl.DeviceSVG("./pattern/pattern.svg", fmm.get_gbbox(), 300)
    dev_ppt = vgl.DevicePPT("./pattern/pattern.pptx",fmm.get_gbbox())
    
    plot(dev_img)
    plot(dev_pdf)
    plot(dev_wmf)
    plot(dev_emf)
    plot(dev_svg)
    plot(dev_ppt)
    
if __name__ == "__main__":
    save()
