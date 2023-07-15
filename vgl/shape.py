'''
    shape.py
'''
from . import vertex
from . import linepat
from . import linetype

class Shape(vertex.Vertex, linetype.LineLevelC):
    def __init__(   self, 
                    sx, sy, 
                    nvert, 
                    edge, 
                    lcol, 
                    lthk,
                    fcol=None, 
                    lpat = linepat._PAT_SOLID,
                    pat_len=0.04
                ):
        vertex.Vertex.__init__(self, nvert=nvert)
        linetype.LineLevelC.__init__(self, lcol=lcol, lthk=lthk, lpat=lpat, pat_len=pat_len)
        self.sx = sx
        self.sy = sy
        self.edge = edge # length of a edge
        #self.lcol = lcol
        #self.lthk = lthk
        self.fcol = fcol
        #self.pat_len = pat_len
        #self.pat_t = lpat
    
    def set_fillcolor(self, col): self.fcol = col
    def set_linecolor(self, col): self.lcol = col
    def set_fill(self, mode): self.fill = mode
