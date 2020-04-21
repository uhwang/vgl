# Vector Graphic Library (VGL) for Python
#
# plot.py
#
# 2020-2-12 Ver 0.1
#
# Author: Uisang Hwang
# Email : uhwangtx@gmail.com
#

from vgl import color, mesh3d
import numpy as np
from operator import itemgetter

def plot_mesh(dev, v3d, mesh):
	
	if mesh.mode is mesh3d.MESH_WIREFRAME:
		mx = mesh.tnode.x
		my = mesh.tnode.y
		
		for e1 in mesh.edge:
			n1 = e1.node1
			n2 = e1.node2
			dev.line(mx[n1], my[n1], mx[n2], my[n2], mesh.lcol, mesh.lthk * dev.frm.hgt())

	elif mesh.mode is mesh3d.MESH_HIDDENLINE:
			
		if not mesh.render_show:
			dev.make_pen(mesh.lcol, mesh.lthk*dev.frm.hgt())
			dev.make_brush(color.WHITE)
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
				dev.polygon(x, y)
			dev.delete_pen()
			dev.delete_brush()
		else:
			P = np.zeros((3,),dtype=np.float32)
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
				P[0] = mesh.node.x[i0]
				P[1] = mesh.node.y[i0]
				P[2] = mesh.node.z[i0]
				L    = v3d.rotate_point(mesh.render.light)
				N    = face.normal
				inst = mesh.render.get_intensity(L, P, N)
				#if inst < 0: fcol = (255,255,255)
				#else       : fcol = (inst*255, inst*255, inst*255)
				print(inst)
				fcol = (inst*255, inst*255, inst*255)
				dev.polygon(x, y, mesh.lcol, mesh.lthk*dev.frm.hgt(), fcol)
