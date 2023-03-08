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
    vgl.drawaxis.draw_axis(dev)
    dev.circle(4,0,rad,vgl.color.BLACK, 0.003*dev.frm.hgt(), lpat=vgl.patline.get_stock_dash())
    #dev.polyline(x, y, vgl.color.RED, 0.002*dev.frm.hgt())
    dev.circle(0, 0, rad, vgl.color.BLUE, 0.003*dev.frm.hgt(), lpat=vgl.patline.get_stock_dashdot())
   
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