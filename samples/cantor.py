import vgl

xmin,xmax,ymin,ymax=-10.,10.,-10.,10.
data = vgl.Data(xmin,xmax,ymin,ymax)
fmm = vgl.FrameManager()
frm = fmm.create(0,0,3,3, data)
c_x1 = xmin
c_y1 = ymax*0.5
len = xmax-xmin
yshift = -1.5

def cantor(dev, x, y, len, yshift, lthk):
    if len >= 0.01:
        dev.line(x, y, x+len, y, vgl.color.BLUE, lthk)
        y += yshift
        new_len = len/3.0
        cantor(dev, x, y, new_len, yshift, lthk)
        cantor(dev, x+new_len*2, y, new_len, yshift, lthk)
        
def save_wmf(fname, gbbox):
    dev = vgl.DeviceWindowsMetafile(fname, gbbox)
    dev.set_device(frm)
    #vgl.drawfrm.draw_axis(dev, dev.frm.data)
    vgl.drawtick.draw_tick_2d(dev)	
    vgl.drawfrm.draw_grid(dev, dev.frm.data, 1)
    vgl.drawlabel.draw_label_2d(dev)
    cantor(dev, c_x1, c_y1, len, yshift, dev.frm.hgt()*0.03)
    dev.close()
    
def save_cairo(fname, gbox, dpi):
    dev = vgl.DeviceCairo(fname, gbox, dpi)
    dev.fill_white()
    dev.set_device(frm)
    #vgl.drawfrm.draw_axis(dev, dev.frm.data)
    vgl.drawtick.draw_tick_2d(dev)	
    vgl.drawfrm.draw_grid(dev, dev.frm.data, 1)
    vgl.drawlabel.draw_label_2d(dev)
    cantor(dev, c_x1, c_y1, len, yshift, dev.frm.hgt()*0.03)
    dev.close()        
    
    
save_cairo("cantor.png", fmm.get_gbbox(), 400)
save_wmf  ("cantor.wmf", fmm.get_gbbox())