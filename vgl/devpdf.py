'''

    devpdf.py

    03/23/2023  
    
'''

'''
    devemf.py


''' 

import numpy as np
from . import color
from . import device
from . import drvpdf
from . import linepat
from . import patline
from . import paper

class DevicePDF(device.DeviceVector):
    def __init__(self, fname, gbox, p=(8.5,11.0)):
        super().__init__()
        self.coordsys_t = device._COORDSYS_CARTESIAN
        self.gbox =gbox
        self.wid = p[0]        
        self.hgt = p[1]        
        self.dev = drvpdf.PDFDriver(fname, p[0], p[1])
        self.pen = False
        self.brush = device.Brush()

    def set_device(self, frm, extend=device._FIT_NONE):
        self.frm = frm
        self.set_plot(frm,extend)

    def _y_viewport(self, y):
        return self.sy_viewport+(y-self.frm.data.ymin)*self.yscale_viewport
        
    def fill_white(self):
        return
        
    def make_pen(self, color, thk):
        self.dev.MakePen(color, thk*drvpdf._points_inch)
        self.pen = True
    
    def delete_pen(self):
        self.dev.DeletePen()
        self.pen = False
        
    #def make_brush(self, fcol):
    #    #self.dev.MakeBrush(fcol)
    #    #self.brush.fcol = fcol
    #    pass
    #
    #def delete_brush(self):
    #    #self.dev.DeleteBrush()
    #    #self.brush.fcol = None
    #    pass
        
    def _line(self, sx, sy, ex, ey, lcol=None, lthk=None, lpat=linepat._PAT_SOLID, viewport=False):
        if viewport:
            sxp = sx*drvpdf._points_inch 
            syp = sy*drvpdf._points_inch
            exp = ex*drvpdf._points_inch
            eyp = ey*drvpdf._points_inch
        else:
            sxp = self._x_viewport(sx)*drvpdf._points_inch
            syp = self._x_viewport(sy)*drvpdf._points_inch
            exp = self._x_viewport(ex)*drvpdf._points_inch
            eyp = self._x_viewport(ey)*drvpdf._points_inch
            
        if isinstance(lpat, linepat.LinePattern):
            x = [x1, x2]
            y = [y1, y2]
            self.polyline(x,y,lcol,lthk,lpat,viewport=True)
        else:
            if self.pen:
                self.dev.MoveTo(sxp, syp)
                self.dev.LineTo(exp, eyp)
            else:
                xx = [sx,ex]
                yy = [sy,ey]
                self.polyline(xx,yy,lcol,lthk,lpat,viewport)
        
    def _moveto(self, x, y, viewport=False):
        if viewport:
            sxp = x*drvpdf._points_inch, 
            syp = y*drvpdf._points_inch 
        else:
            sxp = self._x_viewport(x)*drvpdf._points_inch, 
            syp = self._x_viewport(y)*drvpdf._points_inch 
        self.dev.MoveTo(sxp, syp)

    def _lineto(self, x, y, viewport=False):
        if viewport:
            sxp = x*drvpdf._points_inch, 
            syp = y*drvpdf._points_inch 
        else:
            sxp = self._x_viewport(x)*drvpdf._points_inch, 
            syp = self._x_viewport(y)*drvpdf._points_inch 
        self.dev.MoveTo(sxp, syp)
        
    def moveto(self, x, y):
        self._moveto(x,y,False)
        
    def lmoveto(self, x, y):
        self._moveto(x,y,True)
        
    def lineto(self, x, y):
        self._lineto(x,y,False)

    def llineto(self, x, y):
        self._lineto(x,y,True)
        
    def lline(self, x1, y1, x2, y2, lcol=None, lthk=None, lpat=linepat._PAT_SOLID):
        self._line(x1, y1, x2, y2, lcol, lthk, lpat, True)
        
    def line(self, x1, y1, x2, y2, lcol=None, lthk=None, lpat=linepat._PAT_SOLID):
        self._line(x1, y1, x2, y2, lcol, lthk, lpat, False)
        
    # viewport(True) : lpolygon
    # viewport(False) : polygon
    
    def polygon(self, x, y, lcol=None, lthk=None, fcol=None, lpat=linepat._PAT_SOLID, viewport=False):
        pat_inst = isinstance(lpat, linepat.LinePattern)

        if lthk: _lthk = lthk*drvpdf._points_inch
        if (pat_inst ==False and lcol) or fcol:
            if viewport:
                px = [xx*drvpdf._points_inch for xx in x]
                py = [yy*drvpdf._points_inch for yy in y]
            else:
                px = [self._x_viewport(xx)*drvpdf._points_inch for xx in x]
                py = [self._y_viewport(yy)*drvpdf._points_inch for yy in y]
            if lpat == linepat._PAT_SOLID:
                self.dev.Polygon(px,py,lcol,_lthk,fcol)
            elif fcol:
                self.dev.Polygon(px,py,None,_lthk,fcol)
    
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
            #self.make_pen(lcol, lthk)
            for p1 in pat_seg:
                x2 = [p2[0]*drvpdf._points_inch for p2 in p1 ]
                y2 = [p2[1]*drvpdf._points_inch for p2 in p1 ]
                self.dev.Polyline(x2, y2, lcol, _lthk, fcol=None, closed=False)
            #self.delete_pen()
            
    def begin_symbol(self, sym):
        pass        
    def end_symbol(self):
        pass        
        
    def symbol(self, x,y,sym,draw=False):
        cx = self._x_viewport(x)
        cy = self._y_viewport(y)
        px, py = sym.update_xy(cx,cy)
        ppx = [px1*drvpdf._points_inch for px1 in px]
        ppy = [py1*drvpdf._points_inch for py1 in py]
        self.dev.Polygon(ppx, ppy, sym.lcol, sym.lthk*drvpdf._points_inch, sym.fcol)
    
    def circle(self, x,y, rad, lcol=None, lthk=None, fcol=None, lpat=linepat._PAT_SOLID):
        #if lcol : self.dev.MakePen(lcol, lthk*self.dpi)
        #else    : self.dev.MakePen(fcol, 0.01) # dummy line thickness 0.1
        #if fcol : self.dev.MakeBrush(fcol)
        #else    : self.dev.MakeNullBrush()

        rrad = np.linspace(0, np.pi*2, self._circle_point)
        x1 = x+rad*np.cos(rrad)
        y1 = y+rad*np.sin(rrad)
        self.polygon(x1, y1, lcol, lthk*drvpdf._points_inch, fcol, lpat)
        
    def polyline(self, x, y, lcol=None, lthk=None, lpat=linepat._PAT_SOLID, closed=False, viewport=False):
        pat_inst = isinstance(lpat, linepat.LinePattern)

        if lthk: _lthk = lthk*drvpdf._points_inch
        if pat_inst == False and lcol:
            if viewport:
                px = [xx*drvpdf._points_inch for xx in x]
                py = [yy*drvpdf._points_inch for yy in y]
            else:
                px = [self._x_viewport(xx)*drvpdf._points_inch for xx in x]
                py = [self._y_viewport(yy)*drvpdf._points_inch for yy in y]
            self.dev.Polyline(px,py,lcol,_lthk,fcol=None,closed=False)
    
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

            for p1 in pat_seg:
                x2 = [p2[0]*drvpdf._points_inch for p2 in p1 ]
                y2 = [p2[1]*drvpdf._points_inch for p2 in p1 ]
                self.dev.Polyline(x2, y2, lcol, _lthk, fcol=None, closed=False)
        
        
    def lpolygon(self, x, y, lcol=None, lthk=None, fcol=None, lpat=linepat._PAT_SOLID):
        self.polygon(x,y,lcol,lthk,fcol,lpat,viewport=True)

    def lpolyline(self, x, y, lcol=None, lthk=None, lpat=linepat._PAT_SOLID, closed=False):
        self.polyline(x,y,lcol,lthk,lpat,closed,viewport=True)
        
    def create_clip(self, sx, sy, ex, ey):
        self.dev.CreateClip(sx, sy, ex, ey)
        
    def delete_clip(self):
        self.dev.DeleteClip(0)
        
    def close(self):
        self.dev.Close()

