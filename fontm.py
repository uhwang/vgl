# Vector Graphic Library (VGL) for Python
#
# fontm.py
#
# 2020-2-12 Ver 0.1
#
# Author: Uisang Hwang
# Email : uhwangtx@gmail.com
#

from font import romans           # FONT_ROMANSIMPLEX        = 0
from font import romand           # FONT_ROMANDUPLEX         = 1
from font import romant           # FONT_ROMANTRIPLEX        = 2
from font import cursive          # FONT_CURSIVE             = 3
from font import futural          # FONT_FUTURAL             = 4
from font import futuram          # FONT_FUTURAM             = 5
from font import timesr           # FONT_TIMESROMAN          = 6
from font import timesrb          # FONT_TIMESROMANBOLD      = 7
from font import timesg           # FONT_TIMESGREEK          = 8
from font import timesi           # FONT_TIMESITALIAN        = 9
from font import timesib          # FONT_TIMESITALIANBOLD    = 10
from font import gothgbt          # FONT_GOTHENGTRIPLEX      = 11
from font import gothgrt          # FONT_GOTHGERMANTRIPLEX   = 12
from font import gothiceng        # FONT_GOTHENGLISH         = 13
from font import gothicger        # FONT_GOTHGERMAN          = 14
from font import gothicita        # FONT_GOTHITALIAN         = 15
from font import gothitt          # FONT_GOTHITALIANTRIPLEX  = 16
from font import greek            # FONT_GREEK               = 17
from font import greekc           # FONT_GREEKCOMPLEX        = 18
from font import greeks           # FONT_GREEKSIMPLEX        = 19
from font import mathlow          # FONT_MATHLOW             = 20
from font import mathupp          # FONT_MATHUPPER           = 31
from font import mathsymbol       # FONT_MATHSYMBOL          = 32
from font import scriptc          # FONT_SCRIPTCOMPLEX       = 33
from font import scripts          # FONT_SCRIPTSIMPLEX       = 34
from font import symbol           # FONT_SYMBOL              = 35
from font import marker           # FONT_MARKER              = 36
from font import astrology        # FONT_ASTROLOGY           = 37
from font import cyillic          # FONT_CYILLIC             = 38
from font import cyrilc1          # FONT_CYILLIC1            = 39
from font import meteorology      # FONT_METEOROLOGY         = 30
from font import music            # FONT_MUSIC               = 31

import vgl.fontid as ids

class FontManager():
	def __init__(self):
		self.font_pool = (
			(romans     .font_name, romans     .font_map),
			(romand     .font_name, romand     .font_map),
			(romant     .font_name, romant     .font_map),
			(cursive    .font_name, cursive    .font_map),
			(futural    .font_name, futural    .font_map),
			(futuram    .font_name, futuram    .font_map),
			(timesr     .font_name, timesr     .font_map),
			(timesrb    .font_name, timesrb    .font_map),
			(timesg     .font_name, timesg     .font_map),
			(timesi     .font_name, timesi     .font_map),
			(timesib    .font_name, timesib    .font_map),
			(gothgbt    .font_name, gothgbt    .font_map),
			(gothgrt    .font_name, gothgrt    .font_map),
			(gothiceng  .font_name, gothiceng  .font_map),
			(gothicger  .font_name, gothicger  .font_map),
			(gothicita  .font_name, gothicita  .font_map),
			(gothitt    .font_name, gothitt    .font_map),
			(greek      .font_name, greek      .font_map),
			(greekc     .font_name, greekc     .font_map),
			(greeks     .font_name, greeks     .font_map),
			(mathlow    .font_name, mathlow    .font_map),
			(mathupp    .font_name, mathupp    .font_map),
			(mathsymbol .font_name, mathsymbol .font_map),
			(scriptc    .font_name, scriptc    .font_map),
			(scripts    .font_name, scripts    .font_map),
			(symbol     .font_name, symbol     .font_map),
			(marker     .font_name, marker     .font_map),
			(astrology  .font_name, astrology  .font_map),
			(cyillic    .font_name, cyillic    .font_map),
			(cyrilc1    .font_name, cyrilc1    .font_map),
			(meteorology.font_name, meteorology.font_map),
			(music      .font_name, music      .font_map)
		)
	def get_font(self, fid):
		#if fid < ids.FONT_ROMANSIMPLEX and fid > ids.FONT_MUSIC:
		#	raise 
		return self.font_pool[fid]

	def get_font_map(self, fid):
		return self.font_pool[fid][1]
		
	def get_font_name(self, fid):
		return self.font_pool[fid][0]

font_manager = FontManager()
#def test():

def main():
	fm = FontManager()
	ff = fm.get_font(0)
	print(ff[0])

if __name__ == '__main__':
	main()