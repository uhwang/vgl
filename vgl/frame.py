# Vector Graphic Library (VGL) for Python
#
# frame.py
#
# 2020-2-12 Ver 0.1
#
# Author: Uisang Hwang
# Email : uhwangtx@gmail.com
#
#  +-----------------+  
#  |     HEADER      |
#  +-----------------+
#  |     MARGIN      |
#  |    +=======+    |
#  |    |       |    |
#  |    | PDOM  |    | PDOM: plot domain
#  |    |       |    |
#  |    +=======+    |
#  |                 |
#  +-----------------+
#

from vgl.size import BBox, Rect
from vgl.data import Data
import vgl.color as color
import vgl.vertex as vertex
import vgl.axis as axis
import vgl.text as text

default_plot_domain_xmargin = 0.09
default_plot_domain_ymargin = 0.09

class FrameProperty():
    def __init__(self, col=color.RED):
        self.header_show = True 
        self.header_thk  = 0.03
        self.header_col  = col
        self.border_show = True
        self.border_col  = color.BLACK
        self.border_thk  = 0.001
        self.bk_color    = color.WHITE
        self.bk_show     = True
        self.pdombk_show = True
        self.pdombk_lshow= True
        self.pdombk_lcol = color.BLACK
        self.pdombk_fcol = color.WHITE
        self.pdombk_lthk = 0.001
		
class Frame():
    def __init__(self, id, sx, sy, wid, hgt, data=None):
        self.id   = id
        #self.view_mode = 
        self.fvtx = vertex.Vertex(4)          # frame vertex
        self.pvtx = vertex.Vertex(4)          # plot domain vertex
        self.bbox = BBox(sx,sy,sx+wid,sy+hgt) # frame Bounding Box
        self.data = data                      # data to plot
        self.pdom = Rect()                    # plot domain size
        self.fprt = FrameProperty()           # frame properties (border, bk, ...)
        
        # xy mode
        #self.xaxis1 = 
        #self.yaxis1 = 
        
        # 2d mode
        #self.xaxis2 = 
        #self.yaxis2 = 
   
        # 3d mode
        #self.xaxis3 = 
        #self.yaxis3 = 
        #self.zaxis3 = 
        
        if data is not None:
            xrange = data.get_xrange()
            yrange = data.get_yrange()
            xmin = data.xmin
            ymin = data.ymin
            xmax = data.xmax
            ymax = data.ymax
            
            xscal = wid/xrange
            yscal = hgt/yrange
            
            minscl = min(xscal, yscal)
            wid1 = xrange*minscl
            hgt1 = yrange*minscl
            wid2 = wid-wid1
            hgt2 = hgt-hgt1

            if wid2 > 0.05:
                xmax += wid2/minscl
                
            if hgt2 > 0.05:
                ymax += hgt2/minscl
                
            #print(hgt, hgt1, hgt2, ymax)                
            self.xaxis = axis.Axis(xmin, xmax)# x axis
            self.yaxis = axis.Axis(ymin, ymax)# y axis
            self.xaxis.label.hn()
            self.yaxis.label.wv()
            
            #self.xaxis.xlabel.hn()
            #self.yaxis.ylabel.wv()
        self.update_pdom()                    # compute plot domain vertex
        self.update_vertex()                  # compute frame vertex
   
    def update_vertex(self):
        self.fvtx.set_vertex(0, self.bbox.sx, self.bbox.sy)
        self.fvtx.set_vertex(1, self.bbox.sx, self.bbox.ey)
        self.fvtx.set_vertex(2, self.bbox.ex, self.bbox.ey)
        self.fvtx.set_vertex(3, self.bbox.ex, self.bbox.sy)
        
    def get_clip    (self):                   # clip region is equal to plot domain
        return self.pvtx.get_vertex(0)+self.pvtx.get_vertex(2)
        
    def get_frm_xs  (self): return self.fvtx.get_xs() # frame vertex x-coordinates
    def get_frm_ys  (self): return self.fvtx.get_ys() # frame vertex y-coordinates
    def get_pdom_xs (self): return self.pvtx.get_xs() # plot domain vertex x-coordinates
    def get_pdom_ys (self): return self.pvtx.get_ys() # plot domain vertex y-coordinates
    def hgt         (self): return self.bbox.hgt()    # return frame height
    def wid         (self): return self.bbox.wid()    # return frame width
    def get_property(self): return self.fprt
    def get_xaxis   (self): return self.xaxis
    def get_yaxis   (self): return self.yaxis
    def get_pdom_wid(self): return self.pdom.wid
    def get_pdom_hgt(self): return self.pdom.hgt
    def update_pdom (self, xm=default_plot_domain_xmargin, 
                        ym=default_plot_domain_ymargin):
        wid = self.bbox.wid()
        hgt = self.bbox.hgt()
        self.pdom.sx  = wid*xm
        self.pdom.sy  = hgt*ym
        self.pdom.wid = wid*(1.-2*xm)
        self.pdom.hgt = hgt*(1.-2*ym)
        sx = self.bbox.sx+self.pdom.sx
        sy = self.bbox.sy+self.pdom.sy
        ex = sx+self.pdom.wid
        ey = sy+self.pdom.hgt
        self.pvtx.set_vertex(0, sx, sy)
        self.pvtx.set_vertex(1, sx, ey)
        self.pvtx.set_vertex(2, ex, ey)
        self.pvtx.set_vertex(3, ex, sy)
   
    def set_headershow(self, show): self.fprt.header_show = show
    def set_bordershow(self, show):	self.fprt.border_show = show
    def show_header   (self): self.fprt.header_show = True
    def show_border   (self): self.fprt.border_show = True
    def hide_header   (self): self.fprt.header_show = False
    def hide_border   (self): self.fprt.border_show = False
    def translate_xy  (self, dx, dy):
        self.data.trans(dx,dy,0)
        self.xaxis.update_tick(self.data.xmin, self.data.xmax)
        self.yaxis.update_tick(self.data.ymin, self.data.ymax)
       
    def hide_all_axis(self):
        self.hide_xaxis()
        self.hide_yaxis()
        
    def show_all_axis(self):
        self.show_xaxis()
        self.show_yaxis()

    def show_xaxis(self):
        self.xaxis.show = True
    def hide_xaxis(self):
        self.xaxis.show = False
    def show_yaxis(self):
        self.yaxis.show = True
    def hide_yaxis(self):
        self.yaxis.show = False
        
    def show_all_tick(self):
        self.show_xtick()
        self.show_ytick()
        
    def show_all_grid(self):
        self.show_xgrid()
        self.show_ygrid()

    def show_all_major_grid(self):
        self.show_xmajor_grid()
        self.show_ymajor_grid()
        
    def hide_all_major_grid(self):
        self.hide_xmajor_grid()
        self.hide_ymajor_grid()
        
    def show_all_minor_grid(self):
        self.show_xminor_grid()
        self.show_yminor_grid()
        
    def hide_all_minor_grid(self):
        self.hide_xminor_grid()
        self.hide_yminor_grid()
        
    def hide_all_tick(self):
        self.hide_xtick()
        self.hide_ytick()
        
    def hide_all_grid(self):
        self.hide_xgrid()
        self.hide_ygrid()

    def set_xmajor_tick_show(self, show):
        self.xaxis.major_tick.show = show
        
    def set_xminor_tick_show(self, show):
        self.xaxis.minor_tick.show = show

    def set_xmajor_grid_show(self, show):
        self.xaxis.major_grid.show = show

    def set_xminor_grid_show(self, show):
        self.xaxis.minor_grid.show = show
        
    def hide_xtick(self):
        self.hide_major_tick()
        self.hide_minor_tick()

    def show_xtick(self):
        self.show_major_tick()
        self.show_minor_tick()
        
    def hide_xgrid(self):
        self.hide_xmajor_grid()
        self.hide_xminor_grid()

    def show_xgrid(self):
        self.show_xmajor_grid()
        self.show_xminor_grid()
        
    def hide_xmajor_tick(self):
        self.xaxis.major_tick.show = False
        
    def hide_xminor_tick(self):
        self.xaxis.minor_tick.show = False

    def hide_xmajor_grid(self):
        self.xaxis.major_grid.show = False
        
    def hide_xminor_grid(self):
        self.xaxis.minor_grid.show = False
        
    def show_xmajor_tick(self):
        self.xaxis.major_tick.show = True
        
    def show_xminor_tick(self):
        self.xaxis.minor_tick.show = True

    def show_xmajor_grid(self):
        self.xaxis.major_grid.show = True
        
    def show_xminor_grid(self):
        self.xaxis.minor_grid.show = True
        
    def set_ymajor_tick_show(self, show):
        self.yaxis.major_tick.show = show
        
    def set_yminor_tick_show(self, show):
        self.yaxis.minor_tick.show = show

    def set_ymajor_grid_show(self, show):
        self.yaxis.major_grid.show = show

    def set_yminor_grid_show(self, show):
        self.yaxis.minor_grid.show = show
        
    def hide_ytick(self):
        self.hide_ymajor_tick()
        self.hide_yminor_tick()

    def show_ytick(self):
        self.show_ymajor_tick()
        self.show_yminor_tick()
        
    def show_ygrid(self):
        self.show_ymajor_grid()
        self.show_yminor_grid()

    def hide_ygrid(self):
        self.hide_ymajor_grid()
        self.hide_yminor_grid()
        
    def hide_ymajor_tick(self):
        self.yaxis.major_tick.show = False
        
    def hide_yminor_tick(self):
        self.yaxis.minor_tick.show = False

    def hide_ymajor_grid(self):
        self.yaxis.major_grid.show = False
        
    def hide_yminor_grid(self):
        self.yaxis.minor_grid.show = False
        
    def show_ymajor_tick(self):
        self.yaxis.major_tick.show = True
        
    def show_yminor_tick(self):
        self.yaxis.minor_tick.show = True

    def show_ymajor_grid(self):
        self.yaxis.major_grid.show = True
        
    def show_yminor_grid(self):
        self.yaxis.minor_grid.show = True
	
class FrameId():
    def __init__(self):
        self.id_pool = []
        self.id = []
        self.cur_id = 0
    
    def get(self):
        new_id = 0
        if len(self.id_pool) is 0:
            new_id = self.cur_id
            self.id.append(self.cur_id)
            self.cur_id += 1
        else:
            self.cur_id = self.id_pool.pop()
            self.id.append(self.cur_id)
            new_id = self.cur_id
        return new_id
    
    def find(self, id):
        return id in self.id
        
    def remove(self, id):
        if self.find(id):
            self.id_pool.append(id)
            self.id.remove(id)
        
_find_frame  = lambda self,id: self.f_list[str(id)] if self.id.find(id) else None
_get_clip    = lambda self,id: self.f_list[str(id)].get_clip() if self.id.find(id) else None

class FrameManager():
    def __init__(self):
        self.f_list = dict()
        self.id = FrameId()
        
    def create(self, sx, sy, wid, hgt, data):
        id = self.id.get()
        frm = Frame(id, sx, sy, wid, hgt, data)
        self.f_list[str(id)] = frm
        return frm
        
    def delete(self, id):
        if self.id.find(id):
            self.id.remove(id)
            del self.f_list[str(id)]
            
    def get     (self, id): return _find_frame(self,id)
    def get_clip(self, id):	return _get_clip(self,id)
    def get_gbbox(self):
        sx=1000
        sy=1000
        ex=-1000
        ey=-1000
        
        for i in range(len(self.id.id)):
            bbox = self.f_list[str(self.id.id[i])].bbox
            if sx > bbox.sx: sx = bbox.sx
            if sy > bbox.sy: sy = bbox.sy
            if ex < bbox.ex: ex = bbox.ex
            if ey < bbox.ey: ey = bbox.ey
        return BBox(sx,sy,ex,ey)
        
    def show_header_all(self):
        ids = self.f_list.keys()
        for i in range(len(ids)):
            self.f_list[ids[i]].show_header()
        
    def hide_header_all(self):
        ids = self.f_list.keys()
        for i in range(len(ids)):
            self.f_list[ids[i]].hide_header()
'''		
def main():
	fm = FrameManager()
	fm1=fm.create(0,0,1,1,Data(0,1,0,1))
	fm.create(1,1,1,1,Data(0,1,0,1))
	fm.create(2,2,1,1,Data(0,1,0,1))
	
	print("id", fm.id.id)
	print(fm.f_list.keys())
	
	fm.delete(0)
	
	print("id", fm.id.id)
	print(fm.f_list.keys())
	bbox = fm.get_gbbox()
	print("\nGbox: ",bbox.sx, bbox.sy, bbox.ex, bbox.ey)
	print("Fmm, clip: ", fm.get_clip(0))
	print("Frm, clip: ", fm1.get_clip())
	
if __name__ == '__main__':
	main()
'''