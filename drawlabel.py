# Vector Graphic Library (VGL) for Python
#
# drawlabel.py
#
# 2020-2-12 Ver 0.1
#
# Author: Uisang Hwang
# Email : uhwangtx@gmail.com
#

import vgl.color as color
import vgl.text as text

def draw_label_2d(dev):
	frm = dev.frm
	xx = yy = mispc = oxx = wxx = wyy = mitlen = mjtlen = 0.0
	i  = j  = vi    = 0
	
	hgt = frm.hgt()
	xaxis = frm.get_xaxis()
	xlabel = xaxis.get_xlabel()
	maj_tick = xaxis.get_major_tick()
	
	wxx = xaxis.first_major_tick_pos
	vi = 1
	yy = frm.bbox.sy+frm.pdom.get_ey()
	dev.make_pen(xlabel.lcol, xlabel.lthk*hgt)
	#xlabel.size = 0.02
	#xlabel.lcol = color.BLUE
	#xlabel.lthk = 0.002
	while wxx <= xaxis.max:
		wxxl = dev.wtol_x(wxx)
		#dev.lline(wxxl, yy+maj_ty0, wxxl, yy+maj_ty1)
		ypos = yy + xlabel.pos * hgt
		xlabel.x = wxxl
		xlabel.y = ypos
		xlabel.str = "%1.2f"%wxx
		xlabel.polyline = dev.lpolyline
		xlabel.polygon  = dev.lpolygon
		text.write_text(dev, xlabel)
		wxx = xaxis.first_major_tick_pos+xaxis.spacing*vi
		vi+=1
		#if wxx >= xaxis.max: break
	#dev.delete_pen()
	
	yaxis = frm.get_yaxis()
	ylabel = yaxis.get_ylabel()
	maj_tick = yaxis.get_major_tick()
	wyy = yaxis.first_major_tick_pos
	vi = 1
	xx = frm.bbox.sx+frm.pdom.get_sx()
	ylabel.ev()
	#dev.make_pen(xlabel.lcol, xlabel.lthk*hgt)
	#ylabel.size = 0.02
	#ylabel.lcol = color.BLUE
	#ylabel.lthk = 0.002
	ylabel.pos  = 0.01
	while wyy <= yaxis.max:
		#print(wyy, yaxis.max)
		wyyl = dev.wtol_y(wyy)
		#dev.lline(wxxl, yy+maj_ty0, wxxl, yy+maj_ty1)
		xpos = xx - ylabel.pos * hgt
		ylabel.x = xpos
		ylabel.y = wyyl
		ylabel.str = "%1.2f"%wyy
		ylabel.polyline = dev.lpolyline
		ylabel.polygon  = dev.lpolygon
		text.write_text(dev, ylabel)
		wyy = yaxis.first_major_tick_pos+yaxis.spacing*vi
		vi+=1
		#if wyy >= yaxis.max: break
	#dev.delete_pen()