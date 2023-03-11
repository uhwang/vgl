'''
    shape.py
'''
from . import vertex
from . import linepat
from . import linetype

class Shape(vertex.Vertex, linetype.LineLevelC):
    def __init__(   self, 
                    x, y, 
                    nvert, 
                    edge, 
                    lcol, 
                    lthk,
                    fcol=None, 
                    pat_len=0.04, 
                    lpat = linepat._PAT_SOLID):
        super().__init__(nvert)
        self.sx = x
        self.sy = y
        self.edge = edge 
        self.lcol = lcol
        self.lthk = lthk
        self.fcol = fcol
        self.pat_len = pat_len
        self.pat_t = lpat
    
    def set_fillcolor(self, col): self.fcol = col
    def set_linecolor(self, col): self.lcol = col
    def set_fill(self, mode): self.fill = mode
    def get_line_pattern(self): 
        return self.pat_t\
            if (self.pat_t == linepat._PAT_SOLID) or\
               (self.pat_t == linepat._PAT_NULL)\
            else linepat.LinePattern(self.pat_len, self.pat_t)