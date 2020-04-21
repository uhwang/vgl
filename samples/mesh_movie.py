import vgl
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
mesh = vgl.mesh3d.SquareMesh3d(geom.shape[0], geom.shape[1])
mesh.create_node(geom)
mesh.create_mesh()
dura = 40  # pymovie: duration 40 sec
frmp = 15  # pymovie: frame per sec (low frm rate: slow, high frm rate: fast)
scal = 0.5 
trnx = (xmax-xmin)*0.005 # translation amount in x dir
trny = (ymax-ymin)*0.005 # translation amount in y dir
frmx = 5 # frame width (inch)
frmy = 5 # frame height (inch)

data = vgl.Data(xmin, xmax, ymin, ymax, zmin, zmax)
fmm = vgl.FrameManager()
frm = fmm.create(0,0,frmx,frmy,data)
v3d = vgl.view3d.View3d(frm)
v3d.scaling(scal)
gbbox = fmm.get_gbbox()

dev = vgl.DeviceCairo("", fmm.get_gbbox(), 150)
dev.set_plot(frm)
clip = frm.get_clip()
dev.create_clip(clip[0],clip[1],clip[2],clip[3])

tt = vgl.text.Text(frmx/2, 0.5)
tt.polyline = dev.lpolyline
tt.polygon = dev.lpolygon
tt.lcol = vgl.color.BLUE
tt.hs()
	
def save_wmf(fname, gbbox):
	dev = vgl.DeviceWindowsMetafile(fname, gbbox)
	dev.set_device(frm)
	clip = frm.get_clip()
	dev.create_clip(clip[0],clip[1],clip[2],clip[3])
	vgl.plot.plot_mesh(dev, v3d, mesh)
	dev.close()
	
def plot_geom(t):
	global dev, v3d, scal, gbbox
	if t <= 10:
		v3d.xrotation(t*frmp)
		v3d.yrotation(t*frmp)
		tt.str = "Save: %s"%("wireframe.wmf")
		vgl.text.write_text(dev, tt)
	elif t > 10 and t <= 20:
		v3d.yrotation((t-10)*frmp)
		v3d.xrotation((t-10)*frmp)
		mesh.hiddenline()
		tt.str = "Save: %s"%("hiddenline.wmf")
		vgl.text.write_text(dev, tt)
	elif t > 20 and t <= 25:
		scal -= 0.005
		v3d.scaling(scal)
		tt.str = "Save: %s"%("shrink.wmf")
		vgl.text.write_text(dev, tt)
	elif t > 25 and t <= 30:
		scal += 0.005
		v3d.scaling(scal)
		tt.str = "Save: %s"%("enlarge.wmf")
		vgl.text.write_text(dev, tt)
	elif t > 30 and t <= 35:
		frm.translate_xy(-trnx, -trny)
		dev.set_plot(frm)
	elif t > 35 and t <= 40:
		frm.translate_xy(trnx, trny)
		dev.set_plot(frm)
		tt.str = "Save: %s"%("translate.wmf")
		vgl.text.write_text(dev, tt)
		
	mesh.create_tansform_node(v3d)
	mesh.compute_avg_z()
	dev.fill_white()
	vgl.plot.plot_mesh(dev, v3d, mesh)
	
	if t == 10: save_wmf("wireframe.wmf" , gbbox)
	if t == 20: save_wmf("hiddenline.wmf", gbbox)
	if t == 25: save_wmf("shrink.wmf"    , gbbox)
	if t == 30: save_wmf("enlarge.wmf"   , gbbox)
	if t == 40: save_wmf("translate.wmf" , gbbox)
	
dev1 = vgl.DeviceCairoAnimation('3dgeom.mp4', dev, plot_geom, duration=dura, fps=frmp)
dev1.save_video()
#dev1.save_gif('3dgeom.gif')

