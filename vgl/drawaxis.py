# axis.py
import vgl.frame
import vgl.axis

def draw_axis(dev):
	frm = dev.frm
	xaxis = frm.get_xaxis()
	yaxis = frm.get_yaxis()
	
	# draw x-axis
	dev.make_pen(xaxis.lcol, xaxis.lthk*frm.hgt())
	dev.lline(frm.pdom.get_sx(), frm.pdom.get_ey(), frm.pdom.get_ex(), frm.pdom.get_ey())
	dev.delete_pen()
	
	# draw y-axis
	dev.make_pen(yaxis.lcol, yaxis.lthk*frm.hgt())
	dev.lline(frm.pdom.get_sx(), frm.pdom.get_ey(), frm.pdom.get_sx(), frm.pdom.get_sy())
	dev.delete_pen()