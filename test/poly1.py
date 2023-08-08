# poly1.py
#
#	Ref: Math Adventures with Python by Peter Farell 
#
import numpy as np
import vgl

data = vgl.Data(-10,10,-10,10)
fmm = vgl.FrameManager()
frm = fmm.create(0,0,4,4, data)
frm.show_all_grid()
gbox = fmm.get_gbbox()
plist = []

def create_polygon_list():
    side = 1.7
    jump = 2.2*side
    sx = -5.6
    sy = 5.6
    j = 0
    i = 1
    y = sy
    nstart = 3 
    nend = 19
    step = 170/(nend-nstart)
    for n in range(nstart, nend, 1):
        x = sx+j*jump
        plist.append(vgl.geom.Polygon(x,y,n,side,
                    vgl.color.BLACK,
                    0.001,
                    fcol=vgl.color.hsv((n-3)*step,1,1)))
        j += 1
        if j%4==0:
            y = sy-i*jump
            j = 0
            i += 1
            
def draw(dev):
    dev.set_device(frm)
    vgl.draw_axis(dev)
    
    for i in range(len(plist)):
        sh = plist[i]
        dev.polygon(sh.get_xs(), sh.get_ys(), lcol=sh.lcol, lthk=sh.lthk, fcol=sh.fcol)

    dev.close()
    
create_polygon_list()

def save():
    import chkfld
    
    if not chkfld.create_folder("./poly1"):
        return
    
    dev_wmf = vgl.DeviceWMF("./poly1/poly1.wmf", gbox)
    dev_emf = vgl.DeviceEMF("./poly1/poly1.emf", gbox)
    dev_pdf = vgl.DevicePDF("./poly1/poly1.pdf", gbox)
    dev_svg = vgl.DeviceSVG("./poly1/poly1.svg", gbox, 200)
    dev_ppt = vgl.DevicePPT("./poly1/poly1.pptx",gbox)
    dev_img = vgl.DeviceIMG("./poly1/poly1.jpg", gbox, 200)
    
    draw(dev_wmf)
    draw(dev_emf)
    draw(dev_pdf)
    draw(dev_svg)
    draw(dev_ppt)
    draw(dev_img)
    
if __name__ == "__main__":
    save()
