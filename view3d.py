# view3d.py
import numpy as np
import pyquaternion as pyqt

class View3d:
	#def __init__(self, znear=0.1,zfar=10000.0,fov=90.):
	def __init__(self, frm):
		self.frm = frm
		self.prepare_3d()
		self.qx    = pyqt.Quaternion(axis=[1,0,0], angle=0)
		self.qy    = pyqt.Quaternion(axis=[0,1,0], angle=0)
		self.qz    = pyqt.Quaternion(axis=[0,0,1], angle=0)
		self.qq    = pyqt.Quaternion(axis=[1,1,1], angle=0)
		self.tmat  = np.identity(4)

	def prepare_3d(self):
		frm = self.frm
		data = frm.data
		xvp_range = frm.get_pdom_wid()
		yvp_range = frm.get_pdom_hgt()
		x_range = data.get_xrange()
		y_range = data.get_yrange()
				
		fx = xvp_range/x_range
		fy = yvp_range/y_range
		
		self.ff = fx if fx < fy else fy
		
		x_center = 0.5*(data.xmax+data.xmin)
		y_center = 0.5*(data.ymax+data.ymin)
		xvp_center = frm.bbox.sx+frm.pdom.sx+0.5*xvp_range
		yvp_center = frm.bbox.sy+frm.pdom.sy+0.5*yvp_range
		
		self.cx = xvp_center-fx*x_center
		self.cy = yvp_center-fy*y_center
		self.vp_center = (self.cx, self.cy)
		
	#def prepare_3d(self):
		#self.vmat = np.identity(4)
		#self.rfov = 1.0/np.tan((self.fov*0.5)*np.pi/180)
		#self.q    = self.zfar/(self.zfar-self.znear)
		#
		#self.vmat[0][0] = self.rfov
		#self.vmat[1][1] = self.rfov
		#self.vmat[2][2] = self.q
		#self.vmat[2][3] = -self.znear*self.q
		#self.vmat[3][2] = 1.0
		#self.vmat[3][3] = 0
		
	def xtranslation(self, dx):
		self.tmat[0][3] = dx
		
	def ytranslation(self, dy):
		self.tmat[1][3] = dy
		
	def ztranslation(self, dz):
		self.tmat[2][3] = dz
		
	def scaling(self, ss):
		self.tmat[[0,1,2],[0,1,2]] = ss
		
	def xrotation(self, deg):
		self.qx = pyqt.Quaternion(axis=[1,0,0], degrees=deg)
		
	def yrotation(self, deg):
		self.qy = pyqt.Quaternion(axis=[0,1,0], degrees=deg)
	
	def zrotation(self, deg):
		self.qz = pyqt.Quaternion(axis=[0,0,1], degrees=deg)
		
	def rotate_point(self, v):
		self.qq = self.qx*self.qy
		#return self.qq.rotate(v)
		p = self.qq.rotate(v)
		return np.matmul(self.tmat[0:3,0:3], p)
	
	def vp_translate(self, dx, dy):
		self.cx += dx
		self.cy += dy
	
	def projection(self, v):
		p = np.matmul(self.tmat, [v[0],v[1],v[2],1])
		return (p[0]*self.ff+self.cx, p[1]*self.ff+self.cy)
		#return p

	#def projection(self, v):
	#	x = v[0]*self.vmat[0][0]+v[1]*self.vmat[0][1]+v[2]*self.vmat[0][2]+self.vmat[0][3]
	#	y = v[0]*self.vmat[1][0]+v[1]*self.vmat[1][1]+v[2]*self.vmat[1][2]+self.vmat[1][3]
	#	z = v[0]*self.vmat[2][0]+v[1]*self.vmat[2][1]+v[2]*self.vmat[2][2]+self.vmat[2][3]
	#	w = v[0]*self.vmat[3][0]+v[1]*self.vmat[3][1]+v[2]*self.vmat[3][2]+self.vmat[3][3]
	#	
	#	if w != 0:
	#		x /= w
	#		y /= w
	#	return (x,y)
