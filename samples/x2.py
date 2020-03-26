# ex_x2.py
import numpy as np

from vgl import color, geom, BBox, Frame, FrameManager, Data
from vgl import DeviceWindowsMetafile, DeviceAggdraw, DeviceCairo
from vgl import drawfrm, symbol, drawtick, drawaxis, drawlabel


x = np.arange(-3,3.2,0.2)
y2 = x**2

data = Data(-3,3,-1,10)
fmm = FrameManager()
frm_x2 = fmm.create(0.0,0.0,2,4, data)

def plot_x2(dev):
	drawaxis.draw_axis(dev)
	drawtick.draw_tick_2d(dev)	
	drawlabel.draw_label_2d(dev)
	dev.polyline(x, y2, color.BLUE, 0.001*dev.frm.hgt())
	sym = symbol.Circle(0.01, dev.frm.hgt(), 0.003)
	#sym = symbol.RightTriangle(0.02, dev.frm.hgt(), 0.005)
	#sym = symbol.LeftTriangle(0.02, dev.frm.hgt(), 0.005)
	#sym = symbol.Diamond(0.02, dev.frm.hgt(), 0.005)
	#sym = symbol.Square(0.02, dev.frm.hgt(), 0.005)
	dev.begin_symbol(sym)
	for i in range(0,x.size): dev.symbol(x[i],y2[i],sym)
	dev.end_symbol()

def save_wmf(fname, gbbox):
	dev_wmf = DeviceWindowsMetafile(fname, gbbox)
	dev_wmf.set_device(frm_x2)
	plot_x2(dev_wmf)
	dev_wmf.close()
	
def save_img(fname, gbox, dpi):
	dev_img = DeviceAggdraw(fname, gbox, dpi)
	dev_img.set_device(frm_x2)
	plot_x2(dev_img)
	dev_img.close()
	
def save_cairo(fname, gbox, dpi):
	dev_img = DeviceCairo(fname, gbox, dpi)
	dev_img.fill_white()
	dev_img.set_plot(frm_x2)
	plot_x2(dev_img)
	dev_img.close()
	
save_cairo('x2_cairo.png', fmm.get_gbbox(), 150)
save_img('x2.png', fmm.get_gbbox(), 150)
save_wmf('x2.wmf', fmm.get_gbbox())