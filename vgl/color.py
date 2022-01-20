# Vector Graphic Library (VGL) for Python
#
# color.py
#
# 2020-2-12 Ver 0.1
#
# Author: Uisang Hwang
# Email : uhwangtx@gmail.com
#
def get_rgb(c): return c[0]/255., c[1]/255., c[2]/255.
def get_style(c): return "#%02x%02x%02x"%(c.r, c.g, c.b)
def normalize(c): return color(c.r/255., c.g/255., c.b/255.)

 
class color():
    def __init__(self,r=255,g=255,b=255):
        #self.conv(col)
        self.r = r
        self.g = g
        self.b = b
        
    def __str__(self):
        return "RGB: %03d, %03d, %03d"%(self.r, self.g, self.b)
        
BLACK   = color(0  ,  0,  0)
WHITE   = color(255,255,255)
RED     = color(255,  0,  0)
GREEN   = color(0  ,255,  0)
BLUE    = color(0  ,  0,255)
YELLOW  = color(255,255,  0)
MAGENTA = color(255,  0,255)
CYAN    = color(0  ,255,255)
PURPLE  = color(255,  0,255)
CUSTOM1 = color(255,127,  0)
CUSTOM2 = color(127,255,  0)
CUSTOM3 = color(0  ,255,127)
CUSTOM4 = color(127,  0,255)
CUSTOM5 = color(255,  0,127)
GRAY20  = color( 20, 20, 20)
GRAY50  = color( 50, 50, 50)
GRAY100 = color(100,100,100)

agg_color = lambda x: (0,x[2],x[1],x[0])
get_gray  = lambda x: (int(x*255), int(x*255), int(x*255))

#class rgb():
#    def __init__(self,col=WHITE):
#        self.conv(col)
#        
#    def conv(self,col):
#        self.r, self.g, self.b = get_rgb(col)
#        
#    def __str__(self):
#        return "RGB: %03d, %03d, %03d"%(self.r, self.g, self.b)

#inv_255 = 0.00392156862745

def hsv(H, S, V):
	import math
	I = 0.0
	F = 0.0
	P = 0.0
	Q = 0.0
	T = 0.0
	R1 = 0.0
	G1 = 0.0
	B1 = 0.0
	
	if S == 0:
		if H <= 0 or H > 360 :
			return (V,V,V)

	if H==360: H=0

	H = H/60;
	I = math.floor(H)
	F = H-I
	P = V*(1-S)
	Q = V*(1-S*F)
	T = V*(1-S*(1-F))
	
	int_I = int(I)
	
	if   int_I == 0: 
		R1 = V
		G1 = T
		B1 = P
	elif int_I == 1: 
		R1 = Q
		G1 = V
		B1 = P
	elif int_I == 2: 
		R1 = P
		G1 = V
		B1 = T
	elif int_I == 3: 
		R1 = P
		G1 = Q
		B1 = V
	elif int_I == 4: 
		R1 = T
		G1 = P
		B1 = V
	else           : 
		R1 = V
		G1 = P
		B1 = Q
	
	R = int(R1 * 255)
	G = int(G1 * 255)
	B = int(B1 * 255)

	return color(R,G,B)