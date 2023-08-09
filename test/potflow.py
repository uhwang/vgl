# potflow.py

import numpy as np
import vgl

UNIFORM_SOURCE = 0
UNIFORM_VORTEX = 1
UNIFORM_DIPOLE = 2
UNIFORM_RNKOVL = 3 
    
U    = 1.0
Q    = 1.0
M    = 1.0
RK   = 1.5
RKM  = 0.2
GAM  = 2.2
PI   = 3.141592653589793239
TUPI = 2.0*PI
FOPI = 2*TUPI
R2PI = 1/TUPI
R4PI = 1/FOPI

X2 = lambda x: x*x

#---------------UNIFORM + SOURCE------------------------------

def dist(x0, y0, x1, y1):

    return np.sqrt((x1-x0)**2 + (y1-y0)**2)


def uus(U, alpha, x0, y0, x1, y1):

    R = dist(x0,y0,x1,y1)
    return U*np.cos(alpha) + Q*(x1-x0)/(TUPI*R*R)

def vus(U, alpha, x0,  y0,  x1,  y1):

    R = dist(x0,y0,x1,y1)
    return U*np.sin(alpha) + Q*(y1-y0)/(TUPI*R*R)

#--------------UNIFORM + DIPOLE -----------------------------

def uud(U, alpha, x0,  y0,  x1,  y1):

	return U*np.cos(alpha) - \
           M*R4PI*(X2(y1-y0)-\
           2*X2(x1-x0))/\
           np.power(X2(y1-y0)+X2(x1-x0), 5/2.)

def vud(U, alpha, x0,  y0,  x1,  y1):

	return U*np.sin(alpha) - \
           3*M*R4PI*((y1-y0)*(x1-x0))/\
           np.power((y1-y0)**2+(x1-x0)**2, 5/2.)

#--------------UNIFORM + VORTEX -----------------------------

def uuv(U, alpha, x0,  y0,  x1,  y1):

    return U*np.cos(alpha) + \
           GAM*R2PI*(y1-y0)/\
           ((x1-x0)**2+(y1-y0)**2)


def vuv(U, alpha, x0,  y0,  x1,  y1):

    return U*np.sin(alpha) - \
           GAM*R2PI*(x1-x0)/\
           ((x1-x0)**2+(y1-y0)**2)


#---------------UNIFORM + SOURCE + SINK ----------------------
# Reference: FLUID MECHANICS, 2nd Ed. by A.K. Mohanty         

def usk(U, alpha, x0,  y0,  x1,  y1):

	return U*np.cos(alpha)+\
           RK*R2PI*((x1+RKM)/(y1**2+(x1+RKM)**2)-\
                    (x1-RKM)/(y1**2+(x1-RKM)**2))


def vsk(U, alpha, x0,  y0,  x1,  y1):

	return U*np.sin(alpha) - \
           RK*R2PI*(y1/(y1**2+(x1-RKM)**2)-\
                    y1/(y1**2+(x1+RKM)**2))

uu = [uus, uuv, uud, usk ]
vv = [vus, vuv, vud, vsk ]

def potential( 
              ufl,
              alpha, 
              minx, 
              miny,
              maxx,  
              maxy,  
              nsgx,  
              nsgy, 
              ipot ):

    i, j = 0, 0
    
    delx = (maxx - minx)/(nsgx-1)
    dely = (maxy - miny)/(nsgy-1)
    dell = delx 
    old_degree=0
    
    xm1p, ym1p = 0, 0 
    um  , vm   = 0, 0 
    ump , vmp  = 0, 0 
    qm  , qmp  = 0, 0
    x0  , y0   = 0, 0 
    x1  , y1   = 0, 0 
    startx = 0
    
    gridy = np.linspace(miny, maxy, nsgy, endpoint=True)
    
    x0 = 0.0000
    y0 = 0.0000
    startx = minx

    stream_lines = list()
    
    for yval in gridy:
    
        x1 = startx
        y1 = yval
        
        sub_lines = list()
        sub_lines.append((x1,y1))
    
        while True: 
        
            um = uu[ipot](ufl, alpha, x0, y0, x1, y1)
            vm = vv[ipot](ufl, alpha, x0, y0, x1, y1)
            qm = np.sqrt(um*um + vm*vm)
    
            # 1st order forward difference
            xm1p = x1 + um/qm * dell
            ym1p = y1 + vm/qm * dell
            ump = uu[ipot](ufl, alpha, x0, y0, xm1p, ym1p)
            vmp = vv[ipot](ufl, alpha, x0, y0, xm1p, ym1p)
            qmp = np.sqrt(ump*ump + vmp*vmp)
    
            # central difference method : improved method
            xm1p = (x1 + 0.5 * ( um / qm + ump / qmp ) * dell)
            ym1p = (y1 + 0.5 * ( vm / qm + vmp / qmp ) * dell)
    
            if( xm1p < minx or
                xm1p > maxx or 
                ym1p < miny or 
                ym1p > maxy):
                break

            sub_lines.append((xm1p, ym1p))
            x1 = xm1p
            y1 = ym1p
        
        stream_lines.append(sub_lines)
        
    return stream_lines

def uniform_source(dev):
    
    minx=-1.0
    maxx= 1.0
    miny=-1.0
    maxy= 1.0
    
    stream_lines = potential(U, 0., minx,miny,maxx,maxy, 50, 40, UNIFORM_SOURCE)

    for line in stream_lines:
        
        xx = [l[0] for l in line]
        yy = [l[1] for l in line]
            
        dev.polyline(xx, yy)

def uniform_vortex(dev):

    minx=-1.0
    maxx= 1.0
    miny=-1.0
    maxy= 1.0
    
    stream_lines = potential(U, 0., minx,miny,maxx,maxy, 50, 40, UNIFORM_VORTEX)

    for line in stream_lines:
        
        xx = [l[0] for l in line]
        yy = [l[1] for l in line]
            
        dev.polyline(xx, yy)

def uniform_dipole(dev):

    minx=-1.0
    maxx= 1.0
    miny=-1.0
    maxy= 1.0
    
    stream_lines = potential(U, 0., minx,miny,maxx,maxy, 50, 40, UNIFORM_DIPOLE)

    for line in stream_lines:
        
        xx = [l[0] for l in line]
        yy = [l[1] for l in line]
            
        dev.polyline(xx, yy)
        
def uniform_rankin(dev):

    minx=-1.0
    maxx= 1.0
    miny=-1.0
    maxy= 1.0
    
    stream_lines = potential(U, 0., minx,miny,maxx,maxy, 50, 40, UNIFORM_RNKOVL)

    for line in stream_lines:
        
        xx = [l[0] for l in line]
        yy = [l[1] for l in line]
            
        dev.polyline(xx, yy)
        
fmm  = vgl.FrameManager()
frm1 = fmm.create(0,0,3,3, vgl.Data(-1, 1, -1, 1))
frm2 = fmm.create(3,0,3,3, vgl.Data(-1, 1, -1, 1))
frm3 = fmm.create(0,3,3,3, vgl.Data(-1, 1, -1, 1))
frm4 = fmm.create(3,3,3,3, vgl.Data(-1, 1, -1, 1))

def plot(dev):
    
    print("Unifor + Source")
    dev.set_device(frm1)
    uniform_source(dev)
    
    print("Unifor + Vortex")
    dev.set_device(frm2)
    uniform_vortex(dev)
    
    print("Unifor + Dipole")
    dev.set_device(frm3)
    uniform_dipole(dev)
    
    print("Rankin Oval")
    dev.set_device(frm4)
    uniform_rankin(dev)    
    
    dev.close()
    
def save():
    import chkfld
    
    if not chkfld.create_folder("./potflow"):
        return
            
    dev_img = vgl.DeviceIMG("./potflow/potflow.jpg", fmm.get_gbbox(), 300)
    dev_pdf = vgl.DevicePDF("./potflow/potflow.pdf", fmm.get_gbbox())
    dev_wmf = vgl.DeviceWMF("./potflow/potflow.wmf", fmm.get_gbbox())
    dev_emf = vgl.DeviceEMF("./potflow/potflow.emf", fmm.get_gbbox())
    dev_svg = vgl.DeviceSVG("./potflow/potflow.svg", fmm.get_gbbox(), 300)
    dev_ppt = vgl.DevicePPT("./potflow/potflow.pptx",fmm.get_gbbox())
    
    plot(dev_img)
    plot(dev_pdf)
    plot(dev_wmf)
    plot(dev_emf)
    plot(dev_svg)
    plot(dev_ppt)
    
if __name__ == "__main__":
    save()
        
    