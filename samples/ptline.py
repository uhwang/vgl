import numpy as np

from vgl import color, BBox, Frame, FrameManager, Data
from vgl import DeviceWindowsMetafile, DeviceCairo
from vgl import patline
#from vgl import drawfrm, symbol, drawtick, drawaxis, drawlabel
	
def test(dev):		

	x = np.arange(-3,3.2,0.2)
	y2 = x**2
	pnts = [(x[i], y2[i]) for i in range(len(x))]
	pat_line = patline.get_pattern_line(pnts, 0.05*dev.frm.hgt(), patline.VGL_DASHED)
	
	for ps in pat_line:
		x = (ps[i][0] for i in range(len(ps)))
		y = (ps[i][1] for i in range(len(ps)))
		dev.polyline(x,y,color.BLUE, dev.frm.hgt()*0.1)
		
def main():

	data = Data(-3,3,-1,10)
	fmm = FrameManager()
	frm_x2 = fmm.create(0.0,0.0,2,4, data)
	
	gbbox = fmm.get_gbbox()
	
	dev_wmf = DeviceWindowsMetafile("patlin.wmf", gbbox)
	dev_wmf.set_device(frm_x2)
	test(dev_wmf)
	dev_wmf.close()
	
	dev_img = DeviceCairo("patlin.png", gbbox, dpi)
	dev_img.fill_white()
	dev_img.set_plot(frm_x2)
	test(dev_img)
	dev_img.close()
			
if __name__ == '__main__':
	main()
