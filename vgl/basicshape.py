'''
    basicshape.py
    
    7/11/2023 Added Arrowed Lines
    
'''
import numpy as np
from . import shape
from . import linepat
from . import linetype
from . import util
from . import color

_ARROWTYPE_OPEN         = 0x0001
_ARROWTYPE_CLOSED       = 0x0002
_ARROWTYPE_CLOSEDFILLED = 0x0003
_ARROWTYPE_CLOSEDBLANK  = 0x0004
_ARROWTYPE_VIKING       = 0x0005
_ARROWTYPE_DOT          = 0x0006

_ARROWPOS_START         = 0x0007
_ARROWPOS_END           = 0x0008

_arrow_angle         = 15 # degree
_arrow_length_0      = 0.01 # 
_arrow_length_1      = 0.05 # 
#_arrowhead_start = "START"
#_arrowhead_end = "END"

class ArrowHead():
    def __init__(self, 
                 frm, 
                 sx, 
                 sy, 
                 ex, 
                 ey,
                 show   = True,
                 col    = color.BLACK,
                 pos_t  = _ARROWPOS_START, 
                 type_t = _ARROWTYPE_OPEN, 
                 angle  = _arrow_angle, 
                 length = _arrow_length_1):
                 
        self.show   = show
        self.pos_t  = pos_t
        self.type_t = type_t
        self.angle  = angle # degree
        self.length = length # length of arrow head
        self.col    = col
        
        self.calculate_pos(frm, sx, sy, ex, ey)
        
    def set(self, col, type_t, angle, length):
        self.type_t = type_t
        self.angle  = angle # degree
        self.length = length # length of arrow head
        self.col    = col
        
        
    def calculate_pos(self, frm, sx, sy, ex, ey):
    
        theta = np.arctan2(ey-sy, ex-sx)
        
        # find arrow head wing pos in local coord
        wing = self.length*frm.hgt()
        wing_x = wing*np.cos(util.deg_to_rad(self.angle))
        wing_y = wing*np.sin(util.deg_to_rad(self.angle))
        
        if self.pos_t == _ARROWPOS_START:
            self.wing_up   = util.rad_rotation(wing_x,  wing_y, -theta)
            self.wing_down = util.rad_rotation(wing_x, -wing_y, -theta)
        else:
            self.wing_up   = util.rad_rotation(-wing_x,  wing_y, -theta)
            self.wing_down = util.rad_rotation(-wing_x, -wing_y, -theta)

def draw_arrow_head(dev, sx, sy, arrow, lcol, lthk, viewport):
    
    sx = dev._x_viewport(sx) if viewport==False else sx
    sy = dev._y_viewport(sy) if viewport==False else sy
    xs = [sx+arrow.wing_up[0], sx, sx+arrow.wing_down[0], sx+arrow.wing_up[0]]
    
    if viewport == False:
        ys = [sy+arrow.wing_up[1], sy, sy+arrow.wing_down[1], sy+arrow.wing_up[1]]
    else:
        ys = [sy-arrow.wing_up[1], sy, sy-arrow.wing_down[1], sy-arrow.wing_up[1]]
    
    # open
    if arrow.type_t == _ARROWTYPE_OPEN:
        dev.lpolyline(xs[:3], ys[:3], lcol, lthk)
        
    elif arrow.type_t == _ARROWTYPE_CLOSED:
        dev.lpolygon(xs, ys, lcol=lcol, lthk=lthk, fcol=None)
        
    elif arrow.type_t == _ARROWTYPE_CLOSEDFILLED:
        dev.lpolygon(xs, ys, lcol=lcol, lthk=lthk, fcol=lcol)
        
    elif arrow.type_t == _ARROWTYPE_CLOSEDBLANK:
        dev.lpolygon(xs, ys, lcol=lcol, lthk=lthk, fcol=color.WHITE)

# lcol, lthk, len_pat, pat_t
class GenericLine(linetype.LineLevelC):
    def __init__(self, 
                 frm, 
                 sx, 
                 sy, 
                 ex, 
                 ey, 
                 lcol      = color.BLACK,
                 lthk      = 0.001,
                 lpat      = linepat._PAT_SOLID,
                 pat_len   = 0.04,
                 show      = False,
                 col       = color.BLACK,
                 type_t    = _ARROWTYPE_OPEN, 
                 angle     = _arrow_angle, 
                 length    = _arrow_length_1, 
                 viewport  = False):
                 
        super().__init__(lcol=lcol, lthk=lthk, lpat=lpat, pat_len=pat_len)
        
        self.sx = sx
        self.sy = sy
        self.ex = ex
        self.ey = ey
        self.viewport = viewport
        self.begin_arrow = ArrowHead(frm, sx,sy,ex,ey, 
                                     show, col, _ARROWPOS_START, type_t, angle, length)
        self.end_arrow   = ArrowHead(frm, sx,sy,ex,ey, 
                                     show, col, _ARROWPOS_END, type_t, angle, length)
    def __str__(self):
        return "Lcol : %s\nLthk : %f\nLpat : %s\nPat_len : %f\nShow : %s\n"\
               "Col  : %s\nType : %s\nAngle: %f\nLength: %f\nViewport : %s"%(
               str(self.lcol), 
               self.lthk, 
               self.lpat, 
               self.pat_len, 
               self.end_arrow.show,
               str(self.end_arrow.col) , 
               self.end_arrow.type_t, 
               self.end_arrow.angle, 
               self.end_arrow.length, 
               self.viewport)
    
    def draw(self, dev):
        if self.viewport == False:
            dev.line(self.sx, self.sy, self.ex, self.ey, 
                     self.lcol, self.lthk*dev.frm.hgt(), lpat=self.get_line_pattern())
        else:
            dev.lline(self.sx, self.sy, self.ex, self.ey, 
                      self.lcol, self.lthk*dev.frm.hgt(), lpat=self.get_line_pattern())

        if self.begin_arrow.show:
            acol = self.lcol if self.begin_arrow.col == self.lcol\
                             else self.begin_arrow.col
            draw_arrow_head(dev, self.sx, self.sy, self.begin_arrow, 
            acol, self.lthk*dev.frm.hgt(), self.viewport)
            
        if self.end_arrow.show:
            acol = self.lcol if   self.end_arrow.col == self.lcol\
                             else self.end_arrow.col
            draw_arrow_head(dev, self.ex, self.ey, self.end_arrow, 
            acol, self.lthk*dev.frm.hgt(), self.viewport)

class ArrowLine(GenericLine):
    def __init__(self, 
                 frm, 
                 sx, 
                 sy, 
                 ex, 
                 ey, 
                 lcol     = color.BLACK,
                 lthk     = 0.001,
                 lpat     = linepat._PAT_SOLID,
                 pat_len  = 0.04,                 
                 show     = True,
                 col      = color.BLACK,
                 type_t   = _ARROWTYPE_OPEN, 
                 angle    = _arrow_angle, 
                 length   = _arrow_length_1, 
                 viewport = False):
                 
        super().__init__(frm, 
                         sx, 
                         sy, 
                         ex, 
                         ey, 
                         lcol    = lcol, 
                         lthk    = lthk, 
                         lpat    = lpat, 
                         pat_len = pat_len,
                         show    = show, 
                         col     = col, 
                         type_t  = type_t, 
                         angle   = angle, 
                         length  = length, 
                         viewport= viewport)
        
class BeginArrowLine(GenericLine):
    def __init__(self, 
                 frm, 
                 sx, 
                 sy, 
                 ex, 
                 ey, 
                 lcol     = color.BLACK,
                 lthk     = 0.001,
                 lpat     = linepat._PAT_SOLID,
                 pat_len  = 0.04,                 
                 show     = True,
                 col      = color.BLACK,
                 type_t   = _ARROWTYPE_OPEN, 
                 angle    = _arrow_angle, 
                 length   = _arrow_length_1,
                 viewport = False):
                 
        super().__init__(frm, 
                         sx, 
                         sy, 
                         ex, 
                         ey, 
                         lcol    = lcol, 
                         lthk    = lthk, 
                         lpat    = lpat, 
                         pat_len = pat_len,
                         show    = show, 
                         col     = col, 
                         type_t  = type_t, 
                         angle   = angle, 
                         length  = length, 
                         viewport= viewport)
        self.end_arrow.show = False
        
class EndArrowLine(GenericLine):
    def __init__(self, 
                 frm, 
                 sx, 
                 sy, 
                 ex, 
                 ey, 
                 lcol     = color.BLACK,
                 lthk     = 0.001,
                 lpat     = linepat._PAT_SOLID,
                 pat_len  = 0.04,                 
                 show     = True,
                 col      = color.BLACK,
                 type_t   = _ARROWTYPE_OPEN, 
                 angle    = _arrow_angle, 
                 length   = _arrow_length_1,
                 viewport = False):
                 
        super().__init__(frm, sx, sy, ex, ey, 
                         lcol    = lcol, 
                         lthk    = lthk, 
                         lpat    = lpat, 
                         pat_len = pat_len,
                         show    = show, 
                         col     = col, 
                         type_t  = type_t, 
                         angle   = angle, 
                         length  = length, 
                         viewport= viewport)
        self.begin_arrow.show = False
        
class Box(shape.Shape):
    def __init__(self, 
                 sx, 
                 sy, 
                 wid      = 1,  # edge length
                 hgt      = 1,  # edge length
                 lcol     = color.BLACK,
                 lthk     = 0.001,
                 fcol     = None, 
                 lpat     = linepat._PAT_SOLID,
                 pat_len  = 0.04,  
                 viewport = False):
        
        super().__init__(sx, sy, 4, wid, 
                         lcol=lcol, lthk=lthk, fcol=fcol, lpat=lpat, pat_len=pat_len)
        self.wid= wid
        self.hgt= hgt
        self.viewport = viewport
        sx1 = sx+wid
        sy1 = sy+hgt
        self.vertex.put([0,2,4,6], [sx, sx1, sx1, sx ])
        self.vertex.put([1,3,5,7], [sy, sy , sy1, sy1])
            
    def draw(self, dev):
        if self.viewport==True:
            dev.lpolygon(self.get_xs(), self.get_ys(), 
                         self.lcol, self.lthk*dev.frm.hgt(), self.lpat, self.fcol)
        else:
            dev.polygon(self.get_xs(), self.get_ys(), 
                        self.lcol, self.lthk*dev.frm.hgt(), self.lpat, self.fcol)
        
        
class StarPolygon(shape.Shape):
    def __init__(self, 
                 sx, 
                 sy, 
                 clength  = 1, # length from center to a vertex
                 cline    = False, # show the line from center to a vertex
                 lcol     = color.BLACK,
                 lthk     = 0.001,
                 fcol     = None, 
                 lpat     = linepat._PAT_SOLID,
                 pat_len  = 0.04,  
                 viewport = False):  
                 
        super().__init__(sx, sy, 5, clength, 
                         lcol=lcol, lthk=lthk, fcol=fcol, lpat=lpat, pat_len=pat_len)
        self.cline = cline
        self.viewport = viewport
        
        # calculate vertex pos
        
        