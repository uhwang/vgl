# util.py

import numpy as np

vgl_pi = 3.141592653589793238
vgl_dtr= 0.0174532925199433
vgl_rtd= 57.29577951308233

deg_to_rad = lambda d: d*vgl_dtr
rad_to_deg = lambda r: r*vgl_rtd

def rot_matrix(angle, rad=True):

    if rad:
        c, s = np.cos(angle), np.sin(angle)
    else:
        c, s = np.cos(vgl_dtr*angle), np.sin(vgl_dtr*angle)    
        
    return np.array([[c, -s], [s, c]])
    
def deg_rot_matrix(angle):

    return rot_matrix(angle, rad=False)
    
def rad_rot_matrix(angle):

    return rot_matrix(angle)
    

# angle in degree
def rotation(x,y,angle,rad=True):

    return np.matmul(rot_matrix(angle, rad),[x,y])
        
def deg_rotation(x, y, angle):

    return rotation(x,y,angle,rad=False)
    
def rad_rotation(x, y, angle):

    return rotation(x,y,angle)

