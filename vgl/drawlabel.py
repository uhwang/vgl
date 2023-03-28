# Vector Graphic Library (VGL) for Python
#
# drawlabel.py
#
# 2020-2-12 Ver 0.1
#
# Author: Uisang Hwang
# Email : uhwangtx@gmail.com
#

from . import color
from . import text
from . import axis


def draw_label(dev):
    frm = dev.frm
    xx = yy = mispc = oxx = wxx = wyy = mitlen = mjtlen = 0.0
    i  = j  = vi    = 0
    
    hgt = frm.hgt()
    xaxis = frm.get_xaxis()
    yaxis = frm.get_yaxis()

    xlabel = xaxis.get_label()
    ylabel = yaxis.get_label()
    
    if xlabel.show:
        maj_tick = xaxis.get_major_tick()
        
        wxx = xaxis.first_major_tick_pos
        vi = 1
        yy = axis.get_xaxis_ypos(xaxis,yaxis)
        yy = dev._y_viewport(yy)
    
        while wxx <= xaxis.max:
            wxxl = dev._x_viewport(wxx)
            ypos = yy + xlabel.pos * hgt
            xlabel.x = wxxl
            xlabel.y = ypos
            xlabel.text = "%1.2f"%wxx
            text.write_text(dev, xlabel, True)
            wxx = xaxis.first_major_tick_pos+xaxis.spacing*vi
            vi+=1

    if ylabel.show:
        maj_tick = yaxis.get_major_tick()
        wyy = yaxis.first_major_tick_pos
        vi = 1
        xx = axis.get_yaxis_xpos(xaxis,yaxis)
        xx = dev._x_viewport(xx)
        ylabel.ev()
        ylabel.pos  = 0.01
        while wyy <= yaxis.max:
            wyyl = dev._y_viewport(wyy)
            xpos = xx - ylabel.pos * hgt
            ylabel.x = xpos
            ylabel.y = wyyl
            ylabel.text = "%1.2f"%wyy
            text.write_text(dev, ylabel, True)
            wyy = yaxis.first_major_tick_pos+yaxis.spacing*vi
            vi+=1
