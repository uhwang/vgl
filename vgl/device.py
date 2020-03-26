# Vector Graphic Library (VGL) for Python
#
# device.py
#
# 2020-2-12 Ver 0.1
# 2020-2-19 Cairo deivce added
#
# Author: Uisang Hwang
# Email : uhwangtx@gmail.com
#
 
import numpy as np
import pygame 
from PIL import Image
import moviepy.editor as mpy

import aggdraw
import vgl.devwmf as dw
import vgl.color as color
import vgl.geom as geom
from vgl.size import BBox, Rect
from vgl.data import Data
import math
import cairo

two_pi = 2*math.pi

get_line_thk = lambda x : 1 if int(x) == 0 else x

class Pen():
	def __init__(self):
		self.color = 0
		self.thk = 0
		
	def set_pen(self, color, thk):
		self.color = color
		self.thk =thk

class DeviceVector():
	def __init__(self, gbox):
		self.gbox =gbox
		self.xscl = 0
		self.yscl = 0
		self.scal = 0
		
	def set_plot(self, frm):
		self.frm = frm
		wid          = frm.pdom.get_wid()
		hgt          = frm.pdom.get_hgt()
		self.xscl    = wid/(frm.data.xmax-frm.data.xmin)
		self.yscl    = hgt/(frm.data.ymax-frm.data.ymin)
		self.sx_plot = frm.bbox.sx+frm.pdom.sx
		self.sy_plot = frm.bbox.ey-frm.pdom.sy
		self.ref_y   = frm.bbox.sy+frm.pdom.sy
		self.scal    = self.xscl if self.xscl < self.yscl else self.yscl
		
	def wtol_x(self, x): return self.get_x(x)
	def wtol_y(self, y): return self.get_y(y)
	
	def get_x(self, x):
		return self.sx_plot+(x-self.frm.data.xmin)*self.scal
		
	def get_y(self, y):
		return self.sy_plot-(y-self.frm.data.ymin)*self.scal
		
	def get_ly(self, y):
		return self.ref_y+(y-self.frm.data.ymin)*self.scal
		
class DeviceWindowsMetafile(DeviceVector):
	def __init__(self, fname, gbox):
		super().__init__(gbox)
		self.dev = dw.WindowsMetaFile(fname, gbox)
		self.pen = Pen()
		
	def set_device(self, frm):
		self.frm = frm
		self.set_plot(frm)
		
	def fill_white(self):
		return
		
	def make_pen(self, color, thk):
		self.pen.color = color
		self.pen.thk = thk
		self.dev.MakePen(color, thk)
		
	def delete_pen(self):
		self.dev.DeletePen()
		
	def line(self, sx, sy, ex, ey, lcol=0, lthk=0):
		x1 = self.get_x(sx)
		y1 = self.get_y(sy)
		x2 = self.get_x(ex)
		y2 = self.get_y(ey)
		self.dev.Line(x1, y1, x2, y2, lcol, lthk)

	def stroke(self):
		return
		
	def moveto(self, x, y):
		self.dev.MoveTo(self.get_x(x),self.get_y(y))
		
	def lineto(self, x, y):
		self.dev.LineTo(self.get_x(x),self.get_y(y))
		
	def polygon(self, x, y, lcol, fcol, lthk):
		px=[self.get_x(x[i]) for i in range(len(x))]
		py=[self.get_y(y[i]) for i in range(len(y))]
		self.dev.Polygon(px,py,lcol,fcol,lthk)
		
	def begin_symbol(self, sym):
		self.dev.MakePen(sym.lcol, sym.lthk)
		self.dev.MakeBrush(sym.fcol)
		
	def end_symbol(self):
		self.dev.DeletePen()
		self.dev.DeleteBrush()
		
	def symbol(self, x,y,sym,draw=False):
		cx = self.get_x(x)
		cy = self.get_y(y)
		px, py = sym.update_xy(cx,cy)
		if draw: self.begin_symbol(sym)
		self.dev.Symbol(px,py)
		if draw: self.end_symbol()
	
	def circle(self, x,y, rad, lcol=0, lthk=0, fcol=0):
		if lcol == 0: self.dev.MakePen(fcol, lthk)
		else        : self.dev.MakePen(lcol, lthk)
		if fcol != 0: self.dev.MakeBrush(fcol)
		else        : self.dev.MakeNullBrush()
		x1 = self.get_x(x-rad)
		y1 = self.get_y(y-rad)
		x2 = self.get_x(x+rad)
		y2 = self.get_y(y+rad)
		self.dev.Circle(x1,y1,x2,y2)
		self.dev.DeletePen()
		self.dev.DeleteBrush()
		
	def polyline(self, x, y, lcol=0, lthk=0,closed=False):
		if lcol != 0: self.dev.MakePen(lcol, lthk)
		px=[self.get_x(x[i]) for i in range(len(x))]
		py=[self.get_y(y[i]) for i in range(len(y))]
		self.dev.Polyline(px,py,closed)
		if lcol != 0: self.dev.DeletePen()
		
	def lline(self, x1, y1, x2, y2, color=0, lthk=0):
		if color != 0: self.dev.MakePen(color,lthk)
		self.dev.MoveTo(x1,y1)
		self.dev.LineTo(x2,y2)
		if color != 0: self.dev.DeletePen()

	def lmoveto(self, x, y):
		self.dev.MoveTo(x,y)
		
	def llineto(self, x, y):
		self.dev.LineTo(x,y)
		
	def lpolygon(self, x, y, lcol, fcol, lthk=0):
		self.dev.Polygon(x,y,lcol,fcol,lthk)
		
	def lpolyline(self, x, y, lcol=0, lthk=0, closed=False):
		if lcol != 0: self.dev.MakePen(lcol, lthk)
		self.dev.Polyline(x, y, closed)
		if lcol != 0: self.dev.DeletePen()
		
	def create_clip(self, sx, sy, ex, ey):
		self.dev.CreateClip(sx, sy, ex, ey)
	def delete_clip(self):
		self.dev.DeleteClip(0)
		
	def close(self):
		self.dev.CloseMetafile()

class Position():
	def __init__(self, x, y):
		self.set(x,y)
	
	def set(self, x, y):
		self.x = x
		self.y = y
		
class DeviceRaster():
	def __init__(self, gbox, dpi):
		self.dpi  = dpi
		self.gwid = int(gbox.wid()*dpi)
		self.ghgt = int(gbox.hgt()*dpi)
		self.lscl = float(self.gwid/gbox.wid())
		
	def set_plot(self, frm):
		self.frm = frm
		xrange = frm.data.get_xrange()
		yrange = frm.data.get_yrange()
		
		# logical 
		self.sx_wtol = frm.bbox.sx+frm.pdom.sx
		self.sy_wtol = frm.bbox.sy+frm.pdom.sy
		
		self.sx_ltop = (frm.bbox.sx+frm.pdom.sx)*self.dpi
		self.sy_ltop = (frm.bbox.sy+frm.pdom.sy)*self.dpi
		self.hgt     = self.frm.pdom.hgt*self.dpi
		
		xscl = (frm.pdom.wid*self.dpi)/xrange
		yscl = (frm.pdom.hgt*self.dpi)/yrange
		self.scal = min(xscl, yscl)
		
		wtolx = frm.pdom.wid/xrange
		wtoly = frm.pdom.hgt/yrange
		self.wtol = min(wtolx,wtoly)
		
		self.ref_wtol_y = self.sy_wtol+self.frm.pdom.hgt
		self.ref_y      = self.sy_ltop+self.hgt

	def wtol_x(self, x): return self.sx_wtol+self.wtol*(x-self.frm.data.xmin)
	def wtol_y(self, y): return self.ref_wtol_y-self.wtol*(y-self.frm.data.ymin)
	def get_xl(self, x): return x*self.lscl
	def get_yl(self, y): return y*self.lscl
	def get_x (self, x): return self.sx_ltop+(x-self.frm.data.xmin)*self.scal	
	def get_y (self, y): return self.ref_y-(y-self.frm.data.ymin)*self.scal
	def get_v (self, v): return v*self.scal
	def size  (self   ): return (self.gwid, self.ghgt)
		
class DevicePygame(DeviceRaster):
	def __init__(self, gbox, dpi, fps=30):
		super().__init__(gbox, dpi)
		self.name = "DevicePygame"
		pygame.init()
		self.screen = pygame.display.set_mode((self.gwid, self.ghgt))
		self.clock = pygame.time.Clock()
		self.fps = fps
		self.pen = Pen()
		self.pos = Position(0,0)
		
	def set_device(self, frm):
		self.set_plot(frm)
		return

	def get_tick(self):
		return self.clock.tick(self.fps)/1000

	def fill_black(self):
		self.screen.fill(color.BLACK)

	def fill_white(self):
		self.screen.fill(color.WHITE)

	def fill_cyan(self):
		self.screen.fill(color.CYAN)

	def show(self):
		pygame.display.update()

	def make_pen(self, color, lthk):
		self.pen.set_pen(color, self.get_xl(lthk))
		
	def delete_pen(self):
		return
		
	def line(self, sx, sy, ex, ey, lcol=0, lthk=0):
		if lcol!=0:
			self.make_pen(lcol, lthk)
			self.moveto(sx,sy)
		pygame.draw.line(self.screen, self.pen.color, 
			(self.get_x(sx), self.get_y(sy)),
			(self.get_x(ex), self.get_y(ey)), math.ceil(self.pen.thk))
		
	def stroke(self):
		return
		
	def moveto(self, x, y):
		self.pos.set(x,y)
		
	def lineto(self, x, y):
		pygame.draw.line(self.screen, self.pen.color, 
			(self.get_x(self.pos.x),
			 self.get_y(self.pos.y)),
			(self.get_x(x),
			 self.get_y(y)), math.ceil(self.pen.thk))
		self.pos.set(x,y)
		
	def polygon(self, x, y, lcol=0, fcol=0, lthk=0):
		pnt = [(self.get_x(x[i]),
		        self.get_y(y[i])) for i in range(len(x))]
		if lcol != 0:
			self.make_pen(lcol, lthk)
			
		pygame.draw.polygon(self.screen, fcol, pnt)
		if lcol!= fcol: 
			pygame.draw.polygon(self.screen, self.pen.color, pnt, math.ceil(self.pen.thk))

	def polyline(self, x, y, lcol=0, lthk=0, closed=False):
		pnt = [(self.get_x(x[i]),
		        self.get_y(y[i])) for i in range(len(x))]
		if lcol!=0:
			self.make_pen(lcol, lthk)
		pygame.draw.lines(self.screen, self.pen.color, closed, pnt, math.ceil(self.pen.thk))
		
	def begin(self,lcol,lthk,fcol): return
	def end(self): return
	
	def begin_symbol(self, sym): return
	def end_symbol(self): return
	def create_clip(self, x1, y1, x2, y2):
		self.screen.set_clip(
		pygame.Rect(self.get_xl(x1),
		            self.get_yl(y1),
					self.get_xl(x2-x1),
					self.get_yl(y2-y1)))
	def delete_clip(self):
		self.screen.set_clip(None)
	
	def circle(self, x,y, rad, lcol=0, lthk=0, fcol=0):
		xx = int(self.get_x(x))
		yy = int(self.get_y(y))
		rrad = int(rad*self.scal)
		lthk = int(get_line_thk(lthk*self.lscl))
		if fcol!=0: pygame.draw.circle(self.screen, fcol, (xx,yy), rrad)
		if lcol!=0: pygame.draw.circle(self.screen, lcol, (xx,yy), rrad, lthk)
		
	def symbol(self, x,y, sym, draw=False):
		px, py = sym.update_xy(self.wtol_x(x),self.wtol_y(y))
		pnt = [(self.get_xl(px[i]),
		        self.get_yl(py[i])) for i in range(len(px))]
		pygame.draw.polygon(self.screen, sym.fcol, pnt)
		if sym.lcol!= sym.fcol: pygame.draw.polygon(self.screen, sym.lcol, pnt, 1)

	def lline(self, sx, sy, ex, ey, color=0, thk=0):
		if color != 0: self.make_pen(color, thk)
		pygame.draw.line(self.screen, self.pen.color, 
			(self.get_xl(sx), self.get_yl(sy)),
			(self.get_xl(ex), self.get_yl(ey)), math.ceil(self.pen.thk))

	def lmoveto(self, x, y):
		self.pos.set(x,y)
		
	def llineto(self, x,y):
		pygame.draw.line(self.screen, self.pen.color, 
		    (self.get_xl(self.pos.x), self.get_yl(self.pos.y)),
			(self.get_xl(x), self.get_yl(y)))
		self.pos.set(x,y)
	
	def lpolygon(self, x, y, lcol=0, fcol=0, lthk=0):
		pnt = [(self.get_xl(x[i]),
		        self.get_yl(y[i])) for i in range(len(x))]
		pygame.draw.polygon(self.screen, fcol, pnt)
		if lcol !=0 and lcol != fcol: 
			self.make_pen(lcol, lthk)				
			pygame.draw.polygon(self.screen, self.pen.lcol, pnt, math.ceil(self.pen.thk))

	def lpolyline(self, x, y, lcol=0, lthk=0, closed=False):
		pnt = [(self.get_xl(x[i]),
		        self.get_yl(y[i])) for i in range(len(x))]
		if lcol!=0:
			self.make_pen(lcol, lthk)
		pygame.draw.lines(self.screen, self.pen.color, closed, pnt, math.ceil(self.pen.thk))
		
	def show(self):
		pygame.display.update()
		
	def clip(self):
		return
		
	def close(self):
		return
		
#
# aggdraw device
#

class DeviceAggdraw(DeviceRaster):
	def __init__(self, fname, gbox, dpi):
		super().__init__(gbox, dpi)
		self.fname = fname
		self.pen = Pen()
		self.pos = Position(0,0)
		self.img = Image.new('RGB', (self.gwid, self.ghgt), (255,255,255))
		self.agg = aggdraw.Draw(self.img)
		
	def set_device(self, frm):
		self.frm = frm
		self.set_plot(frm)

	def fill_black(self):
		#self.screen.fill(color.BLACK)
		return

	def fill_white(self):
		#self.screen.fill(color.WHITE)
		return

	def fill_cyan(self):
		#self.screen.fill(color.CYAN)
		return

	def make_pen(self, color, lthk):
		self.pen.thk = self.get_xl(lthk)
		self.pen.color = color
		self.agg_pen = aggdraw.Pen(color, self.pen.thk)
		
	def make_brush(self, fcol):
		self.agg_brush = aggdraw.Brush(fcol)
		
	def delete_pen(self):
		return
		
	def line(self, sx, sy, ex, ey, lcol=0, lthk=0):
		if lcol!=0:
			self.make_pen(lcol, lthk)
		self.agg.line((self.get_x(sx), self.get_y(sy),
		              self.get_x(ex), self.get_y(ey)), self.agg_pen)
		self.agg.flush()
		
	def moveto(self, x, y):
		#self.agg.moveto(x,y)
		return
		
	def lineto(self, x, y):
		#self.agg.lineto(self.get_x(self.pos.x), self.get_y(self.pos.y))
		return
		
	def create_pnt_list(self, x, y, convx, convy, closed):
		npnt = len(x)+1 if closed else len(x)
		self.pnt = np.zeros(npnt*2, dtype=np.uint16)
		npnt = len(x)
		for i in range(npnt):
			self.pnt[i*2]   = convx(x[i])
			self.pnt[i*2+1] = convy(y[i])
		if closed: 
			self.pnt[npnt*2]=self.pnt[0]
			self.pnt[npnt*2+1]=self.pnt[1]
		
	def polygon(self, x, y, lcol, fcol, lthk):
		self.create_pnt_list(x,y,self.get_x, self.get_y,False)
		self.make_pen(lcol, lthk)
		self.make_brush(fcol)
		self.agg.polygon(self.pnt, self.agg_pen, self.agg_brush)
		self.agg.flush()
		
	def polyline(self, x, y, lcol=0, lthk=0, closed=False):
		self.create_pnt_list(x,y,self.get_x,self.get_y, closed)
		if lcol !=0: self.make_pen(lcol, lthk)
		self.agg.line(self.pnt, self.agg_pen)
		self.agg.flush()
		
	def begin(self,lcol,lthk,fcol): return
	def end(self): return
	
	def begin_symbol(self, sym): 
		self.make_pen(sym.lcol, sym.lthk)
		self.make_brush(sym.fcol)
		
	def end_symbol(self): return
	
	def circle(self, x,y, rad, lcol=0, lthk=0, fcol=0):
		x1 = self.get_x(x-rad)
		y1 = self.get_y(y-rad)
		x2 = self.get_x(x+rad)
		y2 = self.get_y(y+rad)
		xy = (x1,y1,x2,y2)
		if fcol!=0: 
			self.make_brush(fcol)
			self.agg.ellipse(xy,self.agg_brush)
		if lcol!=0:
			self.make_pen(fcol,lthk)
			self.agg.ellipse(xy,self.agg_pen)
		self.agg.flush()
		
	def symbol(self, x,y, sym, draw=False):
		px, py = sym.update_xy(self.wtol_x(x),self.wtol_y(y))
		self.create_pnt_list(px,py,self.get_xl, self.get_yl,False)
		if draw: self.begin_symbol(sym)
		self.agg.polygon(self.pnt, self.agg_pen, self.agg_brush)
		if draw: self.end_symbol()
		self.agg.flush()
		
	def lline(self, sx, sy, ex, ey, color=0, lthk=0):
		if color != 0: self.make_pen(color, lthk)
		xy = (self.get_xl(sx), self.get_yl(sy), self.get_xl(ex), self.get_yl(ey))
		self.agg.line(xy, self.agg_pen)
		self.agg.flush()
		
	def create_clip(self, x1, y1, x2, y2):
		return
	def delete_clip(self):
		return
	def lmoveto(self, x, y):
		return
		
	def llineto(self, x,y):
		return
	
	def lpolygon(self, x, y, lcol=0, fcol=0, lthk=0):
		self.create_pnt_list(x,y,self.get_xl,self.get_yl,False)
		if lcol != 0: self.make_pen(lcol, lthk)
		if fcol != 0: self.make_brush(fcol)
		self.agg.polygon(self.pnt, self.agg_pen, self.agg_brush)
		self.agg.flush()

	def lpolyline(self, x, y, lcol=0, lthk=0, closed=False):
		self.create_pnt_list(x,y,self.get_xl,self.get_yl,closed)
		if closed: 
			npnt=len(x)
			self.pnt[npnt*2]=self.pnt[0]
			self.pnt[npnt*2+1]=self.pnt[1]
		if lcol != 0: self.make_pen(lcol, lthk)
		self.agg.line(self.pnt,self.agg_pen)
		self.agg.flush()
		
	def close(self):
		self.pnt = None
		self.img.save(self.fname)
		return		

class DeviceCairo(DeviceRaster):
	def __init__(self, fname, gbox, dpi):
		super().__init__(gbox, dpi)
		self.fname = fname
		self.pen   = Pen()
		self.pos   = Position(0,0)
		self.data  = np.ndarray(shape=(self.ghgt, self.gwid), dtype=np.uint32)
		self.surf  = cairo.ImageSurface.create_for_data(self.data, 
		             cairo.FORMAT_ARGB32, self.gwid, self.ghgt)
		self.cntx  = cairo.Context(self.surf)
		self.lcol  = color.rgb()
		self.fcol  = color.rgb()
		self.nlineto = 0
		
	def set_device(self, frm):
		self.frm = frm
		self.set_plot(frm)
		
	def fill_black(self):
		self.data[::]=0xff000000

	def fill_white(self):
		self.data[::]=0xffffffff

	def fill_cyan(self):
		self.data[::]=0xff00ffff
	
	def make_pen(self, lcol, lthk):
		self.pen.thk = self.get_xl(lthk)
		self.pen.color = lcol
		self.lcol.conv(lcol)
		self.cntx.set_source_rgb(self.lcol.r,self.lcol.g,self.lcol.b)
		self.cntx.set_line_width(self.pen.thk)
		
	def make_brush(self, fcol):
		self.fcol.conv(fcol)
		self.cntx.set_source_rgb(self.fcol.r,self.fcol.g,self.fcol.b)
		
	def delete_pen(self):
		return
		
	def line(self, sx, sy, ex, ey, lcol=0, lthk=0):
		if lcol!=0:
			self.make_pen(lcol, lthk)
		self.cntx.move_to(self.get_x(sx),self.get_y(sy))
		self.cntx.line_to(self.get_x(ex),self.get_y(ey))
		self.cntx.stroke()
		
	def moveto(self, x, y):
		#if self.nlineto > 0: 
		#	self.cntx.stroke()
		#	self.nlineto = 0
		self.cntx.move_to(self.get_x(x),self.get_y(y))
		
	def lineto(self, x, y):
		self.cntx.line_to(self.get_x(x),self.get_y(y))
		self.nlineto += 1

	def stroke(self):
		self.cntx.stroke()
		
	def create_pnt_list(self, x, y, convx, convy):
		self.npnt = len(x)
		self.cntx.move_to(convx(x[0]), convy(y[0]))
		for i in range(1,self.npnt):
			self.cntx.line_to(convx(x[i]), convy(y[i]))
	
	def polygon(self, x, y, lcol, fcol, lthk):
		self.create_pnt_list(x,y,self.get_x,self.get_y)
		self.cntx.close_path()
		self.make_brush(fcol)
		
		if lcol != fcol: 
			self.cntx.fill_preserve()
			self.make_pen(lcol, lthk)
			self.cntx.stroke()
		else:
			self.cntx.fill()
		
	def polyline(self, x, y, lcol=0, lthk=0, closed=False):
		self.create_pnt_list(x,y,self.get_x,self.get_y)
		if closed: 
			self.cntx.close_path()

		if lcol !=0: 
			self.make_pen(lcol, lthk)	
		self.cntx.stroke()
		
	def begin(self,lcol,lthk,fcol): return
	def end(self): return
	
	def begin_symbol(self, sym): 
		self.make_pen(sym.lcol, sym.lthk)
		self.make_brush(sym.fcol)
		
	def end_symbol(self): return
	
	def circle(self, x,y, rad, lcol=0, lthk=0, fcol=0):
		cx = self.get_x(x)
		cy = self.get_y(y)
		rr = self.get_v(rad)
		self.cntx.arc(cx,cy,rr,0,two_pi)
		if lcol!=0: self.make_pen(lcol,lthk)
		if fcol!=0: 
			self.make_brush(fcol)
			if lcol==0: self.cntx.fill()
			else      : 
				self.cntx.fill_preserve()
				self.make_pen(lcol,lthk)
		self.cntx.stroke()
		
	def symbol(self, x,y, sym, draw=False):
		px, py = sym.update_xy(self.wtol_x(x),self.wtol_y(y))
		self.create_pnt_list(px,py,self.get_xl, self.get_yl)
		self.cntx.close_path()
		self.make_brush(sym.fcol)
		self.cntx.fill_preserve()
		#self.make_pen(color.get_rgb(sym.lcol), sym.lthk)
		self.cntx.stroke()
		
	def lline(self, sx, sy, ex, ey, color=0, lthk=0):		
		if color != 0: self.make_pen(color,lthk)
		self.cntx.move_to(self.get_xl(sx),self.get_yl(sy))
		self.cntx.line_to(self.get_xl(ex),self.get_yl(ey))
		self.cntx.stroke()
		
	def lmoveto(self, x, y):
		self.cntx.move_to(self.get_xl(x),self.get_yl(y))
		
	def llineto(self, x,y):
		self.cntx.line_to(self.get_xl(x),self.get_yl(y))
	
	def lpolygon(self, x, y, lcol=0, fcol=0, lthk=0):
		self.create_pnt_list(x,y,self.get_xl,self.get_yl)
		self.cntx.close_path()
		
		self.make_brush(fcol)
		if lcol != fcol:
			self.cntx.fill_preserve()
			self.make_pen(lcol, lthk)
			self.cntx.stroke()
		else:
			self.cntx.fill()

	def lpolyline(self, x, y, lcol=0, lthk=0, closed=False):
		self.create_pnt_list(x,y,self.get_xl,self.get_yl)
		if closed: 
			self.cntx.close_path()
		
		if lcol !=0: 
			self.make_pen(lcol, lthk)	
		self.cntx.stroke()
	
	def create_clip(self, x1, y1, x2, y2):
		self.cntx.save()
		sx=self.get_xl(x1)
		sy=self.get_yl(y1)
		ex=self.get_xl(x2)
		ey=self.get_yl(y2)
		#print("%3.2f %3.2f %3.2f %3.2f"%(sx,sy,ex,ey))
		self.cntx.rectangle(sx,sy,ex-sx,ey-sy)
		self.cntx.clip()
		#print(self.cntx.clip_extents())
		
	def delete_clip(self):
		self.cntx.restore()
		
	def clip(self):	return
		
	def close(self, format='png'):
		ext = format.lower()
		if ext == 'png':
			self.surf.write_to_png(self.fname)
		elif ext == 'jpg':
			self.surf.write_to_jpg(self.fname)
		self.pnt  = None
		self.cntx = None
		self.surf = None
		self.data = None

class DeviceCairoAnimation():
	def __init__(self, fname, dev_cairo, func, duration, fps=30, codec='h264'):
		self.fname    = fname
		self.dev      = dev_cairo
		self.func     = func
		self.time     = duration
		self.fps      = fps
		self.codec    = codec
		
	def get_image(self):
		image = np.frombuffer(self.dev.surf.get_data(), np.uint8)
		image = image.reshape((self.dev.surf.get_height(), self.dev.surf.get_width(), 4))
		image = image[:,:,[2,1,0,3]]
		return image[:,:,:3]
		
	def create_frame(self, t):
		self.func(t)
		return self.get_image()
			
	def save_video(self, fname=0):
		fn = fname if fname!=0 else self.fname
		clip = mpy.VideoClip(self.create_frame, duration=self.time)
		clip.write_videofile(fn,self.fps, self.codec)

	def save_gif(self, fname=0):
		fn = fname if fname!=0 else self.fname
		clip = mpy.VideoClip(self.create_frame, duration=self.time)
		clip.write_gif(fn,self.fps)
