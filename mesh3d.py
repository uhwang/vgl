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

# c : center of the object
class Axis():
	def __init__(self, c, x,y,z):
		self.center = np.array([c[0],c[1],c[2]], dtype=np.float32)
		self.x = np.array([x,0,0], dtype=np.float32)
		self.y = np.array([0,y,0], dtype=np.float32)
		self.z = np.array([0,0,z], dtype=np.float32)
		self.xcol = LineLevelA(color.RED  , 0.03)
		self.ycol = LineLevelA(color.GREEN, 0.03)
		self.zcol = LineLevelA(color.BLUE , 0.03)
		
class Rendering:
	def __init__(self, eye=None, light=None):
		self.mode = RENDER_FLAT
		self.eye   = eye
		self.light = light
		self.rend_col  = color.WHITE

	# L : light
	# P : a point(center) on a mesh
	# N : face normal vector
	def get_intensity(self, L, P, N):
		s = normalize(L-P)
		#s = L-P
		return np.dot(s,N)
	
def compute_planar_squaremesh_center(f, node):
	i = f.index
	b = np.array([node.x[i[1]], node.y[i[1]], node.z[i[1]]], dtype=np.float32)
	d = np.array([node.x[i[3]], node.y[i[3]], node.z[i[3]]], dtype=np.float32)
	return (b-d)*0.5, d
	
def compute_face_normal(node, a,b,c,d):
	p1 = np.array([node.x[a], node.y[a], node.z[a]], dtype=np.float32)
	p2 = np.array([node.x[b], node.y[b], node.z[b]], dtype=np.float32)
	p4 = np.array([node.x[d], node.y[d], node.z[d]], dtype=np.float32)
	v1 = p2-p1
	v2 = p4-p1
	return normalize(np.cross(v1, v2))

# N: face normal vector
# E: eye point or camera point
# P: one vertex of a mesh

def is_face_visible(N, E, P):
	C = E-P
	CC=C**2
	NN=N**2
	MC = math.sqrt(CC[0]+CC[1]+CC[2])
	MN = math.sqrt(NN[0]+NN[1]+NN[2])
	beta = math.acos(np.dot(C,N)/(MC*MN))*180/np.pi
	return True if beta < 90 else False
	
class Node3d():
    def __init__(self, coord=(0,0,0)):
        self.x = coord[0]
        self.y = coord[1]
        self.z = coord[2]
		
class Face3d():
	def __init__(self, node_index, fn):
		self.index = node_index
		self.normal = fn
		
	def compute_center(self, node):
		self.center, self.ref = compute_planar_squaremesh_center(self, node)
		
	def compute_normal(self, node):
		i = self.index
		x = node.x
		y = node.y
		z = node.z
		
		a = np.array([x[i[0]], y[i[0]], z[i[0]]], dtype=np.float32)
		b = np.array([x[i[1]], y[i[1]], z[i[1]]], dtype=np.float32)
		d = np.array([x[i[3]], y[i[3]], z[i[3]]], dtype=np.float32)
				
		v1 = b-a
		v2 = d-a
		
		self.normal = np.cross(v1,v2)
		self.unit_normal = normalize(self.normal)
		
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
		self.nnode  = jpnt*ipnt
		self.nface  =(jpnt-1)*(ipnt-1)
		self.node   = NodeArray3d(self.nnode)
		#self.tnode  = NodeArray2d(self.nnode)
		self.tnode  = NodeArray3d(self.nnode)
		#self.zvalue = np.zeros(self.nnode, dtype=np.float32)
		self.avg_z  = np.zeros(self.nface,  dtype=np.float32)
		self.render_show = False
		self.render = Rendering(eye=np.array([0.0,0.0,0.6], dtype=np.float32), 
		                        light=np.array([0.0,0.0,0.6], dtype=np.float32))
		self.face   = []#[Face3d()]*nface
		self.edge   = []#[Edge3d()]*nface
		self.show_axis = False
		
	def hiddenline(self): 
		self.mode = MESH_HIDDENLINE
		
	def set_show_axis(self, v):
		self.show_axis = v
		
	def is_axis_visible(self):
		return self.show_axis and self.axis
		
	def get_axis(self):
		return self.axis
		
	def set_render_show(self, v):
		self.render_show = v
		
	def create_axis(self, c, x, y, z):
		self.axis = Axis(c, x, y, z)
		
	def create_tansform_node(self, v3d):
		nnode = self.jpnt*self.ipnt
		for i in range(nnode):
			nx = self.node.x
			ny = self.node.y
			nz = self.node.z
			p = v3d.rotate_point([nx[i],ny[i],nz[i]])
			#self.zvalue [i] = p[2]
			self.tnode.x[i] = p[0]
			self.tnode.y[i] = p[1]
			self.tnode.z[i] = p[2]
			
	def compute_avg_z(self):
		for i, face in enumerate(self.face):
			n = self.tnode.z
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
				f = self.face[-1]
				f.compute_normal(self.node)
				f.compute_center(self.node)
				
			self.edge.append(Edge3d(b,c))
			
		jjpnt += ipnt
		for i in range(ipan):
			a = jjpnt + i
			b = jjpnt + (i+1)
			self.edge.append(Edge3d(a,b))
				
