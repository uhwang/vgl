# face3d.py

import numpy as np
from vgl.linetype import *

MESH_WIREFRAME = 0
MESH_HIDDENLINE = 1

class Node3d():
    def __init__(self, coord=(0,0,0)):
        self.x = coord[0]
        self.y = coord[1]
        self.z = coord[2]
		
class Face3d():
	def __init__(self, node_index=[], avgz=0):
		self.index = node_index
	
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
		self.face   = []#[Face3d()]*nface
		self.edge   = []#[Edge3d()]*nface
		
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
				self.face.append(Face3d([a,b,c,d]))
				self.edge.append(Edge3d(a,b))
				self.edge.append(Edge3d(a,d))
			self.edge.append(Edge3d(b,c))
			
		jjpnt += ipnt
		for i in range(ipan):
			a = jjpnt + i
			b = jjpnt + (i+1)
			self.edge.append(Edge3d(a,b))
				
