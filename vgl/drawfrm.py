# Vector Graphic Library (VGL) for Python
#
# drawfrm.py
#
# 2020-2-12 Ver 0.1
#
# Author: Uisang Hwang
# Email : uhwangtx@gmail.com
#

from vgl import color, frame

def draw_axis(dev, data):
	#draw x-axis
	dev.line(data.xmin, data.ymin, data.xmax, data.ymin, color.BLACK, 0.005*dev.frm.hgt())
	#draw y-axis
	dev.line(data.xmin, data.ymin, data.xmin, data.ymax, color.BLACK, 0.005*dev.frm.hgt())
		
def draw_grid(dev, data, spc):
	nxgrid = int((data.xmax-data.xmin)/spc)+1
	nygrid = int((data.ymax-data.ymin)/spc)+1
	dev.make_pen(color.GRAY50, 0.001*dev.frm.hgt())
	for i in range(nxgrid):
		x = data.xmin+i*spc
		dev.line(x, data.ymin, x, data.ymax)
	# draw y grid
	y=data.ymin
	for i in range(nygrid):
		y = data.ymin+i*spc
		dev.line(data.xmin, y, data.xmax, y)
	dev.delete_pen()
	
def draw_frame(dev, frm):
	fp = frm.get_property()
	#if fb.bk_show:
		
	if fp.header_show:
		sx = frm.bbox.sx
		sy = frm.bbox.sy
		ex = frm.bbox.ex
		ey = sy+frm.bbox.hgt()*fp.header_thk
		xx = [sx,sx,ex,ex]
		yy = [sy,ey,ey,sy]
		#dev.lpolygon(xx, yy, lcol=fp.header_col, fcol=fp.header_col)
		dev.lpolygon(xx, yy, fcol=fp.header_col)
		
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
	
	
