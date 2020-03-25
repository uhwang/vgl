# linetype.py
import vgl.color as color

class LineLevelA():
	#def __init__(self, lcol=color.BLACK, lthk=0.001):
	def __init__(self, lcol, lthk):
		self.setA(lcol, lthk)
	
	def setA(self, lcol, lthk):
		self.lcol = lcol
		self.lthk = lthk

# Tick
class LineLevelB(LineLevelA):
	def __init__(self, lcol=color.BLACK, lthk=0.001, llen=0.004):
		super().__init__(lcol, lthk)
		self.llen = llen
	
	def setB(self, lcol, lthk, llen):
		super().setA(lcol, lthk)
		self.llen = llen
		
class LineLevelC(LineLevelA):
	def __init__(self, lcol=color.BLACK, lthk=0.001, lpat=0, patlen=0):
		super().__init__(lcol, lthk)
		self.lpat = lpat
		self.patlen = patlen
				
	def setC(self, lcol, lthk, lpat, patlen):
		super().setA(lcol, lthk)
		self.lpat = lpat
		self.patlen = patlen
		
		
def main():
	x=LineLevelC()
	
if __name__ == '__main__':
	main()