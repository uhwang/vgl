'''
    drvemf.py
    
    DWORD 
    WORD

    Rectangle (16 bytes, optional): A RectL object ([MS-WMF] section 2.2.2.19) that defines a clipping
and/or opaquing rectangle in logical units


'''

import struct
from . import emfconst as ec
from . import color
from . size import BBox
        
_mm_per_inch = 25.4

def get_format_size(format):
    f_size = 0
    for f in format:
        if f == "L" or f == 'i': f_size += 4
        elif f == "h": f_size += 2
    return f_size

_header_member_print_format =\
        "iType             : %d\n"\
        "nSize             : %d\n"\
        "rclBounds_left    : %i\n"\
        "rclBounds_top     : %i\n"\
        "rclBounds_right   : %d\n"\
        "rclBounds_bottom  : %d\n"\
        "rclFrame_left     : %d\n"\
        "rclFrame_top      : %d\n"\
        "rclFrame_right    : %d\n"\
        "rclFrame_bottom   : %d\n"\
        "dSignature        : %d\n"\
        "nVersion          : %d\n"\
        "nBytes            : %d\n"\
        "nRecords          : %d\n"\
        "nHandles          : %d\n"\
        "sReserved         : %d\n"\
        "nDescription      : %d\n"\
        "offDescription    : %d\n"\
        "nPalEntries       : %d\n"\
        "szlDevice_cx      : %d\n"\
        "szlDevice_cy      : %d\n"\
        "szlMillimeters_cx : %d\n"\
        "szlMillimeters_cy : %d\n"\
        "cbPixelFormat     : %d\n"\
        "offPixelFormat    : %d\n"\
        "bOpenGL           : %d\n"\
        "szlMicrometers_cx : %d\n"\
        "szlMicrometers_cy : %d\n"

def unpack_header(format, buf):
    h = struct.unpack(format, buf[:get_format_size(format)])
    return _header_member_print_format%(\
        h[0 ],h[1 ],
        h[2 ],h[3 ],h[4 ],h[5 ],
        h[6 ],h[7 ],h[8 ],h[9 ],
        h[10],h[11],h[12],h[13],h[14],
        h[15],h[16],h[17],h[18],
        h[19],h[20],
        h[21],h[22],
        h[23],h[24],h[25],
        h[26],h[27])

# from pyemf.py
colorref = lambda r,g,b: ((b<<16)|(g<<8)|r)        

def _getBounds(points_x, points_y):
    """Get the bounding rectangle for this list of 2-tuples."""
    left=points_x[0]
    right=left
    top=points_y[0]
    bottom=top
    for x,y in zip(points_x[1:], points_y[1:]):
        if x<left:
            left=x
        elif x>right:
            right=x
        if y<top:
            top=y
        elif y>bottom:
            bottom=y
    return ((left,top),(right,bottom))
        
def _useShort(bounds):
    """Determine if we can use the shorter 16-bit EMR structures.
    If all the numbers can fit within 16 bit integers, return
    true.  The bounds 4-tuple is (left,top,right,bottom)."""

    SHRT_MIN=-32768
    SHRT_MAX=32767
    if bounds[0][0]>=SHRT_MIN and bounds[0][1]>=SHRT_MIN and bounds[1][0]<=SHRT_MAX and bounds[1][1]<=SHRT_MAX:
        return True
    return False

    
class MetaRecord():
    def __init__(self, func, nparam):
        self.set_record(func, nparam)
    
    def release(self):
        self.Field  = self.Field[0:2]
        self.nParam = 0
        self.Size   = 0
        self.Field  = []
        
    def set_record(self, func, nparam):
        # 8 + 4*nparam
        self.Size     = ec.EMF_DEFAULT_RECORD_SIZE+\
                        ec.EMF_PARAM_SIZE*nparam
        self.Function = func
        self.nParam   = nparam
        self.Field    = [] # Parameters
                
    def get_size(self):
        return self.Size
        
    def set_param(self, param):
        self.Field.append(param)
    
    def get_bytes(self, jump=4, format='=L'):
        # Type(4) + Size(4) + Params(n*4)
        #4+4+2*self.nParam
        bytes = bytearray(self.Size)
        bytes[0:4] = struct.pack('=i', self.Function)
        bytes[4:8] = struct.pack('=i', self.Size)
        x=8
        for i in range(self.nParam):
            bytes[x:x+jump] = struct.pack(format, self.Field[i])
            x += jump
        return bytes
        
class EhancedMetaHeader():
    def __init__(self, bbox, dpi):
        self.bbox = bbox
        self._format = "<iiiiiiiiiiiiiihhiiiiiiiiiiii"
        self.dpi = dpi
        self.initialize()
        
    def initialize(self):
        h_size = get_format_size(self.format)
        self.iType = ec.EMR_HEADER                               
        self.nSize = h_size                                      
        self.rclBounds_left   = int(self.bbox.sx*self.dpi)       
        self.rclBounds_top    = int(self.bbox.sy*self.dpi)       
        self.rclBounds_right  = int(self.bbox.ex*self.dpi)       
        self.rclBounds_bottom = int(self.bbox.ey*self.dpi)       
        self.rclFrame_left    = int(self.bbox.sx*_mm_per_inch*100)       
        self.rclFrame_top     = int(self.bbox.sy*_mm_per_inch*100)       
        self.rclFrame_right   = int(self.bbox.ex*_mm_per_inch*100)       
        self.rclFrame_bottom  = int(self.bbox.ey*_mm_per_inch*100)       
        self.dSignature       = ec.ENHMETA_SIGNATURE    # "EMF"        
        self.nVersion         = 0x10000                          
        self.nBytes           = h_size                                       
        self.nRecords         = 1                                
        self.nHandles         = 1                                
        self.sReserved        = 0                                
        self.nDescription     = 0                                
        self.offDescription   = 0                                
        self.nPalEntries      = 0                                
        self.szlDevice_cx     = int(self.bbox.wid()*self.dpi)    
        self.szlDevice_cy     = int(self.bbox.hgt()*self.dpi)    
        self.szlMillimeters_cx= int(self.bbox.wid()*_mm_per_inch)
        self.szlMillimeters_cy= int(self.bbox.hgt()*_mm_per_inch)
        self.cbPixelFormat    = 0                                
        self.offPixelFormat   = 0                                
        self.bOpenGL          = 0                            
        self.szlMicrometers_cx= int(self.bbox.wid()*_mm_per_inch*1000)     
        self.szlMicrometers_cy= int(self.bbox.hgt()*_mm_per_inch*1000)     

    @property
    def format(self):
        return self._format
        
    @format.setter
    def format(self, f):
        self._format = f

    @property
    def handles(self):
        return self.nHandles
        
    @handles.setter
    def handles(self, v):
        self.nHandles += v
        
    def add_handles(self):
        self.nHandles += 1
        
    def __str__(self):
        return _header_member_print_format%(\
            self.iType            ,
            self.nSize            ,
            self.rclBounds_left   ,
            self.rclBounds_top    ,
            self.rclBounds_right  ,
            self.rclBounds_bottom ,
            self.rclFrame_left    ,
            self.rclFrame_top     ,
            self.rclFrame_right   ,
            self.rclFrame_bottom  ,
            self.dSignature       ,
            self.nVersion         ,
            self.nBytes           ,
            self.nRecords         ,
            self.nHandles         ,
            self.sReserved        ,
            self.nDescription     ,
            self.offDescription   ,
            self.nPalEntries      ,
            self.szlDevice_cx     ,
            self.szlDevice_cy     ,
            self.szlMillimeters_cx,
            self.szlMillimeters_cy,
            self.cbPixelFormat    ,
            self.offPixelFormat   ,
            self.bOpenGL          ,
            self.szlMicrometers_cx,
            self.szlMicrometers_cy)
        
    def get_format(self):
        return self.format
        
    def get_bytes(self):
        return struct.pack(
            self.format, 
            self.iType,
            self.nSize,
            self.rclBounds_left,
            self.rclBounds_top,
            self.rclBounds_right,
            self.rclBounds_bottom,
            self.rclFrame_left,
            self.rclFrame_top,
            self.rclFrame_right,
            self.rclFrame_bottom,
            self.dSignature,
            self.nVersion,
            self.nBytes,
            self.nRecords,
            self.nHandles,
            self.sReserved,
            self.nDescription,
            self.offDescription,
            self.nPalEntries,
            self.szlDevice_cx,
            self.szlDevice_cy,
            self.szlMillimeters_cx,
            self.szlMillimeters_cy,
            self.cbPixelFormat,
            self.offPixelFormat,
            self.bOpenGL,
            self.szlMicrometers_cx,
            self.szlMicrometers_cy)

class EnhancedMetaFile():
    def __init__(self, fname, gbox, dpi=300):
        self.gbox     = gbox
        self.dpi      = dpi
        self.head     = EhancedMetaHeader(gbox, dpi)
        self.fp       = open(fname, 'wb')
        self.rec      = MetaRecord(ec.EMR_EOF,0)   
        self.cur_pen  = 0 
        self.cur_brush= 0
        self.nTh_GDI_Object = 0;
    
        self.WriteHeader()
        #self.SetWindowOrg(gbox.sx*dpi, gbox.sy*dpi)
        #self.SetWindowExt(gbox.wid()*dpi, gbox.hgt()*dpi)
    
    def set_header_format(self, f):
        self.head.format = f
        
    def get_header_format(self):
        return self.head.format
        
    def UpdateHeaderHandle(self):
        self.head.nHandles += 1
        
    def UpdateHeaderInfo(self):
        self.head.nBytes += self.rec.Size
        self.head.nRecords += 1
        
    def EndRecord(self):
        self.rec.set_record(ec.EMR_EOF,3)
        self.rec.set_param(0)
        self.rec.set_param(0)
        self.rec.set_param(self.rec.get_size())
        self.UpdateHeaderInfo()
        self.WriteMetaRecord()
        self.rec.release()
    
    def WriteMetaRecord(self):
        self.fp.write(self.rec.get_bytes())
        
    def WriteHeader(self):
        self.fp.seek(0)
        self.fp.write(self.head.get_bytes())
    
    def CloseMetafile(self):
        self.EndRecord()
        self.WriteHeader()
        self.fp.close()
        self.nTh_GDI_Object = -1
    
    def SetWindowOrg(self, x, y):
        self.rec.set_record(ec.EMR_SETWINDOWORGEX, 2)
        self.rec.set_param(y)
        self.rec.set_param(x)
        self.UpdateHeaderInfo()
        self.WriteMetaRecord();
        self.rec.release();
        
    def SetWindowExt(self, x, y): 
        self.rec.set_record(ec.EMR_SETWINDOWEXTEX, 2)
        self.rec.set_param(y)
        self.rec.set_param(x)
        self.UpdateHeaderInfo()
        self.WriteMetaRecord()
        self.rec.release()
        
    def convert_color(self, color):
        #return color[0]|color[1]<<8, color[2]&0x00ff # (green, red), (blue)
        return color.r|color.g<<8, color.b&0x00ff # (green, red), (blue)
        
    def SelectObject(self, gdi_obj):
        self.rec.set_record(ec.EMR_SELECTOBJECT, 1)
        self.rec.set_param(gdi_obj)
        self.UpdateHeaderInfo()
        self.WriteMetaRecord()
        self.rec.release()
    
    def DeleteObject(self, gdi_obj):
        self.rec.set_record(ec.EMR_DELETEOBJECT, 1)
        self.rec.set_param(gdi_obj)
        self.UpdateHeaderInfo()
        self.WriteMetaRecord()
        self.rec.release()
        self.nTh_GDI_Object -= 1
    
    def SaveDC(self):
        self.rec.set_record(ec.EMR_SAVEDC,0)
        self.UpdateHeaderInfo()
        self.WriteMetaRecord()
        self.rec.release()
    
    def RestoreDC(self):
        self.rec.set_record(ec.EMR_RESTOREDC, 1)
        self.rec.set_param(0xffff)
        self.UpdateHeaderInfo()
        self.WriteMetaRecord()
        self.rec.release()
    
    def MoveTo(self, x,y):
        self.rec.set_record(ec.EMR_MOVETOEX, 2)
        self.rec.set_param(x)
        self.rec.set_param(y)
        self.UpdateHeaderInfo()
        self.WriteMetaRecord()
        self.rec.release()
        
    def LineTo(self, x,y):
        self.rec.set_record(ec.EMR_LINETO, 2)
        self.rec.set_param(x)
        self.rec.set_param(y)
        self.UpdateHeaderInfo()
        self.WriteMetaRecord()
        self.rec.release()
    
    def MakePen(self, lcol, lthk):
        self.cur_pen = self.CreatePenIndirect(ec.PS_SOLID, lthk, 0, lcol)
        self.SelectObject(self.cur_pen)
        return self.cur_pen
        
    def DeletePen(self):
        self.DeleteObject(self.cur_pen)
    
    def MakeBrush(self, color, style=ec.BS_SOLID):
        self.cur_brush = self.CreateBrushIndirect(style, color, style)
        self.SelectObject(self.cur_brush)
        return self.cur_brush
    
    def MakeNullBrush(self):
        self.cur_brush = self.CreateBrushIndirect(ec.BS_HOLLOW, color.Color(255,255,255), ec.BS_HOLLOW)
        #self.SelectObject(self.cur_brush)
        return self.cur_brush

    def MakeNullPen(self):
        self.cur_brush = self.CreatePenIndirect(ec.PS_NULL, 0, 0, color.Color(255,255,255))
        #self.SelectObject(self.cur_brush)
        return self.cur_brush
        
    def DeleteBrush(self):
        self.DeleteObject(self.cur_brush)
        
    def Line(self, x1, y1, x2, y2, lcol=None, lthk=None):
        if lcol: 
            self.MakePen(lcol, lthk)
            
        self.MoveTo   (x1, y1)
        self.LineTo   (x2, y2)
        
        if lcol: 
            self.DeletePen()
    
    def CreatePenIndirect(self, style, x_wid, y_hgt, color):
        self.nTh_GDI_Object += 1
        c = colorref(color.r, color.g, color.b)
        self.rec.set_record(ec.EMR_CREATEPEN, 5)
        self.rec.set_param(self.nTh_GDI_Object)
        self.rec.set_param(style)
        self.rec.set_param(x_wid)
        self.rec.set_param(y_hgt)
        self.rec.set_param(c)
        self.UpdateHeaderInfo()
        self.UpdateHeaderHandle()
        self.WriteMetaRecord()
        self.rec.release()
        return self.nTh_GDI_Object
    
    def CreateBrushIndirect(self, style, color, hatch):
        self.nTh_GDI_Object += 1
        c = colorref(color.r, color.g, color.b)
        self.rec.set_record(ec.EMR_CREATEBRUSHINDIRECT, 4)
        self.rec.set_param(self.nTh_GDI_Object)
        self.rec.set_param(style)
        self.rec.set_param(c)
        self.rec.set_param(hatch)
        self.UpdateHeaderInfo()
        self.UpdateHeaderHandle()
        self.WriteMetaRecord()
        self.rec.release()

        return self.nTh_GDI_Object
        
    def Polyline(self, x, y, closed):
        bounds = _getBounds(x,y)
        i16 = _useShort(bounds) 
        npoint = len(x)+1 if closed else len(x)
        
        # Func  : 4 byte
        # Size  : 4 byte
        # Left  : 4 byte
        # Top   : 4 byte
        # Right : 4 byte
        # Bottom: 4 byte
        # Count : 4 byte
        # aPoints
        #   16bit : nParam x 2(x,y) * 2(size)
        #   32bit : nParam x 2(x,y) x 4(size)
        if i16:
            self.rec.Function = ec.EMR_POLYLINE16
            self.rec.Size = 4+4+16+4+npoint*2*2
            jump = 2
            format = '=h'
        else:
            self.rec.Function = ec.EMR_POLYLINE
            self.rec.Size = 4+4+16+4+npoint*2*4
            jump = 4
            format = '=i'
        
        self.rec.set_param(bounds[0][0])
        self.rec.set_param(bounds[0][1])
        self.rec.set_param(bounds[1][0])
        self.rec.set_param(bounds[1][1])
        if closed: npoint += 1
        self.rec.set_param(npoint)
  
        bytes = bytearray(self.rec.Size)
        bytes[0 :4 ] = struct.pack('=i', self.rec.Function)
        bytes[4 :8 ] = struct.pack('=i', self.rec.Size)
        bytes[8 :12] = struct.pack('=i', self.rec.Field[0])
        bytes[12:16] = struct.pack('=i', self.rec.Field[1])
        bytes[16:20] = struct.pack('=i', self.rec.Field[2])
        bytes[20:24] = struct.pack('=i', self.rec.Field[3])
        bytes[24:28] = struct.pack('=i', self.rec.Field[4])
        b_pos=28
        
        for x1, y1 in zip(x,y):
            bytes[b_pos:b_pos+jump] = struct.pack(format, x1)
            b_pos += jump
            bytes[b_pos:b_pos+jump] = struct.pack(format, y1)
            b_pos += jump
            
        if closed:
            bytes[b_pos:b_pos+jump] = struct.pack(format, x[0])
            b_pos += jump
            bytes[b_pos:b_pos+jump] = struct.pack(format, y[0])
            
        self.fp.write(bytes)
        self.UpdateHeaderInfo()
        self.rec.release()
        
    def Circle(self, x1, y1, x2, y2):
        npoint = 4
        self.rec.set_record(ec.EMR_ELLIPSE, npoint)
        self.rec.set_param(y1)
        self.rec.set_param(x1)
        self.rec.set_param(y2)
        self.rec.set_param(x2)
        self.UpdateHeaderInfo()
        self.WriteMetaRecord()
        self.rec.release()
        
    def Symbol(self, x, y):
        self._Polygon(x,y)
        self.UpdateHeaderInfo()
        self.rec.release()

    def _Polygon(self, x,y):
        npoint = len(x)
        bounds = _getBounds(x,y)
        i16 = _useShort(bounds) 
        
        if i16:
            self.rec.Function = ec.EMR_POLYGON16
            self.rec.Size = 4+4+16+4+npoint*2*2
            jump = 2
            format = '=h'
        else:
            self.rec.Function = ec.EMR_POLYGON
            self.rec.Size = 4+4+16+4+npoint*2*4
            jump = 4
            format = '=i'
        
        self.rec.set_param(bounds[0][0])
        self.rec.set_param(bounds[0][1])
        self.rec.set_param(bounds[1][0])
        self.rec.set_param(bounds[1][1])
        self.rec.set_param(npoint)
    
        bytes = bytearray(self.rec.Size)
        bytes[0 :4 ] = struct.pack('=i', self.rec.Function)
        bytes[4 :8 ] = struct.pack('=i', self.rec.Size)
        bytes[8 :12] = struct.pack('=i', self.rec.Field[0])
        bytes[12:16] = struct.pack('=i', self.rec.Field[1])
        bytes[16:20] = struct.pack('=i', self.rec.Field[2])
        bytes[20:24] = struct.pack('=i', self.rec.Field[3])
        bytes[24:28] = struct.pack('=i', self.rec.Field[4])
        b_pos=28

        for x1, y1 in zip(x,y):
            bytes[b_pos:b_pos+jump] = struct.pack(format, x1)
            b_pos += jump
            bytes[b_pos:b_pos+jump] = struct.pack(format, y1)
            b_pos += jump
        self.fp.write(bytes)
    
    def Polygon(self, x, y, lcol, lthk, fcol):
        
        if lcol:
            if not lthk: lthk = 1 # dummy line thikness
            self.cur_pen = self.CreatePenIndirect(ec.PS_SOLID, lthk, 0, lcol)
            self.SelectObject(self.cur_pen);
        else:
            self.cur_pen = self.MakeNullPen()
            self.SelectObject(self.cur_pen);
            
        if fcol:
            self.cur_brush = self.CreateBrushIndirect(ec.BS_SOLID, fcol, ec.BS_SOLID)
            self.SelectObject(self.cur_brush)
        else:
            self.cur_brush = self.MakeNullBrush()
            self.SelectObject(self.cur_brush)
            
        self._Polygon(x,y)
        self.UpdateHeaderInfo()
        self.rec.release()
        
        self.DeleteObject(self.cur_brush)
        self.DeleteObject(self.cur_pen)
    
    def CreateClip(self, sx, sy, ex, ey):
        self.rec.set_record(ec.EMR_INTERSECTCLIPRECT, 4)
        self.rec.set_param(_to_twip(ey))
        self.rec.set_param(_to_twip(ex))
        self.rec.set_param(_to_twip(sy))
        self.rec.set_param(_to_twip(sx))
        self.UpdateHeaderInfo()
        self.WriteMetaRecord()
        self.rec.release()
        
    def DeleteClip(self, hrgn):
        self.rec.set_record(ec.EMR_EXTSELECTCLIPRGN, 1)
        self.rec.set_param(0)
        self.UpdateHeaderInfo()
        self.WriteMetaRecord()
        self.rec.release()
        

