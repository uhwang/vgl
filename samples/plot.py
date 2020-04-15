# Vector Graphic Library (VGL) for Python
#
# plot.py
#
# 2020-2-12 Ver 0.1
#
# Author: Uisang Hwang
# Email : uhwangtx@gmail.com
#

import view3d
from vgl import color
import mesh3d
import numpy as np
from operator import itemgetter

def convertToComputerFrame(point):
	computerFrameChangeMatrix = np.array([[-1, 0, 0], [0, 0, -1], [0, -1, 0]])
	return np.matmul(computerFrameChangeMatrix, point)

def plot_mesh(dev, mesh, v3d):
	
	if mesh.mode is mesh3d.MESH_WIREFRAME:
		mx = mesh.node.x
		my = mesh.node.y
		mz = mesh.node.z
		
		for e1 in mesh.edge:
			n1 = e1.node1
			n2 = e1.node2
			p0 = (mx[n1], my[n1], mz[n1])
			q0 = (mx[n2], my[n2], mz[n2])
			p1 = v3d.rotate_point(p0)
			q1 = v3d.rotate_point(q0)
			dev.line(p1[0], p1[1], q1[0], q1[1], color.BLACK, 0.001)

	elif mesh.mode is mesh3d.MESH_HIDDENLINE:
		for idx, val in sorted(enumerate(mesh.avg_z), key=itemgetter(1)):
			face = mesh.face[idx]
			mx = mesh.tnode.x
			my = mesh.tnode.y
			
			i0 = face.index[0]
			i1 = face.index[1]
			i2 = face.index[2]
			i3 = face.index[3]
			
			x = (mx[i0], mx[i1], mx[i2], mx[i3])
			y = (my[i0], my[i1], my[i2], my[i3])
			dev.polygon(x, y, color.BLACK, color.WHITE, lthk=0.001)
	
#def plot_mesh(dev, mesh, v3d):
#	
#	if mesh.mode is mesh3d.MESH_WIREFRAME:
#		for e1 in mesh.edge:
#			p0 = mesh.node[e1.node1]
#			q0 = mesh.node[e1.node2]
#			p1 = v3d.rotate_point([p0.x, p0.y, p0.z])
#			q1 = v3d.rotate_point([q0.x, q0.y, q0.z])
#			dev.line(p1[0], p1[1], q1[0], q1[1], color.BLACK, 0.001)
#
#	elif mesh.mode is mesh3d.MESH_HIDDENLINE:
#		for idx, val in sorted(enumerate(mesh.avg_z), key=itemgetter(1)):
#			face = mesh.face[idx]
#			p = [mesh.tnode[face.index[0]],
#				    mesh.tnode[face.index[1]],
#					mesh.tnode[face.index[2]],
#					mesh.tnode[face.index[3]]]
#			x = (p[0][0], p[1][0], p[2][0], p[3][0])
#			y = (p[0][1], p[1][1], p[2][1], p[3][1])
#			dev.polygon(x, y, color.BLACK, color.WHITE, lthk=0.001)
			
	#elif mode = MESH_HIDDENLINE: