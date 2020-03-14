import pygame 
from pygame.locals import *
import numpy as np
import moviepy.editor as mpy

from vgl import color, geom, BBox, Frame, FrameManager, Data
from vgl import DeviceCairo, DeviceCairoAnimation
from vgl import drawfrm, symbol

dtheta = 0.05
theta = 0
r1 = 3
r2 = 0.2
sint_trail_xpos = 4
sine_trail=[]
sine_plot_range= 8
max_sine_freq=1 # 2 Hz
max_theta = 2*np.pi*max_sine_freq
max_sine_points=int(max_theta/dtheta)
sine_plot_xratio = float(sine_plot_range)/float(max_sine_points)

data = Data(-5,15,-10,10)
fmm = FrameManager()
frm = fmm.create(0.0,0.0,5,5, data)
gbox = fmm.get_gbbox()
sym = symbol.Gradient(0.04, frm.hgt())

def sine_wave(t):
	global theta, sine_trail, sine_plot_xratio, max_sine_points, dev
	
	dev.fill_white()
	drawfrm.draw_frame(dev,frm)
	drawfrm.draw_axis(dev, data)
	drawfrm.draw_grid(dev, data, 1)

	thk=0.001*dev.frm.hgt()
	x1 = r1*np.cos(theta)
	y1 = r1*np.sin(theta)
	dev.circle(0, 0, r1, lcol=color.BLACK, lthk=thk)
	rr2=6
	rr3=5
	dev.circle(x1, y1, r2, fcol=color.BLACK)

	x2 = sint_trail_xpos
	y2 = y1
	sine_trail = [y2]+sine_trail[:max_sine_points]
	
	for i,p in enumerate(sine_trail):
		x3 = sint_trail_xpos+i*sine_plot_xratio
		deg = int(i/max_sine_points*350.0)
		#sym.set_color_all(color.hsv(deg,1,1))
		#dev.symbol(x3,p,sym,True)
		dev.circle(x3,p,r2,fcol=color.hsv(deg,1,1))
	dev.circle(x2, y2, r2, fcol=color.BLACK)
	dev.line(x1, y1,x2, y2, color.BLUE, lthk=thk)
	theta += dtheta
	
circle_npnt = 50
dtheta = 0.05
theta = 0
running = True
choice = 1

dev = DeviceCairo("===.png", gbox, 100)
dev.set_plot(frm)
#dev.close()

dev_ani = DeviceCairoAnimation('sinmov.mp4', dev, sine_wave, 10)
dev_ani.save_video()
dev_ani.save_gif("sinmov.gif")

	
	
	