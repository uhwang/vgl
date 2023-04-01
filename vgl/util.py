# util.py

from . import mesh3d
#import mesh3d

vgl_pi = 3.141592653589793238
vgl_dtr= vgl_pi/180
vgl_rtd= 180/vgl_pi

deg_to_rad = lambda d: d*vgl_dtr
rad_to_deg = lambda r: r*vgl_rtd

class Pygame3DUtil():
    def __init__(self, dev=None):
        self.dev           = dev
        self.lbutton       = False
        self.buttons       = (False, False, False)
        self.move          = False
        self.trans         = False
        self.show_axis     = False
        self.show_surfnorm = False
        self.scale         = 1
        self.old_pos       = (0,0)
        self.new_pos       = (0,0)
        self.cur_view_mode = mesh3d.MESH_WIREFRAME
        self.prv_view_mode = mesh3d.MESH_WIREFRAME
        self.xrotation     = 0
        self.yrotation     = 0
        self.shade         = False
        
        if dev:
            self.set_util(dev)
            
    def set_util(self, dev):
        if not self.dev: self.dev = dev
        self.screen_scale = self.dev.gwid/self.dev.gbbox.wid()
        self.set_scale_factor()

    def get_scale_amount(self):
        diffy = self.new_pos[1]-self.old_pos[1]
        if diffy!=0:
            if diffy<0: self.scale += self.fscale
            if diffy>0: self.scale -= self.fscale
        return self.scale

    # compute before program begin
    def get_trans_amount(self):
        p1 = self.old_pos
        p2 = self.new_pos
        ff = self.dev.frm
        dd = self.dev.frm.data
        
        lsx = ff.bbox.wid()/dd.get_xrange()
        lsy = ff.bbox.hgt()/dd.get_yrange()
        #dx  = (sx-ex)/screen_scale/lsx
        #dy  = (ey-sy)/screen_scale/lsy
        dx = (p1[0]-p2[0])/self.screen_scale/lsx
        dy = (p2[1]-p1[1])/self.screen_scale/lsx
        return dx, dy

    def set_scale_factor(self):
        xw = self.dev.frm.data.get_xrange()
        yw = self.dev.frm.data.get_yrange()
        zw = self.dev.frm.data.get_zrange()
        minw = min(min(xw,yw),zw)
        self.fscale = minw*0.08
