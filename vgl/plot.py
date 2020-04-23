# Vector Graphic Library (VGL) for Python
#
# plot.py
#
# 2020-2-12 Ver 0.1
#
# Author: Uisang Hwang
# Email : uhwangtx@gmail.com
#

from vgl import color, mesh3d, text
import numpy as np
from operator import itemgetter
import math

def draw_surface_normal(dev, v3d, mesh, f, N):
	c,d = mesh3d.compute_face_center(f, mesh.tnode)
	cp = (d[0]+c[0], d[1]+c[1])
	dev.line(cp[0], cp[1], N[0], N[1], color.MAGENTA, 0.001*dev.frm.hgt())

def plot_mesh(dev, v3d, mesh):
	
	if mesh.mode is mesh3d.MESH_WIREFRAME:
		mx = mesh.tnode.x
		my = mesh.tnode.y
		
		for e1 in mesh.edge:
			n1 = e1.node1
			n2 = e1.node2
			dev.line(mx[n1], my[n1], mx[n2], my[n2], mesh.lcol, mesh.lthk * dev.frm.hgt())

		#for f in mesh.face:
		#	p1= v3d.rotate_point(f.ref)
		#	p2 = v3d.rotate_point(f.center)
		#	p3 = (p1[0]+p2[0], p1[1]+p2[1])
		#	dev.circle(p3[0], p3[1], 0.005, fcol=color.RED)
		#	un = 0.25*f.unit_normal
		#	p4 = v3d.rotate_point(un)
		#	p5 = (p3[0]+p4[0], p3[1]+p4[1])
		#	dev.line(p3[0], p3[1], p5[0], p5[1], color.MAGENTA, mesh.lthk * dev.frm.hgt())
		#	E = v3d.rotate_point(mesh.shade.eye)
		#	dev.line(E[0],E[1], p3[0], p3[1], color.CUSTOM5, mesh.lthk * dev.frm.hgt())
				
	elif mesh.mode is mesh3d.MESH_HIDDENLINE:
			
		if mesh.shade_show:
			P = np.zeros((3,),dtype=np.float32)
			for idx, val in sorted(enumerate(mesh.avg_z), key=itemgetter(1)):
				f  = mesh.face[idx]
				mx = mesh.tnode.x
				my = mesh.tnode.y
				
				i0 = f.index[0]
				i1 = f.index[1]
				i2 = f.index[2]
				i3 = f.index[3]
				
				x = (mx[i0], mx[i1], mx[i2], mx[i3])
				y = (my[i0], my[i1], my[i2], my[i3])

				p1= v3d.rotate_point(f.ref)
				p2 = v3d.rotate_point(f.center)
				p3 = np.array([p1[0]+p2[0], p1[1]+p2[1], p1[2]+p2[2]], dtype=np.float32)
				
				# draw a circle on the mesh center
				#dev.circle(p3[0], p3[1],0.005, fcol=color.RED)

				E = mesh.shade.eye
				L = mesh.shade.light
				N = v3d.rotate_point(f.unit_normal)
				
				# draw unit normal vector on the center of a mesh
				#dev.line(E[0],E[1], p3[0], p3[1])
				
				intensity = math.fabs(mesh.shade.get_intensity(L, p3, N))
				cval = 1.0 if intensity > 1 else intensity
				fcol = color.get_gray(cval)
				dev.polygon(x, y, mesh.lcol, mesh.lthk*dev.frm.hgt(), fcol)

				# draw surface normal vector
				#un = 0.5*f.unit_normal
				#p4 = v3d.rotate_point(un)
				#p5 = (p3[0]+p4[0], p3[1]+p4[1])
				#dev.line(p3[0], p3[1], p5[0], p5[1], color.MAGENTA, mesh.lthk*dev.frm.hgt())
		else:
			for idx, val in sorted(enumerate(mesh.avg_z), key=itemgetter(1)):
				f  = mesh.face[idx]
				mx = mesh.tnode.x
				my = mesh.tnode.y
				
				i0 = f.index[0]
				i1 = f.index[1]
				i2 = f.index[2]
				i3 = f.index[3]
				
				x = (mx[i0], mx[i1], mx[i2], mx[i3])
				y = (my[i0], my[i1], my[i2], my[i3])
				dev.polygon(x, y, mesh.lcol, mesh.lthk*dev.frm.hgt(), color.WHITE)
				
				# draw a circle on the mesh center
				#p1= v3d.rotate_point(f.ref)
				#p2 = v3d.rotate_point(f.center)
				#p3 = (p1[0]+p2[0], p1[1]+p2[1])
				#dev.circle(p3[0], p3[1],0.005, fcol=color.RED)
				
				# draw surface normal vector
				#un = 0.25*f.unit_normal
				#p4 = v3d.rotate_point(un)
				#p5 = (p3[0]+p4[0], p3[1]+p4[1])
				#dev.line(p3[0], p3[1], p5[0], p5[1], color.CUSTOM4, mesh.lthk*dev.frm.hgt())
				
				#E = v3d.rotate_point(mesh.shade.eye)
				#dev.line(E[0],E[1], p3[0], p3[1])

	# plot axis
	if mesh.is_axis_visible():
		ax = mesh.get_axis()
		oo = v3d.rotate_point(ax.center)
		ox = v3d.rotate_point(ax.x)
		oy = v3d.rotate_point(ax.y)
		oz = v3d.rotate_point(ax.z)
		
		dev.line(oo[0], oo[1], ox[0], ox[1], ax.xcol.lcol, ax.xcol.lthk)
		dev.line(oo[0], oo[1], oy[0], oy[1], ax.ycol.lcol, ax.ycol.lthk)
		dev.line(oo[0], oo[1], oz[0], oz[1], ax.zcol.lcol, ax.ycol.lthk)