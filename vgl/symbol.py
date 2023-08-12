# Vector Graphic Library (VGL) for Python
#
# symbol.py
#
# 2020-2-12 Ver 0.1
#
# Author: Uisang Hwang
# Email : uhwangtx@gmail.com
#
from numpy import pi, sin, cos

from . import color
from . import vertex
from .rotation import deg_to_rad

class Symbol(vertex.Vertex):
	def __init__(self, name, nvert, size, lcol, lthk, fill, fcol):
		super().__init__(nvert)
		self.name     = name
		self.lcol     = lcol
		self.fill     = fill
		self.fcol     = fcol
		self.size     = size
		self.lthk     = lthk
		#self.pat      = SVC_SOLID;
		#self.len      = 0.0

	#def __repr__(self):
	#	return "x: "+self.get_xs()+"\n"+"y: "+self.get_ys()
		
	def set_lcolor(self, col): self.lcol = col
	def set_fcolor(self, col): self.fcol = col
	def update_xy(self, x,y):
		return self.vertex[::2]+x, self.vertex[1::2]+y
	def set_color(self, lcol, fcol):
		self.lcol = lcol
		self.fcol = fcol
	def set_color_all(self, col):
		self.set_color(col,col)
	

class Circle(Symbol):
	def __init__(
                 self, 
                 size, 
                 hgt, 
                 lcol=color.BLACK,
                 lthk=0.001,
                 fill=True,
                 fcol=color.RED
                ):
		super().__init__('circle',12,size,lcol,lthk,True,fcol)
		self.hgt = hgt
		self.update(0,0)
			
	def update(self, x,y):
		nvert = self.get_nvertex()
		len= self.hgt * self.size
		step = 360.0/nvert
		for i in range(nvert):
			rad = deg_to_rad(i*step)
			self.vertex[i*2]=x+len*cos(rad)
			self.vertex[i*2+1]=y+len*sin(rad)
			
class Gradient(Symbol):
	def __init__(
                 self, 
                 size, 
                 hgt, 
                 lcol=color.BLACK,
                 lthk=0.001,
                 fill=True,
                 fcol=color.RED
                ):
		super().__init__('gradient',3,size,lcol,lthk,True,fcol)
		self.hgt = hgt
		self.update(0,0)
			
	def update(self, x,y):
		len= self.hgt * self.size
		hgt = len * 0.866025
		hs=len*0.5
		hh=hgt*0.51
		
		self.vertex[0]=x-hs
		self.vertex[1]=y-hh
		self.vertex[2]=x
		self.vertex[3]=y+hh
		self.vertex[4]=x+hs
		self.vertex[5]=y-hh
		
		
class RightTriangle(Symbol):
	def __init__(
                 self, 
                 size, 
                 hgt, 
                 lcol=color.BLACK,
                 lthk=0.001,
                 fill=True,
                 fcol=color.RED
                ):
		super().__init__('rtriangle',3,size,lcol,lthk,True,fcol)
		self.hgt = hgt
		self.update(0,0)

	def update(self, x, y):
		len= self.hgt * self.size
		hgt = len * 0.866025
		hs=len*0.5
		hh=hgt*0.51

		self.vertex[0]=x-hh
		self.vertex[1]=y+hs
		self.vertex[2]=x-hh
		self.vertex[3]=y-hs
		self.vertex[4]=x+hh
		self.vertex[5]=y
		
class LeftTriangle(Symbol):
	def __init__(
                 self, 
                 size, 
                 hgt, 
                 lcol=color.BLACK,
                 lthk=0.001,
                 fill=True,
                 fcol=color.RED
                ):
		super().__init__('ltriangle',3,size,lcol,lthk,True,fcol)
		self.hgt = hgt
		self.update(0,0)
		
	def update(self, x, y):
		len= self.hgt * self.size
		hgt = len * 0.866025
		hs=len*0.5
		hh=hgt*0.51

		self.vertex[0]=x-hh
		self.vertex[1]=y
		self.vertex[2]=x+hh
		self.vertex[3]=y-hs
		self.vertex[4]=x+hh
		self.vertex[5]=y+hs

class Diamond(Symbol):
	def __init__(
                 self, 
                 size, 
                 hgt, 
                 lcol=color.BLACK,
                 lthk=0.001,
                 fill=True,
                 fcol=color.RED
                ):
		super().__init__('diamond',4,size,lcol,lthk,True,fcol)
		self.hgt = hgt
		self.update(0,0)
		
	def update(self, x, y):
		len= self.hgt * self.size
		hh=0.546*len
		
		self.vertex[0]=x
		self.vertex[1]=y+hh
		self.vertex[2]=x-hh
		self.vertex[3]=y
		self.vertex[4]=x
		self.vertex[5]=y-hh
		self.vertex[6]=x+hh
		self.vertex[7]=y
		
class Square(Symbol):
	def __init__(
                 self, 
                 size, 
                 hgt, 
                 lcol=color.BLACK,
                 lthk=0.001,
                 fill=True,
                 fcol=color.RED
                ):
		super().__init__('square',4,size,lcol,lthk,True,fcol)
		self.hgt = hgt
		self.update(0,0)
		
	def update(self, x, y):
		len= self.hgt * self.size
		hh=0.5*len
		
		self.vertex[0]=x-hh
		self.vertex[1]=y+hh
		self.vertex[2]=x-hh
		self.vertex[3]=y-hh
		self.vertex[4]=x+hh
		self.vertex[5]=y-hh
		self.vertex[6]=x+hh
		self.vertex[7]=y+hh
	
		
		
		
		
		
		
