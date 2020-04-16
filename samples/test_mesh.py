# test_mesh.py
import pygame 
from pygame.locals import *
import numpy as np
from vgl import color, geom, BBox, Frame, FrameManager, Data
from vgl import DeviceWindowsMetafile, DeviceCairo, DevicePygame
from vgl import drawfrm, drawtick, drawaxis, drawlabel
from vgl import view3d, mesh3d, plot
import math
import cylinder

def create_sphere(r, jpan, ipan):
	jpnt = jpan+1
	ipnt = ipan+1
	twopi= 2*np.pi
	pi_2 = np.pi*0.5
	dphi = twopi/(jpan)
	dthe = twopi/(ipan)
	geom = np.zeros((jpnt,ipnt,3),dtype=np.float32)
	ang = 0
	for j in range(jpnt):
		#start = pi_2 if math.fabs(ang-twopi) < 0.001 else 0
		#phi = start+j * dphi
		#ang = phi
		phi = j*dphi
		for i in range(ipnt):
			the = i*dthe
			x = r*np.cos(phi)*np.cos(the)
			y = r*np.cos(phi)*np.sin(the)
			z = r*np.sin(phi)
			geom[j][i][0] = x
			geom[j][i][1] = y
			geom[j][i][2] = z
	return geom
	
jpan = 15
ipan = 10
zmin = -0.4
zmax = 0.4

#geom = naca45.create_3d_wing("4412", jpan, ipan, 0, -0.5, 0.5)
#geom = create_sphere(1, jpan, ipan)
geom = cylinder.create_cylinder(0.5, jpan, ipan, zmin, zmax)

#=====================================

def compare_matplot():
	import matplotlib.pyplot as plt
	from matplotlib import cm
	from matplotlib.ticker import LinearLocator, FormatStrFormatter
	
	X = geom[:,:,0]
	Y = geom[:,:,1]
	Z = geom[:,:,2]
	
	fig = plt.figure()
	ax = fig.gca(projection='3d')
	#surf = ax.plot_surface(X, Y, Z, linewidth=1, color = "#ff1010", antialiased=False)
	surf = ax.plot_wireframe(X, Y, Z, linewidth=1, color = "#ff1010", antialiased=False)
	plt.show()

#=====================================

xmin = np.min(geom[:,:,0])
xmax = np.max(geom[:,:,0])
ymin = np.min(geom[:,:,1])
ymax = np.max(geom[:,:,1])

# adjust ymin, ymax for wing geom
#ymin =-0.5
#ymax = 0.5
data = Data(xmin, xmax, ymin, ymax, zmin, zmax)
fmm = FrameManager()
frm = fmm.create(0,0,5,5,data)

mesh = mesh3d.SquareMesh3d(geom.shape[0], geom.shape[1])
mesh.create_node(geom)
mesh.create_mesh()
v3d = view3d.View3d(frm)

running = True
lbutton = False
move = False
old_pos = (0,0)
new_pos = (0,0)
m_xRotate = 0
m_yRotate = 0
first = True
gbbox = fmm.get_gbbox()
dev_rst = DevicePygame(gbbox, 100)
buttons = (False,False,False)
lbutton = False
move = False
prv_mode = mesh3d.MESH_WIREFRAME
win_size = dev_rst.size()
trans = False
trans_dx = data.get_xrange()*0.05
trans_dy = data.get_yrange()*0.05
scale = 1.0
dev_rst.set_plot(frm)
v3d.scaling(0.5)

def plot_geom(dev):
	clip = dev.frm.get_clip()
	dev.create_clip(clip[0],clip[1],clip[2],clip[3])
	plot.plot_mesh(dev, mesh, v3d)
	
def save_cairo(fname, frm, gbox, dpi):
	dev_img = DeviceCairo(fname, gbox, dpi)
	dev_img.fill_white()
	dev_img.set_plot(frm)
	plot_geom(dev_img)
	dev_img.close()
	
def save_wmf(fname, frm, gbbox):
	dev_wmf = DeviceWindowsMetafile(fname, gbbox)
	dev_wmf.set_device(frm)
	plot_geom(dev_wmf)
	dev_wmf.close()

choice = 1
dev_rst.fill_white()
mesh.create_tansform_node(v3d)
mesh.compute_ave_z()
plot_geom(dev_rst)
dev_rst.show()

while running:
	dev_rst.fill_white()
	loopRate = 50
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == K_s:
				prv_choice = choice
				choice='s'
			if event.key == K_i:
				prv_choice = choice
				choice='i'
			elif event.key == K_m:
				prv_choice = choice
				choice='m'
			elif event.key == K_w:
				print("... Wireframe mode")
				mesh.mode = mesh3d.MESH_WIREFRAME
			elif event.key == K_t:
				print("... translation")
				trans = ~trans
				print(trans)
			elif event.key == K_h:
				print("... Hiddenline mode")
				mesh.mode = mesh3d.MESH_HIDDENLINE
				plot_geom(dev_rst)
				dev_rst.show()
				
		elif event.type == pygame.MOUSEBUTTONDOWN:
			prv_mode = mesh.mode
			buttons = pygame.mouse.get_pressed()
			old_pos = event.pos
			lbutton = True
		elif event.type == pygame.MOUSEMOTION:
			new_pos = event.pos
			move = True
			if buttons[0]:
				mesh.mode = mesh3d.MESH_WIREFRAME
				#m_yRotate -= old_pos[0]-new_pos[0]
				#m_xRotate += old_pos[1]-new_pos[1]
				dx = new_pos[0]-old_pos[0]
				dy = new_pos[1]-old_pos[1]
				if trans:
					print("... Trans(dx: %d, dy: %d)"%(dx,dy))
					tqx = trans_dx if dx < 0 else -trans_dx
					tqy = trans_dy if dy > 0 else -trans_dy
					frm.translate_xy(tqx, tqy)
					dev_rst.set_plot(frm)
				else:
					m_xRotate += dy
					m_yRotate += dx
					v3d.xrotation(m_xRotate)
					v3d.yrotation(m_yRotate)
			
			elif buttons[2]:
				diffy = old_pos[1]-new_pos[1]
				if diffy!=0:
					if diffy<0: scale += 0.1
					if diffy>0: scale -= 0.1
					v3d.scaling(scale)
					print('scaling.. ', diffy, scale)
			old_pos = event.pos
			
			if buttons[0] or buttons[2]:
				mesh.create_tansform_node(v3d)
				
		elif event.type == pygame.MOUSEBUTTONUP:
			buttons = pygame.mouse.get_pressed()
			lbutton = False
			move = False
			#trans = False
			mesh.mode = prv_mode
			if mesh.mode is mesh3d.MESH_HIDDENLINE:
				mesh.compute_ave_z()
				plot_geom(dev_rst)
				dev_rst.show()
			
	if lbutton and move:
		plot_geom(dev_rst)
		dev_rst.show()

	if choice == 's':
		print('... 3dgeom wmf')
		save_wmf('3dgeom.wmf', frm, gbbox)
		choice = prv_choice		
	elif choice == 'i':
		print('... 3dgeom png')
		save_cairo('3dgeom.png', frm, gbbox, 150)
		choice = prv_choice		
	elif choice == 'm':
		compare_matplot()
		choice = prv_choice
		
pygame.quit()


