# Vector Graphic Library (VGL) for Python
#
# drawgrid.py
#
# 2020-2-12 Ver 0.1
#
# Author: Uisang Hwang
# Email : uhwangtx@gmail.com
#

import vgl.frame
import vgl.axis

def draw_grid_2d(dev):
    frm = dev.frm
    xx = yy = mispc = oxx = wxx = wyy = mitlen = mjtlen = 0.0
    i  = j  = vi    = 0
    
    # draw tick on x axis
    hgt = frm.hgt()
    xaxis = frm.get_xaxis()
    maj_grid = xaxis.get_major_grid()
    min_grid = xaxis.get_minor_grid()
    
    #mitlen = min_tick.llen*hgt
    #mjtlen = maj_tick.llen*hgt
    mispc  = xaxis.spacing/(xaxis.nminor_tick+1)
    
    #maj_ty0, maj_ty1 = tick_pos_dir(maj_tick, mjtlen)
    #min_ty0, min_ty1 = tick_pos_dir(min_tick, mitlen)
    
    # draw first minor grid
    sy = frm.bbox.sy+frm.pdom.get_sy()+frm.pdom.get_hgt()
    ey = frm.bbox.sy+frm.pdom.get_sy() #frm.pdom.get_ey()
    fnt = xaxis.first_nminor_tick
    
    if min_grid.show:
        dev.make_pen(min_grid.lcol, min_grid.lthk*hgt)
        if fnt > 0:
            for i in range(fnt):
                wxx = xaxis.first_minor_tick_pos+mispc*i
                wxxl= dev.wtol_x(wxx)
                dev.lline(wxxl,sy,wxxl,ey)
            wxx += mispc
        else: 
            wxx = xaxis.first_major_tick_pos + mispc
            
        # draw minor ticks
        j=1
        vi = 1
        owxx = wxx
        
        while wxx <= xaxis.max:
            wxxl= dev.wtol_x(wxx)	
            dev.lline(wxxl,sy,wxxl,ey)
        
            if j == xaxis.nminor_tick:
                vi+=1
                wxx = owxx+mispc*vi
                vi+=1
                j = 0
            else:
                wxx = owxx+mispc*vi
                vi+=1
            j+=1
        dev.delete_pen()
    
    if xaxis.major_grid.show:    
        vi = 1
        wxx = xaxis.first_major_tick_pos
        dev.make_pen(maj_grid.lcol, maj_grid.lthk*hgt)
        while wxx <= xaxis.max:
            wxxl = dev.wtol_x(wxx)
            dev.lline(wxxl, sy, wxxl, ey)
            wxx = xaxis.first_major_tick_pos+xaxis.spacing*vi
            vi+=1
        dev.delete_pen()
   
    ## draw grid on y axis
    yaxis = frm.get_yaxis()
    maj_grid = yaxis.get_major_grid()
    min_grid = yaxis.get_minor_grid()
    #mitlen = min_tick.llen*hgt
    #mjtlen = maj_tick.llen*hgt
    mispc = yaxis.spacing/(yaxis.nminor_tick+1)
    
    sx = frm.bbox.sx+frm.pdom.get_sx()
    ex = sx+frm.pdom.get_wid()
    fnt = yaxis.first_nminor_tick
    #maj_tx0, maj_tx1 = tick_pos_dir(maj_tick, mjtlen)
    #min_tx0, min_tx1 = tick_pos_dir(min_tick, mitlen)
    
    if yaxis.minor_grid.show:
        dev.make_pen(min_grid.lcol, min_grid.lthk*hgt)
        if fnt != 0:
            for i in range(fnt):
                wyy = yaxis.first_minor_tick_pos+mispc*i
                wyyl= dev.wtol_y(wyy)
                dev.lline(sx, wyyl, ex, wyyl)
            wyy += mispc
        else: 
            wyy = yaxis.first_major_tick_pos
        j=0
        vi = 1
        owyy = wyy
        wyy = yaxis.first_minor_tick_pos
    
        while wyy <= yaxis.max:
            wyyl = dev.wtol_y(wyy)
            dev.lline(sx,wyyl,ex,wyyl)	
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
    
    if yaxis.major_grid.show:
        vi = 1;
        wyy = yaxis.first_major_tick_pos
        dev.make_pen(maj_grid.lcol, maj_grid.lthk*hgt)
        while wyy <= yaxis.max:
            wyyl = dev.wtol_y(wyy)
            dev.lline(sx, wyyl, ex, wyyl)
            wyy = yaxis.first_major_tick_pos+yaxis.spacing*vi
            vi+=1
        dev.delete_pen()