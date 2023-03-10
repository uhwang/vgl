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
frm.show_all_grid()
gbox = fmm.get_gbbox()

fps = 30
duration = 10
npnt = fps*duration
f = -1
fy = lambda x,f: -1/(4*f)*x**2
sx = -5
ex  = 5
dx = (ex-sx)/npnt
px, py = sx, 0
pxx, pyy = [], []

def parabola(t):
    global dev, px, py, pxx, pyy
    dev.fill_white()
    vgl.drawaxis.draw_axis(dev)
    
    # plot parabola trace
    px += dx
    py = fy(px,f)
    pxx = [px]+pxx[:npnt]
    pyy = [py]+pyy[:npnt]
    dev.polyline(pxx, pyy, vgl.color.RED, 0.002*dev.frm.hgt())
    
    # draw equ line
    eqx = [px, px, 0]
    eqy = [f, py, -f]
    dev.polyline(eqx, eqy, vgl.color.MAGENTA, 0.002*dev.frm.hgt())
    
    dev.line(-5, f, 5, f, vgl.color.CUSTOM4, 0.004*dev.frm.hgt())
    dev.line(0, -1, 0, 6, vgl.color.CUSTOM4, 0.004*dev.frm.hgt())
    dev.circle(0,-f, 0.1, fcol=vgl.color.GREEN) 
    dev.circle(px,f, 0.1, fcol=vgl.color.GREEN) 
    dev.circle(eqx[1], eqy[1], 0.1, fcol=vgl.color.BLACK) 
    
dev = vgl.DeviceCairo("", gbox, 250)
dev.set_plot(frm)
dev_ani = vgl.DeviceCairoAnimation('parabola.mp4', dev, parabola, fps=fps, duration=duration)
dev_ani.save_video()

px, py = sx, 0
pxx, pyy = [], []

dev = vgl.DeviceCairo("", gbox, 100)
dev.set_plot(frm)
dev_ani = vgl.DeviceCairoAnimation('parabola.gif', dev, parabola, fps=fps, duration=duration)
dev_ani.save_gif()
