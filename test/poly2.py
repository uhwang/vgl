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
    plist.append(vgl.Polygon(-2, 2,4,1.5,vgl.BLACK, 0.007))
    plist.append(vgl.Polygon( 2, 2,5,1.5,vgl.PURPLE, 0.015, 
                              lpat = vgl.linepat._PAT_DASH))
    plist.append(vgl.Polygon( 2,-2,6,1.5,vgl.PURPLE, 0.007, 
                              fcol=vgl.GREEN))
    plist.append(vgl.Polygon(-2,-2,7,1.5,vgl.PURPLE, 0.007, 
                              lpat = vgl.linepat._PAT_DASHDOT,
                              fcol=vgl.YELLOW
                              ))
    plist.append(vgl.Polygon( 0, 0,3,1,vgl.BLACK, 0.007, fcol=vgl.CYAN))
    
def draw_poly(dev):
    dev.set_device(frm)
    vgl.drawaxis.draw_axis(dev)
    
    for p in plist:
        dev.polygon(p.get_xs(), 
                    p.get_ys(), 
                    lcol=p.lcol, 
                    lthk=p.lthk, 
                    lpat=p.get_line_pattern(), 
                    fcol=p.fcol)
    dev.close()
    
create_polygon_list()

def save():
    import chkfld
    
    if not chkfld.create_folder("./poly2"):
        return
    
    dev_wmf = vgl.DeviceWMF("./poly2/poly2.wmf", gbox)
    dev_emf = vgl.DeviceEMF("./poly2/poly2.emf", gbox)
    dev_pdf = vgl.DevicePDF("./poly2/poly2.pdf", gbox)
    dev_svg = vgl.DeviceSVG("./poly2/poly2.svg", gbox, 200)
    dev_ppt = vgl.DevicePPT("./poly2/poly2.pptx",gbox)
    dev_img = vgl.DeviceIMG("./poly2/poly2.jpg", gbox, 200)
    
    draw_poly(dev_wmf)
    draw_poly(dev_emf)
    draw_poly(dev_pdf)
    draw_poly(dev_svg)
    draw_poly(dev_ppt)
    draw_poly(dev_img)

if __name__ == "__main__":
    save()