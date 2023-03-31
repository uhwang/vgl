# vgl
Vector Graphic Library for Python

# Introduction
## Plotting Engine
![Slide2](https://user-images.githubusercontent.com/43251090/229162160-5899a185-4e94-4ea9-90c9-81a33428163b.PNG)

## Sample 01
...Python
import vgl
xmin,xmax,ymin,ymax=-3,3,-3,3
data = vgl.Data(xmin,xmax,ymin,ymax)
fmm = vgl.FrameManager()
frm = fmm.create(1,1,4,4, data)

def plot(dev):
    vgl.draw_frame(dev)
    vgl.draw_axis(dev)
    
dev = vgl.DeviceCairo("intro01-01.jpg", fmm.get_gbbox(), 200)
dev.set_device(frm)
plot(dev)
dev.close()

dev = vgl.DeviceWindowsMetafile("intro01-01.wmf", fmm.get_gbbox())
dev.set_device(frm)
plot(dev)
dev.close()

dev = vgl.DeviceEnhancedMetafile("intro01-01.emf", fmm.get_gbbox())
dev.set_device(frm)
plot(dev)
dev.close()

dev = vgl.DevicePDF("intro01-01.pdf", fmm.get_gbbox())
dev.set_device(frm)
plot(dev)
dev.close()
...
