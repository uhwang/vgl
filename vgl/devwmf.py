# Vector Graphic Library (VGL) for Python
#
# devwmf.py
#
# 2020-2-12 Ver 0.1
#
# Author: Uisang Hwang
# Email : uhwangtx@gmail.com
#

import struct
import vgl.wmfconst as wc
from vgl.size import BBox

_to_twip = lambda x: int((x)*wc.TWIP_PER_INCH)

def rshift_u32(val,n):
	return ((val>>n)&(0x7fffffff>>n-1))

class StandardMetaHeader():
	def __init__(self):
		self.FileType      = 0x0001   #  2     
		self.HeaderSize    = 0x0009   # +2 = 4 
		self.Version       = 0x0300   # +2 = 6 
		self.FileSize      = 18       # +4 = 10
		self.NumOfObjects  = 0        # +2 = 12
		self.MaxRecordSize = 0        # +4 = 16
		self.NumOfParams   = 0        # +2 = 18
		self.format="=hhhLhLh"
		
	def get_format(self):
		return self.format
		
	def get_bytes(self):
		return struct.pack(
			self.format, 
			self.FileType,  
			self.HeaderSize, 
			self.Version,
			self.FileSize,
			self.NumOfObjects,
			self.MaxRecordSize,
			self.NumOfParams)	
		
class PlaceableMetaHeader():
	def __init__(self, bbox):
		self.format = "=LhhhhhhLh"
		self.initialize(bbox)

	def initialize(self, bbox):
		self.MagicNumber= wc.META_MAGICNUMBER
		self.Handle     = 0
		self.Left       = _to_twip(bbox.sx)
		self.Top        = _to_twip(bbox.sy)
		self.Right      = _to_twip(bbox.ex) 
		self.Bottom     = _to_twip(bbox.ey)
		self.Inch       = 1270
		self.Reserved   = 0; 
		self.CheckSum   = 0;
		self.CheckSum  ^= (wc.META_MAGICNUMBER & wc.META_KEYLOW);
		val             = wc.META_MAGICNUMBER & wc.META_KEYHIGH
		self.CheckSum  ^= rshift_u32(val, wc.META_KEYSHIFT)
		self.CheckSum  ^= self.Handle
		self.CheckSum  ^= self.Left;
		self.CheckSum  ^= self.Top;
		self.CheckSum  ^= self.Right;
		self.CheckSum  ^= self.Bottom;
		self.CheckSum  ^= self.Inch;
		self.CheckSum  ^= (self.Reserved & wc.META_KEYLOW)
		val             = self.Reserved & wc.META_KEYHIGH
		self.CheckSum  ^= rshift_u32(val, wc.META_KEYSHIFT)
		
	def get_format(self):
		return self.format
		
	def get_bytes(self):
		return struct.pack(self.format, 
			self.MagicNumber, 
			self.Handle, 
			self.Left, 
			self.Top, 
			self.Right, 
			self.Bottom,
			self.Inch,
			self.Reserved,
			self.CheckSum)
			
class MetaRecord():
	def __init__(self, func, nparam):
		self.set_record(func, nparam)

	def release(self):
		self.Field  = self.Field[0:2]
		self.nParam = 0
		self.Size   = 0
		self.Field  = []
		
	def set_record(self, func, nparam):
		self.Size     = wc.META_DEFAULT_RECORD_SIZE+nparam
		self.Function = func
		self.nParam   = nparam
		self.Field    = [] # Parameters
				
	def set_param(self, param):
		self.Field.append(param)
				
	def get_bytes(self):
		len = 4+2+2*self.nParam
		bytes = bytearray(len)
		bytes[0:4] = struct.pack('=L', self.Size)
		bytes[4:6] = struct.pack('=h', self.Function)
		x=6
		for i in range(self.nParam):
			bytes[x:x+2] = struct.pack('=H', self.Field[i])
			x += 2
		return bytes
		
class WindowsMetaFile():
	def __init__(self, fname, gbox):
		self.gbox     = gbox
		self.std_head = StandardMetaHeader()
		self.ald_head = PlaceableMetaHeader(gbox)
		self.fp       = open(fname, 'wb')
		self.rec      = MetaRecord(wc.META_END,0)   
		self.cur_pen  = 0 
		self.cur_brush= 0
		self.nTh_GDI_Object = -1;

		self.WriteHeader()
		self.SetWindowOrg(gbox.sx, gbox.sy)
		self.SetWindowExt(gbox.wid(), gbox.hgt())
	
	def UpdateHeaderInfo(self):
		if self.rec.Size > self.std_head.MaxRecordSize:
			self.std_head.MaxRecordSize = self.rec.Size
		self.std_head.FileSize += self.rec.Size
		
	def EndRecord(self):
		self.rec.set_record(wc.META_END,0)
		self.UpdateHeaderInfo()
		self.WriteMetaRecord()
		self.rec.release()
	
	def WriteMetaRecord(self):
		self.fp.write(self.rec.get_bytes())
		
	def WriteHeader(self):
		self.fp.seek(0)
		self.fp.write(self.ald_head.get_bytes())
		self.fp.write(self.std_head.get_bytes())

	def CloseMetafile(self):
		self.EndRecord()
		self.WriteHeader()
		self.fp.close()
		self.nTh_GDI_Object = -1
	
	def SetWindowOrg(self, x, y):
		self.rec.set_record(wc.META_SETWINDOWORG, 2)
		self.rec.set_param(_to_twip(y))
		self.rec.set_param(_to_twip(x))
		self.UpdateHeaderInfo()
		self.WriteMetaRecord();
		self.rec.release();
		
	def SetWindowExt(self, x, y): 
		self.rec.set_record(wc.META_SETWINDOWEXT, 2)
		self.rec.set_param(_to_twip(y))
		self.rec.set_param(_to_twip(x))
		self.UpdateHeaderInfo()
		self.WriteMetaRecord()
		self.rec.release()
		
	def convert_color(self, color):
		return color[0]|color[1]<<8, color[2]&0x00ff # (green, red), (blue)
		
	def SelectObject(self, gdi_obj):
		self.rec.set_record(wc.META_SELECTOBJECT, 1)
		self.rec.set_param(gdi_obj)
		self.UpdateHeaderInfo()
		self.WriteMetaRecord()
		self.rec.release()
	
	def DeleteObject(self, gdi_obj):
		self.rec.set_record(wc.META_DELETEOBJECT, 1)
		self.rec.set_param(gdi_obj)
		self.UpdateHeaderInfo()
		self.WriteMetaRecord()
		self.rec.release()
		self.nTh_GDI_Object -= 1
	
	def SaveDC(self):
		self.rec.set_record(wc.META_SAVEDC,0)
		self.UpdateHeaderInfo()
		self.WriteMetaRecord()
		self.rec.release()
	
	def RestoreDC(self):
		self.rec.set_record(wc.META_RESTOREDC, 1)
		self.rec.set_param(0xffff)
		self.UpdateHeaderInfo()
		self.WriteMetaRecord()
		self.rec.release()
	
	def MoveTo(self, x,y):
		self.rec.set_record(wc.META_MOVETO, 2)
		self.rec.set_param(_to_twip(y))
		self.rec.set_param(_to_twip(x))
		self.UpdateHeaderInfo()
		self.WriteMetaRecord()
		self.rec.release()
		
	def LineTo(self, x,y):
		self.rec.set_record(wc.META_LINETO, 2)
		self.rec.set_param(_to_twip(y))
		self.rec.set_param(_to_twip(x))
		self.UpdateHeaderInfo()
		self.WriteMetaRecord()
		self.rec.release()

	def MakePen(self, color, thk):
		thk = _to_twip(thk)
		self.cur_pen = self.CreatePenIndirect(wc.PS_SOLID, thk, 0, color)
		self.SelectObject(self.cur_pen)
		return self.cur_pen
		
	def DeletePen(self):
		self.DeleteObject(self.cur_pen)

	def MakeBrush(self, color, style=wc.BS_SOLID):
		self.cur_brush = self.CreateBrushIndirect(style, color, style)
		self.SelectObject(self.cur_brush)
		return self.cur_brush
	
	def MakeNullBrush(self):
		self.cur_brush = self.CreateBrushIndirect(wc.BS_HOLLOW, (255,255,255), wc.BS_HOLLOW)
		self.SelectObject(self.cur_brush)
		return self.cur_brush
		
	def DeleteBrush(self):
		self.DeleteObject(self.cur_brush)
		
	def Line(self, x1, y1, x2, y2, lcol=0, thk=0):
		if lcol != 0: self.MakePen(lcol, thk)
		self.MoveTo   (x1, y1)
		self.LineTo   (x2, y2)
		if lcol !=0: self.DeletePen()

	def CreatePenIndirect(self, style, x_wid, y_hgt, color):
		self.rec.set_record(wc.META_CREATEPENINDIRECT, 5)
		gr, b = self.convert_color(color)
		self.rec.set_param(style)
		self.rec.set_param(x_wid)
		self.rec.set_param(y_hgt)
		self.rec.set_param(gr)
		self.rec.set_param(b)
		self.UpdateHeaderInfo()
		self.WriteMetaRecord()
		self.rec.release()
		self.nTh_GDI_Object += 1
		self.std_head.NumOfObjects += 1
		return self.nTh_GDI_Object
	
	def CreateBrushIndirect(self, style, color, hatch):
		self.rec.set_record(wc.META_CREATEBRUSHINDIRECT, 4)
		gr, b = self.convert_color(color)
		self.rec.set_param(style)
		self.rec.set_param(gr)
		self.rec.set_param(b)
		self.rec.set_param(hatch)
		self.UpdateHeaderInfo()
		self.WriteMetaRecord()
		self.rec.release()
		self.nTh_GDI_Object += 1
		self.std_head.NumOfObjects += 1
		return self.nTh_GDI_Object
		
	def Polyline(self, x,y,closed):
		get_npoint = lambda n: len(x)+1 if closed else len(x)
		npoint = get_npoint(x)
		self.rec.set_record(wc.META_POLYLINE, 1+npoint*2)
		self.rec.set_param(npoint)
		npoint = len(x)

		for i in range(npoint):
			self.rec.set_param(_to_twip(x[i]))
			self.rec.set_param(_to_twip(y[i]))
		if closed:
			self.rec.set_param(_to_twip(x[0]))
			self.rec.set_param(_to_twip(y[0]))
			
		self.UpdateHeaderInfo()
		self.WriteMetaRecord()
		self.rec.release()

	def Circle(self, x1, y1, x2, y2):
		npoint = 4
		self.rec.set_record(wc.META_ELLIPSE, npoint)
		self.rec.set_param(_to_twip(y1))
		self.rec.set_param(_to_twip(x1))
		self.rec.set_param(_to_twip(y2))
		self.rec.set_param(_to_twip(x2))
		self.UpdateHeaderInfo()
		self.WriteMetaRecord()
		self.rec.release()
		
	def Symbol(self, x, y):
		npoint = len(x)
		self.rec.set_record(wc.META_POLYGON, 1+npoint*2)
		self.rec.set_param(npoint)
		for i in range(npoint):
			self.rec.set_param(_to_twip(x[i]))
			self.rec.set_param(_to_twip(y[i]))
		self.UpdateHeaderInfo()
		self.WriteMetaRecord()
		self.rec.release()
		
	def Polygon(self, x, y, lcol, fcol, thk):
		npoint = len(x)
		self.cur_pen = self.CreatePenIndirect(wc.PS_SOLID, _to_twip(thk), 0, lcol)
		self.SelectObject(self.cur_pen);
		self.cur_brush = self.CreateBrushIndirect(wc.BS_SOLID, fcol, wc.BS_SOLID)
		self.SelectObject(self.cur_brush)
		self.rec.set_record(wc.META_POLYGON, 1+npoint*2)
		self.rec.set_param(npoint)
		
		for i in range(npoint):
			self.rec.set_param(_to_twip(x[i]))
			self.rec.set_param(_to_twip(y[i]))

		#if lcol != fcol: 
		#	self.Polyline(x,y,True)
			
		self.UpdateHeaderInfo()
		self.WriteMetaRecord()
		self.DeleteObject(self.cur_brush)
		self.DeleteObject(self.cur_pen)
		self.rec.release()

	def CreateClip(self, sx, sy, ex, ey):
		self.rec.set_record(wc.META_INTERSECTCLIPRECT, 4)
		self.rec.set_param(_to_twip(ey))
		self.rec.set_param(_to_twip(ex))
		self.rec.set_param(_to_twip(sy))
		self.rec.set_param(_to_twip(sx))
		self.UpdateHeaderInfo()
		self.WriteMetaRecord()
		self.rec.release()
		
	def DeleteClip(self, hrgn):
		self.rec.set_record(wc.META_SELECTCLIPREGION, 1)
		self.rec.set_param(0)
		self.UpdateHeaderInfo()
		self.WriteMetaRecord()
		self.rec.release()
		
		
def main():
	wmf = WindowsMetaFile('t.wmf', BBox(0,0,3,3))
	#wmf.Line(0,0,2,2, (0,150,255), 0.03)
	wmf.Polyline([1,1,2,2],[1,2,2,1], True)
	wmf.CloseMetafile()
	
if __name__ == '__main__':
	main()
