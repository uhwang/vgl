# circle movie
import numpy as np
import moviepy.editor as mpy
from vgl import color, geom, BBox, Frame, FrameManager, Data
from vgl import DeviceCairo, DeviceCairoAnimation

data = Data(-10,10,-10,10)
fmm = FrameManager()
frm = fmm.create(0.0,0.0,3,3, data)
gbox = fmm.get_gbbox()
duration=4
halfd=duration*0.5
fps = 30
dr = 0.1
fr = dr*fps*duration
r = 0.01

dev = DeviceCairo("===.png", gbox, 100)
dev.set_plot(frm)
#dev.close()


def circle_mov(t):
	global r, dev
	r += 0.1 if t <= halfd else -0.1
	dev.fill_white()
	dev.circle(0, 0, r, lcol=color.BLUE, lthk=0.005*frm.hgt())
	
dev_ani = DeviceCairoAnimation('circle_mov.mp4', dev, circle_mov, 4)
#dev_ani.save_video()
dev_ani.save_gif("circle_mov.gif")
