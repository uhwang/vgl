# poly2.py
#
import vgl

data = vgl.Data(-4,4,-4,4)
fmm = vgl.FrameManager()
frm = fmm.create(0,0,4,4, data)
frm.show_all_major_grid()
plist = []
gbox = fmm.get_gbbox()

def create_polygon_list():
    plist.append(vgl.geom.Polygon(-2, 2,4,1.5,vgl.color.BLACK, 0.007))
    plist.append(vgl.geom.Polygon( 2, 2,5,1.5,vgl.color.PURPLE, 0.015, lpat = vgl.linepat._PAT_DASH))
    plist.append(vgl.geom.Polygon( 2,-2,6,1.5,vgl.color.PURPLE, 0.007, fcol=vgl.color.GREEN))
    plist.append(vgl.geom.Polygon(-2,-2,7,1.5,vgl.color.PURPLE, 0.007, fcol=vgl.color.YELLOW, lpat = vgl.linepat._PAT_DASHDOT))
    plist.append(vgl.geom.Polygon( 0, 0,3,1,vgl.color.BLACK, 0.007, vgl.color.CYAN))
    
def draw_shape(dev):
    dev.set_device(frm)
    vgl.drawaxis.draw_axis(dev)
    
    for p in plist:
        dev.polygon(p.get_xs(), p.get_ys(), 
                    p.lcol, p.lthk*dev.frm.hgt(), 
                    lpat=p.get_line_pattern(), fcol=p.fcol)
    dev.close()
    
create_polygon_list()

dev_wmf = vgl.DeviceWMF("poly2.wmf", gbox)
dev_emf = vgl.DeviceEMF("poly2.emf", gbox)
dev_pdf = vgl.DevicePDF("poly2.pdf", gbox)
dev_img = vgl.DeviceIMG("poly2.jpg", gbox, 200)
dev_svg = vgl.DeviceSVG("poly2.svg", gbox, 200)
dev_ppt = vgl.DevicePPT("poly2.pptx",gbox)

draw_shape(dev_wmf)
draw_shape(dev_emf)
draw_shape(dev_pdf)
draw_shape(dev_img)
draw_shape(dev_svg)
draw_shape(dev_ppt)
