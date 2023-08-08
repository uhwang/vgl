import math
import random
import vgl

xmin,xmax,ymin,ymax=-4,4,-4,4
data = vgl.Data(xmin,xmax,ymin,ymax)
fmm = vgl.FrameManager()
frm = fmm.create(0,0,3,3, data)
gbox = fmm.get_gbbox()

def koch_curve(dev, length, theta, order, col):
    global posx, posy
    
    if order == 0:
        x2 = posx+length*math.cos(vgl.deg_to_rad(theta))
        y2 = posy+length*math.sin(vgl.deg_to_rad(theta))
        dev.line(posx, posy, x2, y2, col, 0.001*dev.frm.hgt())
        posx, posy = x2, y2
    else:
        koch_curve(dev, length/3.0, theta    ,order-1, col)
        koch_curve(dev, length/3.0, theta +60,order-1, col)
        koch_curve(dev, length/3.0, theta -60,order-1, col)
        koch_curve(dev, length/3.0, theta    ,order-1, col)
        
def draw(dev):
    global posx, posy
    dev.set_device(frm)
    
    print("... Run Koch curve ...")
    sin60 = math.sin(vgl.deg_to_rad(60))
    step = 6
    order = [x for x in range(step)]
    length = [x+(1-math.sin(vgl.deg_to_rad(90-90.0/step*(x-1)))) for x in range(1,step+1)]
    ctbl = vgl.color.create_color_table(0,240, 0.8, 1, step)

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
    dev.close()

def save():
    import chkfld
    
    chkfld.create_folder("./koch")    
    
    dev_wmf = vgl.DeviceWMF("./koch/koch.wmf", gbox)
    dev_emf = vgl.DeviceEMF("./koch/koch.emf", gbox)
    dev_pdf = vgl.DevicePDF("./koch/koch.pdf", gbox)
    dev_img = vgl.DeviceIMG("./koch/koch.jpg", gbox, 200)
    dev_svg = vgl.DeviceSVG("./koch/koch.svg", gbox, 200)
    dev_ppt = vgl.DevicePPT("./koch/koch.pptx",gbox)
    
    draw(dev_wmf)
    draw(dev_emf)
    draw(dev_pdf)
    draw(dev_img)
    draw(dev_svg)
    draw(dev_ppt
    
if __name__ == "__main__":
    save()    