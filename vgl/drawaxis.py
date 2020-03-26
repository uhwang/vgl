# axis.py
import vgl.frame
import vgl.axis

def draw_axis(dev):
	frm = dev.frm
	xaxis = frm.get_xaxis()
	yaxis = frm.get_yaxis()
	
	# draw x-axis
	dev.make_pen(xaxis.lcol, xaxis.lthk*frm.hgt())
	sx = frm.bbox.sx+frm.pdom.sx
	yy = frm.bbox.sy+frm.pdom.get_ey()
	ex = frm.bbox.sx+frm.pdom.get_ex()
	dev.lline(sx, yy, ex, yy)
	dev.delete_pen()
	
	# draw y-axis
	dev.make_pen(yaxis.lcol, yaxis.lthk*frm.hgt())
	xx = frm.bbox.sx+frm.pdom.sx
	sy = frm.bbox.sy+frm.pdom.sy
	ey = frm.bbox.sy+frm.pdom.get_ey()
	dev.lline(xx, sy, xx, ey)
	dev.delete_pen()