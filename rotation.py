# Vector Graphic Library (VGL) for Python
#
# rotation.py
#
# 2020-2-12 Ver 0.1
#
# Author: Uisang Hwang
# Email : uhwangtx@gmail.com
#

import numpy as np
import vgl.geom as geom
from vgl.util import deg_to_rad, rad_to_deg

class Rotation():
	def __init__(self):
		self.clear()
		
	def clear(self):
		self.rmat = np.array([[1, 0], [0, 1]], dtype='float32')
		self.tmat = np.array( [0, 0], dtype='float32')
		self.cmat = np.array([[1, 0], [0, 1]], dtype='float32')
		self.smat = np.array([[1, 0], [0, 1]], dtype='float32')
	
	def push(self):
		self.save_rmat = self.rmat
		self.save_tmat = self.tmat
		
	def pop(self):
		self.rmat = self.save_rmat
		self.tmat = self.save_tmat
		
	def trans(self, x, y):
		#self.tmat = np.array([[1, x],[y,1]])
		self.tmat[0]=x
		self.tmat[1]=y
		return self.tmat

	def rot(self, deg):
		rad = deg_to_rad(deg)
		#self.rmat = np.array([[np.cos(rad), -np.sin(rad)], 
        #         [np.sin(rad), np.cos(rad)]], dtype='float32')
		
		self.rmat[0][0]=np.cos(rad)
		self.rmat[0][1]=-np.sin(rad)
		self.rmat[1][0]=np.sin(rad)
		self.rmat[1][1]=np.cos(rad)
		
		return self.rmat
		
	def scale(self, scl):
		self.smat[0][0]=scl
		self.smat[1][1]=scl
		return self.smat
		
	def get_conversion_matrix(self):
		#self.cmat = np.dot(self.rmat, self.tmat)
		self.cmat=self.rmat
		return self.cmat
		
	def compute_rotation(self, shape, deg):
		mat = self.rot(deg)
		nvert = shape.get_nvertex()
		new_xy = np.empty(nvert*2, dtype='float32')
		for i in range(nvert):
			x,y = shape.get_vertex(i)
			xy = np.dot(mat, np.array([x,y],dtype='float32'))
			new_xy[i*2:i*2+2] = xy
		return new_xy
		
	def compute_shape(self, shape):
		mat = self.get_conversion_matrix()
		nvert = shape.get_nvertex()
		new_xy = np.empty(nvert*2, dtype='float32')
		for i in range(nvert):
			x,y = shape.get_vertex(i)
			x += self.tmat[0]
			y += self.tmat[1]
			xy = np.dot(mat, np.array([x,y],dtype='float32'))
			new_xy[i*2:i*2+2] = xy
		return new_xy

def get_rotation_bbox(self, bbox, deg):
	nvert = 4
	xs = bbox.get_xs()
	ys = bbox.get_ys()
	rad = deg_to_rad(deg)
	mat=np.emtpy((2,2), dtype='float32')
	mat[0][0]=np.cos(rad)
	mat[0][1]=-np.sin(rad)
	mat[1][0]=np.sin(rad)
	mat[1][1]=np.cos(rad)
		
	new_xy = np.empty(nvert*2, dtype='float32')
	for i in range(nvert):
		xy = np.dot(mat, np.array([xs[i],ys[i]],dtype='float32'))
		new_xy[i*2:i*2+2] = xy
	return new_xy[::2], new_xy[1::2]		
