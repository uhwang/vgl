# Vector Graphic Library (VGL) for Python
#
# drawaxis.py
#
# 03/06/2023
#
# Author: Uisang Hwang
# Email : uhwangtx@gmail.com
#
import math

from . import axis
from . import drawtick
from . import drawgrid
from . import drawlabel
from . import util
from . import text

def draw_axis(dev):

    if dev.frm.axis_t == axis.AXIS_CARTESIAN:
        # TODO: check plot type(xy, 2d, 3d)
        xaxis = dev.frm.get_xaxis()
        yaxis = dev.frm.get_yaxis()
    
        xmin = xaxis.amin
        xmax = xaxis.amax
    
        ymin = yaxis.amin
        ymax = yaxis.amax
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
    else:
        raxis = dev.frm.axis_polar.raxis
        taxis = dev.frm.axis_polar.taxis
        hgt = dev.frm.hgt()
        
        # draw r axis
        if raxis.show:
            # major r-tick
            if raxis.major_tick.show:
                rr = raxis.dr
                while rr <= raxis.rmax:
                    dev.circle(0,0, rr, raxis.major_tick.lcol, 
                                        raxis.major_tick.lthk*dev.frm.hgt(), 
                                        raxis.major_tick.lpat)
                    rr += raxis.dr
            
        # minor r-tick
        # draw theta axis
        if taxis.show:
            if taxis.major_tick.show:
                tt = taxis.dtheta
                while tt <= 360.0:
                    rt = util.deg_to_rad(tt)
                    dev.line(0,0,raxis.rmax*math.cos(rt), 
                                 raxis.rmax*math.sin(rt),
                                 taxis.major_tick.lcol, 
                                 taxis.major_tick.lthk*dev.frm.hgt(), 
                                 taxis.major_tick.lpat)
                    tt += taxis.dtheta
        
            if taxis.label.show:
                tlabel = taxis.get_label()
                tlabel.pos = 0.01*hgt
                tt = 0
                while tt < 360.0:
                    rt = util.deg_to_rad(tt)
                    tlabel.x = dev._x_viewport(raxis.rmax*math.cos(rt))
                    tlabel.y = dev._y_viewport(raxis.rmax*math.sin(rt))
                    if tt == 0:
                        tlabel.wv()
                        tlabel.x += tlabel.pos
                    if tt > 0 and tt < 90: 
                        tlabel.ws()
                        tlabel.x += tlabel.pos
                    elif tt == 90: 
                        tlabel.hs()
                        #tlabel.x += tlabel.pos
                        tlabel.y -= tlabel.pos
                    elif tt == 120 or tt == 150:
                        tlabel.es()
                        tlabel.x -= tlabel.pos
                    elif tt == 180:
                        tlabel.ev()
                        tlabel.x -= tlabel.pos
                    elif tt == 210:
                        tlabel.en()
                        tlabel.x -= tlabel.pos
                       # tlabel.y += tlabel.pos
                    elif tt == 240:
                        tlabel.en()
                        #tlabel.x -= tlabel.pos
                        tlabel.y += tlabel.pos
                    elif tt == 270: 
                        tlabel.hn()
                        tlabel.y += tlabel.pos
                    elif tt == 300:
                        tlabel.wn()
                        tlabel.y += tlabel.pos
                    elif tt == 330:
                        tlabel.wn()
                        tlabel.y += tlabel.pos
                        
                    tlabel.text = "%1.0f\\deg"%tt
                    text.write_text(dev, tlabel, True)
                    tt += taxis.dtheta
                    
        if raxis.show and raxis.label.show:
            rlabel = raxis.get_label()
            maj_tick = raxis.get_major_tick()
        
            wxx = raxis.first_major_tick_pos
            vi = 1
            yy = 0
            yy = dev._y_viewport(yy)
            rlabel.en()
            shift =  rlabel.pos * hgt
            
            while wxx <= raxis.rmax:
                wxxl = dev._x_viewport(wxx)
                ypos = yy
                rlabel.x = wxxl - shift
                rlabel.y = ypos + shift
                rlabel.text = "%1.2f"%wxx
                text.write_text(dev, rlabel, True)
                wxx = raxis.first_major_tick_pos+raxis.spacing*vi
                vi+=1
