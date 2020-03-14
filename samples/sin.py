import pygame 
from pygame.locals import *
import numpy as np

from vgl import color, geom, BBox, Frame, FrameManager, Data
from vgl import DeviceWindowsMetafile, DevicePygame, DeviceAggdraw, DeviceCairo
from vgl import drawfrm, symbol

dtheta = 0.05
theta = 0
r1 = 3
r2 = 0.2
r3 = 0.2
sint_trail_xpos = 4
sine_trail=[]
sine_plot_range= 8
max_sine_freq=2 # 2 Hz
max_theta = 2*np.pi*max_sine_freq
max_sine_points=int(max_theta/dtheta)
sine_plot_xratio = float(sine_plot_range)/float(max_sine_points)

data = Data(-5,15,-10,10)
fmm = FrameManager()
frm = fmm.create(0.0,0.0,5,5, data)
gbox = fmm.get_gbbox()
sym = symbol.Gradient(0.04, frm.hgt())


def sine_wave(dev):
	global theta, sine_trail, sine_plot_xratio, max_sine_points
	
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
		dev.circle(x3,p,r3,fcol=color.hsv(deg,1,1))
	dev.circle(x2, y2, r2, fcol=color.BLACK)
	dev.line(x1, y1,x2, y2, color.BLUE, lthk=thk)
	theta += dtheta
	
def run_sin_wave(dev):
	drawfrm.draw_frame(dev,dev.frm)
	drawfrm.draw_axis(dev, data)
	drawfrm.draw_grid(dev, data, 1)
	sine_wave(dev)
	
def save_img(fname, frm, gbox, dpi):
	dev_img = DeviceAggdraw(fname, gbox, dpi)
	dev_img.set_plot(frm)
	run_sin_wave(dev_img)
	dev_img.close()

def save_cairo(fname, frm, gbox, dpi):
	dev_img = DeviceCairo(fname, gbox, dpi)
	dev_img.set_plot(frm)
	run_sin_wave(dev_img)
	dev_img.close()
	
def save_wmf(fname, frm, gbbox):
	dev_wmf = DeviceWindowsMetafile(fname, gbox)
	dev_wmf.set_plot(frm)
	run_sin_wave(dev_wmf)
	dev_wmf.close()

circle_npnt = 50
dtheta = 0.05
theta = 0
running = True
choice = 1
dev_rst = DevicePygame(fmm.get_gbbox(), 150)

while running:
	dt = dev_rst.get_tick()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == K_ESCAPE:
				running = False
			elif event.key == K_1:
				choice=1
			elif event.key == K_s:
				prv_choice = choice
				choice='s'
			elif event.key == K_i:
				prv_choice = choice
				choice='i'
			elif event.key == K_c:
				prv_choice = choice
				choice='c'
			elif event.key == K_UP:
				r3 += 0.2
				print("Radius = %3.3f"%r3)
			elif event.key == K_DOWN:
				r3 -= 0.2
				if r3 <= 0: r3 = 0
				print("Radius = %3.3f"%r3)
			
	if choice == 1:
		dev_rst.fill_white()
		dev_rst.set_plot(frm)
		run_sin_wave(dev_rst)
	elif choice == 's':
		print('... save wmf')
		save_wmf('sin.wmf', frm, gbox)
		choice = prv_choice		
	elif choice == 'i':
		print('... save img')
		save_img('sin_agg.png', frm, gbox, 200)
		choice = prv_choice
	elif choice == 'c':
		print('... save img')
		save_cairo('sin_cairo.png', frm, gbox, 200)
		choice = prv_choice
	dev_rst.show()

pygame.quit()
		

		