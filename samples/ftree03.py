# ftree03.py
import math
import random
import vgl
import coltbl

xwid,xhgt=300,300
data = vgl.Data(0,xwid,0,xhgt)
fmm = vgl.FrameManager()
frm1 = fmm.create(0,0,3,3, data)
frm2 = fmm.create(3.1,0,3,3, vgl.Data(-5,5,-5,5))

def fixed_tree(dev, order, length, angle):
    global posx, posy, ctbl, dlength, prv_posx, prv_posy, dev_ani, movie, img_seq
    
    dx = length*math.sin(angle);
    dy = length*math.cos(angle);
    scale = random.random()
    prv_posx = posx
    prv_posy = posy
    
    posx -= dx;
    posy += dy;
    
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
        
    posx += dx;
    posy -= dy;

def run_fixed_tree(dev):
    global posx, posy, order, length, ctbl, dlength, prv_posx, prv_posy
   
    print("... Run fixed tree ...")
    order = 10
    length = 60
    dlength = 1./(length-1)*0.5;

    ctbl = coltbl.create_color_table(0,240, 0.8, 1, length)
    posx = xwid/2;
    posy = 0;
    dlength = 1./(length-1)*0.5;

    prv_posx = posx
    prv_posy = posy
    fixed_tree(dev, order, length, 0);

def koch_curve(dev, length, theta, order):
    global posx, posy
    
    if order is 0:
        x2 = posx+length*math.cos(vgl.deg_to_rad(theta))
        y2 = posy+length*math.sin(vgl.deg_to_rad(theta))
        dev.line(posx, posy, x2, y2, vgl.color.BLACK, 0.001*dev.frm.hgt())
        posx, posy = x2, y2
    else:
        koch_curve(dev, length/3.0, theta    ,order-1)
        koch_curve(dev, length/3.0, theta +60,order-1)
        koch_curve(dev, length/3.0, theta -60,order-1)
        koch_curve(dev, length/3.0, theta    ,order-1)
        
def run_koch_curve(dev):
    global posx, posy
    print("... Run Koch curve ...")
    sin60 = math.sin(vgl.deg_to_rad(60))
    length = 6
    h1 = length*sin60
    h2 = length/3.0*sin60
    h3 = (h1+h2)*0.5
    sx, sy = -length*0.5, h3-h2
    
    pxs = [sx,sx+length,sx+length*0.5]
    pys = [sy,sy,-h3]
    ang = [0, -120, -240]
    for i, (px, py, deg) in enumerate(zip(pxs, pys, ang)): 
        posx = px
        posy = py
        koch_curve(dev, length, deg, 3)
    
def save_wmf(fname, gbbox):
    dev = vgl.DeviceWindowsMetafile(fname, gbbox)
    dev.set_device(frm1)
    run_fixed_tree(dev)
    dev.set_device(frm2)
    run_koch_curve(dev)
    vgl.drawfrm.draw_axis(dev, dev.frm.data)
    vgl.drawtick.draw_tick_2d(dev)	
    vgl.drawfrm.draw_grid(dev, dev.frm.data, 1)
    vgl.drawlabel.draw_label_2d(dev)
    dev.close()
    
def save_cairo(fname, gbox, dpi):
    dev_img = vgl.DeviceCairo(fname, gbox, dpi)
    dev_img.fill_white()
    dev_img.set_plot(frm1)
    run_fixed_tree(dev_img)
    dev_img.set_device(frm2)
    run_koch_curve(dev_img)
    dev_img.close()

#save_cairo("ftre03.png", fmm.get_gbbox(), 100)
save_wmf("ftre03.wmf", fmm.get_gbbox())