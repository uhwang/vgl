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

from . import color
from . import geom
from . size import BBox, Rect
from . data import Data
from . import patline
from . import linepat
from . gdiobj import Pen, Brush

# Axis Fit Type
_FIT_NONE      = None
_FIT_EXTEND_X  = 0x0001
_FIT_EXTEND_Y  = 0x0002
_FIT_DEPENDENT = 0x0003

# Coordinate System Types 
_COORDSYS_CARTESIAN = Ox0001
_COORDSYS_PAPER.    = 0x0002

get_line_thk = lambda x : 1 if int(x) == 0 else x

class Position():
    def __init__(self, x, y):
        self.set(x,y)
    
    def set(self, x, y):
        self.x = x
        self.y = y


#class Device(abc.ABC):
#    _default_circle_point = 100
#
#    def __init__(self):
#        self.frm=None
#        self._circle_point = Device._default_circle_point
#        print("root", self._circle_point)
#
#    def set_circle_point(self, npnt): 
#        self._circle_point = npnt
#
#    def reset_circle_point(self): 
#        self._circle_point = _default_circle_point
#
#    @abc.abstractmethod
#    def set_plot(self,frm,extend):
#        pass
        
#class DeviceVector(Device):
_default_circle_point = 100

class DeviceVector():
    def __init__(self):
        #super().__init__()
        self.coordsys_t = _COORDSYS_PAPER
        self.frm=None
        self._circle_point = _default_circle_point
        self.xscale_viewport = 0
        self.yscale_viewport = 0
        self.scal_viewport = 0

    def set_circle_point(self, npnt): 
        self._circle_point = npnt

    def reset_circle_point(self): 
        self._circle_point = _default_circle_point
        
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
        
        
class DeviceRaster(DeviceVector):
    def __init__(self, gbox, dpi):
        super().__init__()
        self.dpi  = dpi
        self.gbbox = gbox
        self.gwid = int(gbox.wid()*dpi)
        self.ghgt = int(gbox.hgt()*dpi)
        
        # logic coord -> pixel coord
        self.lxscl = float(self.gwid/gbox.wid())
        self.lyscl = float(self.ghgt/gbox.hgt())
        self.lscl = min(self.lxscl, self.lyscl)
        
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
            
    def get_xl(self, x): return x*self.lxscl
    def get_yl(self, y): return y*self.lyscl
    def _x_pixel(self, x): return int(self.sx_viewport_pixel+\
                                     (x-self.frm.data.xmin)*\
                                     self.xscale_pixel)    
    def _y_pixel(self, y): return int(self.ey_viewport_pixel-\
                                     (y-self.frm.data.ymin)*\
                                     self.yscale_pixel)
    def get_v (self, v): return v*self.scale_pixel
    def size  (self   ): return (self.gwid, self.ghgt)
    def get_xp(self, x): return int(self.sx_viewport_pixel + x)
    def get_yp(self, y): return int(self.sy_viewport_pixel + y)
 
