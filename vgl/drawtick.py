# Vector Graphic Library (VGL) for Python
#
# drawtick.py
#
# 2020/02/12 Ver 0.1
# 2022/01/16 Fix x tick error
#
# Author: Uisang Hwang
# Email : uhwangtx@gmail.com
#

from . import axis

def tick_pos_dir(tick, len):
    if   tick.dir == axis.TICK_DIR_IN:
        return 0, -len
    elif tick.dir == axis.TICK_DIR_OUT:
        return 0, len
    elif tick.dir == axis.TICK_DIR_CENTER:
        half = len*0.5
        return -half, half
        
def draw_tick(dev):
    xx = yy = mispc = oxx = wxx = wyy = mitlen = mjtlen = 0.0
    i  = j  = vi    = 0
    
    hgt   = dev.frm.hgt()
    xaxis = dev.frm.get_xaxis()
    yaxis = dev.frm.get_yaxis()
    
    # draw tick on x axis

    maj_tick = xaxis.get_major_tick()
    min_tick = xaxis.get_minor_tick()
    
    mjtlen = maj_tick.llen*hgt
    mitlen = min_tick.llen*hgt
    mispc  = xaxis.spacing/(xaxis.nminor_tick+1)
    
    maj_ty0, maj_ty1 = tick_pos_dir(maj_tick, mjtlen)
    min_ty0, min_ty1 = tick_pos_dir(min_tick, mitlen)
    
    # draw first minor ticks
    #yy = frm.bbox.sy+frm.pdom.get_ey()
    yy = axis.get_xaxis_ypos(xaxis,yaxis)
    yy = dev._y_viewport(yy)
    
    fnt = xaxis.first_nminor_tick
    
    if xaxis.minor_tick.show:
        dev.make_pen(min_tick.lcol, min_tick.lthk*hgt)
        if fnt > 0:
            for i in range(fnt):
                wxx = xaxis.first_minor_tick_pos+mispc*i
                wxxl= dev._x_viewport(wxx)
                dev.lline(wxxl,yy+min_ty0,wxxl,yy+min_ty1)
                
        wxx = xaxis.first_major_tick_pos + mispc
        j=1
        vi = 1
        owxx = wxx
    
        while wxx <= xaxis.amax:
            wxxl = dev._x_viewport(wxx)
            dev.lline(wxxl,yy+min_ty0,wxxl,yy+min_ty1)	
            if j == xaxis.nminor_tick:
                vi += 1
                wxx = owxx+mispc*vi
                vi += 1
                j = 0
            else:
                wxx = owxx+mispc*vi
                vi += 1
            j += 1
        dev.delete_pen()
	
    if xaxis.major_tick.show:
        vi = 1;
        wxx = xaxis.first_major_tick_pos
        dev.make_pen(maj_tick.lcol, maj_tick.lthk*hgt)
        while wxx <= xaxis.amax:
            wxxl = dev._x_viewport(wxx)
            dev.lline(wxxl, yy+maj_ty0, wxxl, yy+maj_ty1)
            wxx = xaxis.first_major_tick_pos+xaxis.spacing*vi
            vi+=1
        dev.delete_pen()
	
    ## draw tick on y axis
    maj_tick = yaxis.get_major_tick()
    min_tick = yaxis.get_minor_tick()
    mitlen = min_tick.llen*hgt
    mjtlen = maj_tick.llen*hgt
    mispc = yaxis.spacing/(yaxis.nminor_tick+1)
    
    #xx = frm.bbox.sx+frm.pdom.get_sx()#frm.pdom.get_sx()
    xx = axis.get_yaxis_xpos(xaxis,yaxis)
    xx = dev._x_viewport(xx)
    
    fnt = yaxis.first_nminor_tick
    maj_tx0, maj_tx1 = tick_pos_dir(maj_tick, mjtlen)
    min_tx0, min_tx1 = tick_pos_dir(min_tick, mitlen)
    
    if yaxis.minor_tick.show:
        dev.make_pen(min_tick.lcol, min_tick.lthk*hgt)
        if fnt != 0:
            for i in range(fnt):
                wyy = yaxis.first_minor_tick_pos+mispc*i
                wyyl= dev._y_viewport(wyy)
                dev.lline(xx-min_tx0, wyyl, xx-min_tx1, wyyl)
            wyy += mispc
            
        wyy = yaxis.first_major_tick_pos + mispc
        j=1
        vi = 1
        owyy = wyy
    
        while wyy <= yaxis.amax:
            wyyl = dev._y_viewport(wyy)
            dev.lline(xx-min_tx0,wyyl,xx-min_tx1,wyyl)	
            if j == yaxis.nminor_tick:
                vi += 1
                wyy = owyy+mispc*vi
                vi += 1
                j = 0
            else:
                wyy = owyy+mispc*vi
                vi += 1
            j += 1
        dev.delete_pen()
	
    if yaxis.major_tick.show:
        vi = 1;
        wyy = yaxis.first_major_tick_pos
        dev.make_pen(maj_tick.lcol, maj_tick.lthk*hgt)
        while wyy <= yaxis.amax:
            wyyl = dev._y_viewport(wyy)
            dev.lline(xx-maj_tx0, wyyl, xx-maj_tx1, wyyl)
            wyy = yaxis.first_major_tick_pos+yaxis.spacing*vi
            vi+=1
        dev.delete_pen()