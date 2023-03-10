# Vector Graphic Library (VGL) for Python
#
# device.py
#
# 2020-2-12 Ver 0.1
# 2020-2-19 Cairo deivce added
# 2022-1-19 IPycanvas device added
#
# Author: Uisang Hwang
# Email : uhwangtx@gmail.com
#
import abc
import math
import cairo
import numpy as np
#import pygame 
#import aggdraw
from PIL import Image
import moviepy.editor as mpy

from . import devwmf as dw
from . import color
from . import geom
from . size import BBox, Rect
from . data import Data
from . import patline
from . import linepat

#import devwmf as dw
#import color
#import geom
#from size import BBox, Rect
#from data import Data

# Axis Fit Type
_FIT_NONE      = None
_FIT_EXTEND_X  = 0x0001
_FIT_EXTEND_Y  = 0x0002
_FIT_DEPENDENT = 0x0003

two_pi = 2*math.pi

_default_circle_point = 100
_circle_point = _default_circle_point
def set_circle_point(self, npnt): _circle_point = npnt
def reset_circle_point(self): _circle_point = _default_circle_point
    
get_line_thk = lambda x : 1 if int(x) == 0 else x

class Pen():
    def __init__(self):
        self.lcol = None
        #self.lcol = color.Color()
        self.lthk = None
        
    def set_pen(self, lcol, lthk):
        self.lcol = lcol
        self.lthk =lthk
        
    def __str__(self):
        return "Color: %s\nThickness: %f"%(self.lcol, self.lthk)
        
class Brush():
    def __init__(self):
        self.fcol=None #(0,0,0)
        #self.fcol=color.Color()
        
    def set_brush(self, fcol):
        self.fcol = fcol
        
        
'''
    Frame.py
        default_plot_domain_xmargin = 0.09
        default_plot_domain_ymargin = 0.09
        
        Frame Width: 4' Height: 4'
        
        Plot Domain: (0.09', 0.09', 4-2*0.09, 4-2*0.09)
        (=viewport)  (0.09', 0.09', 3.82, 3.82)
        (=logic)
        (=paper)
        
        Data Range: (xmin, xmax) -> (0, 10)
        (=word)     (ymin, ymax) -> (0, 5)
                    
    Device
        xrange_data = (xmax-xmin) = 10
        yrange_data = (ymax-ymin) = 5
        
        World coord to Viewport coord
            xscale_viewport = width plot domain / x range of data
                            = 3.82/10
                            = 0.382
            yscale_viewport = height plot domain / y range of data
                            = 3.82/5
                            = 0.764
                            
        Dependent on Axis is true(extend one axis(low range) accoring to the other(high range))
        
            if xrange_world == yrange_world and
               wid_viewport != hgt_viewport
                    if hgt_viewport < wid_viewport
                        xmax = xmin+wid_viewport/yscale_viewport
                    else
                        ymax = ymin+hgt_viewport/xscale_viewport
            else
                if xrange_world < yrange_world
                    => vertically long and horizontally narrow mesh
                    => adjust x-axis maximum value
                    xmax = xmin+wid_viewport/yscale_viewport
                elif xrange_world > yrange_world
                    => vertically short and horizontally wide mesh
                    => adjust y-axis maximum value
                    ymax = ymin+hgt_viewport/xscale_viewport
        
                            
'''
        
class Device(abc.ABC):
    def __init__(self):
        self.frm=None

    @abc.abstractmethod
    def set_plot(self,frm,extend=_FIT_NONE):
        pass
        
        
class DeviceVector(Device):
    def __init__(self):
        self.xscale_viewport = 0
        self.yscale_viewport = 0
        self.scal_viewport = 0
        
    def set_plot(self, frm, extend=_FIT_NONE):
        self.frm = frm
        wid_viewport = frm.pdom.get_wid()
        hgt_viewport = frm.pdom.get_hgt()
        xmax, xmin = frm.data.xmax, frm.data.xmin
        ymax, ymin = frm.data.ymax, frm.data.ymin
        
        xrange_world = (xmax-xmin)
        yrange_world = (ymax-ymin)

        self.xscale_viewport = wid_viewport/xrange_world
        self.yscale_viewport = hgt_viewport/yrange_world
        
        self.sx_viewport = frm.bbox.sx+frm.pdom.sx
        self.sy_viewport = frm.bbox.sy+frm.pdom.sy
        self.ey_viewport = self.sy_viewport+frm.pdom.hgt
        
        if extend!=_FIT_NONE:
            if extend==_FIT_DEPENDENT:
                if xrange_world == yrange_world and\
                wid_viewport != hgt_viewport:
                    if hgt_viewport < wid_viewport:
                        xmax = xmin+wid_viewport/self.yscale_viewport
                    else:
                        ymax = ymin+hgt_viewport/self.xscale_viewport
                else:
                    if xrange_world < yrange_world:
                        # vertically long and horizontally narrow mesh
                        # adjust x-axis maximum value
                        xmax = xmin+wid_viewport/self.yscale_viewport
                    elif xrange_world > yrange_world:
                        # vertically short and horizontally wide mesh
                        # adjust y-axis maximum value
                        ymax = ymin+hgt_viewport/self.xscale_viewport
            elif extend==_FIT_EXTEND_Y:
                # long x range, long plot domain in x dir
                # rectangular plot domain in x dir
                # xrange > yrange
                self.xscale_viewport = self.yscale_viewport
                xmax = xmin+wid_viewport/self.yscale_viewport
                
            elif extend==_FIT_EXTEND_X:
                # long y range, long plot domain in y dir
                # rectangular plot domain in y dir
                # long y, narro x
                self.yscale_viewport = self.xscale_viewport
                ymax = ymin+hgt_viewport/self.xscale_viewport
                
            #self.frm.xaxis.update_range(xmin, xmax)
            #self.frm.yaxis.update_range(ymin, ymax)
            self.frm.xaxis.update_tick(xmin, xmax)
            self.frm.yaxis.update_tick(ymin, ymax)
 
    def _x_viewport(self, x):
        return self.sx_viewport+(x-self.frm.data.xmin)*self.xscale_viewport
        
    def _y_viewport(self, y):
        return self.ey_viewport-(y-self.frm.data.ymin)*self.yscale_viewport
        
class DeviceWindowsMetafile(DeviceVector):
    def __init__(self, fname, gbox):
        super().__init__()
        self.gbox =gbox
        self.dev = dw.WindowsMetaFile(fname, gbox)
        self.pen = Pen()
        self.brush = Brush()

    def set_device(self, frm, extend=_FIT_NONE):
        self.frm = frm
        self.set_plot(frm,extend)
        
    def fill_white(self):
        return
        
    def make_pen(self, color, thk):
        self.pen.lcol = color
        self.pen.lthk = thk
        self.dev.MakePen(color, thk)
    
    def delete_pen(self):
        self.dev.DeletePen()
        self.pen.lcol = None
        self.pen.lthk = None
        
    def make_brush(self, fcol):
        self.dev.MakeBrush(fcol)
        self.brush.fcol = fcol
    
    def delete_brush(self):
        self.dev.DeleteBrush()
        self.brush.fcol = None
        
    def line(self, sx, sy, ex, ey, lcol=None, lthk=None, lpat=linepat._PAT_SOLID):
    
        if isinstance(lpat, linepat.LinePattern):
            xp = [sx, ex]
            yp = [sy, ey]
            pat_seg = patline.get_pattern_line(self, xp, yp, lpat.pat_len, lpat.pat_t)
            for p1 in pat_seg:
                x1 = [ p2[0] for p2 in p1 ]
                y1 = [ p2[1] for p2 in p1 ]
                self.dev.Polyline(x1, y1) 
        else:
            x1 = self._x_viewport(sx)
            y1 = self._y_viewport(sy)
            x2 = self._x_viewport(ex)
            y2 = self._y_viewport(ey)
            self.dev.Line(x1, y1, x2, y2, lcol, lthk)

    def stroke(self):
        return
        
    def moveto(self, x, y):
        self.dev.MoveTo(self._x_viewport(x),self._y_pixel(y))
        
    def lineto(self, x, y):
        self.dev.LineTo(self._x_viewport(x),self._y_viewport(y))
        
    def polygon(self, x, y, lcol=None, lthk=None, fcol=None, lpat=linepat._PAT_SOLID, viewport=False):
        pat_inst = isinstance(lpat, linepat.LinePattern)
        
        if (pat_inst ==False and lcol) or fcol:
            if viewport:
                px = x
                py = y
            else:
                px=[self._x_viewport(xx) for xx in x]
                py=[self._y_viewport(yy) for yy in y]
            if lpat == linepat._PAT_SOLID:
                self.dev.Polygon(px,py,lcol,lthk,fcol)
            elif fcol:
                self.dev.Polygon(px,py,lcol=None,lthk=lthk,fcol=fcol)
    
        if lcol and pat_inst:
            if isinstance(x, np.ndarray):
                xp = np.append(x, x[0])
                yp = np.append(y, y[0])
            elif isinstance(x, list):
                xp = x.copy()
                yp = y.copy()
                xp.append(x[0])
                yp.append(y[0])
            if viewport:
                pat_seg = patline.get_pattern_line(self, xp, yp, lpat.pat_len, lpat.pat_t, viewport=True)
            else:
                pat_seg = patline.get_pattern_line(self, xp, yp, lpat.pat_len, lpat.pat_t)
            self.make_pen(lcol, lthk)
            for p1 in pat_seg:
                x2 = [ p2[0] for p2 in p1 ]
                y2 = [ p2[1] for p2 in p1 ]
                self.dev.Polyline(x2, y2, closed=False)
            self.delete_pen()
            
    def begin_symbol(self, sym):
        self.dev.MakePen(sym.lcol, sym.lthk)
        self.dev.MakeBrush(sym.fcol)
        
    def end_symbol(self):
        self.dev.DeletePen()
        self.dev.DeleteBrush()
        
    def symbol(self, x,y,sym,draw=False):
        cx = self._x_viewport(x)
        cy = self._y_viewport(y)
        px, py = sym.update_xy(cx,cy)
        if draw: self.begin_symbol(sym)
        self.dev.Symbol(px,py)
        if draw: self.end_symbol()
    
    def circle(self, x,y, rad, lcol=None, lthk=None, fcol=None, lpat=linepat._PAT_SOLID):
        if lcol : self.dev.MakePen(lcol, lthk)
        else    : self.dev.MakePen(fcol, 0.01) # dummy line thickness 0.1
        if fcol : self.dev.MakeBrush(fcol)
        else    : self.dev.MakeNullBrush()
        
        #x1 = self._x_viewport(x-rad)
        #y1 = self._y_viewport(y-rad)
        #x2 = self._x_viewport(x+rad)
        #y2 = self._y_viewport(y+rad)
        #self.dev.Circle(x1,y1,x2,y2)
        rrad = np.linspace(0, np.pi*2, _circle_point)
        x1 = x+rad*np.cos(rrad)
        y1 = y+rad*np.sin(rrad)
        
        self.polygon(x1, y1, lcol, lthk, fcol, lpat)
        #if isinstance(lpat, linepat.LinePattern):
        #    pat_seg = patline.get_pattern_line(self, x1, y1, lpat.pat_len, lpat.pat_t)
        #    for p1 in pat_seg:
        #        x2 = [ p2[0] for p2 in p1 ]
        #        y2 = [ p2[1] for p2 in p1 ]
        #        self.dev.Polyline(x2, y2, closed=False)
        #else:
        #    #xp = [self._x_viewport(x2) for x2 in x1]
        #    #yp = [self._y_viewport(y2) for y2 in y1]
        #    #self.dev.Polyline(xp, yp, closed)
        #    self.polygon(x1,y1,lcol, lthk, fcol)
        #    
        #self.dev.DeleteBrush()
        #if lcol: self.dev.DeletePen()
        #if fcol: self.dev.DeleteBrush()
        
    def polyline(self, x, y, lcol=None, lthk=None, lpat=linepat._PAT_SOLID, closed=False):
        if lcol: self.dev.MakePen(lcol, lthk)
        
        if isinstance(lpat, linepat.LinePattern):
            if closed:
                if isinstance(x, np.ndarray):
                    xp = np.append(x, x[0])
                    yp = np.append(x, y[0])
                elif isinstance(x, list):
                    xp = x.copy()
                    yp = y.copy()
                    xp.append(x[0])
                    yp.append(y[0])
            else:
                xp = x
                yp = y
            pat_seg = patline.get_pattern_line(self, xp, yp, lpat.pat_len, lpat.pat_t)
            for p1 in pat_seg:
                x1 = [ p2[0] for p2 in p1 ]
                y1 = [ p2[1] for p2 in p1 ]
                self.dev.Polyline(x1, y1,closed=False)
        else:
            px=[self._x_viewport(x[i]) for i in range(len(x))]
            py=[self._y_viewport(y[i]) for i in range(len(y))]
            self.dev.Polyline(px,py,closed)
        if lcol: self.dev.DeletePen()
        
    def lline(self, x1, y1, x2, y2, lcol=None, lthk=None, lpat=linepat._PAT_SOLID):
        if lcol: self.dev.MakePen(lcol,lthk)
        
        if isinstance(lpat, linepat.LinePattern):
            x = [x1, x2]
            y = [y1, y2]
            pat_seg = patline.get_pattern_line(self, x, y, lpat.pat_len, lpat.pat_t, viewport=True)
            for p1 in pat_seg:
                x1 = [ p2[0] for p2 in p1 ]
                y1 = [ p2[1] for p2 in p1 ]
                self.dev.Polyline(x1, y1)
        else:
            self.dev.MoveTo(x1,y1)
            self.dev.LineTo(x2,y2)
            
        if lcol: self.dev.DeletePen()

    def lmoveto(self, x, y):
        self.dev.MoveTo(x,y)
        
    def llineto(self, x, y):
        self.dev.LineTo(x,y)
        
    def lpolygon(self, x, y, lcol=None, lthk=None, fcol=None, lpat=linepat._PAT_SOLID):
        self.polygon(x,y,lcol,lthk,fcol,lpat,viewport=True)

    def lpolyline(self, x, y, lcol=None, lthk=None, lpat=linepat._PAT_SOLID, closed=False):
        if lcol: 
            self.dev.MakePen(lcol, lthk)
            
        if isinstance(lpat, linepat.LinePattern):
            if closed:
                if isinstance(x, np.ndarray):
                    xp = np.append(x, x[0])
                    yp = np.append(x, y[0])
                elif isinstance(x, list):
                    xp = x.copy()
                    yp = y.copy()
                    xp.append(x[0])
                    yp.append(y[0])
            else:
                xp = x
                yp = y
            pat_seg = patline.get_pattern_line(self, xp, yp, lpat.pat_len, lpat.pat_t, viewport=True)
            for p1 in pat_seg:
                x1 = [ p2[0] for p2 in p1 ]
                y1 = [ p2[1] for p2 in p1 ]
                self.dev.Polyline(x1, y1)
        else:        
            self.dev.Polyline(x, y, closed)
        
        if lcol: 
            self.dev.DeletePen()
        
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
        
class DeviceRaster(DeviceVector):
    def __init__(self, gbox, dpi):
        self.dpi  = dpi
        self.gbbox = gbox
        self.gwid = int(gbox.wid()*dpi)
        self.ghgt = int(gbox.hgt()*dpi)
        
        # logic coord -> pixel coord
        self.lxscl = float(self.gwid/gbox.wid())
        self.lyscl = float(self.ghgt/gbox.hgt())
        #self.lscl = float(self.gwid/gbox.wid())
        self.lscl = min(self.lxscl, self.lyscl)
        #self.axis_dependancy = True
        
    def set_plot(self, frm, extend=_FIT_NONE):
        super().set_plot(frm, extend)
        xrange = frm.xaxis.get_range()
        yrange = frm.yaxis.get_range()
        
        self.sx_viewport_pixel = self.sx_viewport*self.dpi
        self.sy_viewport_pixel = self.sy_viewport*self.dpi
        self.ey_viewport_pixel = self.ey_viewport*self.dpi
        
        self.xscale_pixel = (frm.pdom.wid*self.dpi)/xrange
        self.yscale_pixel = (frm.pdom.hgt*self.dpi)/yrange
        self.scale_pixel = min(self.xscale_pixel, self.yscale_pixel)

    def set_axis_dependancy(self):
        xrange = self.frm.data.get_xrange()
        yrange = self.frm.data.get_yrange()
        
        #self.axis_dependancy = status
        self.xscale = (self.frm.pdom.wid*self.dpi)/xrange
        self.yscale = (self.frm.pdom.hgt*self.dpi)/yrange
        self.scale = min(self.xscale, self.yscale)
        
        if xrange == yrange and self.frm.pdom.wid == self.frm.pdom.hgt:
            self.xscale, self.yscale = self.scale, self.scale
        else:
            self.xscale, self.yscale = self.xscale, self.yscale

        self.scale = min(self.xscale, self.yscale)
            
    #def wtol_x(self, x): return self.sx_wtol+self.wtol*(x-self.frm.data.xmin)
    #def wtol_y(self, y): return self.ref_wtol_y-self.wtol*(y-self.frm.data.ymin)
    #def wtol_x(self, x): return self.sx_viewport+self.xscale_viewport*(x-self.frm.data.xmin)
    #def wtol_y(self, y): return self.ey_viewport-self.yscale_viewport*(y-self.frm.data.ymin)
    def get_xl(self, x): return x*self.lxscl
    def get_yl(self, y): return y*self.lyscl
    #def get_x (self, x): return self.sx_viewport_pixel+(x-self.frm.data.xmin)*self.scal    
    #def get_y (self, y): return self.ref_y-(y-self.frm.data.ymin)*self.scal
    #def get_v (self, v): return v*self.scal
    def _x_pixel (self, x): return self.sx_viewport_pixel+(x-self.frm.data.xmin)*self.xscale_pixel    
    def _y_pixel (self, y): return self.ey_viewport_pixel-(y-self.frm.data.ymin)*self.yscale_pixel
    def get_v (self, v): return v*self.scale_pixel
    def size  (self   ): return (self.gwid, self.ghgt)
    def get_xp(self, x): return int(self.sx_viewport_pixel + x)
    def get_yp(self, y): return int(self.sy_viewport_pixel + y)
 
'''
class DevicePygame(DeviceRaster):
    def __init__(self, gbox, dpi, fps=30):
        super().__init__(gbox, dpi)
        self.name = "DevicePygame"
        pygame.init()
        self.screen = pygame.display.set_mode((self.gwid, self.ghgt))
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.pen = Pen()
        self.brush = Brush()
        self.pos = Position(0,0)
        
    def set_device(self, frm, extend=_FIT_NONE):
        self.set_plot(frm, extend)
        return

    def get_tick(self):
        return self.clock.tick(self.fps)/1000

    def fill_black(self):
        self.screen.fill(color.BLACK.get_tuple())

    def fill_white(self):
        self.screen.fill(color.WHITE.get_tuple())

    def fill_cyan(self):
        self.screen.fill(color.CYAN.get_tuple())

    def show(self):
        pygame.display.update()

    def make_pen(self, lcol, lthk):
        self.pen.set_pen(lcol, self.get_xl(lthk))
        
    def make_brush(self, fcol):
        self.brush.set_brush(fcol)
        return
        
    def delete_pen(self):
        self.pen.lcol = None
        self.pen.lthk = None
        return
        
    def delete_brush(self):
        self.brush.fcol = None
        return
        
    def line(self, sx, sy, ex, ey, lcol=None, lthk=None):
        if lcol:
            self.make_pen(lcol, lthk)
            self.moveto(sx,sy)
        pygame.draw.line(self.screen, self.pen.lcol.get_tuple(), 
            (self._x_pixel(sx), self._y_pixel(sy)),
            (self._x_pixel(ex), self._y_pixel(ey)), math.ceil(self.pen.lthk))
        
    def stroke(self):
        return
        
    def moveto(self, x, y):
        self.pos.set(x,y)
        
    def lineto(self, x, y):
        pygame.draw.line(self.screen, self.pen.lcol, 
            (self._x_pixel(self.pos.x),
             self._y_pixel(self.pos.y)),
            (self._x_pixel(x),
             self._y_pixel(y)), math.ceil(self.pen.lthk))
        self.pos.set(x,y)
        
    def polygon(self, x, y, lcol=None, lthk=None, fcol=None):
        pnt = [(self._x_pixel(x[i]),
                self._y_pixel(y[i])) for i in range(len(x))]
                
        if lcol or fcol:
            if lcol: self.make_pen(lcol, lthk)
            if fcol: self.make_brush(fcol)
        
        if self.brush.fcol:
            pygame.draw.polygon(self.screen, self.brush.fcol.get_tuple(), pnt)
            
        if self.pen.lcol: 
            pygame.draw.polygon(self.screen, self.pen.lcol.get_tuple(), pnt, math.ceil(self.pen.lthk))

    def polyline(self, x, y, lcol=None, lthk=None, closed=False):
        pnt = [(self._x_pixel(x[i]),
                self._y_pixel(y[i])) for i in range(len(x))]
        if lcol:
            self.make_pen(lcol, lthk)
        pygame.draw.lines(self.screen, self.pen.lcol.get_tuple(), closed, pnt, math.ceil(self.pen.lthk))
        
    def begin(self,lcol,lthk,fcol): 
        return
    
    def end(self): 
        return
    
    def begin_symbol(self, sym): 
        return
    
    def end_symbol(self): 
        return
    
    def create_clip(self, x1, y1, x2, y2):
        self.screen.set_clip(
        pygame.Rect(self.get_xl(x1),
                    self.get_yl(y1),
                    self.get_xl(x2-x1),
                    self.get_yl(y2-y1)))
                    
    def delete_clip(self):
        self.screen.set_clip(None)
    
    def circle(self, x,y, rad, lcol=None, lthk=None, fcol=None):
        xx = int(self._x_pixel(x))
        yy = int(self._y_pixel(y))
        rrad = int(rad*self.scale_pixel)
        
        if fcol: 
            pygame.draw.circle(self.screen, fcol.get_tuple(), (xx,yy), rrad)
        if lcol: 
            lthk = int(get_line_thk(lthk*self.lscl))
            pygame.draw.circle(self.screen, lcol.get_tuple(), (xx,yy), rrad, lthk)
        
    def symbol(self, x,y, sym, draw=False):
        px, py = sym.update_xy(self._x_viewport(x),self._y_viewport(y))
        
        pnt = [(self.get_xl(px[i]),
                self.get_yl(py[i])) for i in range(len(px))]
                
        pygame.draw.polygon(self.screen, sym.fcol.get_tuple(), pnt)
        
        if sym.lcol != sym.fcol: 
            pygame.draw.polygon(self.screen, sym.lcol.get_tuple(), pnt, 1)

    def lline(self, sx, sy, ex, ey, lcol=None, lthk=None):
        if lcol: 
            self.make_pen(lcol, lthk)
            
        pygame.draw.line(self.screen, self.pen.lcol.get_tuple(), 
            (self.get_xl(sx), self.get_yl(sy)),
            (self.get_xl(ex), self.get_yl(ey)), 
            math.ceil(self.pen.lthk))
        if lcol:
            self.delete_pen()

    def lmoveto(self, x, y):
        self.pos.set(x,y)
        
    def llineto(self, x,y):
        pygame.draw.line(self.screen, self.pen.lcol.get_tuple(), 
            (self.get_xl(self.pos.x), self.get_yl(self.pos.y)),
            (self.get_xl(x), self.get_yl(y)))
        self.pos.set(x,y)
    
    def lpolygon(self, x, y, lcol=None, lthk=None, fcol=None):
        pnt = [(self.get_xl(x[i]),
                self.get_yl(y[i])) for i in range(len(x))]
                
        if fcol:             
            pygame.draw.polygon(self.screen, fcol.get_tuple(), pnt)
        
        if lcol and (lcol != fcol):
            self.make_pen(lcol, lthk)
            pygame.draw.polygon(self.screen, self.pen.lcol.get_tuple(), pnt, math.ceil(self.pen.lthk))
            
    def lpolyline(self, x, y, lcol=None, lthk=None, closed=False):
        pnt = [(self.get_xl(x[i]),
                self.get_yl(y[i])) for i in range(len(x))]
        if lcol:
            self.make_pen(lcol, lthk)
            
        pygame.draw.lines(self.screen, self.pen.lcol.get_tuple(), closed, pnt, math.ceil(self.pen.lthk))
        
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
        self.brush = Brush()
        self.pos = Position(0,0)
        self.img = Image.new('RGB', (self.gwid, self.ghgt), (255,255,255))
        self.agg = aggdraw.Draw(self.img)
        
    def set_device(self, frm, extend=_FIT_NONE):
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

    def make_pen(self, lcol, lthk):
        self.pen.lthk = lthk #self.get_xl(lthk)
        self.pen.lcol = lcol
        self.agg_pen = aggdraw.Pen(color, self.get_xl(lthk))
        
    def make_brush(self, fcol):
        self.brush.fcol = fcol
        self.agg_brush = aggdraw.Brush(fcol)
        
    def delete_pen(self):
        self.pen.lcol = None
        self.pen.lthk = None
        return
        
    def delete_brush(self):
        self.brush.fcol = None
        
    def line(self, sx, sy, ex, ey, lcol=None, lthk=None):
        if lcol           : self.make_pen(lcol, lthk)
        elif self.pen.lcol: self.make_pen(self.pen.lcol, self.pen.lthk)
        
        self.agg.line((self._x_pixel(sx), self._y_pixel(sy),
                      self._x_pixel(ex), self._y_pixel(ey)), self.agg_pen)
        self.agg.flush()
        
        if lcol: self.delete_pen()
        
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
        
    def polygon(self, x, y, lcol=None, lthk=None, fcol=None):
        self.create_pnt_list(x,y,self._x_pixel, self._y_pixel,False)
        
        if lcol: self.make_pen(lcol, lthk)
        else   : self.make_pen(self.pen.lcol, self.pen.lthk)

        if fcol: self.make_brush(fcol)
        else   : self.make_brush(self.brush.fcol)
            
        if (lcol and not fcol) or (self.pen.lcol and not self.brush.fcol): 
            self.agg.polygon(self.pnt, self.agg_pen)
        if (lcol and fcol) or (self.pen.lcol and self.brush.fcol): 
            self.agg.polygon(self.pnt, self.agg_pen, self.agg_brush)
            
        self.agg.flush()
        
        if lcol: self.delete_pen()
        if fcol: self.delete_brush()
        
    def polyline(self, x, y, lcol=0, lthk=0, closed=False):
        self.create_pnt_list(x,y,self._x_pixel,self._y_pixel, closed)
        if lcol !=0: self.make_pen(lcol, lthk)
        self.agg.line(self.pnt, self.agg_pen)
        self.agg.flush()
        
    def begin(self,lcol,lthk,fcol): return
    def end(self): return
    
    def begin_symbol(self, sym): 
        self.make_pen(sym.lcol, sym.lthk)
        self.make_brush(sym.fcol)
        
    def end_symbol(self): return
    
    def circle(self, x,y, rad, lcol=None, lthk=None, fcol=None):
        x1 = self._x_pixel(x-rad)
        y1 = self._y_pixel(y-rad)
        x2 = self._x_pixel(x+rad)
        y2 = self._y_pixel(y+rad)
        xy = (x1,y1,x2,y2)
        #if fcol!=0: 
        #    self.make_brush(fcol)
        #    self.agg.ellipse(xy,self.agg_brush)
        #if lcol!=0:
        #    self.make_pen(fcol,lthk)
        #    self.agg.ellipse(xy,self.agg_pen)
        if fcol or self.brush.fcol:
            if fcol: self.make_brush(fcol)
            elif self.brush.fcol: self.make_brush(self.brush.fcol)
            self.agg.ellipse(xy,self.agg_brush)
        
        if lcol or self.pen.lcol:
            if lcol: self.make_pen(fcol,lthk)
            elif self.pen.lcol: self.make_pen(self.pen.lcol, self.pen.lthk)
            self.agg.ellipse(xy,self.agg_pen)
        
        self.agg.flush()
        if lcol: self.delete_pen()
        if fcol: self.delete_brush()
        
    def symbol(self, x,y, sym, draw=False):
        px, py = sym.update_xy(self._x_viewport(x),self._y_viewport(y))
        self.create_pnt_list(px,py,self.get_xl, self.get_yl,False)
        if draw: self.begin_symbol(sym)
        self.agg.polygon(self.pnt, self.agg_pen, self.agg_brush)
        if draw: self.end_symbol()
        self.agg.flush()
        
    def lline(self, sx, sy, ex, ey, lcol=None, lthk=None):
        if lcol: self.make_pen(color, lthk)
        elif self.pen.lcol: self.make_pen(self.pen.lcol, self.pen.lthk)
        xy = (self.get_xl(sx), self.get_yl(sy), self.get_xl(ex), self.get_yl(ey))
        self.agg.line(xy, self.agg_pen)
        self.agg.flush()
        if lcol: self.delete_pen()
        
    def create_clip(self, x1, y1, x2, y2):
        return
        
    def delete_clip(self):
        return
        
    def lmoveto(self, x, y):
        return
        
    def llineto(self, x,y):
        return
    
    def lpolygon(self, x, y, lcol=None, lthk=None, fcol=None):
        self.create_pnt_list(x,y,self.get_xl,self.get_yl,False)
        
        if lcol:
            self.make_pen(lcol, lthk)
            
        if fcol:
            if not lcol: self.make_pen(fcol, 0.001) # dummy line thk
            self.make_brush(fcol)
            
        self.agg.polygon(self.pnt, self.agg_pen, self.agg_brush)
        self.agg.flush()

    def lpolyline(self, x, y, lcol=None, lthk=None, closed=False):
        self.create_pnt_list(x,y,self.get_xl,self.get_yl,closed)
        
        if closed: 
            npnt=len(x)
            self.pnt[npnt*2]=self.pnt[0]
            self.pnt[npnt*2+1]=self.pnt[1]
            
        if lcol: 
            self.make_pen(lcol, lthk)
        self.agg.line(self.pnt,self.agg_pen)
        self.agg.flush()
        
    def close(self):
        self.pnt = None
        self.img.save(self.fname)
        return        
'''
class DeviceCairo(DeviceRaster):
    def __init__(self, fname, gbox, dpi):
        super().__init__(gbox, dpi)
        self.fname = fname
        self.pen   = Pen()
        self.prv_pen = Pen()
        self.brush = Brush()
        self.pos   = Position(0,0)
        self.data  = np.ndarray(shape=(self.ghgt, self.gwid), dtype=np.uint32)
        self.surf  = cairo.ImageSurface.create_for_data(self.data, 
                     cairo.FORMAT_ARGB32, self.gwid, self.ghgt)
        self.cntx  = cairo.Context(self.surf)
        self.lcol  = color.WHITE
        self.fcol  = color.WHITE
        self.fill_white()
        self.nlineto = 0
        
    def set_device(self, frm, extend=_FIT_NONE):
        self.set_plot(frm, extend)
        
    def set_surface_pixel(self, x, y, col):
        self.data[y][x] = int("0xFF%02X%02X%02X"%(col.r,col.g,col.b),16)
        
    def set_pixel(self, x, y, col):
        self.set_surface_pixel(self.get_xp(x), self.get_yp(y), col)
        
    def fill_black(self):
        self.data[::]=0xff000000

    def fill_white(self):
        self.data[::]=0x0ffffffff

    def fill_cyan(self):
        self.data[::]=0xff00ffff
    
    def make_pen(self, lcol, lthk):
        self.pen.lthk = lthk
        self.pen.lcol = lcol
        c = color.normalize(lcol)
        #self.cntx.set_source_rgb(self.lcol.r,self.lcol.g,self.lcol.b)
        #self.cntx.set_source_rgb(r,g,b)
        self.cntx.set_source_rgb(c.r,c.g,c.b)
        self.cntx.set_line_width(self.get_xl(lthk))
        
    def make_brush(self, fcol):
        self.fcol = color.normalize(fcol)
        self.cntx.set_source_rgb(self.fcol.r,self.fcol.g,self.fcol.b)
        self.brush.fcol = fcol
        
    def delete_pen(self):
        self.pen.lcol = None
        self.pen.lthk = None
        
    def delete_brush(self):
        self.brush.fcol = None
        
    def line(self, sx, sy, ex, ey, lcol=None, lthk=None, lpat=linepat._PAT_SOLID):
        if lcol:
            self.make_pen(lcol, lthk)
            
        if isinstance(lpat, linepat.LinePattern):
            xp = [sx, ex]
            yp = [sy, ey]
            pat_seg = patline.get_pattern_line(self, xp, yp, lpat.pat_len, lpat.pat_t)
            for p1 in pat_seg:
                x1 = [ p2[0] for p2 in p1 ]
                y1 = [ p2[1] for p2 in p1 ]
                self.cntx.move_to(self.get_xl(x1[0]),self.get_yl(y1[0]))
                for x2, y2 in zip(x1, y1):
                    self.cntx.line_to(self.get_xl(x2),self.get_yl(y2))
                self.cntx.stroke()
        else:
            self.cntx.move_to(self._x_pixel(sx),self._y_pixel(sy))
            self.cntx.line_to(self._x_pixel(ex),self._y_pixel(ey))
            self.cntx.stroke()
        
    def moveto(self, x, y):
        self.cntx.move_to(self._x_pixel(x),self._y_pixel(y))
        
    def lineto(self, x, y):
        self.cntx.line_to(self._x_pixel(x),self._y_pixel(y))
        self.nlineto += 1

    def stroke(self):
        self.cntx.stroke()
        
    def create_pnt_list(self, x, y, convx, convy):
        self.npnt = len(x)
        self.cntx.move_to(convx(x[0]), convy(y[0]))
        for i in range(1,self.npnt):
            self.cntx.line_to(convx(x[i]), convy(y[i]))
    
    def draw_geometry(self, lcol, lthk, fcol, lpat):
        if fcol or self.brush.fcol: 
            if fcol: 
                self.make_brush(fcol)
            elif self.brush.fcol:
                self.make_brush(self.brush.fcol)
            
            if lpat==linepat._PAT_SOLID and (lcol or self.pen.lcol):
                self.cntx.fill_preserve()
            else:
                self.cntx.fill()
            
        if lpat==linepat._PAT_SOLID and (lcol or self.pen.lcol):
            if lcol: 
                self.make_pen(lcol, lthk)
            self.cntx.stroke()
        
        if lcol: self.delete_pen()
        if fcol: self.delete_brush()
        
    def polygon(self, x, y, lcol=None, lthk=None, fcol=None, lpat=linepat._PAT_SOLID, viewport=False):
        if (lpat == linepat._PAT_SOLID and lcol) or fcol:
            if viewport:
                self.create_pnt_list(x,y,self.get_xl,self.get_yl)
            else:
                self.create_pnt_list(x,y,self._x_pixel,self._y_pixel)
            self.cntx.close_path()        
            self.draw_geometry(lcol, lthk, fcol, lpat)

        if lcol and isinstance(lpat, linepat.LinePattern):
            if isinstance(x, np.ndarray):
                xp = np.append(x, x[0])
                yp = np.append(y, y[0])
            elif isinstance(x, list):
                xp = x.copy()
                yp = y.copy()
                xp.append(x[0])
                yp.append(y[0])
            if viewport:
                pat_seg = patline.get_pattern_line(self, xp, yp, lpat.pat_len, lpat.pat_t, viewport = True)
            else:
                pat_seg = patline.get_pattern_line(self, xp, yp, lpat.pat_len, lpat.pat_t)
            self.make_pen(lcol, lthk)
            for p1 in pat_seg:
                x1 = [ p2[0] for p2 in p1 ]
                y1 = [ p2[1] for p2 in p1 ]
                self.cntx.move_to(self.get_xl(x1[0]),self.get_yl(y1[0]))
                for x2, y2 in zip(x1, y1):
                    self.cntx.line_to(self.get_xl(x2),self.get_yl(y2))
            self.delete_pen()
            self.cntx.stroke()
            
    def polyline(self, x, y, lcol=None, lthk=None, lpat=linepat._PAT_SOLID, closed=False):
        if isinstance(lpat, linepat.LinePattern):
            if closed:
                if isinstance(x, np.ndarray):
                    xp = np.append(x, x[0])
                    yp = np.append(x, y[0])
                elif isinstance(x, list):
                    xp = x.copy()
                    yp = y.copy()
                    xp.append(x[0])
                    yp.append(y[0])
            pat_seg = patline.get_pattern_line(self, xp, yp, lpat.pat_len, lpat.pat_t)
            for p1 in pat_seg:
                x1 = [ p2[0] for p2 in p1 ]
                y1 = [ p2[1] for p2 in p1 ]
                self.cntx.move_to(self.get_xl(x1[0]),self.get_yl(y1[0]))
                for x2, y2 in zip(x1[1:], y1[1:]):
                    self.cntx.line_to(self.get_xl(x2),self.get_yl(y2))
        else:
            self.create_pnt_list(x,y,self._x_pixel,self._y_pixel)
                            
            if closed: 
                self.cntx.close_path()
    
        if lcol: self.make_pen(lcol, lthk)
        else   : self.make_pen(self.pen.lcol, self.pen.lthk)

        self.cntx.stroke()
            
        if lcol: self.delete_pen()
        
    def begin(self,lcol,lthk,fcol): 
        return
        
    def end(self): 
        return
    
    def begin_symbol(self, sym): 
        self.make_pen(sym.lcol, sym.lthk)
        self.make_brush(sym.fcol)
        
    def end_symbol(self): 
        return
    
    def circle(self, x,y, rad, lcol=None, lthk=None, fcol=None, lpat=linepat._PAT_SOLID):
        if isinstance(lpat, linepat.LinePattern):
            rrad = np.linspace(0, np.pi*2, _circle_point)
            x1 = x+rad*np.cos(rrad)
            y1 = y+rad*np.sin(rrad)
            #pat_seg = patline.get_pattern_line(self, x1, y1, lpat.pat_len, lpat.pat_t)
            #self.make_pen(lcol, lthk)
            #for p1 in pat_seg:
            #    x2 = [ p2[0] for p2 in p1 ]
            #    y2 = [ p2[1] for p2 in p1 ]
            #    self.cntx.move_to(self.get_xl(x2[0]),self.get_yl(y2[0]))
            #    for x3, y3 in zip(x2[1:], y2[1:]):
            #        self.cntx.line_to(self.get_xl(x3),self.get_yl(y3))
            #self.cntx.stroke()
            #self.delete_pen()
            self.polygon(x1, y1, lcol, lthk, fcol, lpat)
        else:
            cx = self._x_pixel(x)
            cy = self._y_pixel(y)
            rr = self.get_v(rad)
            self.cntx.arc(cx,cy,rr,0,two_pi)
            self.draw_geometry(lcol, lthk, fcol, lpat)
            
            
    def symbol(self, x,y, sym, draw=False):
        px, py = sym.update_xy(self._x_viewport(x),self._y_viewport(y))
        self.create_pnt_list(px,py,self.get_xl, self.get_yl)
        self.cntx.close_path()
        self.make_brush(sym.fcol)
        self.cntx.fill_preserve()
        self.make_pen(sym.lcol, sym.lthk)
        self.cntx.stroke()
        
    def lline(self, sx, sy, ex, ey, lcol=None, lthk=None, lpat=linepat._PAT_SOLID):
        if lcol: self.make_pen(lcol, lthk)
        else   : self.make_pen(self.pen.lcol, self.pen.lthk)
        
        if isinstance(lpat, linepat.LinePattern):
            x = [sx, ex]
            y = [sy, ey]
            pat_seg = patline.get_pattern_line(self, x, y, lpat.pat_len, lpat.pat_t, viewport=True)
            for p1 in pat_seg:
                x1 = [ p2[0] for p2 in p1 ]
                y1 = [ p2[1] for p2 in p1 ]
                self.cntx.move_to(self.get_xl(x1[0]),self.get_yl(y1[0]))
                for x2, y2 in zip(x1[1:], y1[1:]):
                    self.cntx.line_to(self.get_xl(x2),self.get_yl(y2))
        else:
            self.cntx.move_to(self.get_xl(sx),self.get_yl(sy))
            self.cntx.line_to(self.get_xl(ex),self.get_yl(ey))
            
        self.cntx.stroke()
        
        if lcol: self.delete_pen()
        
    def lmoveto(self, x, y):
        self.cntx.move_to(self.get_xl(x),self.get_yl(y))
        
    def llineto(self, x,y):
        self.cntx.line_to(self.get_xl(x),self.get_yl(y))
    
    def lpolygon(self, x, y, lcol=None, lthk=None, fcol=None, lpat=linepat._PAT_SOLID):
        self.polygon(x,y,lcol,lthk, fcol, lpat, viewport=True)
        #self.create_pnt_list(x,y,self.get_xl,self.get_yl)
        #self.cntx.close_path()
        #
        #if isinstance(lpat, linepat.LinePattern):
        #    if isinstance(x, np.ndarray):
        #        xp = np.append(x, x[0])
        #        yp = np.append(x, y[0])
        #    elif isinstance(x, list):
        #        xp = x.copy()
        #        yp = y.copy()
        #        xp.append(x[0])
        #        yp.append(y[0])
        #    pat_seg = patline.get_pattern_line(self, xp, yp, lpat.pat_len, lpat.pat_t, viewport=True)
        #    self.dev.MakePen(lcol,lthk)
        #    for p1 in pat_seg:
        #        x1 = [ p2[0] for p2 in p1 ]
        #        y1 = [ p2[1] for p2 in p1 ]
        #        self.cntx.move_to(self.get_xl(x1[0]),self.get_yl(y1[0]))
        #        for x2, y2 in zip(x1[1:], y1[1:]):
        #            self.cntx.line_to(self.get_xl(x2),self.get_yl(y2))
        #    self.dev.DeletePen()
        
        
        #self.make_brush(fcol)
        #if lcol and (lcol != fcol):
        #    self.cntx.fill_preserve()
        #    self.make_pen(lcol, lthk)
        #    self.cntx.stroke()
        #else:
        #    self.cntx.fill()
        
        #if fcol or self.brush.fcol:
        #    if fcol: self.make_brush(fcol)
        #    else   : self.make_brush(self.brush.fcol)
        #    self.cntx.fill_preserve()
        #
        #if lcol: self.make_pen(lcol, lthk)
        #else   : self.make_pen(self.pen.lcol, self.pen.lthk)
        #
        #self.cntx.stroke()
        #
        #if lcol: self.delete_pen()
        #if fcol: self.delete_brush()
        
        #self.draw_geometry(lcol, lthk, fcol)
        
    def lpolyline(self, x, y, lcol=None, lthk=None, lpat=linepat._PAT_SOLID, closed=False):
    
        if isinstance(lpat, linepat.LinePattern):
            if closed:
                if isinstance(x, np.ndarray):
                    xp = np.append(x, x[0])
                    yp = np.append(x, y[0])
                elif isinstance(x, list):
                    xp = x.copy()
                    yp = y.copy()
                    xp.append(x[0])
                    yp.append(y[0])
            else:
                xp = x
                yp = y    
                pat_seg = patline.get_pattern_line(self, xp, yp, lpat.pat_len, lpat.pat_t, viewport=True)
            for p1 in pat_seg:
                x1 = [ p2[0] for p2 in p1 ]
                y1 = [ p2[1] for p2 in p1 ]
                self.cntx.move_to(self.get_xl(x1[0]),self.get_yl(y1[0]))
                for x2, y2 in zip(x1[1:], y1[1:]):
                    self.cntx.line_to(self.get_xl(x2),self.get_yl(y2))
        else:        
            self.create_pnt_list(x,y,self.get_xl,self.get_yl)
            if closed: 
                self.cntx.close_path()
            
        if lcol: self.make_pen(lcol, lthk)    
        else   : self.make_pen(self.pen.lcol, self.pen.lthk)
        self.cntx.stroke()
        if lcol: self.delete_pen()
    
    def create_clip(self, x1, y1, x2, y2):
        self.cntx.save()
        sx=self.get_xl(x1)
        sy=self.get_yl(y1)
        ex=self.get_xl(x2)
        ey=self.get_yl(y2)
        self.cntx.rectangle(sx,sy,ex-sx,ey-sy)
        self.cntx.clip()
        
    def delete_clip(self):
        self.cntx.restore()
        
    def clip(self):    
        return
        
    def save_image(self, fname):
        png = fname.lower().find('.png')
        jpg = fname.lower().find('.jpg')
        if png:
            self.surf.write_to_png(fname)
        elif jpg:
            self.surf.write_to_jpg(fname)
            
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


from ipycanvas import Canvas        
        
class DeviceIPycanvas(DeviceRaster):
    def __init__(self, gbox, dpi):
        super().__init__(gbox, dpi)
        self.pen   = Pen()
        self.prv_pen = Pen()
        self.brush = Brush()
        self.pos   = Position(0,0)
        self.canvas= Canvas(width=self.gwid, height=self.ghgt)
        self.lcol  = color.WHITE
        self.fcol  = color.WHITE
        #self.fill_white()
        self.nlineto = 0
        
    def set_device(self, frm, extend=_FIT_NONE):
        self.set_plot(frm, extend)
                
    def set_pixel(self, x, y, col):
        return
        
    def fill_black(self):
        self.canvas.fill_style = color.get_style(color.BLACK)
        self.canvas.fill_rect(0,0, self.canvas.width, self.canvas.height)

    def fill_white(self):
        self.canvas.fill_style = color.get_style(color.WHITE)
        self.canvas.fill_rect(0,0, self.canvas.width, self.canvas.height)

    def fill_cyan(self):
        self.canvas.fill_style = color.get_style(color.CYAN)
        self.canvas.fill_rect(0,0, self.canvas.width, self.canvas.height)
        
    def make_pen(self, lcol, lthk):
        self.pen.lthk = lthk
        self.pen.lcol = lcol
        self.canvas.stroke_style = color.get_style(lcol)
        self.canvas.line_width = self.get_xl(lthk)
        
    def make_brush(self, fcol):
        self.canvas.fill_style = color.get_style(fcol)
        self.brush.fcol = fcol
        
    def delete_pen(self):
        self.pen.lcol = None
        self.pen.lthk = None
        
    def delete_brush(self):
        self.brush.fcol = None
        
    def moveto(self, x, y):
        self.pos.set(x,y)
        
    def lineto(self, x, y):
        x1 = self._x_pixel(self.pos.x)
        y1 = self._y_pixel(self.pos.y)
        x2 = self._x_pixel(x)
        y2 = self._y_pixel(y)
        self.canvas.stroke_line(x1, y1, x2, y2)
        self.nlineto += 1

    def stroke(self):
        self.canvas
        
    def create_pnt_list(self, x, y, convx, convy):
        #self.points = np.zeros((npnt, 2), dtype=np.uint16)
        #for i, (x1, y1) in enumerate(zip(x, y)):
        #    self.points[i][0] = convx(x1)
        #    self.points[i][1] = convy(y1)
        self.points= [[convx(x[j]), convy(y[j])] for j in range(len(y))]
            
    def draw_geometry(self, lcol, lthk, fcol):

        if fcol or self.brush.fcol: 
            if fcol: self.make_brush(fcol)
            self.canvas.fill_polygon(self.points)
            self.delete_brush()
            
        if lcol or self.pen.lcol:
            if lcol: self.make_pen(lcol, lthk)
            self.canvas.stroke_polygon(self.points)
            self.delete_pen()
        
    def polygon(self, x, y, lcol=None, lthk=None, fcol=None):
        self.create_pnt_list(x,y,self._x_pixel,self._y_pixel)
        self.draw_geometry(lcol, lthk, fcol)

    def polyline(self, x, y, lcol=None, lthk=None, closed=False):
        self.create_pnt_list(x,y,self._x_pixel,self._y_pixel)
                        
        if lcol: 
            self.make_pen(lcol, lthk)
        
        self.canvas.stroke_lines(self.points)
        if closed: 
            p1 = self.points[0]
            p2 = self.points[-1]
            self.canvas.stroke_line(p1[0], p1[1], p2[0], p2[1])
        
        if lcol: self.delete_pen()
        
    def begin(self,lcol,lthk,fcol): 
        return
        
    def end(self): 
        return
    
    def begin_symbol(self, sym): 
        self.make_pen(sym.lcol, sym.lthk)
        self.make_brush(sym.fcol)
        
    def end_symbol(self): 
        self.delete_brush()
        self.delete_pen()
    
    def circle(self, x,y, rad, lcol=None, lthk=None, fcol=None):
        cx = self._x_pixel(x)
        cy = self._y_pixel(y)
        rr = self.get_v(rad)
        
        if fcol or self.brush.fcol:
            if fcol: self.make_brush(fcol)
            self.cavnas.fill_circle(cx, cy, rr)
            self.delete_brush()
        
        if lcol or self.pen.lcol:
            if lcol: self.make_pen(lcol, lthk)
            self.canvas.stroke_circle(cx, cy, rr)
            self.delete_pen()
        
    def symbol(self, x,y, sym, draw=False):
        px, py = sym.update_xy(self._x_viewport(x),self._y_viewport(y))
        self.create_pnt_list(px,py,self.get_xl, self.get_yl)
        #self.polygon(px, py, sym.lcol, sym.lthk, sym.fcol)
        self.draw_geometry(sym.lcol, sym.lthk, sym.fcol)

    def line(self, sx, sy, ex, ey, lcol=None, lthk=None):
        if lcol: self.make_pen(lcol, lthk)
        
        x1 = int(self._x_pixel(sx))
        y1 = int(self._y_pixel(sy))
        x2 = int(self._x_pixel(ex))
        y2 = int(self._y_pixel(ey))
        
        self.canvas.stroke_line(x1, y1, x2, y2)
        
        #if lcol: self.delete_pen()
        
    def lline(self, sx, sy, ex, ey, lcol=None, lthk=None):
        if lcol: self.make_pen(lcol, lthk)
        
        x1 = self.get_xl(sx)
        y1 = self.get_yl(sy)
        x2 = self.get_xl(ex)
        y2 = self.get_yl(ey)
        
        self.canvas.stroke_line(x1, y1, x2, y2)
        
        if lcol: self.delete_pen()
        
    def lmoveto(self, x, y):
        self.pos.x = self.get_xl(x)
        self.pos.y = self.get_yl(y)
        
    def llineto(self, x,y):
        x2 = self.get_xl(x)
        y2 = self.get_yl(y)
        self.stroke_line(self.pos.x, self.pos.y, x2, y2)
    
    def lpolygon(self, x, y, lcol=None, fcol=None, lthk=None):
        self.create_pnt_list(x,y,self.get_xl,self.get_yl)
        self.draw_geometry(lcol, lthk, fcol)
        
    def lpolyline(self, x, y, lcol=None, lthk=None, closed=False):
        self.create_pnt_list(x,y,self.get_xl,self.get_yl)
                        
        if lcol: 
            self.make_pen(lcol, lthk)
        
        self.canvas.stroke_lines(self.points)
        if closed: 
            p1 = self.points[0]
            p2 = self.points[-1]
            
            self.canvas.stroke_line(p1[0], p1[1], p2[0], p2[1])
        
        if lcol: self.delete_pen()
            
    def create_clip(self, x1, y1, x2, y2):
        self.canvas.save()
        sx=self.get_xl(x1)
        sy=self.get_yl(y1)
        ex=self.get_xl(x2)
        ey=self.get_yl(y2)
        self.canvas.stroke_rect(sx,sy,ex-sx,ey-sy)
        self.canvas.clip()
        #self.canvas.restore()
        
    def delete_clip(self):
        self.canvas.restore()
        
    def clip(self):    
        return    
    def close(self, format='png'):
        #self.canvas.clear()    
        return self.canvas
       