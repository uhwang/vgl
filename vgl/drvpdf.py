'''
    drvpdf.py
    
    Newline sould be 0x0A. Windows CR(0x0D), LF(0x0A) ==> 0x0A
    Object: 
        obj number generation number obj ==> ex) 2 0 obj
        indirect object (Referenct to obj) ==> 2 0 R
        
        Drawing line
            1 0 obj <</Length ...>>
            stream
            
            path construction: m, l, c, v, y, re
            Path painting: S, s, F, f, f*, B, B*, b, b*, n
            Clipping: W, W*
            Color: CS, cs, SC, SCN, sc, scn, G, g, RG, rg, K, k
            
        q : save DC
        Q : restore DC
        w : line width (non-neg num in user spc)
        J : line cap (butt(0)/round(1)/projecting square(2) cap)
        j : line join (miter(0)/round(1)/bevel(2) join)
        M : miter limit
        
        Line
        =========================
        m : move to  ex) x, y m
        l : line to  ex) x, y l
        h : close the path  ex) h
        
        Painting
        =========================
        S : stroke
        s : close and stroke = h S
        f : fill the path
        B : fill + stroke
        b : close, fill and stroke = h B
        
        Color
        =========================
        RG : set color
            
        Clipping
        =========================
        n : end of path w/o stroke, fill = path painting no-op
        W : modify the cur clipping path by intersecting it w/ the cur path, non-zero winding
        W*: 
        ex) W n
'''

from . import size
from . import color
from . import gdiobj

_pdf_header = "%PDF-1.7\n"
_points_inch = 72
_CTM = "1 0 0 -1 0 %3.4f cm\n"

class pdf_pen(gdiobj.Pen):
    def __init__(self):
        super().__init__()
        self.obj_index = 0
        self.buf = []
        
    def set_pen(self, lcol, lthk, obj_index):
        super().set_pen(lcol,lthk)
        self.obj_index = obj_index
        
class PDFDriver():
    def __init__(self, fname, gbbox, wid, hgt):
        self.start_obj_index = 3
        self.cur_obj_index = self.start_obj_index
        self.body=[]
        self.wid = wid
        self.hgt = hgt
        self.obj_list = {}
        self.file_size = 0
        self.cur_pen_index = 0
        self.pen = None
        self.clip_region = None
        self.gbbox = gbbox
        #self.prv_pen = bdiobj.Pen()
        self.fp = open(fname, "wb")
        #self.set_pdf(wid, hgt)
        
    def MakePen(self, lcol, lthk):
        self.cur_obj_index += 1
        lc = color.normalize(lcol)
        self.pen = pdf_pen()
        self.pen.set_pen(lc, lthk, self.cur_obj_index)

    def DeletePen(self):
        buffer_2_list = ["q\n"] #saveDC
        buffer_2_list.append(_CTM%(self.hgt*_points_inch))
        buffer_2_list.append("%1.4f %1.4f %1.4f RG\n"%(self.pen.lcol.r, self.pen.lcol.g, self.pen.lcol.b))
        buffer_2_list.append("%3.3f w\n"% self.pen.lthk)
        
        for p in self.pen.buf:
            buffer_2_list.append(p)
        buffer_2_list.append("S\nQ\n")
        buffer_2 = ''.join(buffer_2_list)
            
        buffer_1 = "%d 0 obj\n<</Length %d>>\nstream\n"%(self.pen.obj_index,len(buffer_2))
        buffer_3 = "endstream\nendobj\n"
        self.obj_list[self.cur_obj_index] = bytes(buffer_1+buffer_2+buffer_3,'utf-8')
        self.pen = None

    def MoveTo(self, x, y):
        self.pen.buf.append("%3.4f %3.4f m\n"%(x,y))
        
    def LineTo(self, x, y):
        self.pen.buf.append("%3.4f %3.4f l\n"%(x,y))
        
    def Line(self, sx, sy, ex, ey, lcol=None, lthk=None):
        xx = [sx, ex]
        yy = [sy, ey]
        self.Polyline(xx,yy,lcol,lthk,None,False)

    def Polyline(self, x, y, lcol, lthk, fcol, closed=False):
        self.cur_obj_index += 1
        lc = color.normalize(lcol) if lcol else lcol
        fc = color.normalize(fcol) if fcol else fcol
        buffer_2_list = ["q\n"] #saveDC
        buffer_2_list.append(_CTM%(self.hgt*_points_inch))
        
        if self.clip_region:
            #buffer_2_list.append("%3.4f %3.4f %3.4f %3.4f re n W\n"%\
            buffer_2_list.append("W\n%3.4f %3.4f %3.4f %3.4f re\nh\nn\nW\n"%\
                                (self.clip_region.sx,
                                 self.clip_region.sy,
                                 self.clip_region.ex,
                                 self.clip_region.ey))
        
        if lcol:
            buffer_2_list.append("%1.4f %1.4f %1.4f RG\n"%(lc.r, lc.g, lc.b))
            buffer_2_list.append("%3.3f w\n"%lthk)
        
        if fcol:
            buffer_2_list.append("%1.4f %1.4f %1.4f rg\n"%(fc.r, fc.g, fc.b))
            
        buffer_2_list.append("%3.3f %3.3f m\n"%(x[0],y[0]))
        
        for x1, y1 in zip(x[1:],y[1:]):
            buffer_2_list.append("%3.3f %3.3f l\n"%(x1,y1))
        
        if closed:
            if lcol and fcol:
                buffer_2_list.append("b\nQ\n") # close, fill, stroke and restore DC
            elif not isinstance(lcol, color.Color) and fcol:
                buffer_2_list.append("f\nQ\n") # close, fill, and restore DC
            else:
                buffer_2_list.append("s\nQ\n") # close, stroke and restore DC
        else:
            buffer_2_list.append("S\nQ\n")     # stroke and restoreDC
            
        buffer_2 = ''.join(buffer_2_list)
        buffer_1 = "%d 0 obj\n<</Length %d>>\nstream\n"%(
                    self.cur_obj_index,
                    len(buffer_2))
        buffer_3 = "endstream\nendobj\n"
        self.obj_list[self.cur_obj_index] = bytes(buffer_1+buffer_2+buffer_3,'utf-8')
        
    def Polygon(self, x, y, lcol, lthk, fcol):
        self.Polyline(x,y,lcol,lthk,fcol,True)
        
    def Close(self):
        ex = self.wid*_points_inch
        ey = self.hgt*_points_inch
        obj1 = "1 0 obj\n<< /Type /Catalog /Pages 2 0 R>>\nendobj\n"
        obj2 = "2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1>>\nendobj\n"
        obj3_list = ["3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n"\
                     "/MediaBox [%3.4f %3.4f %3.4f %3.4f]\n"\
                     #"/CropBox[%3.4f %3.4f %3.4f %3.4f]\n"\
                     "/Contents [\n"%\
                     #"/MediaBox [%3.4f %3.4f %3.4f %3.4f]\n/Contents [\n"%\
                     #(self.gbbox.sx*_points_inch, 
                     # self.gbbox.sy*_points_inch, 
                     # self.gbbox.ex*_points_inch, 
                     # self.gbbox.ey*_points_inch)]
                     #(0, 0, ex, ey)]
                      (0, 0, ex, ey)]
        r_list = ""
        for i, k in enumerate(self.obj_list.keys()):
                r_list += "%d 0 R "%k
                if i%4 == 0:
                    r_list += "\n"
        obj3_list.append(r_list)
        obj3_list.append("]\n>>\nendobj\n")
        #obj3_list.append("]\n1 -1 scale\n0 %d translate>>\nendobj\n"%
        #                int(self.hgt*_points_inch))
        #obj3_list.append("]\n1 0 0 -1 0 %d cm>>\nendobj\n"%
        #                int(self.hgt*_points_inch))
        obj3 = "".join(obj3_list)
        
        self.file_size = 0
        self.fp.write(bytes(_pdf_header,'utf-8'))
        self.file_size += len(_pdf_header)
        obj_pos = [self.file_size]   
        
        obj_index = 1
        self.fp.write(bytes(obj1,'utf-8'))
        self.file_size += len(obj1)
        obj_pos.append(self.file_size)
        
        obj_index += 1
        self.fp.write(bytes(obj2,'utf-8'))
        self.file_size += len(obj2)
        obj_pos.append(self.file_size)
        
        obj_index += 1
        self.fp.write(bytes(obj3,'utf-8'))
        self.file_size += len(obj3)
        obj_pos.append(self.file_size)        

        for k, v in self.obj_list.items():
            self.fp.write(v)
            self.file_size += len(v)
            obj_pos.append(self.file_size)
            
        start_xref = self.file_size
        nobj = len(obj_pos)+1
        self.fp.write(bytes("xref\n0 %d\n0000000000 65535 f\n"%nobj,'utf-8'))
        for v in obj_pos:
            self.fp.write(bytes("%010d 00000 n\n"%(v),'utf-8'))
            
        self.fp.write(bytes("trailer<<Size %d/Root 1 0 R>>\n"%len(self.obj_list),'utf-8'))
        self.fp.write(bytes("startxref\n%d\n"%start_xref,'utf-8'))
        self.fp.write(bytes("%%EOF",'utf-8'))
        self.fp.close()
        
    def CreateClip(self, sx, sy, ex, ey):
        #pass
        #self.cur_obj_index += 1
        self.clip_region = size.BBox(sx,sy,ex,ey)
        #self.clip = True
        #buffer_2 = "q\n%3.4f %3.4f %3.4f %3.4f re\nW\n"
        #buffer_1 = "%d 0 obj\n<</Length %d>>\nstream\n"%(
        #            self.cur_obj_index,
        #            len(buffer_2))
        #buffer_3 = "endstream\nendobj\n"
        #self.obj_list[self.cur_obj_index] = bytes(buffer_1+buffer_2+buffer_3,'utf-8')
        
    def DeleteClip(self):
        #pass
        self.clip_region = None
        #self.cur_obj_index += 1
        #buffer_2 = "Q\n"
        #buffer_1 = "%d 0 obj\n<</Length %d>>\nstream\n"%(
        #            self.cur_obj_index,
        #            len(buffer_2))
        #buffer_3 = "endstream\nendobj\n"
        #self.obj_list[self.cur_obj_index] = bytes(buffer_1+buffer_2+buffer_3,'utf-8')
        
    
      
   