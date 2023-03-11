# Vector Graphic Library (VGL) for Python
#
# geom.py
#
# 2020-2-12 Ver 0.1
#
# Author: Uisang Hwang
# Email : uhwangtx@gmail.com
#

import numpy as np
from . import color, rotation, vertex
from . import linetype
from . import shape
from . import linepat
from . import shape

def distP(x1,y1,x2,y2): return np.sqrt((x2-x1)**2+(y2-y1)**2)
def distV(vlist): return np.sqrt( (vlist[2]-vlist[0])**2+(vlist[3]-vlist[1])**2 )

SQUARE_MODE_NEW = -1
SQUARE_MODE_CENTER = 0
SQUARE_MODE_LEFTTOP = 1
SQUARE_MODE_RIGHTTOP = 2
SQUARE_MODE_LEFTBOTTOM = 3 
SQUARE_MODE_RIGHTBOTTOM = 4

class Square(shape.Shape):
    def __init__(self,x,y,edge,lcol=color.BLACK, lthk=0.001,fcol=None, 
        mode=SQUARE_MODE_CENTER):
        super().__init__(x,y,4,edge,lcol,lthk,fcol,fill)
        self.mode = mode
    
        if mode != SQUARE_MODE_NEW:
            if   mode == SQUARE_MODE_CENTER:
                self.compute_vertex_centermode()
            elif mode == SQUARE_MODE_LEFTTOP:
                self.compute_vertex_topleftmode()
            elif mode == SQUARE_MODE_RIGHTTOP:
                self.compute_vertex_toprightmode()
            elif mode == SQUARE_MODE_LEFTBOTTOM :
                self.compute_vertex_bottomleftmode()
            elif mode == SQUARE_MODE_RIGHTBOTTOM:
                self.compute_vertex_bottomrightmode()
            else: print('wrong mode')
            
    '''
        (0,1)         (6,7)
        *-------------*
        |             |
        |      x      |
        |             |
        *-------------*
        (2,3)         (4,5)
    '''
    def compute_vertex_centermode(self):
        half = self.edge*0.5
        self.center = (self.sx, self.sy)
        self.vertex.put([0,2], self.sx-half)
        self.vertex.put([4,6], self.sx+half)
        self.vertex.put([1,7], self.sy+half)
        self.vertex.put([3,5], self.sy-half)
            
    def compute_vertex_topleftmode(self):
        half = self.edge/2.
        self.center = (self.sx+half, self.y-half)
        self.vertex.put([0,2], self.sx)
        self.vertex.put([4,6], self.x+self.edge)
        self.vertex.put([1,7], self.sy)
        self.vertex.put([3,5], self.sy-self.edge)
    
    def compute_vertex_toprightmode(self):
        half = self.edge/2.
        self.center = (self.sx-half, self.sy-half)
        self.vertex.put([0,2], self.sx-self.edge)
        self.vertex.put([4,6], self.sx)
        self.vertex.put([1,7], self.sy)
        self.vertex.put([3,5], self.sy-self.edge)
    
    def compute_vertex_bottomleftmode(self):
        half = self.edge/2.
        self.center = (self.sx+half, self.sy+half)
        self.vertex.put([0,2], self.sx)
        self.vertex.put([4,6], self.sx+self.edge)
        self.vertex.put([1,7], self.sy)
        self.vertex.put([3,5], self.sy+self.edge)	
        
    def compute_vertex_bottomrightmode(self):
        half = self.edge/2.
        self.center = (self.sx-half, self.sy-half)
        self.vertex.put([0,2], self.sx)
        self.vertex.put([4,6], self.sx-self.edge)
        self.vertex.put([1,7], self.sy)
        self.vertex.put([3,5], self.sy+self.edge)	

class EquiTriangle(shape.Shape):
    def __init__(self,xc,yc,edge,lcol=color.BLACK,lthk=0.001,fcol=None):
        super().__init__(xc,yc,3,edge,lcol,lthk,fcol,fill)
        len = edge/np.sqrt(3)
        leg1 = edge*0.5
        leg2 = np.sqrt(len**2-leg1**2)
        self.vertex[0] = xc
        self.vertex[1] = yc+len
        self.vertex[2] = xc-leg1
        self.vertex[3] = yc-leg2
        self.vertex[4] = xc+leg1
        self.vertex[5] = yc-leg2

class Polygon(shape.Shape):
    def __init__(self,
                xc, yc, 
                nvert, 
                edge, 
                lcol=color.BLACK, 
                lthk=0.001,
                fcol=None, 
                pat_len=0.04, 
                lpat = linepat._PAT_SOLID):
        super().__init__( xc,yc, 
                          nvert, 
                          edge, 
                          lcol, 
                          lthk, 
                          fcol, 
                          pat_len, 
                          lpat)
        step = 360.0/nvert
        for i in range(nvert):
            rad = rotation.deg_to_rad(i*step)
            self.vertex[i*2]=xc+edge*np.cos(rad)
            self.vertex[i*2+1]=yc+edge*np.sin(rad)
            
    def __str__(self):
        return "x: %f\ny: %f\nnvert: %d\nedge: %f\n"\
               "lcol: %s\nlthk: %f\nfcol: %s\npat_len: %f\nlpat: %s\n"%\
        (self.xc, self.yc, self.nvert, self.edge, 
        self.lcol, self.lthk, self.fcol, self.pat_len, self.pat_t)
