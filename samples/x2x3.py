# ex plot x**2, x**3

import pygame 
from pygame.locals import *
import numpy as np

from vgl import color, geom, BBox, Frame, FrameManager, Data
from vgl import DeviceWindowsMetafile, DevicePygame, DeviceAggdraw, DeviceCairo
from vgl import drawfrm, symbol, drawtick, drawaxis, drawlabel

x = np.arange(-3,3.2,0.2)
y2 = x**2
#y3 = x**2+3*np.sin(x)
y3 = x**3

data = Data(-6,6,-2,10)
fmm = FrameManager()
frm_x2 = fmm.create(0.0,0.0,3,3, data)
frm_x3 = fmm.create(3.2,3.4,3,3, data)
frm_x4 = fmm.create(0.0,3.2,3,2, Data(-4,4,-3,3))

def plot_x2(dev):
	drawaxis.draw_axis(dev)
	drawtick.draw_tick_2d(dev)	
	drawlabel.draw_label_2d(dev)
	dev.polyline(x, y2, color.BLUE, 0.003*dev.frm.hgt())
	sym = symbol.Circle(0.01, dev.frm.hgt())
	dev.begin_symbol(sym)
	for i in range(0,x.size): dev.symbol(x[i],y2[i],sym)
	dev.end_symbol()
	
def plot_x3(dev):
	drawaxis.draw_axis(dev)
	drawtick.draw_tick_2d(dev)	
	drawlabel.draw_label_2d(dev)
	clip = dev.frm.get_clip()
	dev.create_clip(clip[0],clip[1],clip[2],clip[3])
	dev.polyline(x, y3, color.BLUE, 0.003*dev.frm.hgt())
	
	sym = symbol.Gradient(0.03, dev.frm.hgt())
	sym.set_fcolor(color.CUSTOM5)
	dev.begin_symbol(sym)
	for i in range(0,x.size): dev.symbol(x[i],y3[i],sym)
	dev.end_symbol()
	dev.delete_clip()
	
def plot_square(dev):
	drawaxis.draw_axis(dev)
	drawtick.draw_tick_2d(dev)	
	drawlabel.draw_label_2d(dev)
	N = 7
	npnt = 101
	fx1 = 0
	PI = 3.1415926535
	dpi = 2*np.pi/(npnt-1)
	invpi = 2/np.pi
	x = np.arange(-np.pi, np.pi+dpi, dpi)
	y = np.zeros(npnt)
	
	for i in range(npnt):
		fx1 = 0
		for n in range(1, N):
			fx1 += (1 - np.cos(n*PI))*np.sin(n*x[i])/n
		y[i] = invpi*fx1
	
	dev.polyline(x, y*2, color.MAGENTA, 0.006*dev.frm.hgt())

def plot_all(dev):
	dev.set_device(frm_x2)
	drawfrm.draw_frame(dev, frm_x2)
	drawfrm.draw_axis(dev, data)
	drawfrm.draw_grid(dev, data, 1)
	plot_x2(dev)
	
	dev.set_device(frm_x3)
	drawfrm.draw_frame(dev, frm_x3)
	drawfrm.draw_axis(dev, data)
	drawfrm.draw_grid(dev, data, 1)
	plot_x3(dev)
	
	dev.set_device(frm_x4)
	drawfrm.draw_frame(dev, frm_x4)
	drawfrm.draw_axis(dev, frm_x4.data)
	drawfrm.draw_grid(dev, frm_x4.data, 1)
	plot_square(dev)
	

def save_img(fname, gbox, dpi):
	dev_img = DeviceCairo(fname, gbox, dpi)
	dev_img.fill_white()
	plot_all(dev_img)
	dev_img.close()
	
def save_wmf(fname, gbbox):
	dev_wmf = DeviceWindowsMetafile(fname, gbox)
	plot_all(dev_wmf)
	dev_wmf.close()

running = True
drawable = True
choice = 1
gbox = fmm.get_gbbox()
dev_rst = DevicePygame(gbox, 72)

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
			elif event.key == K_i:
				prv_choice = choice
				choice='i'
			elif event.key == K_s:
				prv_choice = choice
				choice='s'
			
	if choice == 1:	
		if drawable:
			dev_rst.fill_white()
			plot_all(dev_rst)
			drawable=False
	elif choice == 's':
		print('... save wmf')
		save_wmf('x2x3.wmf',gbox)
		choice = prv_choice		
	elif choice == 'i':
		print('... save img')
		save_img('x2x3.png',gbox, 200)
		choice = prv_choice		
	dev_rst.show()

pygame.quit()
		
#def main():
#	save_wmf()
#	
#if __name__ == '__main__':
#	main()