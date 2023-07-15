# test arrow

import vgl
import numpy as np

xmin,xmax,ymin,ymax=-1.2, 1.2, -1.2, 1.2
data = vgl.Data(xmin,xmax,ymin,ymax)
fmm = vgl.FrameManager()
frm = fmm.create(1,1,4,4, data)
frm.show_all_major_grid()
nth = 13
r = 0.9
th = np.linspace(0, np.pi*2, nth)
ctbl = vgl.create_color_table(0,270, 0.8, 1, nth)

arrows = [vgl.basicshape.EndArrowLine(frm, 
            0,0,
            r*np.cos(t),
            r*np.sin(t),
            lpat=vgl.linepat._PAT_DASH,
            lthk = 0.005,
            col = ctbl[i],
            #type_t = vgl.basicshape._ARROWTYPE_OPEN) 
            #type_t = vgl.basicshape._ARROWTYPE_CLOSED) 
            type_t = vgl.basicshape._ARROWTYPE_CLOSEDFILLED) 
            for i,t in enumerate(th)]

del arrows[-1]

arrow = vgl.basicshape.EndArrowLine(frm, 
            1.5, 1.2, 3.5, 1.2,
            #lpat=vgl.linepat._PAT_DASH,
            lthk = 0.005,
            col=vgl.color.GREEN,
            type_t = vgl.basicshape._ARROWTYPE_CLOSED,
            viewport=True) 

box = vgl.basicshape.Box(-1,-1,0.25,0.25,
                        lcol=vgl.color.BLUE,
                        lthk=0.005,
                        fcol=vgl.color.CUSTOM1)
def plot(dev):
    vgl.draw_frame(dev)
    vgl.draw_axis(dev)
    
    arrow.draw(dev)
    
    for a in arrows:
        a.draw(dev)
        
    box.draw(dev)
    
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
