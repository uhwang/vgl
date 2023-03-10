import numpy as np
import vgl

data = vgl.data.Data(-3,10,-3,3)
fmm = vgl.frame.FrameManager()
frm = fmm.create(0.0,0.0,5,3, data)
frm.show_all_major_grid()
gbox = fmm.get_gbbox()

rad = 2.0
npnt = 100
theta = np.linspace(0, 2*np.pi, npnt)
x = rad*np.sin(theta)
y = rad*np.cos(theta)

def circle(dev):
    vgl.drawaxis.draw_axis(dev)
    dev.circle(4,0,rad,vgl.color.RED, 0.007*dev.frm.hgt(), lpat=vgl.linepat.get_stock_dash())
    dev.circle(0, 0, rad, vgl.color.CYAN, 0.02*dev.frm.hgt(), lpat=vgl.linepat.get_stock_dash())
    dev.circle(0, 0, rad/3, vgl.color.GREEN, 0.02*dev.frm.hgt(), fcol=vgl.color.PURPLE)
    dev.polyline(x, y, vgl.color.BLACK, 0.003*dev.frm.hgt())
   
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