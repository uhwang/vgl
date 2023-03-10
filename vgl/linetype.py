# linetype.py
from . import color
#import color

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
    def __init__(self, lcol=color.BLACK, lthk=0.001, pat_len=0, pat_t=0):
        #super().__init__(lcol, lthk)
        #self.lpat = lpat
        #self.patlen = patlen
        self.set(lcol, lthk, pat_len, pat_t)
                
    def set(self, lcol, lthk, pat_len, pat_t):
        super().set(lcol, lthk)
        self.pat_len = pat_len
        self.pat_t = pat_t
        
    def __str__(self):
        return "LineLevelC\nColor: %s\nThink: %f"\
        %(str(self.lcol), self.lthk)		
        
def main():
    x=LineLevelC()
	
if __name__ == '__main__':
	main()