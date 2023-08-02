![polar-cardioid](https://github.com/uhwang/vgl/assets/43251090/35b52715-eaf6-4181-88f5-fd633271204b)

```python
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
    vgl.draw_axis(dev)
    dev.close()

dev_img = vgl.DeviceIMG("polar-cardioid.jpg", fmm.get_gbbox(), 300)
dev_pdf = vgl.DevicePDF("polar-cardioid.pdf", fmm.get_gbbox())
dev_wmf = vgl.DeviceWMF("polar-cardioid.wmf", fmm.get_gbbox())
dev_emf = vgl.DeviceEMF("polar-cardioid.emf", fmm.get_gbbox())
dev_svg = vgl.DeviceSVG("polar-cardioid.svg", fmm.get_gbbox(), 300)
dev_ppt = vgl.DevicePPT("polar-cardioid.pptx", fmm.get_gbbox())

plot(dev_img)
plot(dev_pdf)
plot(dev_wmf)
plot(dev_emf)
plot(dev_svg)
plot(dev_ppt)
