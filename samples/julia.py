from vgl import color, BBox, Frame, FrameManager, Data, symbol
from vgl import DeviceCairo
import coltbl
from math import sin, cos

data = Data(0,1,0,1)
fmm = FrameManager()
frm = fmm.create(0,0,4,4, data)

def julia(dev):
	global wid, hgt
	
	zoom = 1 
	moveX = 0 
	moveY = 0
	maxIterations = 300
	
	# pick some values for the constant c, 
	# this determines the shape of the Julia Set
	cRe = -0.7;
	cIm = 0.27015;
	
	#loop through every pixel
	for x in range(wid):
		for y in range(hgt):
			# calculate the initial real and imaginary part of z, 
			# based on the pixel location and zoom
			# and position values
			newRe = 1.5 * (x - wid / 2) / (0.5 * zoom * wid) + moveX;
			newIm = (y - hgt / 2) / (0.5 * zoom * hgt) + moveY;
			# start the iteration process
			for i in range(maxIterations):
				# remember value of previous iteration
				oldRe = newRe
				oldIm = newIm
				
				# the actual iteration, the real and imaginary part are calculated
				newRe = oldRe * oldRe - oldIm * oldIm + cRe
				newIm = 2 * oldRe * oldIm + cIm
				# if the point is outside the circle with radius 2: stop
				if (newRe * newRe + newIm * newIm) > 4:
					break
			
			# use color model conversion to get rainbow palette, 
			# make brightness black if maxIterations reached
			col = color.hsv(i % 256, 1, 1 if i < maxIterations else 0)
			dev.set_pixel(x, y, col)

def save_cairo(fname, gbox, dpi):
	global wid, hgt
	wid = int(frm.get_pdom_wid()*dpi)
	hgt = int(frm.get_pdom_hgt()*dpi)

	dev_img = DeviceCairo(fname, gbox, dpi)
	dev_img.fill_black()
	dev_img.set_plot(frm)
	julia(dev_img)
	#dev_img.set_pixel(100,100, (255,0,0))
	#dev_img.set_pixel(102,100, (0,255,0))
	#dev_img.set_pixel(104,100, (0,0,255))
	dev_img.close()
	
save_cairo("julia.png", fmm.get_gbbox(), 70)
	