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

def draw_grdd_2d(dev):
	frm = dev.frm
	xx = yy = mispc = oxx = wxx = wyy = mitlen = mjtlen = 0.0
	i  = j  = vi    = 0
	
	# draw tick on x axis
	hgt = frm.hgt()
	xaxis = frm.get_xaxis()
	maj_tick = xaxis.get_major_tick()
	min_tick = xaxis.get_minor_tick()
	
	mitlen = min_tick.llen*hgt
	mjtlen = maj_tick.llen*hgt
	mispc  = xaxis.spacing/(xaxis.nminor_tick+1)
	
	maj_ty0, maj_ty1 = tick_pos_dir(maj_tick, mjtlen)
	min_ty0, min_ty1 = tick_pos_dir(min_tick, mitlen)
	
	# draw first minor ticks
	dev.make_pen(min_tick.lcol, min_tick.lthk*hgt)
	yy = frm.bbox.sy+frm.pdom.get_ey() #frm.pdom.get_ey()
		
	fnt = xaxis.first_nminor_tick
	if fnt != 0:
		vi = 0;
		for i in range(fnt):
			wxx = xaxis.first_minor_tick_pos+mispc*vi
			wxxl= dev.wtol_x(wxx)
			dev.lline(wxxl,yy+min_ty0,wxxl,yy+min_ty1)
			vi+=1
		wxx += mispc
	else: 
		wxx = xaxis.first_minor_tick_pos
		
	# draw minor ticks
	j=0
	vi = 1
	owxx = wxx
	wxx = xaxis.first_minor_tick_pos
	while wxx <= xaxis.max:
		wxxl= dev.wtol_x(wxx)	
		dev.lline(wxxl,yy+min_ty0,wxxl,yy+min_ty1)
	
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
	
	wxx = xaxis.first_major_tick_pos
	dev.make_pen(maj_tick.lcol, maj_tick.lthk*hgt)
	vi = 1
	while wxx <= xaxis.max:
		#if wxx > xaxis.max: break
		wxxl = dev.wtol_x(wxx)
		dev.lline(wxxl, yy+maj_ty0, wxxl, yy+maj_ty1)
		wxx = xaxis.first_major_tick_pos+xaxis.spacing*vi
		vi+=1
	dev.delete_pen()

	## draw tick on y axis
	yaxis = frm.get_yaxis()
	maj_tick = yaxis.get_major_tick()
	min_tick = yaxis.get_minor_tick()
	mitlen = min_tick.llen*hgt
	mjtlen = maj_tick.llen*hgt
	mispc = yaxis.spacing/(yaxis.nminor_tick+1)
	
	dev.make_pen(min_tick.lcol, min_tick.lthk*hgt)
	xx = frm.bbox.sx+frm.pdom.get_sx()#frm.pdom.get_sx()
	fnt = yaxis.first_nminor_tick
	maj_tx0, maj_tx1 = tick_pos_dir(maj_tick, mjtlen)
	min_tx0, min_tx1 = tick_pos_dir(min_tick, mitlen)
	
	if fnt != 0:
		for i in range(fnt):
			wyy = yaxis.first_minor_tick_pos+mispc*i
			wyyl= dev.wtol_y(wyy)
			dev.lline(xx-min_tx0, wyyl, xx-min_tx1, wyyl)
		wyy += mispc
	else: 
		wyy = yaxis.first_minor_tick_pos
	j=0
	vi = 1
	owyy = wyy
	wyy = yaxis.first_minor_tick_pos

	while wyy <= yaxis.max:
		wyyl = dev.wtol_y(wyy)
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
	
	vi = 1;
	wyy = yaxis.first_major_tick_pos
	dev.make_pen(maj_tick.lcol, maj_tick.lthk*hgt)
	while wyy <= yaxis.max:
		wyyl = dev.wtol_y(wyy)
		dev.lline(xx-maj_tx0, wyyl, xx-maj_tx1, wyyl)
		wyy = yaxis.first_major_tick_pos+yaxis.spacing*vi
		vi+=1
	dev.delete_pen()