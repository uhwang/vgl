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
from . import color
#import color

class LinePattern():
    def __init__(self, pat_len, pat_t):
        self.pat_len = pat_len
        self.pat_t = pat_t

_default_pattern_length = 0.04
_pattern_length = _default_pattern_length
        
_pattern_name = ["SOLID", "DASHED", "DASHDOT", "DOTTED", "LONGDASH", "DASHDOTDOT"]

_PAT_SOLID     = _pattern_name[0]
_PAT_DASHED    = _pattern_name[1]
_PAT_DASHDOT   = _pattern_name[2]
_PAT_DOTTED    = _pattern_name[3]
_PAT_LONGDASH  = _pattern_name[4]
_PAT_DASHDOTDOT= _pattern_name[5]
_PAT_EPS       = 1.e-6

_PAT_MARK_0 ='0'
_PAT_MARK_1 ='1'

def set_stock_pattern_length(pat_len): _pattern_length = pat_len
def reset_stock_pattern_length(pat_len): _pattern_length = pat_len

def get_dash(pat_len): return LinePattern(pat_len, _PAT_DASHED)  
def get_dashdot(pat_len): return LinePattern(pat_len, _PAT_DASHDOT)  
def get_dotted(pat_len): return LinePattern(pat_len, _PAT_DOTTED)  
def get_longdash(pat_len): return LinePattern(pat_len, _PAT_LONGDASH)  
def get_dashdotdot(pat_len): return LinePattern(pat_len, _PAT_DASHDOTDOT)  

def get_stock_dash(): return LinePattern(_pattern_length, _PAT_DASHED)  
def get_stock_dashdot(): return LinePattern(_pattern_length, _PAT_DASHDOT)  
def get_stock_dotted(): return LinePattern(_pattern_length, _PAT_DOTTED)  
def get_stock_longdash(): return LinePattern(_pattern_length, _PAT_LONGDASH)  
def get_stock_dashdotdot(): return LinePattern(_pattern_length, _PAT_DASHDOTDOT)  

def _get_pattern_name_dashed(): return _pattern_name[1]
def _get_pattern_name_dashdot(): return _pattern_name[2]
def _get_pattern_name_dotted(): return _pattern_name[3]
def _get_pattern_name_longdash(): return _pattern_name[4]
def _get_pattern_name_dashdotdot(): return _pattern_name[5]

_pat_line_info = {
    # DASHED
	_get_pattern_name_dashed(): ["10", ( 1.0, 1.0, )], 
    # DASHDOT
	_get_pattern_name_dashdot(): ["1010", ( 1.0, 0.399132, 0.199566, 0.399132, 0.0, )],  
    # DOTTED
	_get_pattern_name_dotted(): ["10", ( 0.247289, 0.0021692, 0.0 )],
    # LONGDASH
	_get_pattern_name_longdash(): ["10", ( 1.49892, 0.498915, 0.0 )] ,
    # DASHDOTDOT
	_get_pattern_name_dashdotdot(): ["101010", ( 1.0, 0.249458, 0.167028, 0.249458, 0.167028, 0.249458 )]
}

def _get_pattern_info(pat):
    return _pat_line_info[pat] if pat in _pattern_name else None

def distPP(p1,p2): 
	return np.sqrt((p2[0]-p1[0])**2+(p2[1]-p1[1])**2)

def set_vector(sp, ep):
    return ep[0]-sp[0], ep[1]-sp[1]
    
def get_norm(vp):
    return np.sqrt(vp[0]**2+vp[1]**2)

def get_pattern_line(dev, x, y, patlen, pat_t, viewport=False):
    '''
        x, y : real world to plot
        getxl
        getyl: return viewport coord in response data(x,y)
        patlen: pattern length in percent of the hgt of plot domain
        pat: pattern list in viewport coord
        viewport: x, y is not world data but logical unit (inch)
    '''
    if viewport:
        f_x = lambda x: x
        f_y = lambda y: y
    else:
        f_x = dev._x_viewport
        f_y = dev._y_viewport
    
    if pat_t == _PAT_SOLID: return
    
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
    pat_info = _get_pattern_info(pat_t)
    if pat_info == None: 
        print("Error: wrong pattern")
        return
    
    npat = len(pat_info[0])
    pat_mark = pat_info[0]
    pat = pat_info[1]
    sp[0], sp[1] = f_x(x[ip2]), f_y(y[ip2])
    pat_seg = []	
    
    #while ip2 < npnt:
    while True:
        sub_seg = []
        pat_len1 = pat[ipat]*patlen*dev.frm.hgt();
        pat_len2 = pat_len1
        sub_seg.append((sp[0],sp[1]));
        p2_len1 = 0;
   
        #while ip2 < npnt:
        while True:
            ep[0] = f_x(x[ip2+1])
            ep[1] = f_y(y[ip2+1])
            
            #lp1[0], lp1[1] = getxl(sp[0]), getyl(sp[1])
            #lp2[0], lp2[1] = getxl(ep[0]), getyl(ep[1])
            
            p2_len2 = distPP(sp, ep)
            p2_len1 += p2_len2
            labs = np.fabs(p2_len1-pat_len1)
            #--------------------------------------------------
            #    *-----------------------------* pat_len1
            #    *==========*==========*=======@====* 
            #    p1         p2           p3
            #    << p2_len1 >>
            #    find @
            #--------------------------------------------------
            if p2_len1 < pat_len1:
                sub_seg.append((ep[0], ep[1]))
                sp[0], sp[1] = ep[0], ep[1]
                case1 = True
                pat_len2 -= p2_len2
                ip2+=1
                if ip2 == npnt1: break
            
            #--------------------------------------------------
            #   p1(sp)                         p2(ep)
            #    *===========================@=*=@      p2_len1
            #    *---------------------------*  pat_len1
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
            elif labs < _PAT_EPS:
                sub_seg.append((ep[0],ep[1]))
                ip2 += 1
                sp[0], sp[1] = ep[0], ep[1]
                break
            #--------------------------------------------------
            #   p1                            p2
            #    *============@================* p2_len1
            #    *------------*  pat_len1
            #    find @
            #--------------------------------------------------
            elif p2_len1 > pat_len1:
                v2[0], v2[1] = set_vector(sp, ep)
                if case1:
                    v2 *= pat_len2/get_norm(v2)
                    case1 = False
                else:
                    v2 *= pat_len1/get_norm(v2)
                ep1[0], ep1[1] = sp[0]+v2[0], sp[1]+v2[1]
                sub_seg.append((ep1[0], ep1[1]))
                sp[0], sp[1] = ep1[0], ep1[1]
                break
                
        if pat_mark[ipat] == _PAT_MARK_1:
            pat_seg.append(sub_seg)
        ipat += 1
        if ipat==npat: ipat=0
        if ip2 == npnt1: break
    
    return pat_seg
   
