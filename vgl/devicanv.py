'''
    devicanv.py
    
    03/10/2023  Separate device file

'''

from ipycanvas import Canvas        
from . import color
from . import device
from . import linepat
from . import patline
        
class DeviceIPycanvas(device.DeviceRaster):
    def __init__(self, gbox, dpi):
        super().__init__(gbox, dpi)
        self.pen   = Pen()
        self.prv_pen = device.Pen()
        self.brush = device.Brush()
        self.pos   = device.Position(0,0)
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
        self.points= [[convx(x1), convy(y1)] for x1, y1 in zip(x,y)]
            
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
       