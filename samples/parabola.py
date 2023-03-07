'''
    directrix   y = -f
    focal point F = (0, F)
    a point     P = (x,y)
    |PF|^2 = |Pf|^2*np
    
    y=1/vf x**2

'''
import numpy as np
import vgl

data = vgl.data.Data(-6,6,-3,8)
fmm = vgl.frame.FrameManager()
frm = fmm.create(0,0,5,5, data)
#frm.show_all_grid()
frm.show_all_axis()
gbox = fmm.get_gbbox()

f = -1
npnt = 100
x = np.linspace(data.xmin+1, data.xmax-1, npnt)
y = -1/(4*f)*x**2
fy = lambda x,f: -1/(4*f)*x**2
x1 = -4
y1 = fy(x1,f)

xx = (x1, x1, 0)
yy = (f, y1, -f)

def parabola(dev):
    #vgl.drawgrid.draw_grid(dev)
    vgl.drawlabel.draw_label(dev)
    vgl.drawtick.draw_tick(dev)
    vgl.drawaxis.draw_axis(dev)
    dev.polyline(x, y, vgl.color.RED, 0.002*dev.frm.hgt())
    dev.line(-5, f, 5, f, vgl.color.BLACK, 0.001*dev.frm.hgt())
    dev.line(0, -1, 0, 6, vgl.color.BLACK, 0.001*dev.frm.hgt())
    dev.circle(0,f, 0.1, fcol=vgl.color.GREEN) #, 0.001*dev.frm.hgt())
    dev.circle(0,-f, 0.1, fcol=vgl.color.GREEN) #, 0.001*dev.frm.hgt())
    dev.polyline(xx, yy, vgl.color.MAGENTA, 0.002*dev.frm.hgt())
    dev.circle(xx[1], yy[1], 0.1, fcol=vgl.color.BLACK) #, 0.001*dev.frm.hgt())
    
def main():
    dev_img = vgl.device.DeviceCairo("parabola.jpg", gbox, 300)
    dev_img.set_plot(frm)
    parabola(dev_img)
    dev_img.close()

    dev_wmf = vgl.device.DeviceWindowsMetafile("parabola.wmf", gbox)
    dev_wmf.set_plot(frm)
    parabola(dev_wmf)
    dev_wmf.close()
    
if __name__ == '__main__':
	main()