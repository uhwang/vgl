# ex_x3.py
import numpy as np
from vgl import color, geom, BBox, Frame, FrameManager, Data
from vgl import DeviceWindowsMetafile, DevicePygame, DeviceAggdraw, DeviceCairo
from vgl import drawfrm, symbol, drawtick, drawaxis, drawlabel

x = np.arange(-3,3,0.2)
y = x**3

data = Data(-3,3,-1,10)
fmm = FrameManager()
fmm.create(0,0,3,3, data)
frm = fmm.create(0,3.4,3,3, data)

dev = DeviceWindowsMetafile('x3.wmf', fmm.get_gbbox())

dev.set_device(frm)
drawfrm.draw_frame(dev, frm)
clip = dev.frm.get_clip()
dev.create_clip(clip[0],clip[1],clip[2],clip[3])
dev.polyline(x, y, color.BLUE, 0.001*frm.hgt())
dev.delete_clip()
dev.close()
