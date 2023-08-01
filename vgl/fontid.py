# Vector Graphic Library (VGL) for Python
#
# fontid.py
#
# 2020-2-12 Ver 0.1
#
# Author: Uisang Hwang
# Email : uhwangtx@gmail.com
#

FONT_ROMANSIMPLEX        = 0
FONT_ROMANDUPLEX         = 1
FONT_ROMANTRIPLEX        = 2
FONT_CURSIVE             = 3
FONT_FUTURAL             = 4
FONT_FUTURAM             = 5
FONT_TIMESROMAN          = 6
FONT_TIMESROMANBOLD      = 7
FONT_TIMESGREEK          = 8
FONT_TIMESITALIAN        = 9
FONT_TIMESITALIANBOLD    = 10
FONT_GOTHENGTRIPLEX      = 11
FONT_GOTHGERMANTRIPLEX   = 12
FONT_GOTHENGLISH         = 13
FONT_GOTHGERMAN          = 14
FONT_GOTHITALIAN         = 15
FONT_GOTHITALIANTRIPLEX  = 16
FONT_GREEK               = 17
FONT_GREEKCOMPLEX        = 18
FONT_GREEKSIMPLEX        = 19
FONT_MATHLOW             = 20
FONT_MATHUPPER           = 21
FONT_MATHSYMBOL          = 22
FONT_SCRIPTCOMPLEX       = 23
FONT_SCRIPTSIMPLEX       = 24
FONT_SYMBOL              = 25
FONT_MARKER              = 26
FONT_ASTROLOGY           = 27
FONT_CYILLIC             = 28
FONT_CYILLIC1            = 29
FONT_METEOROLOGY         = 30
FONT_MUSIC               = 31

_FONT_LIST = [
    FONT_ROMANSIMPLEX      ,
    FONT_ROMANDUPLEX       ,
    FONT_ROMANTRIPLEX      ,
    FONT_CURSIVE           ,
    FONT_FUTURAL           ,
    FONT_FUTURAM           ,
    FONT_TIMESROMAN        ,
    FONT_TIMESROMANBOLD    ,
    FONT_TIMESGREEK        ,
    FONT_TIMESITALIAN      ,
    FONT_TIMESITALIANBOLD  ,
    FONT_GOTHENGTRIPLEX    ,
    FONT_GOTHGERMANTRIPLEX ,
    FONT_GOTHENGLISH       ,
    FONT_GOTHGERMAN        ,
    FONT_GOTHITALIAN       ,
    FONT_GOTHITALIANTRIPLEX,
    FONT_GREEK             ,
    FONT_GREEKCOMPLEX      ,
    FONT_GREEKSIMPLEX      ,
    FONT_MATHLOW           ,
    FONT_MATHUPPER         ,
    FONT_MATHSYMBOL        ,
    FONT_SCRIPTCOMPLEX     ,
    FONT_SCRIPTSIMPLEX     ,
    FONT_SYMBOL            ,
    FONT_MARKER            ,
    FONT_ASTROLOGY         ,
    FONT_CYILLIC           ,
    FONT_CYILLIC1          ,
    FONT_METEOROLOGY       ,
    FONT_MUSIC             
]

_valid_fid = lambda fid: fid >= FONT_ROMANSIMPLEX and fid <= FONT_MUSIC