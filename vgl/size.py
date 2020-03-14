# Vector Graphic Library (VGL) for Python
#
# size.py
#
# 2020-2-12 Ver 0.1
#
# Author: Uisang Hwang
# Email : uhwangtx@gmail.com
#

class BBox():
	def __init__(self,sx,sy,ex,ey):
		self.set_bbox(sx,sy,ex,ey)
	
	def wid(self): return self.ex-self.sx
	def hgt(self): return self.ey-self.sy
	def get_xs(self): return [self.sx,self.sx,self.ex,self.ex]
	def get_ys(self): return [self.sy,self.ey,self.ey,self.sy]
	
	def set_bbox(self, sx,sy,ex,ey):
		self.sx=sx
		self.sy=sy
		self.ex=ex
		self.ey=ey
	
	def expand(self, ds): 
		self.sx -= ds
		self.ex += ds
		self.sy -= ds
		self.ey += ds
		
	def trans(self, tx, ty): 
		self.sx += tx
		self.sy += ty
		self.ex += tx
		self.ey += ty
		
	def transx(self, dx):
		self.sx += dx
		self.ex += dx
		
	def transy(self, dy):
		self.sy += dy
		self.ey += dy

class Rect():
	def __init__(self, sx=0,sy=0,wid=0,hgt=0):
		self.sx = sx
		self.sy = sy
		self.wid = wid
		self.hgt = hgt
		
	def get_wid(self): return self.wid
	def get_hgt(self): return self.hgt
	def get_sx(self): return self.sx
	def get_sy(self): return self.sy
	def get_ex(self): return self.sx+self.wid
	def get_ey(self): return self.sy+self.hgt

		