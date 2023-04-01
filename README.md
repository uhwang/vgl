# vgl
Vector Graphic Library for Python

# Introduction
## Plotting Engine
![Slide2](https://user-images.githubusercontent.com/43251090/229162160-5899a185-4e94-4ea9-90c9-81a33428163b.PNG)

## Screenshot
![screenshot](https://user-images.githubusercontent.com/43251090/229262519-20975306-abd1-4048-93cf-4eb76aad2e43.jpg)

```Python
# Screenshot.py

import random
import numpy as np
import math
import vgl

xwid,xhgt=300,300
fmm = vgl.FrameManager()
frm_00 = fmm.create(0,0,2,2, vgl.Data(0,xwid,0,xhgt))
frm_01 = fmm.create(2.1,0,2,2, vgl.Data(-4,4,-4,4))
frm_10 = fmm.create(0,2.1,2,2, vgl.Data(-3,3,-1,10))

# Draw Fractal Tree
def fixed_tree(dev, order, length, angle):
    global posx, posy, ctbl, dlength, prv_posx, prv_posy, dev_ani, movie
    
    dx = length*math.sin(angle)
    dy = length*math.cos(angle)
    scale = random.random()
    prv_posx = posx
    prv_posy = posy
    
    posx -= dx
    posy += dy
    
    dev.line(prv_posx, prv_posy, posx, posy, ctbl[int(length-1)], length*dlength*0.04*dev.frm.hgt())
    
    if length <= 10:
        col = vgl.color.hsv(0, scale, 1)
        fruit = vgl.symbol.Circle(scale*0.01, dev.frm.hgt(), 0.001)
        fruit.set_color(col,col)
        dev.begin_symbol(fruit)
        dev.symbol(posx, posy, fruit)
        dev.end_symbol()
    
    if order > 0:
        fixed_tree(dev, order - 1, length*0.8, angle + 0.5)
        fixed_tree(dev, order - 1, length*0.8, angle - 0.5)
        
    posx += dx
    posy -= dy

def run_fixed_tree(dev):
    global posx, posy, order, length, ctbl, dlength, prv_posx, prv_posy
    
    order = 10
    length = 60
    dlength = 1./(length-1)*0.5
    
    ctbl = vgl.create_color_table(0,240, 0.8, 1, length)
    posx = xwid/2;
    posy = 0;
    dlength = 1./(length-1)*0.5
    
    prv_posx = posx
    prv_posy = posy
    fixed_tree(dev, order, length, 0)
    dev.stroke()
 
# Draw Polygons
plist = []

def create_polygon_list():
    plist.append(vgl.geom.Polygon(-2, 2,4,1.5,vgl.color.BLACK, 0.007))
    plist.append(vgl.geom.Polygon( 2, 2,5,1.5,vgl.color.PURPLE, 0.007, lpat = vgl.linepat._PAT_DASH))
    plist.append(vgl.geom.Polygon( 2,-2,6,1.5,vgl.color.PURPLE, 0.007, fcol=vgl.color.GREEN))
    plist.append(vgl.geom.Polygon(-2,-2,7,1.5,vgl.color.PURPLE, 0.007, fcol=vgl.color.YELLOW, lpat = vgl.linepat._PAT_DASHDOT))
    plist.append(vgl.geom.Polygon( 0, 0,3,1,vgl.color.BLACK, 0.007, vgl.color.CYAN))
    
def draw_shape(dev):
    vgl.drawaxis.draw_axis(dev)
    for p in plist:
        dev.polygon(p.get_xs(), p.get_ys(), 
                    p.lcol, p.lthk*dev.frm.hgt(), 
                    p.fcol, lpat=p.get_line_pattern())   

# Plot X^2 curve                    
x2 = np.arange(-3,3.2,0.2)
y2 = x2**2
def plot_x2(dev):
    vgl.drawaxis.draw_axis(dev)
    dev.polyline(x2, y2, vgl.color.BLUE, 0.005*dev.frm.hgt())
    #sym = vgl.symbol.Circle(0.008, dev.frm.hgt(), 0.002)
    #sym = vgl.symbol.RightTriangle(0.02, dev.frm.hgt(), 0.005)
    #sym = vgl.symbol.LeftTriangle(0.02, dev.frm.hgt(), 0.005)
    sym = vgl.symbol.Diamond(0.03, dev.frm.hgt(), 0.005)
    #sym = vgl.symbol.Square(0.02, dev.frm.hgt(), 0.005)
    dev.begin_symbol(sym)
    for x2p, y2p in zip(x2,y2): dev.symbol(x2p,y2p,sym)
    dev.end_symbol()

# Plot Marine Propeller w/ Tecplot data format    
def plot_prop(dev):
    tec_file = "sydney.tec"
    tec_geom = vgl.mesh3d.TecMesh3d(tec_file)
    tec_geom.create_mesh()
    mb = vgl.mesh3d.MeshBBox(tec_geom.mesh)
    xmin, xmax, ymin, ymax, zmin, zmax = mb.get_bbox()
    data = vgl.Data(xmin, xmax, ymin, ymax, zmin, zmax)
    frm_11 = fmm.create(2.1,2.1,2,2, data)
    v3d = vgl.view3d.View3d(frm_11)
    
    v3d.xrotation(30)
    v3d.yrotation(30)
    tec_geom.create_tansform_node(v3d)    
    tec_geom.mode = vgl.mesh3d.MESH_HIDDENLINE
    dev.set_plot(frm_11)
    vgl.plot.plot_tec_mesh(dev, v3d, tec_geom, False)

# Plot Cycloid    
dur = 20
fps = 30
r1 = 1
max_freq  = 3 # 2 Hz
t1 = 0
t2 = 2*np.pi*max_freq
dt = (t2-t1)/(dur*fps)

fpx = lambda a,t : a*(t-math.sin(t))
fpy = lambda a,t : a*(1-math.cos(t))

tt = np.arange(t1, t2, dt)
x = np.array([fpx(r1, t) for t in tt])
y = np.array([fpy(r1, t) for t in tt])
fpx = lambda a,t : a*(t-math.sin(t))
fpy = lambda a,t : a*(1-math.cos(t))

tt = np.arange(t1, t2, dt)
xcy = np.array([fpx(r1, t) for t in tt])
ycy = np.array([fpy(r1, t) for t in tt])

frm_20 = fmm.create(1,2,1.6,0.7, vgl.Data(-1,20,-1,5)) 
frm_20.set_bk_show(True)
frm_20.set_pdom_bk_show(True)
frm_20.show_xgrid()
frm_20.show_ymajor_grid()
frm_20.set_bk_color(vgl.color.Color(200, 180, 100))

def plot_cycloid(dev):
    vgl.draw_frame(dev)
    vgl.draw_axis(dev)
    dev.polyline(xcy,ycy,vgl.color.BLUE, dev.frm.hgt()*0.009)
    
def save_cairo(fname):
    dev = vgl.DeviceCairo(fname, fmm.get_gbbox(), 300)
    
    dev.set_plot(frm_00)
    run_fixed_tree(dev)
    
    create_polygon_list()
    dev.set_plot(frm_01)
    draw_shape(dev)
    
    dev.set_plot(frm_10)
    plot_x2(dev)
    
    plot_prop(dev)
    
    dev.set_device(frm_20, extend=vgl.device._FIT_EXTEND_X)
    plot_cycloid(dev)
    
    dev.close()

save_cairo("screenshot.jpg")
```
