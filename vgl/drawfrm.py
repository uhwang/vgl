# Vector Graphic Library (VGL) for Python
#
# drawfrm.py
#
# 2020-2-12 Ver 0.1
#
# Author: Uisang Hwang
# Email : uhwangtx@gmail.com
#

from . import color

def draw_frame(dev):
    frm = dev.frm
    fp = frm.get_property()
    
    if fp.bk_show:
        dev.lpolygon(frm.get_frm_xs(),
                     frm.get_frm_ys(), 
                     lcol=None, lthk=None, fcol=fp.bk_color)
        
    if fp.header_show:
        sx = frm.bbox.sx
        sy = frm.bbox.sy
        ex = frm.bbox.ex
        ey = sy+frm.bbox.hgt()*fp.header_thk
        xx = [sx,sx,ex,ex]
        yy = [sy,ey,ey,sy]
        #dev.lpolygon(xx, yy, lcol=fp.header_col, fcol=fp.header_col)
        dev.lpolygon(xx, yy, lcol=None, fcol=fp.header_col)
        
    # Draw frame border
    if fp.border_show:
        dev.lpolyline(frm.get_frm_xs(), 
                      frm.get_frm_ys(), 
                      fp.border_col, 
                      fp.border_thk*frm.hgt(), closed=True)
    
    # Plot domain background
    if fp.pdombk_show:
        if fp.pdombk_show:
            dev.lpolygon(frm.get_pdom_xs(), 
                        frm.get_pdom_ys(), 
                        lcol=None, lthk=None, fcol=fp.pdombk_fcol)
                        
        if fp.pdombk_border:
            dev.lpolyline(frm.get_pdom_xs(), 
                          frm.get_pdom_ys(), 
                          fp.pdombk_lcol, 
                          fp.pdombk_lthk*frm.hgt(), closed=True)
