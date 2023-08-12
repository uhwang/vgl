![pramsym](https://github.com/uhwang/vgl/assets/43251090/3547a129-31e2-488b-a9b0-2b3cb3ececea)

```python
# pramsym.py
# r = sin(4θ/9) for 0 ≤ θ ≤ 18π
# [− 9/2π, 9/2π], [0, 9π], and [0, 18π] 

import numpy as np
import vgl

theta1 = np.linspace(-4.5*np.pi, 4.5*np.pi, 300, endpoint=True)
theta2 = np.linspace( 0.0      ,   9*np.pi, 400, endpoint=True)
theta3 = np.linspace( 0.0      ,  18*np.pi, 700, endpoint=True)

rho1 = np.sin(4*theta1/9)
rho2 = np.sin(4*theta2/9)
rho3 = np.sin(4*theta3/9)

fmm  = vgl.FrameManager()
frm1 = fmm.create(0.0,1.0,3,3, vgl.Data(-1, 1, -1, 1))
frm2 = fmm.create(2.7,1.0,3,3, vgl.Data(-1, 1, -1, 1))
frm3 = fmm.create(5.4,1.0,3,3, vgl.Data(-1, 1, -1, 1))

def plot(dev):
    dev.set_device(frm1)
    vgl.polarplot(dev, theta1, rho1, axis_t = vgl.axis.AXIS_CARTESIAN)
    
    dev.set_device(frm2)
    vgl.polarplot(dev, theta2, rho2, axis_t = vgl.axis.AXIS_CARTESIAN)
    
    dev.set_device(frm3)
    vgl.polarplot(dev, theta3, rho3, axis_t = vgl.axis.AXIS_CARTESIAN)
    dev.close()

def save():
    import chkfld
    
    if not chkfld.create_folder("./pramsym"):
        return
            
    dev_img = vgl.DeviceIMG("./pramsym/pramsym.jpg", fmm.get_gbbox(), 300)
    dev_pdf = vgl.DevicePDF("./pramsym/pramsym.pdf", fmm.get_gbbox())
    dev_wmf = vgl.DeviceWMF("./pramsym/pramsym.wmf", fmm.get_gbbox())
    dev_emf = vgl.DeviceEMF("./pramsym/pramsym.emf", fmm.get_gbbox())
    dev_svg = vgl.DeviceSVG("./pramsym/pramsym.svg", fmm.get_gbbox(), 300)
    dev_ppt = vgl.DevicePPT("./pramsym/pramsym.pptx", fmm.get_gbbox())
    
    plot(dev_img)
    plot(dev_pdf)
    plot(dev_wmf)
    plot(dev_emf)
    plot(dev_svg)
    plot(dev_ppt)
    
if __name__ == "__main__":
    save()
