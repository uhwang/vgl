# test arrow

import vgl
import numpy as np

xmin,xmax,ymin,ymax=-1.2, 1.2, -1.2, 1.2
data = vgl.Data(xmin,xmax,ymin,ymax)
fmm = vgl.FrameManager()
frm = fmm.create(1,1,4,4, data)
frm.show_all_major_grid()
nth = 20
r = 1
th = np.linspace(0, np.pi*2, nth)
arrows = [vgl.basicshape.EndArrowLine(frm, 
            0,0,
            r*np.cos(t),
            r*np.sin(t)) for t in th]
            
def plot(dev):
    #vgl.draw_frame(dev)
    #vgl.draw_axis(dev)
    
    for a in arrows:
        a.end_arrow.col = vgl.color.RED
        a.end_arrow.type_t=vgl.basicshape._ARROWTYPE_CLOSEDFILLED
        a.draw(dev)
        
    dev.close()
    
dev_img = vgl.DeviceCairo("test-arrow.jpg", fmm.get_gbbox(), 300)
dev_pdf = vgl.DevicePDF  ("test-arrow.pdf", fmm.get_gbbox())
dev_wmf = vgl.DeviceWMF  ("test-arrow.wmf", fmm.get_gbbox())
dev_emf = vgl.DeviceEMF  ("test-arrow.emf", fmm.get_gbbox())
dev_svg = vgl.DeviceSVG  ("test-arrow.svg", fmm.get_gbbox(), 300)

dev_img.set_plot(frm)
plot(dev_img)

dev_pdf.set_plot(frm)
plot(dev_pdf)

dev_wmf.set_plot(frm)
plot(dev_wmf)

dev_emf.set_plot(frm)
plot(dev_emf)

dev_svg.set_plot(frm)
plot(dev_svg)
