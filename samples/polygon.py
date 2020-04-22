# ex_polygon.py
#
#	Ref: Math Adventures with Python by Peter Farell 
#
import pygame 
from pygame.locals import *
import numpy as np

from vgl import Frame, FrameManager, Data
from vgl import DevicePygame, DeviceWindowsMetafile
from vgl import drawfrm, color, symbol, geom
from vgl.device import DeviceAggdraw

data = Data(-10,10,-10,10)
fmm = FrameManager()
frm = fmm.create(0.0,0.0,4,4, data)
plist = []

def create_polygon_list():
	side = 1.7
	jump = 2.2*side
	sx = -5.6
	sy = 5.6
	j = 0
	i = 1
	y = sy
	nstart = 3 
	nend = 19
	step = 170/(nend-nstart)
	for n in range(nstart, nend, 1):
		x = sx+j*jump
		plist.append(geom.Polygon(x,y,n,side,color.BLACK,0.001,color.hsv((n-3)*step,1,1),True))
		j += 1
		if j%4==0:
			y = sy-i*jump
			j = 0
			i += 1
			
def draw_shape(dev):
	drawfrm.draw_frame(dev, dev.frm)
	drawfrm.draw_grid(dev, dev.frm.data, 1)
	drawfrm.draw_axis(dev, dev.frm.data)
	for i in range(len(plist)):
		sh = plist[i]
		dev.polygon(sh.get_xs(), sh.get_ys(), sh.lcol, sh.lthk*dev.frm.hgt(), sh.fcol)

def save_wmf(fname, frm, gbbox):
	dev_wmf = DeviceWindowsMetafile(fname, gbbox)
	dev_wmf.set_device(frm)
	draw_shape(dev_wmf)
	dev_wmf.close()
	
def save_img(fname, frm, gbox, dpi):
	dev_img = DeviceAggdraw(fname, gbox, dpi)
	dev_img.set_device(frm)
	draw_shape(dev_img)
	dev_img.close()

create_polygon_list()
running = True
choice = 1
gbbox = fmm.get_gbbox()
dev_rst = DevicePygame(gbbox, 100)

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
			
	if choice == 1:
		dev_rst.fill_white()
		dev_rst.set_plot(frm)
		draw_shape(dev_rst)
	elif choice == 's':
		print('... save wmf')
		save_wmf('polygon.wmf', frm, gbbox)
		choice = prv_choice		
	elif choice == 'i':
		print('... save img')
		save_img('polygon.png', frm, gbbox, 200)
		choice = prv_choice
	dev_rst.show()

pygame.quit()
