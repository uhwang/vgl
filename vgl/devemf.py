'''
    devemf.py


''' 

import numpy as np
from . import color
from . import device
from . import drvemf 
from . import linepat
from . import patline
from . import gdiobj

class DeviceEMF(device.DeviceRaster):
    def __init__(self, fname, gbox, dpi=300):
        super().__init__(gbox, dpi)
        self.gbox =gbox
        self.dpi = dpi
        self.dev = drvemf.EnhancedMetaFile(fname, gbox)
        self.pen = gdiobj.Pen()
        self.brush = gdiobj.Brush()

    def _x_pixel(self, x):
        return int(super()._x_pixel(x))

    def _y_pixel(self, y):
        return int(super()._y_pixel(y))
        
    def set_device(self, frm, extend=device._FIT_NONE):
        self.frm = frm
        self.set_plot(frm,extend)
        
    def fill_white(self):
        return
        
    def make_pen(self, color, thk):
        self.pen.lcol = color
        self.pen.lthk = thk
        self.dev.MakePen(color, int(self.get_ylt(thk)))
    
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
        
    def line(self, sx, sy, ex, ey, lcol=color.BLACK, lthk=0.001, lpat=linepat._PAT_SOLID):

        if isinstance(lpat, linepat.LinePattern):
            if not isinstance(self.pen.lcol, color.Color) and lcol: 
                self.make_pen(lcol, lthk*self.frm.hgt())
            xp = [sx, ex]
            yp = [sy, ey]
            pat_seg = patline.get_pattern_line(self, xp, yp, lpat.pat_len, lpat.pat_t)
            
            for p1 in pat_seg:
                x1 = [int(self.get_xl(p2[0])) for p2 in p1 ]
                y1 = [int(self.get_yl(p2[1])) for p2 in p1 ]
                self.dev.Polyline(x1, y1, closed=False) 
                
            if not isinstance(self.pen.lcol, color.Color) and lcol: 
                self.delete_pen()
        else:
            x1 = self._x_pixel(sx)
            y1 = self._y_pixel(sy)
            x2 = self._x_pixel(ex)
            y2 = self._y_pixel(ey)
            self.dev.Line(x1, y1, x2, y2, lcol, int(self.get_ylt(lthk*self.frm.hgt())))
        
    def stroke(self):
        return
        
    def moveto(self, x, y):
        self.dev.MoveTo(self._x_pixel(x),self._y_pixel(y))
        
    def lineto(self, x, y):
        self.dev.LineTo(self._x_pixel(x),self._y_pixel(y))
        
    # viewport(True) : lpolygon
    # viewport(False) : polygon
    
    def polygon(self, x, y, lcol=color.BLACK, lthk=0.001, lpat=linepat._PAT_SOLID, fcol=None, viewport=False):
        pat_inst = isinstance(lpat, linepat.LinePattern)

        if (pat_inst ==False and lcol) or fcol:
            if viewport:
                px = [int(self.get_xl(xx)) for xx in x]
                py = [int(self.get_yl(yy)) for yy in y]
            else:
                px = [int(self._x_pixel(xx)) for xx in x]
                py = [int(self._y_pixel(yy)) for yy in y]
            if isinstance(lcol, color.Color) and lpat == linepat._PAT_SOLID:
                self.dev.Polygon(px,py,lcol, 
                                 int(self.get_ylt(lthk*self.frm.hgt())),fcol)
            elif fcol:
                self.dev.Polygon(px,py,None, None, fcol)
    
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

            self.make_pen(lcol, lthk*self.frm.hgt())
            for p1 in pat_seg:
                x2 = [int(self.get_xl(p2[0])) for p2 in p1 ]
                y2 = [int(self.get_xl(p2[1])) for p2 in p1 ]
                self.dev.Polyline(x2, y2, closed=False)
            self.delete_pen()
            
    def begin_symbol(self, sym):
        #self.make_pen(sym.lcol, sym.lthk)
        #self.make_brush(sym.fcol)
        pass
    def end_symbol(self):
        #self.delete_pen()
        #self.delete_brush()
        pass
        
    def symbol(self, x,y,sym,draw=False):
        cx = self._x_viewport(x)
        cy = self._y_viewport(y)
        px, py = sym.update_xy(cx,cy)
        ppx = [int(self.get_xl(px1)) for px1 in px]
        ppy = [int(self.get_yl(py1)) for py1 in py]
        #self.dev.Symbol(ppx,ppy)
        self.dev.Polygon(ppx,ppy, sym.lcol, 
        int(self.get_ylt(sym.lthk*self.frm.hgt())), sym.fcol)
    
    def circle(self, x,y, rad, lcol=color.BLACK, lthk=0.001, lpat=linepat._PAT_SOLID, fcol=None):
        rrad = np.linspace(0, np.pi*2, self._circle_point)
        x1 = x+rad*np.cos(rrad)
        y1 = y+rad*np.sin(rrad)
        self.polygon(x1, y1, lcol, lthk, lpat, fcol)
        
    def polyline(self, x, y, lcol=color.BLACK, lthk=0.001, lpat=linepat._PAT_SOLID, closed=False):
        #if lcol: 
        if not isinstance(self.pen.lcol, color.Color) and lcol:
            self.dev.MakePen(lcol, int(self.get_xlt(lthk*self.frm.hgt())))
        
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
                x1 = [int(self.get_xl(p2[0])) for p2 in p1 ]
                y1 = [int(self.get_yl(p2[1])) for p2 in p1 ]
                self.dev.Polyline(x1, y1,closed=False)
        else:
            px=[int(self._x_pixel(x1)) for x1 in x]
            py=[int(self._y_pixel(y1)) for y1 in y]
            self.dev.Polyline(px,py,closed)
            
        #if lcol: 
        #if not isinstance(self.pen.lcol, color.Color):
        if not isinstance(self.pen.lcol, color.Color) and lcol:
            self.dev.MakePen(lcol, int(self.get_xlt(lthk*self.frm.hgt())))        
            self.dev.DeletePen()
        
    def lline(self, x1, y1, x2, y2, lcol=color.BLACK, lthk=0.001, lpat=linepat._PAT_SOLID):
        x = [x1, x2]
        y = [y1, y2]
        self.lpolyline(x,y,lcol,lthk,lpat)

    def lmoveto(self, x, y):
        self.dev.MoveTo(int(self.get_xl(x)),int(self.get_yl(y)))
        
    def llineto(self, x, y):
        self.dev.LineTo(int(self.get_xl(x)),int(self.get_yl(y)))
        
    def lpolygon(self, x, y, lcol=color.BLACK, lthk=0.001, lpat=linepat._PAT_SOLID, fcol=None):
        self.polygon(x,y,lcol,lthk,fcol,lpat,viewport=True)

    def lpolyline(self, x, y, lcol=color.BLACK, lthk=0.001, lpat=linepat._PAT_SOLID, closed=False):
        #if lcol: 
        #if not isinstance(self.pen.lcol, color.Color):
        #    self.make_pen(lcol, lthk*self.frm.hgt())
        if not isinstance(self.pen.lcol, color.Color):
            self.dev.MakePen(lcol, int(self.get_xlt(lthk*self.frm.hgt())))
            
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
                x1 = [ int(self.get_xl(p2[0])) for p2 in p1 ]
                y1 = [ int(self.get_yl(p2[1])) for p2 in p1 ]
                self.dev.Polyline(x1, y1, closed)
        else:
            x1 = [ int(self.get_xl(p2)) for p2 in x ]
            y1 = [ int(self.get_yl(p2)) for p2 in y ]   
            self.dev.Polyline(x1, y1, closed)
        
        #if lcol: 
        #if not isinstance(self.pen.lcol, color.Color):
        if not isinstance(self.pen.lcol, color.Color) and lcol:
            self.dev.MakePen(lcol, int(self.get_xlt(lthk*self.frm.hgt())))        
            self.delete_pen()
        
    def create_clip(self, sx, sy, ex, ey):
        self.dev.CreateClip(sx, sy, ex, ey)
        
    def delete_clip(self):
        self.dev.DeleteClip(0)
        
    def close(self):
        self.dev.CloseMetafile()

class DeviceEnhancedMetafile(DeviceEMF):
    def __init__(self, fname, gbox, dpi=300):
        super().__init__(fname, gbox, dpi)
        