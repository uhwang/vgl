# Vector Graphic Library (VGL) for Python
#
# text.py
#
# 2020-2-12 Ver 0.1
#
# Author: Uisang Hwang
# Email : uhwangtx@gmail.com
#

from .font import romans
import math
import numpy as np
import vgl.color as color
from vgl.size import BBox
import vgl.rotation
import vgl.fontid as fontid
import vgl.fontm as fontm

to_rad = 3.1415926535/180
#void TG_TextOut(TG_Device_Ptr dev, TG_StrPtr str, TG_Float x, TG_Float y, TG_UShort align, TG_Float lthk, TG_Color fc, TG_Color lc)

TEXT_ALIGN_VCENTER   = 0x0001
TEXT_ALIGN_LEFT      = 0x0002
TEXT_ALIGN_RIGHT     = 0x0004
TEXT_ALIGN_TOP       = 0x0008
TEXT_ALIGN_BOTTOM    = 0x0010
TEXT_ALIGN_HCENTER   = 0x0020
TEXT_BOX             = 0X0040
TEXT_FILLEDBOX       = 0X0080

STD_FONT_HEIGHT        = 21.0
STD_FONT_TOP_OFFSET    = 12
STD_FONT_BOTTOM_OFFSET =  9
TEXT_DROP              =  2 

IS_BOX       = lambda a: (a)&TEXT_BOX
IS_FILLEDBOX = lambda a: (a)&TEXT_FILLEDBOX

IS_LEFT      = lambda a: (a)&TEXT_ALIGN_LEFT   
IS_RIGHT     = lambda a: (a)&TEXT_ALIGN_RIGHT   
IS_HCENTER   = lambda a: (a)&TEXT_ALIGN_HCENTER

IS_TOP       = lambda a: (a)&TEXT_ALIGN_TOP    
IS_BOTTOM    = lambda a: (a)&TEXT_ALIGN_BOTTOM 
IS_VCENTER   = lambda a: (a)&TEXT_ALIGN_VCENTER

class Font():
    def __init__(self, fid=fontid.FONT_ROMANSIMPLEX, size=0.05,\
                    lcol = color.BLACK, lthk=0.001, align = TEXT_ALIGN_BOTTOM):
        self.font_name = fontm.font_manager.get_font_name(fid)
        self.font_id   = fid
        self.size      = size
        self.lcol      = lcol
        self.lthk      = lthk
        self.align     = align
        self.show_box  = False
        self.fill_box  = False
        self.box_lcol  = color.BLACK
        self.box_fcol  = color.WHITE
        self.box_lthk  = 0.001
        
    def set_size(self, size): self.size = sz
    #def set_halign_center(self): self.align = 

class Text(Font):
    def __init__(self, x=0, y=0, text=''):
        super().__init__()
        self.x     = x
        self.y     = y
        self.text  = text
        self.rotation = 0
        #self.moveto= moveto
        #self.lineto= lineto
        #self.polyline = polyline
        #self.polygon  = polygon
        #self.rotation = rotation
        
    def set_text(self, x, y, text):
        self.x     = x
        self.y     = y
        self.text  = text
    '''
        E(ast) : LEFT
        W(est) : RIGHT
        N(orth): TOP
        S(outh): BOTTOM
        V(center), H(center)
    '''
    def wv(self): self.align = TEXT_ALIGN_LEFT|TEXT_ALIGN_VCENTER
    def wn(self): self.align = TEXT_ALIGN_LEFT|TEXT_ALIGN_TOP
    def ws(self): self.align = TEXT_ALIGN_LEFT|TEXT_ALIGN_BOTTOM
    def ev(self): self.align = TEXT_ALIGN_RIGHT|TEXT_ALIGN_VCENTER
    def en(self): self.align = TEXT_ALIGN_RIGHT|TEXT_ALIGN_TOP 
    def es(self): self.align = TEXT_ALIGN_RIGHT|TEXT_ALIGN_BOTTOM
    #def nv(self): self.align = TEXT_ALIGN_TOP|TEXT_ALIGN_VCENTER
    #def ne(self): self.align = TEXT_ALIGN_TOP|TEXT_ALIGN_LEFT
    #def nw(self): self.align = TEXT_ALIGN_TOP|TEXT_ALIGN_RIGHT
    #def sv(self): self.align = TEXT_ALIGN_BOTTOM|TEXT_ALIGN_VCENTER
    #def se(self): self.align = TEXT_ALIGN_BOTTOM|TEXT_ALIGN_LEFT
    #def sw(self): self.align = TEXT_ALIGN_BOTTOM|TEXT_ALIGN_RIGHT
    def hv(self): self.align = TEXT_ALIGN_HCENTER|TEXT_ALIGN_VCENTER
    def hn(self): self.align = TEXT_ALIGN_HCENTER|TEXT_ALIGN_TOP
    def hs(self): self.align = TEXT_ALIGN_HCENTER|TEXT_ALIGN_BOTTOM

class Point():
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
        
def write_text(dev, t, viewport=True):
    SHIFT_FACTOR = 1.2;
    ich=0 
    ias=0 
    ivt=0 
    chwid=0 
    chhgt=0 
    nvert=0 
    moveto=0
    nstr=0 
    px=0 
    py=0
    ccos = math.cos(t.rotation*to_rad)
    csin = math.sin(t.rotation*to_rad)
    
    if viewport:
        curx=t.x 
        cury=t.y 
    else:
        curx=dev._x_viewport(t.x)
        cury=dev._y_viewport(t.y) 
    rx=0.0 
    ry=0.0 
    cx=0.0 
    cy=0.0 
    tx=0.0 
    ty=0.0
    
    #TG_Float 
    scale=0.0 
    max_y=0.0 
    max_x=0.0 
    delx =0.0 
    dely =0.0 
    #xx=np.zeros(5)
    #yy=np.zeros(5)
    ll=Point(0.0,0.0) 
    rt=Point(0.0,0.0)
    box = [Point]*5
    
    if t.text == '': return
    
    if t.font_id == fontid.FONT_CURSIVE or \
    t.font_id == fontid.FONT_SCRIPTCOMPLEX or \
    t.font_id == fontid.FONT_SCRIPTSIMPLEX:
        SHIFT_FACTOR=1.0
    
    nstr = len(t.text)
    curx = 0
    cury = 0
    scale = 1./STD_FONT_HEIGHT*t.size*dev.frm.hgt();
    fbox = BBox(-1000, 1000, -1000, -1000)
    
    clist = []
    font_map = fontm.font_manager.get_font_map(t.font_id)
    
    for ich in range(nstr):
        #glyp  = romans.font_map[ord(t.text[ich])-ord(' ')]
        glyp = font_map[ord(t.text[ich])-ord(' ')]
        npnt  = glyp[0]
        prs   = glyp[1]
        bbox  = glyp[2] # ll(x,y), rt(x,y)
        chwid = bbox[1][0] - bbox[0][0]
        
        nvert = npnt
        llist = []
        xp  = []
        yp  = []
        nline = 0
        for ivt in range(nvert):
            pp = prs[ivt]
            px = pp[0]
            py = pp[1]
            
            if px==-1 and py==-1:
                llist.append((xp,yp))
                xp = []
                yp = []
                continue
            else:
                cx = px*scale;
                cy = (py+TEXT_DROP)*scale
                #rx = cx*ccos-cy*csin
                #ry = cx*csin+cy*ccos
                #tx = curx+rx+scale*(chwid*0.5)*ccos
                #ty = cury+ry
                rx = cx
                ry = cy#*y_reverse
                tx = curx+rx+scale*(chwid*0.5)
                ty = cury+ry
                if fbox.sy > ty: fbox.sy = ty
                if fbox.ey < ty: fbox.ey = ty
                xp.append(tx)
                yp.append(ty)
        
        if len(xp) != 0:
            llist.append((xp,yp))
        clist.append(llist)
        
        chwid = 2 if chwid == 2 else chwid
        #delx = chwid*ccos*SHIFT_FACTOR*scale
        #dely = chwid*csin*SHIFT_FACTOR*scale
        delx = chwid*SHIFT_FACTOR*scale
        dely = 0
        curx += delx
        cury += dely
    
    el = clist[-1]
    for l in el: ex = max(l[0])
    fbox.sx = 0
    fbox.ex = ex
    
    #fbox.expand(min(fbox.hgt(), fbox.wid())*0.05)
    dx = 0
    dy = 0
    # default align is Left & Vcenter
    #if IS_LEFT   (t.align): dx =  fbox.wid()
    fhgt = fbox.hgt()*0.5
    if IS_RIGHT  (t.align): dx = -fbox.wid()
    if IS_HCENTER(t.align): dx = -fbox.wid()*0.5
    if IS_TOP    (t.align): dy = -fhgt if dev.iscartesian() else fhgt
    if IS_BOTTOM (t.align): dy =  fhgt if dev.iscartesian() else -fhgt
    
    fthk = t.lthk*dev.frm.hgt()
    bthk = t.box_lthk*dev.frm.hgt()
    if t.show_box or t.fill_box:
        if t.rotation != 0:
            x1 = fbox.sx*ccos-fbox.sy*csin
            y1 = fbox.sx*csin+fbox.sy*ccos
            x2 = fbox.ex*ccos-fbox.ey*csin
            y2 = fbox.ex*csin+fbox.ey*ccos
            fbox.set_bbox(x1,y1,x2,y2)
        fbox.transx(dx)
        fbox.transy(dy)
        if viewport:
            curx = t.x
            cury = t.y
        else:
            curx = dev._x_viewport(t.x)
            cury = dev._y_viewport(t.y)
            
        #fbox.trans(t.x,t.y)
        fbox.trans(curx,cury)
        if t.fill_box:
            dev.lpolygon(fbox.get_xs(), fbox.get_ys(), None, None, t.box_fcol)
        if t.show_box:
            dev.lpolyline(fbox.get_xs(), fbox.get_ys(), t.box_lcol, bthk, True)
    
    #dev.make_pen(t.lcol, fthk)
    for ll in clist:
        for ls in ll:
            #xx = np.array(ls[0])
            #yy = np.array(ls[1])
            if viewport:
                xx = np.array(ls[0])
                yy = np.array(ls[1])
            else:
                xx = dev._x_viewport(np.array(ls[0]))
                yy = dev._y_viewport(np.array(ls[1]))
            
            if t.rotation != 0:
                for i in range(xx.size):
                    xs = xx[i]*ccos-yy[i]*csin
                    ys = xx[i]*csin-yy[i]*ccos
                    xx[i] = xs
                    yy[i] = ys
            if viewport:
                xx += dx + t.x
                yy += dy + t.y
            else:
                xx += dx + dev._x_viewport(t.x)
                yy += dy + dev._y_viewport(t.y)
            #t.polyline(xx,yy)
            dev.lpolyline(xx,yy,t.lcol, fthk)
    #dev.delete_pen()