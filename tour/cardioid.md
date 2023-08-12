![cardioid](https://github.com/uhwang/vgl/assets/43251090/4eaf3917-a5b4-45d1-bf27-73dd4ebdc437)
```Python
# cardioid.py
import numpy as np
import vgl

theta = np.linspace(0, 2*np.pi, 300, endpoint=True)
rho = 3*(1+np.cos(theta))
rmax = np.max(rho)
fmm = vgl.FrameManager()
frm = fmm.create(1,1,4,4, vgl.Data(-rmax, rmax, -rmax, rmax))

def plot(dev):
    dev.set_device(frm)
    vgl.polarplot(dev, theta, rho, fcol=vgl.Color(0xF0,0xE6,0x8C))
    dev.close()

def save():
    import chkfld
    
    if not chkfld.create_folder("./cardioid"):
        return
            
    dev_img = vgl.DeviceIMG("./cardioid/cardioid.jpg", fmm.get_gbbox(), 300)
    dev_pdf = vgl.DevicePDF("./cardioid/cardioid.pdf", fmm.get_gbbox())
    dev_wmf = vgl.DeviceWMF("./cardioid/cardioid.wmf", fmm.get_gbbox())
    dev_emf = vgl.DeviceEMF("./cardioid/cardioid.emf", fmm.get_gbbox())
    dev_svg = vgl.DeviceSVG("./cardioid/cardioid.svg", fmm.get_gbbox(), 300)
    dev_ppt = vgl.DevicePPT("./cardioid/cardioid.pptx", fmm.get_gbbox())
    
    plot(dev_img)
    plot(dev_pdf)
    plot(dev_wmf)
    plot(dev_emf)
    plot(dev_svg)
    plot(dev_ppt)
    
if __name__ == "__main__":
    save()
