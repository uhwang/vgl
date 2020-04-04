# Vector Graphic Library (VGL) for Python
#
# color.py
#
# 2020-2-12 Ver 0.1
#
# Author: Uisang Hwang
# Email : uhwangtx@gmail.com
#

BLACK   = (0  ,  0,  0)
WHITE   = (255,255,255)
RED     = (255,  0,  0)
GREEN   = (0  ,255,  0)
BLUE    = (0  ,  0,255)
YELLOW  = (255,255,  0)
MAGENTA = (255,  0,255)
CYAN    = (0  ,255,255)
PURPLE  = (255,  0,255)
CUSTOM1 = (255,127,  0)
CUSTOM2 = (127,255,  0)
CUSTOM3 = (0  ,255,127)
CUSTOM4 = (127,  0,255)
CUSTOM5 = (255,  0,127)
GRAY20  = ( 20, 20, 20)
GRAY50  = ( 50, 50, 50)
GRAY100 = (100,100,100)

agg_color = lambda x: (0,x[2],x[1],x[0])

def get_rgb(c): return c[0]/255., c[1]/255., c[2]/255.

#def get_cairo_rgb(c): 
#	return 

class rgb():
	def __init__(self,col=WHITE):
		self.conv(col)
		
	def conv(self,col):
		self.r, self.g, self.b = get_rgb(col)

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

	return (R,G,B)