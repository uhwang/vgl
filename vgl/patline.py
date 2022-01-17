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
	( 2, ( 1.0      , 1.0, )),                      # DASHED
	( 4, ( 1.0      , 0.399132, 0.199566,           # DASHDOT
                      0.399132, 0.0, )),            
	( 2, ( 0.0021692, 0.247289, 0.0 )) ,            # DOTTED
	( 2, ( 1.49892  , 0.498915, 0.0 )) ,            # LONGDASH
	( 6, ( 1.0      , 0.249458, 0.167028, 0.249458, # DASHDOTDOT
                      0.167028, 0.249458 ))
)


def distPP(p1,p2): 
	return np.sqrt((p2[0]-p1[0])**2+(p2[1]-p1[1])**2)

def set_vector(sp, ep, vp):
    vp[0], vp[1] = ep[0]-sp[0], ep[1]-sp[1]
    
def get_norm(vp):
    return np.sqrt(vp[0]**2+vp[1]**2)
    
def get_pattern_line(x,y, getxl, getyl, patlen, pat):
    sp = np.empty(2, dtype='float32')
    ep = np.empty(2, dtype='float32')
    v2 = np.empty(2, dtype='float32')
    ep1 = np.empty(2, dtype='float32')
    lp1  = np.empty(2, dtype='float32')
    lp2  = np.empty(2, dtype='float32')
    
    case1=False
    npnt = len(x)
    npnt1 = npnt-1
    ip2 = 0
    ipat = 0
    npat = pat_line_info[pat][0]
    pat = pat_line_info[pat][1]
    sp[0], sp[1] = x[ip2], y[ip2]
    ep[0], ep[1] = 0.0, 0.0
    pat_seg = []	
    
    #while ip2 < npnt:
    while True:
        sub_seg = []
        pat_len = pat[ipat]*patlen;
        pat_len1 = pat_len
        sub_seg.append((sp[0],sp[1]));
        p2_len = 0;
   
        #while ip2 < npnt:
        while True:
            ep[0], ep[1] = x[ip2+1], y[ip2+1]
            
            lp1[0], lp1[1] = getxl(sp[0]), getyl(sp[1])
            lp2[0], lp2[1] = getxl(ep[0]), getyl(ep[1])
            
            p2_len1 = distPP(lp1, lp2)
            
            #p2_len1 = distPP(sp, ep)
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
                sub_seg.append((ep[0], ep[1]))
                sp[0], sp[1] = ep[0], ep[1]
                case1 = True
                pat_len1 -= p2_len1
                ip2+=1
                if ip2 == npnt1: break
            
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
                sub_seg.append((ep[0],ep[1]))
                ip2 += 1
                sp[0], sp[1] = ep[0], ep[1]
                break
            #--------------------------------------------------
            #   p1                            p2
            #    *============@================* p2_len
            #    *------------*  pat_len
            #    find @
            #--------------------------------------------------
            elif p2_len > pat_len:
                set_vector(sp, ep, v2)
                if case1:
                    v2 *= p2_len1/get_norm(v2)
                    case1 = False
                else:
                    v2 *= p2_len/get_norm(v2)
                ep1[0], ep1[1] = sp[0]+v2[0], sp[1]+v2[1]
                sub_seg.append((ep1[0], ep1[1]))
                sp[0], sp[1] = ep1[0], ep1[1]
                break
                
        #pat_seg.append(sub_seg)
        if ipat%2 is 0:
            pat_seg.append(sub_seg)
        ipat += 1
        if ipat==npat: ipat=0
        if ip2 == npnt1: break
    
    return pat_seg
   
def test(dev):		
    #from vgl import symbol
    t1, t2 = 0, 2*np.pi
    nt = 10
    dt = (t2-t1)/nt
    tt = np.arange(t1, t2+dt, dt)
    x=np.array([np.sin(t) for t in tt], dtype=np.float32)
    y=np.array([np.cos(t) for t in tt],dtype=np.float32)
    #dev.polyline(x,y, color.BLUE,0.003*dev.frm.hgt())
    pat_line = get_pattern_line(x, y, dev.wtol_x, dev.wtol_y,0.05*dev.frm.hgt(), VGL_DASHED)

    for pl in pat_line:
        xx = [p[0] for p in pl]
        yy = [p[1] for p in pl]
        dev.polyline(xx,yy,color.RED,0.01*dev.frm.hgt())
	
def main():
	import vgl
	
	data = vgl.Data(-1.5,1.5,-1.5,1.5)
	fmm = vgl.FrameManager()
	frm_x2 = fmm.create(0.0,0.0,4,4, data)
	
	gbbox = fmm.get_gbbox()

	dev_img = vgl.DeviceCairo("patlin.png", gbbox, 100)
	dev_img.set_plot(frm_x2)
	test(dev_img)
	dev_img.close()
	
	#dev_wmf = DeviceWindowsMetafile("patlin.wmf", gbbox)
	#dev_wmf.set_device(frm_x2)
	#test(dev_wmf)
	#dev_wmf.close()
	
			
if __name__ == '__main__':
	main()
