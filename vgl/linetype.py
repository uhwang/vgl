# linetype.py
from . import color
from . import linepat

class LineLevelA():
    #def __init__(self, lcol=color.BLACK, lthk=0.001):
    def __init__(self, lcol, lthk):
        self.set(lcol, lthk)
    
    def set(self, lcol, lthk):
        self.lcol = lcol
        self.lthk = lthk
        
    def __str__(self):
        return "LineLevelA\n%s\nThink: %f"%(str(self.lcol), self.lthk)
   
# Tick
class LineLevelB(LineLevelA):
    def __init__(self, lcol=color.BLACK, lthk=0.001, llen=0.004):
        #super().__init__(lcol, lthk)
        #self.llen = llen
        self.set(lcol, lthk, llen)
    
    def set(self, lcol, lthk, llen):
        super().set(lcol, lthk)
        self.llen = llen
   
    def __str__(self):
        return "LineLevelB\nColor: %s\nThink: %f\nLength: "\
        %(str(self.lcol), self.lthk, self.llen)
        
class LineLevelC(LineLevelA):
    def __init__(self, lcol=color.BLACK, lthk=0.001, lpat=linepat._PAT_SOLID, pat_len=0.04):
        #super().__init__(lcol, lthk)
        #self.lpat = lpat
        #self.patlen = patlen
        self.set(lcol, lthk, pat_len, lpat)
                
    def set(self, lcol, lthk, pat_len, lpat):
        super().set(lcol, lthk)
        self.pat_len = pat_len
        self.lpat = lpat
        
    def get_line_pattern(self): 
        return self.lpat\
            if (self.lpat == linepat._PAT_SOLID) or\
               (self.lpat == linepat._PAT_NULL)\
            else linepat.LinePattern(self.pat_len, self.lpat)
            
    def __str__(self):
        return "LineLevelC\nColor: %s\nThink: %f"\
        %(str(self.lcol), self.lthk)		
        
def main():
    x=LineLevelC()
	
if __name__ == '__main__':
	main()