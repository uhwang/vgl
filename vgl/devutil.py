'''
devlist.py

'''

from . import devcairo
from . import devwmf
from . import devemf
from . import devpdf
from . import devsvg
from . import devppt
from . import paper
from . import size
from . import frame
from . import data

_dev_name = [
    "IMG",
    "WMF",
    "EMF",
    "PDF",
    "SVG",
    "PPT"
]

_dev_img = _dev_name[0]
_dev_wmf = _dev_name[1]
_dev_emf = _dev_name[2]
_dev_pdf = _dev_name[3]
_dev_svg = _dev_name[4]
_dev_ppt = _dev_name[5]

_dev_list = [
    _dev_img,
    _dev_wmf,
    _dev_emf,
    _dev_pdf,
    _dev_svg,
    _dev_ppt
]

_default_dev_dpi = 300
_p_dev = None
_p_frm = None
_p_data= None
_g_top   = 0.5
_g_left  = 0.5
_g_w     = 0
_g_h     = 5
_g_fid   = 999

def open_device(dev_name, fn):
    global _p_dev, _p_data, _p_frm, _g_left, _g_top, _g_h, _g_w
    
    w, h = paper.get_paper_letter_inch()
    _g_w = w - _g_left*2
    _p_data = data.Data(-1,1,-1,1)
    _p_frm = frame.Frame(_g_fid, _g_left, _g_top, _g_w, _g_h, _p_data)
    gbbox = _p_frm.bbox

    if dev_name == _dev_img:
        _p_dev = devcairo.DeviceIMG("%s.png"%fn, gbbox, _default_dev_dpi)
    elif dev_name == _dev_wmf:
        _p_dev = devwmf.DeviceWMF("%s.wmf"%fn, gbbox)    
    elif dev_name == _dev_emf:
        _p_dev = devemf.DeviceEMF("%s.emf"%fn, gbbox)    
    elif dev_name == _dev_pdf:
        _p_dev = devpdf.DevicePDF("%s.pdf"%fn, gbbox)    
    elif dev_name == _dev_svg:
        _p_dev = devsvg.DeviceSVG("%s.svg"%fn, gbbox, _default_dev_dpi)    
    elif dev_name == _dev_ppt:
        _p_dev = devppt.DevicePPT("%s.ppt"%fn, gbbox)  
    else:
        return None
        
    _p_dev.set_device(_p_frm)
    
    return _p_dev
    
def close_device():
    global _p_dev, _p_data, _p_frm
    
    if _p_dev:
        _p_dev.close()
        _p_data= None
        _p_frm = None
        _p_dev = None
    
