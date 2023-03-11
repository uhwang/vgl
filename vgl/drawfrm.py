# Vector Graphic Library (VGL) for Python
#
# drawfrm.py
#
# 2020-2-12 Ver 0.1
#
# Author: Uisang Hwang
# Email : uhwangtx@gmail.com
#

from . import color, frame
#import color, frame

#def draw_axis(dev, data):
#	#draw x-axis
#	dev.line(data.xmin, 0, data.xmax, 0, color.BLACK, 0.005*dev.frm.hgt())
#	#draw y-axis
#	dev.line(0, data.ymin, 0, data.ymax, color.BLACK, 0.005*dev.frm.hgt())
		
#def draw_grid(dev, data, spc):
#
#    xmin = dev.frm.xaxis.min
#    xmax = dev.frm.xaxis.max
#    ymin = dev.frm.yaxis.min
#    ymax = dev.frm.yaxis.max
#    
#    nxgrid = int((xmax-xmin)/spc)+1
#    nygrid = int((ymax-ymin)/spc)+1
#    dev.make_pen(color.GRAY50, 0.001*dev.frm.hgt())
#    for i in range(nxgrid):
#    	x = xmin+i*spc
#    	dev.line(x, ymin, x, ymax)
#    # draw y grid
#    y=ymin
#    for i in range(nygrid):
#    	y = ymin+i*spc
#    	dev.line(xmin, y, xmax, y)
#    dev.delete_pen()
	
def draw_frame(dev):
    frm = dev.frm
    fp = frm.get_property()
    
    if fp.header_show:
    	sx = frm.bbox.sx
    	sy = frm.bbox.sy
    	ex = frm.bbox.ex
    	ey = sy+frm.bbox.hgt()*fp.header_thk
    	xx = [sx,sx,ex,ex]
    	yy = [sy,ey,ey,sy]
    	#dev.lpolygon(xx, yy, lcol=fp.header_col, fcol=fp.header_col)
    	dev.lpolygon(xx, yy, lcol=None, fcol=fp.header_col)
    	
    if fp.border_show:
    	dev.lpolyline(frm.get_frm_xs(), 
    	              frm.get_frm_ys(), 
    	              fp.border_col, 
    	              fp.border_thk*frm.hgt(), True)
    	
    if fp.pdombk_show:
    	if fp.pdombk_lshow:
    		dev.lpolyline(frm.get_pdom_xs(), 
    		              frm.get_pdom_ys(), 
    					  fp.pdombk_lcol, 
                          fp.pdombk_lthk*frm.hgt(), True)
	
	
