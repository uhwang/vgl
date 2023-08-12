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
import vgl.symtbl as sym_search

from . import util
from . import vertex

to_rad = 3.1415926535/180
#void TG_TextOut(TG_Device_Ptr dev, TG_StrPtr str, TG_Float x, TG_Float y, TG_UShort align, TG_Float lthk, TG_Color fc, TG_Color lc)


ESCAPE = "\\"

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
    def __init__(self, 
                 fid      = fontid.FONT_ROMANSIMPLEX, 
                 size     = 0.05,
                 lcol     = color.BLACK, 
                 lthk     = 0.001, 
                 align    = TEXT_ALIGN_BOTTOM,
                 show_box = False,
                 fill_box = False,
                 box_lcol = color.BLACK,
                 box_lthk = 0.001,
                 box_fcol = color.WHITE
                ):
                
        self.font_name = fontm.font_manager.get_font_name(fid)
        self.font_id   = fid
        self.size      = size
        self.lcol      = lcol
        self.lthk      = lthk
        self.align     = align
        self.show_box  = show_box
        self.fill_box  = fill_box
        self.box_lcol  = box_lcol
        self.box_lthk  = box_lthk
        self.box_fcol  = box_fcol

    def set_font(self, fid):
        self.font_name = fontm.font_manager.get_font_name(fid)
        self.font_id   = fid
        
    def set_size(self, size): self.size = sz
    #def set_halign_center(self): self.align = 

class Text(Font):
    def __init__(self, 
                 x        = 0, 
                 y        = 0, 
                 text     = '', 
                 deg      = 0,
                 size     = 0.05,
                 lcol     = color.BLACK, 
                 lthk     = 0.001, 
                 align    = TEXT_ALIGN_BOTTOM,
                 show_box = False,
                 fill_box = False,
                 box_lcol = color.BLACK,
                 box_lthk = 0.001,
                 box_fcol = color.WHITE
                ):
        super().__init__( size     = size,
                          lcol     = lcol,
                          lthk     = lthk,
                          align    = align,
                          show_box = show_box,
                          fill_box = fill_box,
                          box_lcol = box_lcol,
                          box_lthk = box_lthk,
                          box_fcol = box_fcol)
        self.x     = x
        self.y     = y
        self.text  = text
        self.deg   = deg

    def __str__(self):
        return "x   : %f\n"\
               "y   : %f\n"\
               "text: %s\n"\
               "deg : %f\n"\
               "lcol: %s\n"\
               "lthk: %f\n"%\
               (self.x, self.y, self.text, self.deg, str(self.lcol), self.lthk)
               
    def set_text(self, x, y, text, deg=0, lcol=color.BLACK, lthk=0.001):
        self.x    = x
        self.y    = y
        self.text = text
        self.deg  = deg
        self.lcol = lcol
        self.lthk = lthk
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

def get_next_token(txt, idx):
    i_token = 0
    for s in txt[idx:]:
        if s.isspace() == True: break
        i_token += 1
    return txt[idx:idx+i_token], i_token
    
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
    end_x = 0

    non_escape = True
    
    while ich < nstr:
        if t.text[ich] == ESCAPE:
            token, i_token = get_next_token(t.text, ich)
            glyp = sym_search.get_symbol_glyp(token)
            if glyp:
                ich += i_token
                non_escape = False
            else:
                non_escape = True
        if non_escape:
            glyp = font_map[ord(t.text[ich])-ord(' ')]
            ich += 1
            
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
                if xp and yp:
                    llist.append([xp,yp])
                xp = []
                yp = []
                continue
            else:
                cx = px*scale;
                cy = (py+TEXT_DROP)*scale
                tx = curx+cx+scale*(chwid*0.5)
                ty = cury+cy
                if fbox.sy > ty: fbox.sy = ty
                if fbox.ey < ty: fbox.ey = ty
                xp.append(tx)
                yp.append(ty)
        
        if len(xp) != 0:
            llist.append([xp,yp])
        clist.append(llist)
        
        chwid = 2 if chwid == 2 or chwid == 0 else chwid
        delx = chwid*SHIFT_FACTOR*scale
        dely = 0
        curx += delx
        cury += dely
    
    fbox.sx = 0
    fbox.ex = curx
    
    dx = 0
    dy = 0
    # default align is Left & Vcenter
    #if IS_LEFT   (t.align): dx =  fbox.wid()
    fhgt = fbox.hgt()*0.5
    if IS_RIGHT  (t.align): dx = -fbox.wid()
    if IS_HCENTER(t.align): dx = -fbox.wid()*0.5
    if IS_TOP    (t.align): dy =  fhgt
    if IS_BOTTOM (t.align): dy = -fhgt
    
    fthk = t.lthk
    bthk = t.box_lthk
    
    bvtx = vertex.Vertex(5)
    bvtx.set_vertex(0, fbox.sx, fbox.sy)
    bvtx.set_vertex(1, fbox.sx, fbox.ey)
    bvtx.set_vertex(2, fbox.ex, fbox.ey)
    bvtx.set_vertex(3, fbox.ex, fbox.sy)
    bvtx.set_vertex(4, fbox.sx, fbox.sy)
    
    if t.show_box or t.fill_box:
        if t.deg != 0:
            bvtx.rotate(t.deg)
        bvtx.trans(dx,dy)
        if viewport:
            curx = t.x
            cury = t.y
        else:
            curx = dev._x_viewport(t.x)
            cury = dev._y_viewport(t.y)
            
        bvtx.trans(curx,cury)
        if t.fill_box:
            dev.lpolygon(bvtx.get_xs(), bvtx.get_ys(), None, None, t.box_fcol)
        if t.show_box:
            dev.lpolyline(bvtx.get_xs(), bvtx.get_ys(), t.box_lcol, bthk, True)
    
    if t.deg != 0:
        for ll in clist:
            for ls in ll:
                r = util.deg_rotation(ls[0], ls[1], t.deg)
                ls[0], ls[1] = r[0], r[1]

    for ll in clist:
        for ls in ll:
            if viewport:
                xx = np.array(ls[0])
                yy = np.array(ls[1])
            else:
                xx = np.array([dev._x_viewport(x1) for x1 in ls[0]])
                yy = np.array([dev._x_viewport(y1) for y1 in ls[1]])
            
            if viewport:
                xx += dx + t.x
                yy += dy + t.y
            else:
                xx += dx + dev._x_viewport(t.x)
                yy += dy + dev._y_viewport(t.y)
            dev.lpolyline(xx,yy,t.lcol, fthk)
