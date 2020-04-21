# face3d.py

import numpy as np
import math
from vgl.linetype import *
from vgl import color

MESH_WIREFRAME  = 0x0001
MESH_HIDDENLINE = 0x0002
RENDER_FLAT     = 0x0001

def normalize(v):
	vv = v**2
	nv = v/math.sqrt(vv[0]+vv[1]+vv[2])
	return nv
	
class Rendering:
	def __init__(self, eye=None, light=None):
		self.mode = RENDER_FLAT
		self.eye   = eye
		self.light = light
		self.rend_col  = color.WHITE

	def get_intensity(self, L, P, N):
		s = normalize(L-P)
		return np.dot(s,N)
	
	#def is_visible(self, P, N):
		
def compute_face_normal(node, a,b,c,d):
	p1 = np.array([node.x[a], node.y[a], node.z[a]], dtype=np.float32)
	p2 = np.array([node.x[b], node.y[b], node.z[b]], dtype=np.float32)
	p3 = np.array([node.x[c], node.y[c], node.z[c]], dtype=np.float32)
	p4 = np.array([node.x[d], node.y[d], node.z[d]], dtype=np.float32)
	v1 = p2-p1
	v2 = p4-p1
	#return np.linalg.norm(np.cross(v1, v2))
	return normalize(np.cross(v1, v2))

class Node3d():
    def __init__(self, coord=(0,0,0)):
        self.x = coord[0]
        self.y = coord[1]
        self.z = coord[2]
		
class Face3d():
	def __init__(self, node_index, fn):
		self.index = node_index
		self.normal = fn
		
# p1, p2 are node indices
class Edge3d():
	def __init__(self, i1=0, i2=0):
		self.node1 = i1
		self.node2 = i2
		
class NodeArray3d():
	def __init__(self, nnode):
		self.x = np.zeros(nnode, dtype=np.float32)
		self.y = np.zeros(nnode, dtype=np.float32)
		self.z = np.zeros(nnode, dtype=np.float32)

class NodeArray2d():
	def __init__(self, nnode):
		self.x = np.zeros(nnode, dtype=np.float32)
		self.y = np.zeros(nnode, dtype=np.float32)
		
class SquareMesh3d(LineLevelA):
	def __init__(self, jpnt, ipnt):
		super().__init__(color.BLACK, 0.001)
		self.mode   = MESH_WIREFRAME
		self.jpnt   = jpnt
		self.ipnt   = ipnt
		nnode       = jpnt*ipnt
		nface       =(jpnt-1)*(ipnt-1)
		self.node   = NodeArray3d(nnode)
		self.tnode  = NodeArray2d(nnode)
		self.zvalue = np.zeros(nnode, dtype=np.float32)
		self.avg_z  = np.zeros(nface,  dtype=np.float32)
		self.render_show = False
		self.render = Rendering(eye=np.array([0,0,10], dtype=np.float32), 
		                        light=np.array([10,10,10], dtype=np.float32))
		self.face   = []#[Face3d()]*nface
		self.edge   = []#[Edge3d()]*nface
		
	def hiddenline(self): 
		self.mode = MESH_HIDDENLINE
		
	def create_tansform_node(self, v3d):
		nnode = self.jpnt*self.ipnt
		for i in range(nnode):
			nx = self.node.x
			ny = self.node.y
			nz = self.node.z
			p = v3d.rotate_point([nx[i],ny[i],nz[i]])
			self.zvalue [i] = p[2]
			self.tnode.x[i] = p[0]
			self.tnode.y[i] = p[1]

	def compute_avg_z(self):
		for i, face in enumerate(self.face):
			n = self.zvalue
			z = (n[face.index[0]] + n[face.index[1]] +
				 n[face.index[2]] + n[face.index[3]]) / 4.0
			self.avg_z[i] = z

	def create_node(self, geom):
		for j in range(self.jpnt):
			jjpos = j * self.ipnt
			for i in range(self.ipnt):
				npos = jjpos+i
				gp = geom[j][i]
				self.node.x[jjpos+i] = gp[0]
				self.node.y[jjpos+i] = gp[1]
				self.node.z[jjpos+i] = gp[2]

	def create_mesh(self):
		jpan = self.jpnt-1
		ipan = self.ipnt-1
		jpnt = self.jpnt
		ipnt = self.ipnt
		for j in range(jpan):
			jjpnt = j*ipnt
			for i in range(ipan):
				a = jjpnt + i  
				b = jjpnt + (i+1)
				c = (j+1)*ipnt+(i+1)
				d = (j+1)*ipnt+i
				self.face.append(Face3d([a,b,c,d], compute_face_normal(self.node, a,b,c,d)))
				self.edge.append(Edge3d(a,b))
				self.edge.append(Edge3d(a,d))
			self.edge.append(Edge3d(b,c))
			
		jjpnt += ipnt
		for i in range(ipan):
			a = jjpnt + i
			b = jjpnt + (i+1)
			self.edge.append(Edge3d(a,b))
				
