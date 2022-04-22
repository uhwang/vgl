import math
import random
import vgl
import coltbl

xmin,xmax,ymin,ymax=-4,4,-4,4
data = vgl.Data(xmin,xmax,ymin,ymax)
fmm = vgl.FrameManager()
frm = fmm.create(0,0,3,3, data)
def koch_curve(dev, length, theta, order, col):
    global posx, posy
    
    if order is 0:
        x2 = posx+length*math.cos(vgl.deg_to_rad(theta))
        y2 = posy+length*math.sin(vgl.deg_to_rad(theta))
        dev.line(posx, posy, x2, y2, col, 0.001*dev.frm.hgt())
        posx, posy = x2, y2
    else:
        koch_curve(dev, length/3.0, theta    ,order-1, col)
        koch_curve(dev, length/3.0, theta +60,order-1, col)
        koch_curve(dev, length/3.0, theta -60,order-1, col)
        koch_curve(dev, length/3.0, theta    ,order-1, col)
        
def run_koch_curve(dev):
    global posx, posy
    print("... Run Koch curve ...")
    sin60 = math.sin(vgl.deg_to_rad(60))
    step = 6
    order = [x for x in range(step)]
    length = [x+(1-math.sin(vgl.deg_to_rad(90-90.0/step*(x-1)))) for x in range(1,step+1)]
    #length = [2*x*(1-math.sin(vgl.deg_to_rad(90-90.0/step*(x-1)))) for x in range(1,step+1)]
    #length = [x for x in range(1,step+1)]
    ctbl = coltbl.create_color_table(0,240, 0.8, 1, step)

    for o in range(step):
        h1 = length[o]*sin60
        h2 = length[o]/3.0*sin60
        h3 = (h1+h2)*0.5
        sx, sy = -length[o]*0.5, h3-h2

        pxs = [sx,sx+length[o],sx+length[o]*0.5]
        pys = [sy,sy,-h3]
        ang = [0, -120, -240]
        for px, py, deg in zip(pxs, pys, ang): 
            posx = px
            posy = py
            koch_curve(dev, length[o], deg, order[o], ctbl[o])
            
def save_wmf(fname, gbbox):
    dev = vgl.DeviceWindowsMetafile(fname, gbbox)
    dev.set_device(frm)
    #vgl.drawfrm.draw_axis(dev, dev.frm.data)
    vgl.drawtick.draw_tick_2d(dev)	
    vgl.drawgrid.draw_grid(dev)
    vgl.drawlabel.draw_label_2d(dev)
    run_koch_curve(dev)
    dev.close()
    
def save_cairo(fname, gbox, dpi):
    dev = vgl.DeviceCairo(fname, gbox, dpi)
    dev.fill_white()
    dev.set_device(frm)
    vgl.drawtick.draw_tick_2d(dev)	
    vgl.drawgrid.draw_grid(dev)
    vgl.drawlabel.draw_label_2d(dev)
    run_koch_curve(dev)
    dev.close()

save_cairo("koch.png", fmm.get_gbbox(), 400)
save_wmf("koch.wmf", fmm.get_gbbox())
