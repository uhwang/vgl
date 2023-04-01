'''
    shapeline.py
    
'''
import numpy as np
from . import shape

_ARROWHEAD_OPEN         = 0x0001
_ARROWHEAD_CLOSED       = 0x0002
_ARROWHEAD_CLOSEDFILLED = 0x0003
_ARROWHEAD_CLOSEDBLANK  = 0x0004
_ARROWHEAD_VIKING       = 0x0005
_ARROWHEAD_DOT          = 0x0006

_arrowhead_depth_0 = 0.125 # 1/8'
_arrowhead_depth_1 = 0.25  # 1/4'
_arrowhead_start = "START"
_arrowhead_end = "END"

class ArrowHead():
    def __init__(self, pos, show=True, arrow_t=_ARROWHEAD_OPEN, angle=30, depth=_arrowhead_depth_1):
        self.pos = pos
        self.how = show
        self.arrow_t = arrow_t
        self.angle = angle # degree
        self.length = length # length of arrow head
        # calculate start upper wing
        x1, y1 = depth, depth*np.arctan(np.deg2rad(angle))
        x2, y2 = depth, -y1
        
        if pos == _arrowhead_start:
            self.wing_up = [x1, y1]
            self.wing_down = [x2, y2]
        else:
            self.wing_up = [-x1, y1]
            self.wing_down = [-x2, y2]
        
class Line(shape.Shape):
    def __init__(self, sx, sy, ex, ey):
        self.sx = sx
        self.sy = sy
        self.ex = ex
        self.ey = ey
        self.start_arrow = ArrowHead(_arrowhead_start)
        self.end_arrow = ArrowHead(_arrowhead_end)
        
    def draw_arrowhead(self, dev, ah):
        passs
        
    #def draw(self, dev):
        #if self.start_arrow.show:
        #_ARROWHEAD_OPEN
        
        
        