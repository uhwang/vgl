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
import numpy

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
	return numpy.sqrt((p2[0]-p1[0])**2+(p2[1]-p2[0])**2)

def get_pattern_line(x,y, getxl, getyl, patlen, pat):
	v2 = numpy.empty(2, dtype='float32')
	ep1 = (0,0) #numpy.empty(2, dtype='float32')
	case1=False
	pat_line = []
	pat_seg = []
	np = len(x)
	np1 = np-1
	ip2 = 0
	ipat = 0
	npat = pat_line_info[pat][0]
	pat = pat_line_info[pat][1]
	#sp = pnts[ip2]
	sp = (getxl(x[ip2]), getyl(y[ip2]))
	ep = (0,0)
	
	while True:
		#print(ip2, np1)
		pat_len = pat[ipat]*patlen;
		pat_len1 = pat_len
		pat_seg.append(sp);
		p2_len = 0;
		while True:
			#ep = pnts[ip2+1]
			ep = (getxl(x[ip2+1]), getyl(y[ip2+1]))
			p2_len1 = distPP(sp, ep)
			p2_len += p2_len1
			#print(p2_len1, pat_len)
			#labs = np.fabs(p2_len-pat_len)
			labs = numpy.fabs(p2_len-pat_len)
			#--------------------------------------------------
			#    *-----------------------------* pat_len
			#    *==========*==========*=======@====* 
			#    p1         p2           p3
			#    << p2_len >>
			#    find @
			#--------------------------------------------------
			if p2_len < pat_len:
				#print("case 1: ", sp, ep)
				pat_seg.append(ep)
				sp = ep
				case1 = True
				pat_len1 -= p2_len1
				ip2+=1
				if ip2 == np1: break
			
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
				#print("case 2")
				pat_seg.append(ep)
				ip2+=1
				sp = ep
				break
			#--------------------------------------------------
			#   p1                            p2
			#    *============@================* p2_len
			#    *------------*  pat_len
			#    find @
			#--------------------------------------------------
			elif p2_len > pat_len:
				#print("case 3")
				#v2.setVector(sp, ep);
				v2[0] = ep[0]-sp[0]
				v2[1] = ep[1]-sp[1]
				v2_norm = numpy.sqrt(v2[0]**2+v2[1]**2)
				v2 /= v2_norm
				if case1:
					#v2 *= pat_len1/v2.norm();
					v2 *= pat_len1#/v2_norm
					case1 = False
				else:
					#v2 *= pat_len/v2.norm();
					v2 *= pat_len#/v2_norm
				
				#ep1[0] = sp[0]+v2[0]
				#ep1[1] = sp[1]+v2[1]
				ep1 = (sp[0]+v2[0], sp[1]+v2[1])
				pat_seg.append(ep1)
				sp = ep1
				ip2 +=1
				break
		#nseg = len(pat_seg)
		#(*svc_DevRaw_DrawPolylineList)(&pat_seg);
		#pat_seg.clear();
		pat_line.append(pat_seg)
		pat_seg = []
		ipat += 1
		if ipat==npat: ipat=0
		if ip2 == np1: break
		
	return pat_line
		

def test(dev):		
	from vgl import color
	x = np.arange(-3,3.2,0.2)
	y2 = x**2
	#pnts = [(x[i], y2[i]) for i in range(len(x))]
	pat_line = get_pattern_line(x, y2, dev.wtol_x, dev.wtol_y, 0.05*dev.frm.hgt(), VGL_DASHED)
	
	for ps in pat_line:
		#print(ps)
		x = [ps[i][0] for i in range(len(ps))]
		y = [ps[i][1] for i in range(len(ps))]
		#print(x)
		#print(y)
		dev.lpolyline(x,y,color.BLUE, dev.frm.hgt()*0.01)
		
def main():
	from vgl import color, BBox, Frame, FrameManager, Data
	from vgl import DeviceWindowsMetafile, DeviceCairo
	#from vgl import drawfrm, symbol, drawtick, drawaxis, drawlabel
	
	data = Data(-3,3,-1,10)
	fmm = FrameManager()
	frm_x2 = fmm.create(0.0,0.0,2,4, data)
	
	gbbox = fmm.get_gbbox()
	
	dev_wmf = DeviceWindowsMetafile("patlin.wmf", gbbox)
	dev_wmf.set_device(frm_x2)
	test(dev_wmf)
	dev_wmf.close()
	
	dev_img = DeviceCairo("patlin.png", gbbox, 100)
	dev_img.fill_white()
	dev_img.set_plot(frm_x2)
	test(dev_img)
	dev_img.close()
			
if __name__ == '__main__':
	main()
