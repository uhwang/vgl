'''
    devsvg.py

    04/03/2023

    <rect width="300" height="100" style="fill:rgb(0,0,255);stroke-width:3;stroke:rgb(0,0,0)" />
    <circle cx="50" cy="50" r="40" stroke="black" stroke-width="3" fill="red" />
    <ellipse cx="200" cy="80" rx="100" ry="50"
    style="fill:yellow;stroke:purple;stroke-width:2" />
    <line x1="0" y1="0" x2="200" y2="200" style="stroke:rgb(255,0,0);stroke-width:2" />
    <polygon points="200,10 250,190 160,210" style="fill:lime;stroke:purple;stroke-width:1" />
    <polyline points="20,20 40,25 60,40 80,120 120,140 200,180"
    style="fill:none;stroke:black;stroke-width:3" />
'''
import numpy as np
from . import device
from . import color
from . import linepat
from . import patline
from . import gdiobj

_line_format_begin = "<line x1=\"%d\" y1=\"%d\" x2=\"%d\" y2=\"%d\" "
_line_format_end = " style=\"fill:none;stroke:rgb(%d,%d,%d);stroke-width:%d\" />\n"
_polygon_format_end = "style=\"stroke:rgb(%d,%d,%d);stroke-width:%d;fill:rgb(%d,%d,%d);\"/>\n"
_polygon_format_end_nostroke = "style=\"stroke:none;fill:rgb(%d,%d,%d);\"/>\n"
_polygon_format_end_nofill = "style=\"stroke:rgb(%d,%d,%d);stroke-width:%d;fill:none;\"/>\n"
_next_line = "\n"              
_points_per_line = 5
_move_to_str = 'M'
_line_to_str = "L"
               
class DeviceSVG(device.DeviceRaster):
    def __init__(self, fname, gbbox, dpi):
        super().__init__(gbbox, dpi)
        self.fp = open(fname, "wt")
        self.pen   = None
        self.brush = None
        
        self.fp.write("<svg version=\"1.1\"\n"\
                      "width=\"%d\" height=\"%d\"\n"
                      "xmlns=\"http://www.w3.org/2000/svg\">\n"\
                      %(int(self.gwid),int(self.ghgt)))
        
    def set_device(self, frm, extend=device._FIT_NONE):
        self.set_plot(frm, extend)
        
    def fill_white(self):
        self.fp.write("<rect width=\"100%\" height=\"100%\""\
                      " style=\"fill:rgb(255,255,255)\"/>")

    def _svg_lthk(self, lthk):
        lthk_ = int(self.get_xlt(lthk))
        return 1 if lthk_ == 0 else lthk_
        
    def make_pen(self, lcol, lthk):
        self.pen = gdiobj.StreamPen()
        self.pen.lthk = self._svg_lthk(lthk)
        self.pen.lcol = lcol
        self.fp.write("<path d=\"")
        
    def make_brush(self, fcol):
        self.brush = gdiobj.Brush()
        self.brush.fcol = fcol
        
    def delete_pen(self):
        for i, item in enumerate(self.pen.buf):
            self.fp.write("%s %d %d,"%(item[0], item[1], item[2]))
            if (i+1)%_points_per_line == 0:
                self.fp.write(_next_line)
        
        self.fp.write("\"\n"+_line_format_end%(\
                      self.pen.lcol.r, 
                      self.pen.lcol.g, 
                      self.pen.lcol.b,
                      self.pen.lthk))
        self.pen = None
        
    def delete_brush(self):
        self.brush = None
        
    def stroke(self):
        pass
        
    def begin_symbol(self, sym): 
        pass
        
    def symbol(self, x,y, sym, draw=False):
        px, py = sym.update_xy(self._x_viewport(x),self._y_viewport(y))
        self.polygon(px,py,sym.lcol,sym.lthk,sym.fcol,viewport=True)
                
    def end_symbol(self):  
        pass
            
    def _write_polypoints(self, x, y):
        for i, (x1, y1) in enumerate(zip(x,y)):
            self.fp.write("%d %d,"%(x1,y1))
            if (i+1)%_points_per_line == 0:
                self.fp.write(_next_line)
        #self.fp.write("\"\n")
        
    def _write_pathpoints(self, x, y):
        self.fp.write("M %d %d "%(x[0],y[0]))
        for i, (x1, y1) in enumerate(zip(x[1:],y[1:])):
            self.fp.write("L %d %d "%(x1,y1))
            if (i+1)%_points_per_line == 0:
                self.fp.write(_next_line)
        
    def create_pnt_list(self, x, y, convx, convy):
        for i, (x1, y1) in enumerate(zip(x, y)):
            self.fp.write("%d %d, "%(int(convx(x1)), int(convy(y1))))
            if (i+1)%_points_per_line == 0:
                self.fp.write(_next_line)
        self.fp.write("\"\n")    
        
    def _line(self, sx, sy, ex, ey, lcol=None, lthk=None, lpat=linepat._PAT_SOLID, viewport=False):
            
        if isinstance(lpat, linepat.LinePattern):
            if not self.pen:
                self.fp.write("<path d=\"\n")

            xp = [sx, ex]
            yp = [sy, ey]
            if viewport:
                pat_seg = patline.get_pattern_line(self, xp, yp, lpat.pat_len, lpat.pat_t, viewport=True)
            else:
                pat_seg = patline.get_pattern_line(self, xp, yp, lpat.pat_len, lpat.pat_t)
                
            for p1 in pat_seg:
                x1 = [ self.get_xl(p2[0]) for p2 in p1 ]
                y1 = [ self.get_yl(p2[1]) for p2 in p1 ]
                if self.pen:
                    self._write_pathpoints(x1,y1)
                else:
                    self._write_polypoints(x1,y1)
            self.fp.write("\"\n")
        else:
            if viewport:
                if self.pen: 
                    self.lmoveto(sx,sy)
                    self.llineto(ex,ey)
                else:
                    self.fp.write(_line_format_begin%(\
                        self.get_xl(sx),
                        self.get_yl(sy),
                        self.get_xl(ex),
                        self.get_yl(ey)))
            else:
                if self.pen:
                    self.lmoveto(sx,sy)
                    self.llineto(ex,ey)
                else:            
                    self.fp.write(_line_format_begin%(\
                        self._x_pixel(sx),
                        self._y_pixel(sy),
                        self._x_pixel(ex),
                        self._y_pixel(ey)))
        
        if isinstance(lcol, color.Color):
            self.fp.write(_line_format_end%(\
                        lcol.r, 
                        lcol.g, 
                        lcol.b, 
                        self._svg_lthk(lthk)))
         
    def lline(self, x1, y1, x2, y2, lcol=None, lthk=None, lpat=linepat._PAT_SOLID):
        self._line(x1, y1, x2, y2, lcol, lthk, lpat, True)
        
    def line(self, x1, y1, x2, y2, lcol=None, lthk=None, lpat=linepat._PAT_SOLID):
        self._line(x1, y1, x2, y2, lcol, lthk, lpat, False)
        
    def _moveto(self, x, y, viewport=False):
        if viewport:
            sxp = int(self.get_xl(x))
            syp = int(self.get_yl(y))
        else:
            sxp = int(self._x_pixel(x))
            syp = int(self._y_pixel(y))
            
        self.pen.buf.append((_move_to_str,sxp,syp))    
        
    def moveto(self, x, y):
        self._moveto(x,y)
        
    def lmoveto(self, x, y):
        self._moveto(x,y,True)
        
    def _lineto(self, x, y, viewport=False):
        if viewport:
            sxp = int(self.get_xl(x))
            syp = int(self.get_yl(y))
        else:
            sxp = int(self._x_pixel(x))
            syp = int(self._y_pixel(y))
            
        self.pen.buf.append((_line_to_str,sxp,syp))
    
    def lineto(self, x,y):
        self._lineto(x,y)
    def llineto(self, x,y):
        self._lineto(x,y, True)
        
    def polygon(self, x, y, lcol=None, lthk=None, fcol=None, lpat=linepat._PAT_SOLID, viewport=False):
        if lpat == linepat._PAT_SOLID or fcol:
            self.fp.write("<polygon points=\"")
            if viewport:
                self.create_pnt_list(x,y,self.get_xl,self.get_yl)
            else:
                self.create_pnt_list(x,y,self._x_pixel,self._y_pixel)
                
            if lcol and fcol:
                if lpat == linepat._PAT_SOLID:
                    self.fp.write(_polygon_format_end%(\
                        lcol.r, lcol.g, lcol.b, self._svg_lthk(lthk),
                        fcol.r, fcol.g, fcol.b))
                else:
                    self.fp.write(_polygon_format_end_nostroke%(fcol.r, fcol.g, fcol.b))
            elif lcol and not isinstance(fcol,color.Color):
                self.fp.write(_polygon_format_end_nofill%(\
                    lcol.r, lcol.g, lcol.b, self._svg_lthk(lthk)))
            else:
                self.fp.write(_polygon_format_end_nostroke%(fcol.r, fcol.g, fcol.b))

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
            
            self.fp.write("<path d=\"")            
            for p1 in pat_seg:
                x1 = [ self.get_xl(p2[0]) for p2 in p1 ]
                y1 = [ self.get_yl(p2[1]) for p2 in p1 ]
                self._write_pathpoints(x1,y1)
            self.fp.write("\"\n"+_polygon_format_end_nofill%(\
                lcol.r, lcol.g, lcol.b, self._svg_lthk(lthk)))
            
    def polyline(self, x, y, lcol=None, lthk=None, lpat=linepat._PAT_SOLID, closed=False, viewport=False):
        if closed:
            if isinstance(x, np.ndarray):
                xp = np.append(x, x[0])
            elif isinstance(x, list):
                xp = x.copy()
                xp.append(x[0])
                
            if isinstance(y, np.ndarray):
                yp = np.append(y, y[0])
            elif isinstance(x, list):
                yp = y.copy()
                yp.append(y[0])
        else:
            xp = x
            yp = y
            
        if isinstance(lpat, linepat.LinePattern):
            self.fp.write("<path d=\"")
            if viewport:
                pat_seg = patline.get_pattern_line(self, xp, yp, lpat.pat_len, lpat.pat_t, viewport=True)
            else:
                pat_seg = patline.get_pattern_line(self, xp, yp, lpat.pat_len, lpat.pat_t)
                
            for p1 in pat_seg:
                x1 = [ self.get_xl(p2[0]) for p2 in p1 ]
                y1 = [ self.get_yl(p2[1]) for p2 in p1 ]
                self._write_pathpoints(x1,y1)
            self.fp.write("\"\n")
        else:
            self.fp.write("<polyline points=\"\n")
            if viewport:
                self.create_pnt_list(xp,yp,self.get_xl,self.get_yl)
            else:
                self.create_pnt_list(xp,yp,self._x_pixel,self._y_pixel)

        if self.pen:
            self.fp.write(_line_format_end%(\
                        self.pen.lcol.r, 
                        self.pen.lcol.g, 
                        self.pen.lcol.b,
                        self.pen.lthk))
        else:
            self.fp.write(_line_format_end%(\
                        lcol.r, 
                        lcol.g, 
                        lcol.b,
                        self._svg_lthk(lthk)))
                      
    def lpolygon(self, x, y, lcol=None, lthk=None, fcol=None, lpat=linepat._PAT_SOLID):
        self.polygon(x,y,lcol,lthk,fcol,lpat,viewport=True)

    def lpolyline(self, x, y, lcol=None, lthk=None, lpat=linepat._PAT_SOLID, closed=False):
        self.polyline(x,y,lcol,lthk,lpat,closed,viewport=True)
        
    def close(self):
        self.fp.write("</svg>")
        self.fp.close()
        