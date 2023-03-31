# vgl
Vector Graphic Library for Python

# Introduction
## Plotting Engine
![Slide2](https://user-images.githubusercontent.com/43251090/229162160-5899a185-4e94-4ea9-90c9-81a33428163b.PNG)

## Sample 01
```Python
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
```
![intro01-01](https://user-images.githubusercontent.com/43251090/229165118-929608e3-734f-4bb9-8b3f-4a4ea5d3cb30.jpg)
