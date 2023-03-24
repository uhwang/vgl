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
        