from math import sin, cos
import random
import vgl

xwid,xhgt=300,300
data = vgl.Data(0,xwid,0,xhgt)
fmm = vgl.FrameManager()
frm = fmm.create(1,1,6,6, data)
gbox= fmm.get_gbbox()

def fixed_tree(dev, order, length, angle):
    global posx, posy, ctbl, dlength, prv_posx, prv_posy, dev_ani, movie
    
    dx = length*sin(angle)
    dy = length*cos(angle)
    scale = random.random()
    prv_posx = posx
    prv_posy = posy
    
    posx -= dx
    posy += dy
    
    dev.line(prv_posx, prv_posy, posx, posy, ctbl[int(length-1)], length*dlength*0.04)
    
    #if length <= 10:
    if length <= 30:
        col = vgl.color.hsv(0, scale, 1)
        fruit = vgl.symbol.Circle(scale*0.01, dev.frm.hgt(), 0.001)
        fruit.set_color(col,col)
        dev.symbol(posx, posy, fruit)

    if order > 0:
        fixed_tree(dev, order - 1, length*0.8, angle + 0.5)
        fixed_tree(dev, order - 1, length*0.8, angle - 0.5)
        
    posx += dx
    posy -= dy
   
def draw(dev):
    global posx, posy, order, length, ctbl, dlength, prv_posx, prv_posy
    
    dev.set_device(frm)
    #order = 10
    order = 4
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
    dev.close()

def save():
    import chkfld
    
    chkfld.create_folder("./fractree")
    
    dev_wmf = vgl.DeviceWMF("./fractree/fractree.wmf", gbox)
    dev_emf = vgl.DeviceEMF("./fractree/fractree.emf", gbox)
    #dev_pdf = vgl.DevicePDF("./fractree/fractree.pdf", gbox)
    #dev_svg = vgl.DeviceSVG("./fractree/fractree.svg", gbox, 200)
    #dev_img = vgl.DeviceIMG("./fractree/fractree.jpg", gbox, 200)
    #dev_ppt = vgl.DevicePPT("./fractree/fractree.pptx",gbox)
    
    draw(dev_wmf)
    draw(dev_emf)
    #draw(dev_pdf)
    #draw(dev_svg)
    #draw(dev_ppt)
    #draw(dev_img)
    
if __name__ == "__main__":
    save()
