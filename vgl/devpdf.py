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
        self.gbox =gbox
        self.wid = p[0]        
        self.hgt = p[1]        
        self.dev = drvpdf.PDFDriver(fname, gbox, p[0], p[1])
        self.pen = False
        self.brush = device.Brush()

    def set_device(self, frm, extend=device._FIT_NONE):
        self.frm = frm
        self.set_plot(frm,extend)

    def fill_white(self):
        return
        
    def make_pen(self, color, thk):
        self.dev.MakePen(color, thk*drvpdf._points_inch)
        self.pen = True
    
    def delete_pen(self):
        self.dev.DeletePen()
        self.pen = False
        
    def _line(self, sx, sy, ex, ey, lcol=None, lthk=None, lpat=linepat._PAT_SOLID, viewport=False):
        xx = [sx, ex]
        yy = [sy, ey]
            
        if viewport:
            sxp = sx*drvpdf._points_inch
            syp = sy*drvpdf._points_inch
            exp = ex*drvpdf._points_inch
            eyp = ey*drvpdf._points_inch
        else:
            sxp = sx
            syp = sy
            exp = ex
            eyp = ey
            
        if isinstance(lpat, linepat.LinePattern):
            self.polyline(xx,yy,lcol,lthk,lpat,viewport=True)
        else:
            if self.pen:
                self.dev.MoveTo(sxp, syp)
                self.dev.LineTo(exp, eyp)
            else:
                self.polyline(xx,yy,lcol,lthk,linepat._PAT_SOLID,viewport=True)
        
    def _moveto(self, x, y, viewport=False):
        if viewport:
            sxp = x*drvpdf._points_inch, 
            syp = y*drvpdf._points_inch 
        else:
            sxp = self._x_viewport(x)*drvpdf._points_inch, 
            syp = self._y_viewport(y)*drvpdf._points_inch 
        self.dev.MoveTo(sxp, syp)

    def _lineto(self, x, y, viewport=False):
        if viewport:
            sxp = x*drvpdf._points_inch, 
            syp = y*drvpdf._points_inch 
        else:
            sxp = self._x_viewport(x)*drvpdf._points_inch, 
            syp = self._y_viewport(y)*drvpdf._points_inch 
        self.dev.LineTo(sxp, syp)
        
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
            if isinstance(lcol, color.Color) and lpat == linepat._PAT_SOLID:
                self.dev.Polygon(px,py,lcol,_lthk,fcol)
            elif fcol:
                self.dev.Polygon(px,py,None,None,fcol)
    
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
                y2 = [-p2[1]*drvpdf._points_inch for p2 in p1 ]
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
        rrad = np.linspace(0, np.pi*2, self._circle_point)
        x1 = x+rad*np.cos(rrad)
        y1 = y+rad*np.sin(rrad)
        self.polygon(x1, y1, lcol, lthk*drvpdf._points_inch, fcol, lpat)
        
    def polyline(self, x, y, lcol=None, lthk=None, lpat=linepat._PAT_SOLID, closed=False, viewport=False):
        pat_inst = isinstance(lpat, linepat.LinePattern)

        if lthk: _lthk = lthk*drvpdf._points_inch
        else: lthk = 0
        
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
        self.dev.CreateClip(sx*drvpdf._points_inch, 
                            sy*drvpdf._points_inch, 
                            ex*drvpdf._points_inch, 
                            ey*drvpdf._points_inch)
        
    def delete_clip(self):
        self.dev.DeleteClip()
        
    def close(self):
        self.dev.Close()

