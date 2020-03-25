# Vector Graphic Library (VGL) for Python
#
# axis.py
#
# 2020-2-12 Ver 0.1
#
# Author: Uisang Hwang
# Email : uhwangtx@gmail.com
#

import math
import vgl.color as color
from vgl.linetype import *
import vgl.text as text

TICK_DIR_IN     = 0x01
TICK_DIR_OUT    = 0x02
TICK_DIR_CENTER = 0x03

def get_mantissaexp(v):
	ie = 0;
	vv = math.fabs(v)
	
	if v == 0:
		return 0.0, 0
	
	while vv >= 10.0:
		vv /= 10.0
		ie += 1
	
	while vv < 1.0:
		vv *= 10.0
		ie -= 1
	
	if v >= 0: return  vv, ie
	else:      return -vv, ie

def compute_tick_spacing(vmin, vmax):
	vv=0
	exp=0
	v1=0
	tickSpacing = 0
	minMan, minExp = get_mantissaexp(vmin)
	maxMan, maxExp = get_mantissaexp(vmax)

	if maxExp == minExp:
		if maxExp == 0: # 9.xx~1.xx, 9.xx~1.xx
			v1 = int(vmax-vmin)
			if   v1 <= 2 : tickSpacing = 0.25
			elif v1 >= 10: tickSpacing = 5.0
			else         : tickSpacing = 1.0
		elif maxExp < 0:
			vv = math.pow(10.0, maxExp)
			v1 = (vmax-vmin)/vv
			if   v1 <= 1: vv *= 0.25
			elif v1 > 10:
				while True:
					vv *= 2.0
					v1 = (vmax-vmin)/vv
					if v1 < 10: break
			tickSpacing = vv
		else:
			vv = math.pow(10.0, maxExp)
			v1 = (vmax-vmin)/vv
			if   v1 <= 1: vv *= 0.125
			elif v1 > 10:
				while True:
					vv *= 2.0
					v1 = (vmax-vmin)/vv
					if v1 < 10: break
			tickSpacing = vv
	else:
		if maxExp < 0 and minExp < 0:
			maxExp = maxExp if fabs(vmax) > fabs(vmin) else minExp
			vv = math.pow(10.0, maxExp)*0.5
			v1 = int((vmax-vmin)/vv)
			if   v1 < 4 : vv *= 0.5
			elif v1 > 10: vv *= 2.0
			tickSpacing = vv
		elif (maxExp >= 0 and minExp <= 0) or (maxExp <= 0 and minExp >= 0):
			if maxExp == 0 and minExp < 0:
				exp = maxExp
				vv = math.pow(10.0, exp)
			elif maxExp < 0 and minExp == 0:
				exp = minExp
				vv = math.pow(10.0, exp)
			else:
				exp = max(maxExp, minExp)
				vv = math.ceil(pow(10.0, exp))
			v1 = int((vmax-vmin)/vv)
			
			if v1 <= 1:
				exp = 0.25
				vv *= 0.25
			elif v1 > 10:
				while True:
					vv *= 2.0
					v1 = (vmax-vmin)/vv
					if v1 < 10: break
			tickSpacing = vv
		else: # both are positive
			vv = math.pow(10.0, max(maxExp, minExp))*0.1
			v1 = int(vmax-vmin)/vv
			if v1 > 10: 
				while True:
					vv *= 2.0
					v1 = (vmax-vmin)/vv
					if v1 < 10: break
			tickSpacing = vv

	return tickSpacing

#return: startMjTick, startMiTick, firstNMiTick	
def compute_tick_position(vmin, vmax, mjspace, nMiTick):
	a=0.
	c=0.
	d=0
	b=mjspace/float(nMiTick+1)
	vmax = float(vmax)
	vmin = float(vmin)
	
	if vmax > 0 and vmin >= 0:
		if vmin == 0:
			startMjTick = vmin
			startMiTick = vmin+b
			firstNMiTick = 0
			return startMjTick, startMiTick, firstNMiTick
		a = 0
		while a < vmin: a += mjspace
		startMjTick = a
	else:
		a = 0
		while a > vmin: a-= mjspace
		a += mjspace
		startMjTick = a
		
	c = a - vmin
	if c < b:
		startMiTick = 0
		firstNMiTick = 0
	elif c == b:
		startMiTick = startMjTick-b
		firstNMiTick = 1
	else:
		d = 0
		while c > b:  
			c -= b
			d += 1
		startMiTick = startMjTick-b*d
		firstNMiTick = d
	
	return startMjTick, startMiTick, firstNMiTick	
	
class Label(text.Text):
	def __init__(self, pos=0.02):
		super().__init__()
		self.pos = pos
		self.size = 0.02

class Grid(LineLevelC):
	def __init__(self, show, lcol=color.BLACK, lthk=0.001, lpat=0, patlen=0):
		super().__init__(lcol, lthk, lpat, patlen)
		self.show = show
		
	def set(self, show, lcol, lthk, lpat, patlen):
		super().set(lcol, lthk, lpat, patlen)
		self.show = show
		
class Tick(LineLevelB):
	def __init__(self, show=True, lcol=color.BLACK, lthk=0.001, llen=0.007):
		super().__init__(lcol, lthk, llen)
		self.show         = show
		self.auto_spacing = True
		self.dir          = TICK_DIR_IN

class Axis(LineLevelA):
	def __init__(self, min, max, lcol = color.BLACK, lthk=0.004):
		super().__init__(lcol, lthk)
		self.min                 = min
		self.max                 = max
		self.major_tick          = Tick(lthk=0.004, llen=0.018)
		self.minor_tick          = Tick(lthk=0.001, llen=0.01)
		self.major_grid          = Grid(show=False)
		self.minor_grid          = Grid(show=False)
		self.nminor_tick         = 4
		self.update_tick(min, max)
		self.xlabel              = Label()
		self.ylabel              = Label()
		
	def update_tick(self, min, max):
		self.spacing             = compute_tick_spacing(min,max)
		a,b,c=compute_tick_position(min,max,self.spacing,self.nminor_tick)
		self.first_major_tick_pos = a
		self.first_minor_tick_pos = b
		self.first_nminor_tick    = c
	
	def get_major_tick(self): return self.major_tick	
	def get_minor_tick(self): return self.minor_tick
	def get_xlabel(self): return self.xlabel
	def get_ylabel(self): return self.ylabel

	
def main():
	x=Axis(-3,3)
	a,b,c=compute_tick_position(-1,1,0.25,4)
	print(a,b,c)
	
if __name__ == '__main__':
	main()