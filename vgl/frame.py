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
	def __init__(self, id, sx, sy, wid, hgt, data):
		self.id   = id
		self.fvtx = vertex.Vertex(4)          # frame vertex
		self.pvtx = vertex.Vertex(4)          # plot domain vertex
		self.bbox = BBox(sx,sy,sx+wid,sy+hgt) # frame Bounding Box
		self.data = data                      # data to plot
		self.pdom = Rect()                    # plot domain size
		self.fmpt = FrameProperty()           # frame properties (border, bk, ...)
		self.xaxis= axis.Axis(data.xmin, data.xmax)# x axis
		self.yaxis= axis.Axis(data.ymin, data.ymax)# y axis
		self.xaxis.xlabel.hn()
		self.yaxis.ylabel.wv()
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
	def get_property(self): return self.fmpt
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

	def set_headershow(self, show): self.fmpt.header_show = show
	def set_bordershow(self, show):	self.fmpt.border_show = show
	def show_header   (self): self.fmpt.header_show = True
	def show_border   (self): self.fmpt.border_show = True
	def hide_header   (self): self.fmpt.header_show = False
	def hide_border   (self): self.fmpt.border_show = False
		
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