'''

    devwmf.py

    03/10/2023  Separate device file
'''
import numpy as np
from . import color
from . import device
from . import drvwmf as dw
from . import linepat
from . import patline
from . import gdiobj

class DeviceWMF(device.DeviceVector):
    def __init__(self, fname, gbox):
        super().__init__()
        self.gbox =gbox
        self.dev = dw.WindowsMetaFile(fname, gbox)
        self.pen = gdiobj.Pen()
        self.brush = gdiobj.Brush()

    def set_device(self, frm, extend=device._FIT_NONE):
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
        if lcol:
            self.dev.MakePen(lcol, lthk)
    
        if isinstance(lpat, linepat.LinePattern):
            xp = [sx, ex]
            yp = [sy, ey]
            pat_seg = patline.get_pattern_line(self, xp, yp, lpat.pat_len, lpat.pat_t)
            for p1 in pat_seg:
                x1 = [ p2[0] for p2 in p1 ]
                y1 = [ p2[1] for p2 in p1 ]
                self.dev.Polyline(x1, y1, closed=False) 
        else:
            x1 = self._x_viewport(sx)
            y1 = self._y_viewport(sy)
            x2 = self._x_viewport(ex)
            y2 = self._y_viewport(ey)
            self.dev.Line(x1, y1, x2, y2, lcol, lthk)
            
        if lcol:
            self.dev.DeletePen()

    def stroke(self):
        return
        
    def moveto(self, x, y):
        self.dev.MoveTo(self._x_viewport(x),self._y_viewport(y))
        
    def lineto(self, x, y):
        self.dev.LineTo(self._x_viewport(x),self._y_viewport(y))
        
    def polygon(self, x, y, lcol=None, lthk=None, lpat=linepat._PAT_SOLID, fcol=None, viewport=False):
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
    
    def circle(self, x,y, rad, lcol=None, lthk=None, lpat=linepat._PAT_SOLID, fcol=None):
        if lcol : self.dev.MakePen(lcol, lthk)
        else    : self.dev.MakePen(fcol, 0.01) # dummy line thickness 0.1
        if fcol : self.dev.MakeBrush(fcol)
        else    : self.dev.MakeNullBrush()
        
        #x1 = self._x_viewport(x-rad)
        #y1 = self._y_viewport(y-rad)
        #x2 = self._x_viewport(x+rad)
        #y2 = self._y_viewport(y+rad)
        #self.dev.Circle(x1,y1,x2,y2)
        rrad = np.linspace(0, np.pi*2, self._circle_point)
        x1 = x+rad*np.cos(rrad)
        y1 = y+rad*np.sin(rrad)
        
        self.polygon(x1, y1, lcol, lthk, lpat, fcol)
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
        self.dev.DeletePen()
        self.dev.DeleteBrush()
        
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
            px=[self._x_viewport(xx) for xx in x]
            py=[self._y_viewport(yy) for yy in y]
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
                self.dev.Polyline(x1, y1, closed=False)
        else:
            self.dev.MoveTo(x1,y1)
            self.dev.LineTo(x2,y2)
            
        if lcol: self.dev.DeletePen()

    def lmoveto(self, x, y):
        self.dev.MoveTo(x,y)
        
    def llineto(self, x, y):
        self.dev.LineTo(x,y)
        
    def lpolygon(self, x, y, lcol=None, lthk=None, lpat=linepat._PAT_SOLID, fcol=None):
        self.polygon(x,y,lcol,lthk,lpat,fcol,viewport=True)

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
                self.dev.Polyline(x1, y1, closed)
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

class DeviceWindowsMetafile(DeviceWMF):
    def __init__(self, fname, gbox):
        super().__init__(fname, gbox)