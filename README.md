# vgl
Vector Graphic Library for Python

# Introduction
## Plotting Engine
![VGL](https://github.com/uhwang/vgl/assets/43251090/9dd8c0b5-a10b-449e-9f74-b524721b50b7)

## Screenshot
![screenshot](https://user-images.githubusercontent.com/43251090/229310460-f6ff7567-4b2d-4e27-b041-45ad96263086.jpg)

```Python
# Screenshot.py

import random
import numpy as np
import math
import vgl
f_wid, f_hgt = 3,3 # inch
f_sx, f_sy = 0.5, 0.5
skip = 0.1
xwid = 300
fmm = vgl.FrameManager()
frm_00 = fmm.create(f_sx,f_sy,f_wid,f_hgt, vgl.Data(0,xwid,0,300))
frm_01 = fmm.create(f_sx+skip+f_wid,f_sy,f_wid,f_hgt, vgl.Data(-4,4,-4,4))
frm_10 = fmm.create(f_sx,f_sy+skip+f_hgt,f_wid, f_hgt, vgl.Data(-3,3,-1,10))

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
    
    dev.line(prv_posx, prv_posy, posx, posy, ctbl[int(length-1)], length*dlength*0.04)
    
    if length <= 10:
        col = vgl.color.hsv(0, scale, 1)
        fruit = vgl.symbol.Circle(scale*0.01, dev.frm.hgt(), 0.001)
        fruit.set_color(col,col)
        dev.symbol(posx, posy, fruit)
    
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
    vgl.draw_axis(dev)
    for p in plist:
        dev.polygon(p.get_xs(), p.get_ys(), 
                    lcol=p.lcol,
                    lthk=p.lthk,
                    lpat=p.get_line_pattern(),
                    fcol=p.fcol)   

# Plot X^2 curve                    
x2 = np.arange(-3,3.2,0.2)
y2 = x2**2
def plot_x2(dev):
    vgl.drawaxis.draw_axis(dev)
    dev.polyline(x2, y2, vgl.color.BLUE, 0.005)
    vgl.plot_diamond_symbol(dev, x2, y2)

# Plot Marine Propeller w/ Tecplot data format    
def plot_prop(dev):
    tec_file = "sydney.tec"
    tec_geom = vgl.mesh3d.TecMesh3d(tec_file)
    tec_geom.create_mesh()
    mb = vgl.mesh3d.MeshBBox(tec_geom.mesh)
    xmin, xmax, ymin, ymax, zmin, zmax = mb.get_bbox()
    data = vgl.Data(xmin, xmax, ymin, ymax, zmin, zmax)
    frm_11 = fmm.create(f_sx+skip+f_wid,f_sy+skip+f_hgt,f_wid,f_hgt, data)
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
xcy = np.array([fpx(r1, t) for t in tt])
ycy = np.array([fpy(r1, t) for t in tt])
frm_20 = fmm.create(f_sx,f_sy+2*(skip+f_hgt),skip+f_wid*2,f_hgt/2, vgl.Data(-1,20,-1,5)) 
frm_20.show_all_grid()
frm_20.set_xlabel_size(0.06)
frm_20.set_ylabel_size(0.06)
frm_20.set_label_font(vgl.fontid.FONT_TIMESROMANBOLD)

def plot_cycloid(dev):
    vgl.draw_frame(dev)
    vgl.draw_axis(dev)
    dev.polyline(xcy,ycy,vgl.color.MAGENTA, 0.02)
    
def save(dev):
    dev.set_device(frm_00)
    run_fixed_tree(dev)
    
    create_polygon_list()
    frm_01.show_all_major_grid()
    dev.set_device(frm_01)
    draw_shape(dev)
    
    dev.set_device(frm_10)
    plot_x2(dev)
    
    plot_prop(dev)
    
    dev.set_device(frm_20, extend=vgl.device._FIT_EXTEND_X)
    plot_cycloid(dev)
    
    dev.close()

dev_img = vgl.DeviceCairo("screenshot.jpg", fmm.get_gbbox(),300)
dev_pdf = vgl.DevicePDF("screenshot.pdf", fmm.get_gbbox())
dev_wmf = vgl.DeviceWMF("screenshot.wmf", fmm.get_gbbox())
dev_emf = vgl.DeviceEMF("screenshot.emf", fmm.get_gbbox())
dev_svg = vgl.DeviceSVG("screenshot.svg", fmm.get_gbbox(),300)
    
save(dev_img)
save(dev_pdf)
save(dev_wmf)
save(dev_emf)
save(dev_svg)
```
