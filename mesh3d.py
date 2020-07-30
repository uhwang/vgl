# face3d.py

import numpy as np
import math
import re
from vgl.linetype import *
from vgl import color

MESH_WIREFRAME  = 0x0001
MESH_HIDDENLINE = 0x0002
SHADE_FLAT     = 0x0001

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
		
class Shading:
	def __init__(self, eye=None, light=None):
		self.mode = SHADE_FLAT
		self.eye   = eye
		self.light = light
		self.rend_col  = color.WHITE

	# L : light
	# P : a point(center) on a mesh
	# N : face normal vector
	def get_intensity(self, L, P, N):
		return np.dot(normalize(L-P),N)
	
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
	def __init__(self, node_index):
		self.index = node_index
		
	def compute_center(self, node):
		self.center, self.ref = compute_planar_squaremesh_center(self, node)
		
	def compute_normal(self, node):
		i = self.index
		x = node.x
		y = node.y
		z = node.z
		
		a = np.array([x[i[0]], y[i[0]], z[i[0]]], dtype=np.float32)
		b = np.array([x[i[1]], y[i[1]], z[i[1]]], dtype=np.float32)
		c = np.array([x[i[2]], y[i[2]], z[i[2]]], dtype=np.float32)
		d = np.array([x[i[3]], y[i[3]], z[i[3]]], dtype=np.float32)
		
		if np.array_equal(a, b): 
			p1 = a
			p2 = c
			p3 = d
		elif np.array_equal(a, d):
			p1 = a
			p2 = b
			p3 = c
		elif np.array_equal(b, c):
			p1 = b
			p2 = d
			p3 = a
		elif np.array_equal(c, d):
			p1 = c
			p2 = a
			p3 = b
		else:
			p1 = a
			p2 = b
			p3 = d
		#v1 = b-a
		#v2 = d-a
		v1 = p2 - p1
		v2 = p3 - p1
		
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
		self.nface  = (jpnt-1)*(ipnt-1)
		self.node   = NodeArray3d(self.nnode)
		self.tnode  = NodeArray3d(self.nnode)
		self.avg_z  = np.zeros(self.nface,  dtype=np.float32)
		self.shade_show = False
		self.shade = Shading(eye=np.array([0,0,2], dtype=np.float32), 
		                     light=np.array([0,0,2], dtype=np.float32))
		self.face   = []
		self.edge   = []
		self.show_axis = False
		
	def hiddenline(self): 
		self.mode = MESH_HIDDENLINE
		
	def set_show_axis(self, v):
		self.show_axis = v
		
	def is_axis_visible(self):
		return self.show_axis and self.axis
		
	def get_axis(self):
		return self.axis
		
	def set_shade_show(self, v):
		self.shade_show = v
		
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
				self.face.append(Face3d([a,b,c,d]))
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

		
class RectangularMesh3d(LineLevelA):
	def __init__(self, jpnt, ipnt):
		super().__init__(color.BLACK, 0.001)
		self.mode   = MESH_WIREFRAME
		self.jpnt   = jpnt
		self.ipnt   = ipnt
		self.nnode  = jpnt*ipnt
		self.node   = NodeArray3d(self.nnode)
		self.tnode  = NodeArray3d(self.nnode)
		self.edge   = []
		self.show_axis = False
		self.axis = None
		
	def is_axis_visible(self):
		return self.show_axis and self.axis
		
class TecFace3d(Face3d):
	def __init__(self, im, node_index):
		super().__init__(node_index)
		self.imesh = im
	

class Hiddenline():
	def __init__(self, nface):
		self.face = []
		self.avg_z= np.zeros((nface), dtype=np.float32)
		
	def compute_avg_z(self, mlist):
		for i, f in enumerate(self.face):
			im = f.imesh
			tz = mlist[im].tnode.z
			z = (tz[f.index[0]] + tz[f.index[1]] +
				 tz[f.index[2]] + tz[f.index[3]]) / 4.0
			self.avg_z[i] = z
	
_find_ijpan = re.compile(r"[iI]\s*=\s*(\d*)\s*,\s*[jJ]\s*=\s*(\d*)")
_non_empty_line = re.compile(r"[0-9a-zA-Z,=\"]")
_get_value = re.compile(r"\s*([-+]?\d*\.?\d*[eE]?[-+]?\d*)")

BIG_POSITIVE_NUMBER = 1.e+20
BIG_NEGATIVE_NUMBER = 1.e-20

class MeshBBox():
	def __init__(self, mlist):
		self.xmin = BIG_POSITIVE_NUMBER
		self.xmax = BIG_NEGATIVE_NUMBER
		self.ymin = BIG_POSITIVE_NUMBER
		self.ymax = BIG_NEGATIVE_NUMBER
		self.zmin = BIG_POSITIVE_NUMBER
		self.zmax = BIG_NEGATIVE_NUMBER
		
		for m in mlist:
			self.xmin = min(self.xmin, np.min(m.node.x))
			self.xmax = max(self.xmax, np.max(m.node.x))
			self.ymin = min(self.ymin, np.min(m.node.y))
			self.ymax = max(self.ymax, np.max(m.node.y))
			self.zmin = min(self.zmin, np.min(m.node.z))
			self.zmax = max(self.zmax, np.max(m.node.z))
			
	def get_bbox(self):
		return self.xmin, self.xmax, self.ymin, self.ymax, self.zmin, self.zmax
			
class TecMesh3d():
	def __init__(self, fname):
		fp = open(fname, "rt")
		self.mesh = []
		self.shade_show = False
		self.mode = MESH_WIREFRAME
		nface = 0
		self.shade = Shading(eye=np.array([0,0,-12], dtype=np.float32), 
		                     light=np.array([0,0,-10], dtype=np.float32))
		for line in fp: 
			if not _non_empty_line.search(line): 
				continue
			match = _find_ijpan.search(line)
			if match:
				ipnt = int(match.group(1))
				jpnt = int(match.group(2))
				rm = RectangularMesh3d(jpnt, ipnt)
				self.mesh.append(rm)
				nface += (jpnt-1)*(ipnt-1)
				for j in range(jpnt):
					jjpos = j * ipnt
					for i in range(ipnt):
						npos = jjpos+i
						line = fp.readline()
						if not _non_empty_line.search(line): continue
						match = _get_value.findall(line)
						rm.node.x[jjpos+i] = float(match[0])
						rm.node.y[jjpos+i] = float(match[1])
						rm.node.z[jjpos+i] = float(match[2])

		self.hidn = Hiddenline(nface)
	
	def set_shade_show(self, v):
		self.shade_show = v
		
	def create_mesh(self):
		for mi, m in enumerate(self.mesh):
			jpan = m.jpnt-1
			ipan = m.ipnt-1
			jpnt = m.jpnt
			ipnt = m.ipnt
			for j in range(jpan):
				jjpnt = j*ipnt
				for i in range(ipan):
					a = jjpnt + i  
					b = jjpnt + (i+1)
					c = (j+1)*ipnt+(i+1)
					d = (j+1)*ipnt+i
					self.hidn.face.append(TecFace3d(mi, [a,b,c,d]))
					m.edge.append(Edge3d(a,b))
					m.edge.append(Edge3d(a,d))
					f = self.hidn.face[-1]
					f.compute_normal(m.node)
					f.compute_center(m.node)
					
				m.edge.append(Edge3d(b,c))
			jjpnt += ipnt
			for i in range(ipan):
				a = jjpnt + i
				b = jjpnt + (i+1)
				m.edge.append(Edge3d(a,b))
				
	def create_tansform_node(self, v3d):
		for mi, m in enumerate(self.mesh):
			nnode = m.jpnt*m.ipnt
			for i in range(nnode):
				px = m.node.x
				py = m.node.y
				pz = m.node.z
				p = v3d.rotate_point([px[i],py[i],pz[i]])
				m.tnode.x[i] = p[0]
				m.tnode.y[i] = p[1]
				m.tnode.z[i] = p[2]	

		self.hidn.compute_avg_z(self.mesh)
		
