import numpy as np
import vgl

data = vgl.data.Data(-3,10,-3,3)
fmm = vgl.frame.FrameManager()
frm = fmm.create(0.0,0.0,5,3, data)
frm.show_all_grid()
frm.show_all_axis()
gbox = fmm.get_gbbox()

rad = 2.0
npnt = 100
theta = np.linspace(0, 2*np.pi, npnt)
x = rad*np.sin(theta)
y = rad*np.cos(theta)

def circle(dev):
    vgl.drawgrid.draw_grid(dev)
    vgl.drawlabel.draw_label(dev)
    vgl.drawtick.draw_tick(dev)
    dev.circle(4,0,rad,vgl.color.BLACK, 0.001*dev.frm.hgt())
    dev.polyline(x, y, vgl.color.RED, 0.002*dev.frm.hgt())
    dev.circle(0, 0, rad, vgl.color.BLUE, 0.001*dev.frm.hgt())
    
    x0=dev._x_viewport(0)
    y0=dev._x_viewport(0)
    x1=dev._x_viewport(x0-rad)
    x2=dev._x_viewport(x0+rad)
    y1=dev._y_viewport(y0-rad)
    y2=dev._y_viewport(y0+rad)
    xdif=(x2-x0)-(x0-x1)
    ydif=(y2-y0)-(y0-y1)
    print("xdif",xdif)
    print("ydif",ydif)
    
def main():
    dev_img = vgl.device.DeviceCairo("circle.jpg", gbox, 300)
    dev_img.set_plot(frm, extend=vgl.device._FIT_EXTEND_Y)
    circle(dev_img)
    dev_img.close()

    dev_wmf = vgl.device.DeviceWindowsMetafile("circle.wmf", gbox)
    dev_wmf.set_plot(frm, extend=vgl.device._FIT_EXTEND_Y)
    circle(dev_wmf)
    dev_wmf.close()
    
if __name__ == '__main__':
	main()