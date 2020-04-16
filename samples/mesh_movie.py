from vgl import color, geom, BBox, Frame, FrameManager, Data
from vgl import DeviceWindowsMetafile, DeviceCairo, DeviceCairoAnimation
from vgl import view3d, mesh3d, plot
import numpy as np
import cylinder

jpan = 15
ipan = 10
zmin = -0.4
zmax = 0.4
geom = cylinder.create_cylinder(0.5, jpan, ipan, zmin, zmax)

xmin = np.min(geom[:,:,0])
xmax = np.max(geom[:,:,0])
ymin = np.min(geom[:,:,1])
ymax = np.max(geom[:,:,1])
mesh = mesh3d.SquareMesh3d(geom.shape[0], geom.shape[1])
mesh.create_node(geom)
mesh.create_mesh()
dura = 40
frmp = 15
scal = 0.5
trnx = (xmax-xmin)*0.005
trny = (ymax-ymin)*0.005

def plot_geom(t):
	global dev, v3d, scal
	if t <= 10:
		v3d.xrotation(t*frmp)
		v3d.yrotation(t*frmp)
	elif t > 10 and t <= 20:
		v3d.yrotation((t-10)*frmp)
		v3d.xrotation((t-10)*frmp)
		mesh.mode = mesh3d.MESH_HIDDENLINE
	elif t > 20 and t <= 25:
		scal -= 0.005
		v3d.scaling(scal)
	elif t > 25 and t <= 30:
		scal += 0.005
		v3d.scaling(scal)
	elif t > 30 and t <= 35:
		frm.translate_xy(-trnx, -trny)
		dev.set_plot(frm)
	elif t > 35 and t <= 40:
		frm.translate_xy(trnx, trny)
		dev.set_plot(frm)
		
	mesh.create_tansform_node(v3d)
	mesh.compute_ave_z()
	dev.fill_white()
	plot.plot_mesh(dev, mesh, mesh)
	
data = Data(xmin, xmax, ymin, ymax, zmin, zmax)
fmm = FrameManager()
frm = fmm.create(0,0,5,5,data)
v3d  = view3d.View3d(frm)
v3d.scaling(scal)

dev = DeviceCairo("", fmm.get_gbbox(), 150)
dev.set_plot(frm)
clip = frm.get_clip()
dev.create_clip(clip[0],clip[1],clip[2],clip[3])

dev1 = DeviceCairoAnimation('3dgeom.mp4', dev, plot_geom, duration=dura, fps=frmp)
dev1.save_video()

