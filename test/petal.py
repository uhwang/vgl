# petal.py

import numpy as np
import vgl

theta = np.linspace(0, 2*np.pi, 300, endpoint=True)
rho = np.sin(2*theta)*np.cos(2*theta);
rmax = np.max(rho)
fmm = vgl.FrameManager()
frm = fmm.create(1,1,4,4, vgl.Data(-rmax, rmax, -rmax, rmax))

def draw(dev):
    dev.set_device(frm)
    vgl.polarplot(dev, theta, rho, fcol=vgl.Color(0xF0,0xE6,0x8C))
    vgl.draw_axis(dev)
    dev.close()

def save():
    import chkfld
    
    if not chkfld.create_folder("./petal"):
        return
            
    dev_img = vgl.DeviceIMG("./petal/petal.jpg", fmm.get_gbbox(), 300)
    dev_pdf = vgl.DevicePDF("./petal/petal.pdf", fmm.get_gbbox())
    dev_wmf = vgl.DeviceWMF("./petal/petal.wmf", fmm.get_gbbox())
    dev_emf = vgl.DeviceEMF("./petal/petal.emf", fmm.get_gbbox())
    dev_svg = vgl.DeviceSVG("./petal/petal.svg", fmm.get_gbbox(), 300)
    dev_ppt = vgl.DevicePPT("./petal/petal.pptx", fmm.get_gbbox())
    
    draw(dev_img)
    draw(dev_pdf)
    draw(dev_wmf)
    draw(dev_emf)
    draw(dev_svg)
    draw(dev_ppt)

if __name__ == "__main__":
    save()    