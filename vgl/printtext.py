# printtext.py

from . import text
from . import color
from . import fontid

def print_top_center(
                     dev, 
                     txt="", 
                     size=0.05,
                     lcol=color.BLACK,
                     lthk=0.001,
                     fid=fontid.FONT_ROMANDUPLEX,
                     skip_y=0.007):

    if txt == "": return
    
    bbox = dev.frm.bbox
    
    sx = bbox.sx+bbox.wid()*0.5
    sy = bbox.sy+bbox.hgt()*skip_y
    
    t = text.Text(sx,sy,txt,0,size,lcol,lthk,fid=fid)
    t.hn()
    text.write_text(dev, t)