# square01.py
#
#  bn = 4k/npi, n is odd
#  b1 = 4k/pi
#  b3 = 4k/3pi
#  b5 = 4k/5pi
#
#  f(x) = 4k/pi [sin(x) + 1/3 sin(3x) + 1/5 sin(5x) + ... ]
#

import pygame 
from pygame.locals import *
import numpy as np
from vgl import device, data, frame, color, text

data = data.Data(-8,21,-10,10)
fmm = frame.FrameManager()
frm = fmm.create(0,0,7,5, data)
gbox = fmm.get_gbbox()

nn = [1]
k  = 4
coef = 4*k/np.pi
dtheta = 0.05
theta = 0
r3 = 0.1
r4 = r3*0.25
sint_trail_xpos = 8
sine_trail=[]
sine_plot_range= 11
max_sine_freq=1 # 2 Hz
max_theta = 2*np.pi*max_sine_freq
max_sine_points=int(max_theta/dtheta)
sine_plot_xratio = float(sine_plot_range)/float(max_sine_points)
sine_track_list = [[0]]
circle_point = []
final_wave=[]
#tt = text.Text(3.5, 2.5)
tt = text.Text(3.5, 4.7)
tt.lthk = 0.005
tt.lcol = color.BLUE
tt.hn()

color_list = [
	color.CUSTOM1 ,	color.CUSTOM2 ,	color.CUSTOM3 ,	
	color.CUSTOM4 ,	color.CUSTOM5 , color.RED     ,	
	color.GREEN   ,	color.BLUE    ,	color.YELLOW  ,	
	color.MAGENTA ,	color.CYAN    ,	color.PURPLE  
]

def draw_grid(dev):
	data = dev.frm.data
	dev.make_pen(color.GRAY20, 0.001*dev.frm.hgt())
	for i in range(data.xmin, data.xmax+1):
		dev.line(i, data.ymin, i, data.ymax)
	for i in range(data.ymin, data.ymax+1):
		dev.line(data.xmin, i, data.xmax, i)
	dev.delete_pen()
			
def square_wave(t):
	global dev, theta, sine_track_list, final_wave, duration
	thk=0.003*dev.frm.hgt()
	thk1=thk*4
	dev.fill_white()
	draw_grid(dev)
	
	x0 = 0
	y0 = 0
	yy = 0
	tx = 0
	ty = 0
	
	if t > 0:
		if t in duration:
			nn.append(nn[-1]+2)
			sine_track_list.append([0])
		
	for i, n in enumerate(nn):
		amp = coef/n
		x1 = amp*np.cos(theta*n)
		y1 = amp*np.sin(theta*n)
		dev.line(tx,ty,tx+x1,ty+y1,color_list[i%len(color_list)], thk1-i*thk1*0.1)
		sine_track_list[i] = [y1]+sine_track_list[i][:max_sine_points]
		yy += y1
		tx += x1
		ty += y1
		
	final_wave = [yy]+final_wave[:max_sine_points]
	dev.line(tx, ty, sint_trail_xpos, yy, lcol=color.BLACK, lthk=thk)

	#plot lines
	for i, pnts in enumerate(sine_track_list):
		x3 = [j*sine_plot_xratio+sint_trail_xpos for j in range(len(pnts))]
		dev.polyline(x3, pnts, lcol=color_list[i%len(color_list)], lthk=thk)

	npnts = len(final_wave)
	if npnts > 1:
		x3 = [j*sine_plot_xratio+sint_trail_xpos for j in range(npnts)]
		dev.polyline(x3, final_wave, lcol=color.GRAY50, lthk=thk)
		
	# plot points
	#for i, pnts in enumerate(sine_track_list):
	#	for j, p in enumerate(pnts):
	#		x3 = sint_trail_xpos+j*sine_plot_xratio
	#		#dev.circle(x3,p,r4,fcol=color.BLACK)
	#		dev.circle(x3,p,r4,fcol=color_list[i%len(color_list)])
	#
	#for i,p in enumerate(final_wave):
	#	x3 = sint_trail_xpos+i*sine_plot_xratio
	#	deg = int(i/max_sine_points*350.0)
	#	dev.circle(x3,p,r3,fcol=color.hsv(deg,1,1))

	tt.polyline = dev.lpolyline
	tt.polygon = dev.lpolygon
	tt.str = 'n = %d'%len(nn)
	text.write_text(dev, tt)
	
	theta += dtheta

def save_cairo(fname, frm, gbox, dpi):
	global dev
	dev_img = device.DeviceCairo(fname, gbox, dpi)
	dev_img.set_plot(frm)
	old_dev = dev
	dev = dev_img
	square_wave(-1)
	dev_img.close()
	dev = old_dev
	
def save_wmf(fname, frm, gbbox):
	global dev
	dev_wmf = device.DeviceWindowsMetafile(fname, gbox)
	dev_wmf.set_plot(frm)
	old_dev = dev
	dev = dev_wmf
	square_wave(-1)
	dev_wmf.close()
	dev = old_dev

def save_movie(fname):
	global dev, duration, nn
	dur = 30
	nnn = nn[:]
	nn = [1]
	old_dev = dev
	dev_img = device.DeviceCairo("", gbox, 90)
	dev_img.set_plot(frm)
	dev = dev_img
	duration = list(range(3,dur+1,3))
	dev_mov = device.DeviceCairoAnimation(fname, dev_img, square_wave, dur)
	dev_mov.save_video()
	#dev_mov.save_gif("square01.gif")
	nn = nnn[:]
	dev = old_dev
	
running = True
choice = 1
dev_rst = device.DevicePygame(fmm.get_gbbox(), 100)
dev = dev_rst

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
			elif event.key == K_m:
				prv_choice = choice
				choice='m'
			elif event.key == K_c:
				prv_choice = choice
				choice='c'
			elif event.key == K_UP:
				nn.append(nn[-1]+2)
				sine_track_list.append([0])
				print(nn)
			elif event.key == K_DOWN:
				if len(nn) > 1:
					nn.pop()
					sine_track_list.pop()
					print(nn)
			elif event.key == K_LEFT:
				r3 += 0.2
				if r3 <= 0: r3 = 0
				print("Radius = %3.3f"%r3)
			
			elif event.key == K_RIGHT:
				r3 -= 0.2
				if r3 <= 0: r3 = 0
				print("Radius = %3.3f"%r3)
			
	if choice == 1:
		dev_rst.fill_white()
		dev_rst.set_plot(frm)
		square_wave(-1)
	elif choice == 's':
		print('... save wmf')
		save_wmf('square01.wmf', frm, gbox)
		choice = prv_choice		
	elif choice == 'c':
		print('... save img')
		save_cairo('square01.png', frm, gbox, 200)
		choice = prv_choice
	elif choice == 'm':
		print('... save movie')
		save_movie('square01.mp4')
		choice = prv_choice
	dev_rst.show()

pygame.quit()