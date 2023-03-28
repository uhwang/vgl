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
        pos_y = axis.get_xaxis_ypos(xaxis,yaxis)
        x1 = dev._x_viewport(xmin)
        x2 = dev._x_viewport(xmax)
        yy = dev._y_viewport(pos_y)
        dev.lline(x1, yy, x2, yy, lcol= xaxis.lcol, 
                                 lthk=xaxis.lthk*dev.frm.hgt())
    
    #draw y-axis
    if yaxis.show:
        pos_x = axis.get_yaxis_xpos(xaxis,yaxis)
        y1 = dev._y_viewport(ymin)
        y2 = dev._y_viewport(ymax)
        xx = dev._x_viewport(pos_x)
        dev.lline(xx, y1, xx, y2, lcol=yaxis.lcol, 
                                 lthk=yaxis.lthk*dev.frm.hgt())
        
    drawtick.draw_tick(dev)
    drawgrid.draw_grid(dev)
    drawlabel.draw_label(dev)