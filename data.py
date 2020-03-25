# Vector Graphic Library (VGL) for Python
#
# data.py
#
# 2020-2-12 Ver 0.1
#
# Author: Uisang Hwang
# Email : uhwangtx@gmail.com
#

class Data():
	def __init__(self, xmin, xmax, ymin, ymax, zmin=0, zmax=0):
		self.xmin=xmin
		self.xmax=xmax 
		self.ymin=ymin 
		self.ymax=ymax 
		self.zmin=zmin 
		self.zmax=zmax
		
	def get_xrange(self): return self.xmax-self.xmin
	def get_yrange(self): return self.ymax-self.ymin
	def get_zrange(self): return self.zmax-self.zmin
	def set_yrange(self, ymin, ymax): 
		self.ymin = ymin
		self.ymax = ymax
		
	def xcenter(self): return self.xmin+(self.xmax-self.xmin)*0.5
	def ycenter(self): return self.ymin+(self.ymax-self.ymin)*0.5
