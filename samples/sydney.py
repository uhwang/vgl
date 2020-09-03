# multi mesh
import pygame 
from pygame.locals import *
import vgl
import numpy as np

tec_file = "sydney.tec"

tec_geom = vgl.mesh3d.TecMesh3d(tec_file)
tec_geom.create_mesh()
mb = vgl.mesh3d.MeshBBox(tec_geom.mesh)
xmin, xmax, ymin, ymax, zmin, zmax = mb.get_bbox()
data = vgl.Data(xmin, xmax, ymin, ymax, zmin, zmax)
fmm = vgl.FrameManager()
frm= fmm.create(0,0,4,4,data)
v3d = vgl.view3d.View3d(frm)
gbbox = fmm.get_gbbox()

pyg_dev = vgl.DevicePygame(gbbox, 150)
pyg_dev.set_plot(frm)
ctrl = vgl.util.Pygame3DUtil(pyg_dev)

v3d.xrotation(30)
v3d.yrotation(30)
v3d.scaling(ctrl.scale)
tec_geom.create_tansform_node(v3d)

def plot_geom(dev, move=False):
    vgl.drawfrm.draw_frame(dev, frm)
    clip = dev.frm.get_clip()
    dev.create_clip(clip[0],clip[1],clip[2],clip[3])
    vgl.plot.plot_tec_mesh(dev, v3d, tec_geom, move)
    dev.delete_clip()

def plot_all(dev, move=None):
    dev.set_plot(frm)
    plot_geom(dev, move)
    
def save_cairo():
	dev_cairo = vgl.DeviceCairo("sydney.jpg", gbbox, 200)
	dev_cairo.fill_white()
	plot_all(dev_cairo)
	dev_cairo.close()

def save_wmf():
	dev_wmf = vgl.DeviceWindowsMetafile("sydney.wmf", gbbox)
	plot_all(dev_wmf)
	dev_wmf.close()

choice = 1
running = True
pyg_dev.fill_white()
plot_all(pyg_dev)
pyg_dev.show()

while running:
	pyg_dev.fill_white()
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == K_s:
				ctrl.prv_choice = choice
				choice='s'
			if event.key == K_i:
				ctrl.prv_choice = choice
				choice='i'
			elif event.key == K_m:
				ctrl.prv_choice = choice
				choice='m'
			elif event.key == K_r:
				ctrl.shade = ~ctrl.shade
				tec_geom.set_shade_show(ctrl.shade)
				plot_all(pyg_dev)
				pyg_dev.show()
			elif event.key == K_w:
				print("... Wireframe mode")
				tec_geom.mode = vgl.mesh3d.MESH_WIREFRAME
				plot_all(pyg_dev)
				pyg_dev.show()
			elif event.key == K_t:
				print("... translation")
				ctrl.trans = ~ctrl.trans
				print(ctrl.trans)
			elif event.key == K_h:
				print("... Hiddenline mode")
				tec_geom.mode = vgl.mesh3d.MESH_HIDDENLINE
				ctrl.shade = False
				tec_geom.set_shade_show(ctrl.shade)
				plot_all(pyg_dev)
				pyg_dev.show()
				
		elif event.type == pygame.MOUSEBUTTONDOWN:
			ctrl.prv_view_mode = tec_geom.mode
			ctrl.buttons = pygame.mouse.get_pressed()
			ctrl.old_pos = event.pos
			ctrl.lbutton = True
		elif event.type == pygame.MOUSEMOTION:
			ctrl.new_pos = event.pos
			ctrl.move = True
			if ctrl.buttons[0]:
				tec_geom.mode = vgl.mesh3d.MESH_WIREFRAME
				dx = ctrl.new_pos[0]-ctrl.old_pos[0]
				dy = ctrl.new_pos[1]-ctrl.old_pos[1]
				if ctrl.trans:
					print("... Trans(dx: %d, dy: %d)"%(dx,dy))
					dxx, dyy = ctrl.get_trans_amount()
					frm.translate_xy(dxx, dyy)
					pyg_dev.set_plot(frm)
				else:
					ctrl.xrotation += dy
					ctrl.yrotation += dx
					v3d.xrotation(ctrl.xrotation)
					v3d.yrotation(ctrl.yrotation)
			
			elif ctrl.buttons[2]:
				v3d.scaling(ctrl.get_scale_amount())
				print('scaling.. ', ctrl.scale)
			ctrl.old_pos = event.pos
			
		elif event.type == pygame.MOUSEBUTTONUP:
			ctrl.buttons = pygame.mouse.get_pressed()
			ctrl.lbutton = False
			if ctrl.move:
				tec_geom.create_tansform_node(v3d)
			ctrl.move = False
			tec_geom.mode = ctrl.prv_view_mode
			plot_all(pyg_dev)
			pyg_dev.show()
			#if tec_geom.mode is vgl.mesh3d.MESH_HIDDENLINE:
			#	plot_all(pyg_dev)
			#	pyg_dev.show()
			
	if ctrl.lbutton and ctrl.move:
		plot_all(pyg_dev, True)
		pyg_dev.show()

	if choice == 's':
		print('... sydney wmf')
		save_wmf()
		choice = ctrl.prv_choice		
	elif choice == 'i':
		print('... sydney jpg')
		save_cairo()
		choice = ctrl.prv_choice		

pygame.quit()
