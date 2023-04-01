# Vector Graphic Library (VGL) for Python
#
# plot.py
#
# 2020-2-12 Ver 0.1
#
# Author: Uisang Hwang
# Email : uhwangtx@gmail.com
#

import numpy as np
from operator import itemgetter
import math

from . import color, mesh3d, text
#import color, mesh3d, text


def draw_surface_normal(dev, v3d, mesh, f, N):
	c,d = mesh3d.compute_face_center(f, mesh.tnode)
	cp = (d[0]+c[0], d[1]+c[1])
	dev.line(cp[0], cp[1], N[0], N[1], color.MAGENTA, 0.001*dev.frm.hgt())

def plot_tec_mesh(dev, v3d, geom, move=False):

	if move:
		p1 = np.zeros((3,),dtype=np.float32)
		p2 = np.zeros((3,),dtype=np.float32)
		for m in geom.mesh:
			mx = m.node.x
			my = m.node.y
			mz = m.node.z
			
			#p1[0] = mx[0]
			#p1[1] = mx[1]
			#p1[2] = mx[2]
			#p2[0] = mx[-1]
			#p2[1] = mx[-1]
			#p2[2] = mx[-1]
			#p11 = v3d.rotate_point(p1)
			#p22 = v3d.rotate_point(p2)
			#dev.line(p11[0], p11[0], p22[-1], p22[-2], m.lcol, m.lthk * dev.frm.hgt())
			for xx,yy,zz in zip(mx[0::8],my[0::8],mz[0::8]):
				p1[0] = xx
				p1[1] = yy
				p1[2] = zz
				p2 = v3d.rotate_point(p1)
				dev.circle(p2[0], p2[1],0.005, fcol=color.RED)
		
	elif geom.mode is mesh3d.MESH_WIREFRAME:
		for m in geom.mesh:
			mx = m.tnode.x
			my = m.tnode.y
			
			for e1 in m.edge:
				n1 = e1.node1
				n2 = e1.node2
				dev.line(mx[n1], my[n1], mx[n2], my[n2], m.lcol, m.lthk * dev.frm.hgt())
		E = geom.shade.eye
		RE= v3d.rotate_point(E)
		dev.circle(RE[0], RE[1], 0.001, fcol=color.RED)
		#dev.line(0,0,RE[0],RE[1], lcol=color.MAGENTA, lthk=0.001*dev.frm.hgt())
	elif geom.mode is mesh3d.MESH_HIDDENLINE:
		if geom.shade_show:
			P = np.zeros((3,),dtype=np.float32)
			for idx, val in sorted(enumerate(geom.hidn.avg_z), key=itemgetter(1)):
				f  = geom.hidn.face[idx]
				mx = geom.mesh[f.imesh].tnode.x
				my = geom.mesh[f.imesh].tnode.y
				
				i0 = f.index[0]
				i1 = f.index[1]
				i2 = f.index[2]
				i3 = f.index[3]
				
				x = (mx[i0], mx[i1], mx[i2], mx[i3])
				y = (my[i0], my[i1], my[i2], my[i3])

				p1 = v3d.rotate_point(f.ref)
				p2 = v3d.rotate_point(f.center)
				p3 = np.array([p1[0]+p2[0], p1[1]+p2[1], p1[2]+p2[2]], dtype=np.float32)
				#print("P1 P2 P3: ", p1,p2,p3)


				E = geom.shade.eye
				L = geom.shade.light
				N = v3d.rotate_point(f.unit_normal)
				#RE= v3d.rotate_point(E)
				#print("E L N: ", E,L,N)
				# draw unit normal vector on the center of a mesh
				#dev.line(E[0],E[1], p3[0], p3[1])
				
				intensity = math.fabs(geom.shade.get_intensity(L, p3, N))
				#if intensity is NaN: 
				cval = 1.0 if intensity > 1 else intensity
				fcol = color.get_gray(cval)
				#fcol = color.hsv(200*cval, 1,1)
				dev.polygon(x, y, geom.mesh[f.imesh].lcol, geom.mesh[f.imesh].lthk*dev.frm.hgt(), fcol)

				# draw surface normal vector
				#p4 = 0.02*N
				#p5 = (p3[0]+p4[0], p3[1]+p4[1])
				#dev.line(p3[0], p3[1], p5[0], p5[1], color.BLACK, geom.mesh[f.imesh].lthk*dev.frm.hgt())

				# draw a circle on the mesh center
				#dev.circle(p3[0], p3[1],0.005, fcol=color.RED)
				
				# draw a line from the mesh center to Light
				#LL = v3d.rotate_point(L)
				#dev.line(LL[0],LL[1],p3[0],p3[1], lcol=color.GRAY20, lthk=0.001*dev.frm.hgt())
				# draw a circle at the positon of Camera
			#dev.circle(RE[0], RE[1], 0.005, fcol=color.RED)
			#dev.line(0,0,E[0],E[1], lcol=color.MAGENTA, lthk=0.001*dev.frm.hgt())
		else:
			for idx, val in sorted(enumerate(geom.hidn.avg_z), key=itemgetter(1)):
				f  = geom.hidn.face[idx]
				mx = geom.mesh[f.imesh].tnode.x
				my = geom.mesh[f.imesh].tnode.y
				
				i0 = f.index[0]
				i1 = f.index[1]
				i2 = f.index[2]
				i3 = f.index[3]
				
				x = (mx[i0], mx[i1], mx[i2], mx[i3])
				y = (my[i0], my[i1], my[i2], my[i3])
				dev.polygon(x, y, geom.mesh[f.imesh].lcol, geom.mesh[f.imesh].lthk*dev.frm.hgt(), color.WHITE)
				
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
				dev.line(E[0],E[1], p3[0], p3[1])
				
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