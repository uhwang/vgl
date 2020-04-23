# Vector Graphic Library (VGL) for Python
#
# frame.py
#
# 2020-2-12 Ver 0.1
#
# Author: Uisang Hwang
# Email : uhwangtx@gmail.com

# Number of pattern, Patterns
import numpy as np
import math
from vgl import color

VGL_DASHED    = 0
VGL_DASHDOT   = 1
VGL_DOTTED    = 2
VGL_LONGDASH  = 3
VGL_DASHDOTDOT= 4
PAT_EPS       = 1.e-6

pat_line_info = (
	( 2, ( 1.0      , 1.0, )),
	( 4, ( 1.0      , 0.399132, 0.199566, 0.399132, 0.0, )),
	( 2, ( 0.0021692, 0.247289, 0.0 )) ,
	( 2, ( 1.49892  , 0.498915, 0.0 )) ,
	( 6, ( 1.0      , 0.249458, 0.167028, 0.249458, 0.167028, 0.249458 ))
)


def distPP(p1,p2): 
	return np.sqrt((p2[0]-p1[0])**2+(p2[1]-p1[1])**2)

def get_pattern_line(dev, x,y, getxl, getyl, patlen, pat):
	v2 = np.empty(2, dtype='float32')
	ep1 = (0,0) #numpy.empty(2, dtype='float32')
	case1=False
	npnt = len(x)
	npnt1 = npnt-1
	ip2 = 0
	ipat = 0
	npat = pat_line_info[pat][0]
	pat = pat_line_info[pat][1]
	sp = (getxl(x[ip2]), getyl(y[ip2]))
	ep = (0,0)
	
	while ip2 < npnt:
		pat_seg = []
		pat_len = pat[ipat]*patlen;
		pat_len1 = pat_len
		pat_seg.append(sp);
		p2_len = 0;
		while ip2 < npnt:
			ip2 += 1
			#ep = (getxl(x[ip2+1]), getyl(y[ip2+1]))
			ep = (getxl(x[ip2]), getyl(y[ip2]))
			p2_len1 = distPP(sp, ep)
			p2_len += p2_len1
			labs = np.fabs(p2_len-pat_len)
			#--------------------------------------------------
			#    *-----------------------------* pat_len
			#    *==========*==========*=======@====* 
			#    p1         p2           p3
			#    << p2_len >>
			#    find @
			#--------------------------------------------------
			if p2_len < pat_len:
				print("case 1")
				pat_seg.append(ep)
				sp = ep
				case1 = True
				pat_len1 -= p2_len1
				#ip2+=1
				#if ip2 == npnt1: break
			
			#--------------------------------------------------
			#   p1(sp)                         p2(ep)
			#    *===========================@=*=@      p2_len
			#    *---------------------------*  pat_len
			#    *-------------------------------*
			#                                <-> epsilon
			#
			#   p2 will be the end of a pat-line segment.
			#
			#   p1                             p2(ep)
			#    *===sp======================@=*=@
			#        *-----------------------*
			#        *---------------------------*        
			#--------------------------------------------------
			elif labs < PAT_EPS:
				print("case 2")
				pat_seg.append(ep)
				#ip2+=1
				sp = ep
				break
			#--------------------------------------------------
			#   p1                            p2
			#    *============@================* p2_len
			#    *------------*  pat_len
			#    find @
			#--------------------------------------------------
			elif p2_len > pat_len:
				#llp = p2_len - pat_len
				dist_pp = distPP(sp,ep)
				while p2_len > pat_len:
					v2[0] = ep[0]-sp[0]
					v2[1] = ep[1]-sp[1]
					v2_norm = np.sqrt(v2[0]**2+v2[1]**2)
					v2 /= v2_norm
					if case1:
						v2 *= pat_len1
						case1 = False
					else:
						v2 *= pat_len
					ep1 = (sp[0]+v2[0], sp[1]+v2[1])
					pat_seg.append(ep1)
					print("case 3: ep1=> ", ep1)
					sp = ep1

				#v2[0] = ep[0]-sp[0]
				#v2[1] = ep[1]-sp[1]
				#v2_norm = np.sqrt(v2[0]**2+v2[1]**2)
				#v2 /= v2_norm/pat_len
				#if case1:
				#	v2 *= v2_norm/pat_len1
				#	case1 = False
				#else:
				#	v2 *= v2_norm/pat_len
				#ep1 = (sp[0]+v2[0], sp[1]+v2[1])
				
				#dx = ep[0]-sp[0]
				#dy = ep[1]-sp[1]
				#theta = math.atan2(dy,dx)
				#theta = math.atan(v2[1]/v2[0])
				#if case1:
				#	ep1 = (pat_len1*math.cos(theta), pat_len1*math.sin(theta))
				#else:	
				#	ep1 = (pat_len*math.cos(theta), pat_len*math.sin(theta))
				
				#pat_seg.append(ep1)
				#sp = ep1
				#ip2 +=1
				break

		if ipat%2 is 0:
			xx = [pat_seg[i][0] for i in range(len(pat_seg))]
			yy = [pat_seg[i][1] for i in range(len(pat_seg))]
			dev.lpolyline(xx,yy,color.BLUE, dev.frm.hgt()*0.003)
		pat_seg = []
		ipat += 1
		if ipat==npat: ipat=0
		if ip2 == npnt1: break


def test(dev):		
	from vgl import symbol
	#x = np.arange(-3,3.2,0.2)
	#y2 = x**2
	x=np.array([0,1,2,3],dtype=np.float32)
	y2=np.array([0,1,4,3],dtype=np.float32)
	dev.polyline(x,y2,color.RED,0.003*dev.frm.hgt())
	get_pattern_line(dev, x, y2, dev.wtol_x, dev.wtol_y, 0.05*dev.frm.hgt(), VGL_DASHED)
	#get_pattern_line(dev, x, y2, dev.get_x, dev.get_y, 0.005*dev.frm.hgt(), VGL_DASHED)
	
	sym = symbol.Circle(0.005, dev.frm.hgt(), 0.003)
	dev.begin_symbol(sym)
	for i in range(0,x.size): dev.symbol(x[i],y2[i],sym)
	dev.end_symbol()
	
def main():
	from vgl import color, BBox, Frame, FrameManager, Data
	from vgl import DeviceWindowsMetafile, DeviceCairo
	#from vgl import drawfrm, symbol, drawtick, drawaxis, drawlabel
	
	data = Data(-3,3,-1,10)
	fmm = FrameManager()
	frm_x2 = fmm.create(0.0,0.0,4,4, data)
	
	gbbox = fmm.get_gbbox()

	dev_img = DeviceCairo("patlin.png", gbbox, 100)
	dev_img.fill_white()
	dev_img.set_plot(frm_x2)
	test(dev_img)
	dev_img.close()
	
	dev_wmf = DeviceWindowsMetafile("patlin.wmf", gbbox)
	dev_wmf.set_device(frm_x2)
	test(dev_wmf)
	dev_wmf.close()
	
			
if __name__ == '__main__':
	main()
