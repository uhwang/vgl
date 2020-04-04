from vgl import color, BBox, Frame, FrameManager, Data, symbol
from vgl import DeviceWindowsMetafile, DeviceCairo, DeviceCairoAnimation
import coltbl
from math import sin, cos
import random
from moviepy.editor import *

xwid,xhgt=300,300
data = Data(0,xwid,0,xhgt)
fmm = FrameManager()
frm_x2 = fmm.create(0,0,4,4, data)
clips = []

def rand_tree(dev, order, length, angle):
	global posx, posy, ctbl, dlength, prv_posx, prv_posy, dev_ani, movie
	
	dx = length*sin(angle);
	dy = length*cos(angle);
	scale = random.random()
	turnl = random.random()
	turnr = random.random()
	
	prv_posx = posx
	prv_posy = posy
	
	posx -= dx;
	posy += dy;
	
	dev.line(prv_posx, prv_posy, posx, posy, ctbl[int(length-1)], length*dlength*0.04*dev.frm.hgt())
	
	if length <= 10:
		col = color.hsv(0, scale, 1)
		fruit = symbol.Circle(scale*0.01, dev.frm.hgt(), 0.001)
		fruit.set_color(col,col)
		dev.begin_symbol(fruit)
		dev.symbol(posx, posy, fruit)
		dev.end_symbol()

	if movie:
		#print("append img")
		#clips.append(ImageClip(dev_ani.get_image()).set_duration(1))
		clips.append(ImageClip(dev_ani.get_image()).set_duration(0.1))
	
	if order > 0:
		rand_tree(dev, order - 1, length*0.8, angle + turnl)
		rand_tree(dev, order - 1, length*0.8, angle - turnr)
		
	posx += dx;
	posy -= dy;

def run_rand_tree(dev):
	global posx, posy, order, length, ctbl, dlength, prv_posx, prv_posy
	
	order = 9
	length = 60
	dlength = 1./(length-1)*0.5;

	ctbl = coltbl.create_color_table(0,240, 0.8, 1, length)
	posx = xwid/2;
	posy = 0;
	dlength = 1./(length-1)*0.5;

	prv_posx = posx
	prv_posy = posy
	rand_tree(dev, order, length, 0);
	dev.stroke()

def save_wmf(fname, gbbox):
	global movie
	movie = False
	dev_wmf = DeviceWindowsMetafile(fname, gbbox)
	dev_wmf.set_device(frm_x2)
	run_rand_tree(dev_wmf)
	dev_wmf.close()
	
def save_cairo(fname, gbox, dpi):
	global dev_ani, movie
	movie = False
	dev_img = DeviceCairo(fname, gbox, dpi)
	dev_img.fill_black()
	dev_img.set_plot(frm_x2)
	run_rand_tree(dev_img)
	if movie:
		print(len(clips))
		dev_ani = DeviceCairoAnimation("ftree2.mp4", dev_img, 0,0)
		video = concatenate_videoclips(clips, method='compose')
		#video.write_videofile("ftree01.mp4", fps=30)
		video.write_gif("ftree2.gif", fps=30)
	dev_img.close()
	
save_wmf("ftree2.wmf", fmm.get_gbbox())
save_cairo("ftree2.png", fmm.get_gbbox(), 100)