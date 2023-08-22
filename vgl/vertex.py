# Vector Graphic Library (VGL) for Python
#
# vertex.py
#
# 2020-2-12 Ver 0.1
#
# Author: Uisang Hwang
# Email : uhwangtx@gmail.com
#

import numpy as np

from . import util

class Vertex():
    def __init__(self, nvert, dim=2, src=None):
        self.nvert = nvert
        self.dim = dim
        self.vertex = np.empty(nvert*dim, dtype='float32')
        
        if isinstance(src, np.ndarray) or\
           isinstance(src, list) or\
           isinstance(src, tuple):
            self.point = src
            
    def get_vertices(self): 
        return self.vertex
    
    def get_vertex(self, index): 
        return [self.vertex[index*2], self.vertex[index*2+1]]
        
    def get_nvertex(self): 
        return int(self.vertex.size/2)
    
    def get_xs(self): 
        return self.vertex[::2]
    
    def get_ys(self): 
        return self.vertex[1::2]

    def get_xss(self): 
        return np.append(self.vertex[::2], self.vertex[0])
    
    def get_yss(self): 
        return np.append(self.vertex[1::2], self.vertex[1])
    
    def set_vertex(self, i, x,y): 
        self.vertex[i*2]=x
        self.vertex[i*2+1]=y
        
    def rotate(self, deg):
        rm = util.deg_rot_matrix(deg)
        self.vertex = np.array([ np.dot(rm, v) 
                                 for v in self.vertex.reshape(self.nvert,2) ]).flatten()
        return self
        
    def rotate_about_point(self, px, py, deg):
        vv = util.deg_rot_about_point(px,py,self.get_xs(), self.get_ys(), deg)
        self.vertex[::2] = vv[0]
        self.vertex[1::2] = vv[1]
        
    def npoint(self):
        return self.nvert
        
    def transx(self, tx):
        self.vertex[ ::2] += tx
    
    def transy(self, ty):
        self.vertex[1::2] += ty
        
    def trans(self, tx, ty):
        self.transx(tx)
        self.transy(ty)
        return self
    
    def join(self, src):
        vv = np.concatenate((self.vertex, src.vertex), axis=None)
        return Vertex(vv.size//self.dim, src=vv)
        
    def endpoint(self):
        return self.vertex[-2], self.vertex[-1]
        
    def firstpoint(self):
        return self.vertex[0], self.vertex[1]
                
    def xmin(self):
        return self.vertex[::2].min()

    def xmax(self):
        return self.vertex[::2].max()
        
    def ymin(self):
        return self.vertex[1::2].min()
        
    def ymax(self):
        return self.vertex[1::2].max()
        
    @property
    def point(self):
        return self.vertex
        
    # alist should be one dim array, list, or tuple
    @point.setter
    def point(self, alike):
        if hasattr(alike, "__iter__"):
            if isinstance(alike, np.ndarray): 
                size = alike.size
            if isinstance(alike, list) or\
               isinstance(alike, tuple):
                size = len(alike)
               
            if size == self.vertex.size:
                for i, x in enumerate(alike):
                    self.vertex[i] = x
            else:
                raise ValueError('Vertes: dimension mismatch')
                
    # iterable : array, tuple, list
    def copy(self):
        return Vertex(self.nvert, src=self.vertex)

