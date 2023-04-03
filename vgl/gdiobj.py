'''

    gdiobj.py

'''

class Pen():
    def __init__(self):
        self.lcol = None
        self.lthk = None
        
    def set_pen(self, lcol, lthk):
        self.lcol = lcol
        self.lthk =lthk
        
    def __str__(self):
        return "Color: %s\nThickness: %f"%(self.lcol, self.lthk)
        
class Brush():
    def __init__(self):
        self.fcol=None #(0,0,0)
        
    def set_brush(self, fcol):
        self.fcol = fcol
        
class StreamPen(Pen):
    def __init__(self):
        self.buf = []
        
class PDFPen(StreamPen):
    def __init__(self):
        super().__init__()
        self.obj_index = 0
        
    def set_pen(self, lcol, lthk, obj_index):
        super().set_pen(lcol,lthk)
        self.obj_index = obj_index
               