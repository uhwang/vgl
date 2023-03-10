# Vector Graphic Library (VGL) for Python
#
# drawaxis.py
#
# 03/06/2023
#
# Author: Uisang Hwang
# Email : uhwangtx@gmail.com
#

from . import axis
from . import drawtick
from . import drawgrid
from . import drawlabel

def draw_axis(dev):
    # TODO: check plot type(xy, 2d, 3d)
    xaxis = dev.frm.get_xaxis()
    yaxis = dev.frm.get_yaxis()

    xmin = xaxis.min
    xmax = xaxis.max

    ymin = yaxis.min
    ymax = yaxis.max
    
    # draw x-axis
    if xaxis.show:
        pos_y = ymin # default axis._POS_BOTTOM
        pos_t = xaxis.pos_t
        
        if pos_t == axis._POS_TOP:
            pos_y = ymax
        elif pos_t == axis._POS_ZERO:
            pos_y = 0
        
        x1 = dev._x_viewport(xmin)
        x2 = dev._x_viewport(xmax)
        yy = dev._y_viewport(pos_y)
        dev.lline(x1, yy, x2, yy, lcol= xaxis.lcol, 
                                 lthk=xaxis.lthk*dev.frm.get_pdom_hgt())
    
    #draw y-axis
    if yaxis.show:
        pos_x = xmin # default axis._POS_LEFT
        pos_t = yaxis.pos_t
        
        if pos_t == axis._POS_RIGHT:
            pos_x = xmax
        elif pos_t == axis._POS_ZERO:
            pos_x = 0
        
        y1 = dev._y_viewport(ymin)
        y2 = dev._y_viewport(ymax)
        xx = dev._x_viewport(pos_x)
        
        dev.lline(xx, y1, xx, y2, lcol=yaxis.lcol, 
                                 lthk=yaxis.lthk*dev.frm.get_pdom_hgt())
        
    drawtick.draw_tick(dev)
    drawgrid.draw_grid(dev)
    drawlabel.draw_label(dev)