# Vector Graphic Library (VGL) for Python
#
# vertex.py
#
# 2020-2-12 Ver 0.1
#
# Author: Uisang Hwang
# Email : uhwangtx@gmail.com
#

import numpy as np

class Vertex():
	def __init__(self, nvert):
		self.vertex = np.empty(nvert*2, dtype='float32')
		
	def get_vertices(self): return self.vertex
	def get_vertex(self, index): return [self.vertex[index*2], self.vertex[index*2+1]]
	def get_nvertex(self): return int(self.vertex.size/2)
	def get_xs(self): return self.vertex[::2]
	def get_ys(self): return self.vertex[1::2]
	def set_vertex(self, i, x,y): 
		self.vertex[i*2]=x
		self.vertex[i*2+1]=y
		


