# Vector Graphic Library (VGL) for Python
#
# wmfconst.py
#
# 2020-2-12 Ver 0.1
#
# Author: Uisang Hwang
# Email : uhwangtx@gmail.com
#

META_SETBKCOLOR             = 0x0201
META_SETBKMODE              = 0x0102
META_SETMAPMODE             = 0x0103
META_SETROP2                = 0x0104
META_SETRELABS              = 0x0105
META_SETPOLYFILLMODE        = 0x0106
META_SETSTRETCHBLTMODE      = 0x0107
META_SETTEXTCHAREXTRA       = 0x0108
META_SETTEXTCOLOR           = 0x0209
META_SETTEXTJUSTIFICATION   = 0x020A
META_SETWINDOWORG           = 0x020B
META_SETWINDOWEXT           = 0x020C
META_SETVIEWPORTORG         = 0x020D
META_SETVIEWPORTEXT         = 0x020E
META_OFFSETWINDOWORG        = 0x020F
META_SCALEWINDOWEXT         = 0x0410
META_OFFSETVIEWPORTORG      = 0x0211
META_SCALEVIEWPORTEXT       = 0x0412
META_LINETO                 = 0x0213
META_MOVETO                 = 0x0214
META_EXCLUDECLIPRECT        = 0x0415
META_INTERSECTCLIPRECT      = 0x0416
META_ARC                    = 0x0817
META_ELLIPSE                = 0x0418
META_FLOODFILL              = 0x0419
META_PIE                    = 0x081A
META_RECTANGLE              = 0x041B
META_ROUNDRECT              = 0x061C
META_PATBLT                 = 0x061D
META_SAVEDC                 = 0x001E
META_SETPIXEL               = 0x041F
META_OFFSETCLIPRGN          = 0x0220
META_TEXTOUT                = 0x0521
META_BITBLT                 = 0x0922
META_STRETCHBLT             = 0x0B23
META_POLYGON                = 0x0324
META_POLYLINE               = 0x0325
META_ESCAPE                 = 0x0626
META_RESTOREDC              = 0x0127
META_FILLREGION             = 0x0228
META_FRAMEREGION            = 0x0429
META_INVERTREGION           = 0x012A
META_PAINTREGION            = 0x012B
META_SELECTCLIPREGION       = 0x012C
META_SELECTOBJECT           = 0x012D
META_SETTEXTALIGN           = 0x012E
META_DRAWTEXT               = 0x062F
META_CHORD                  = 0x0830
META_SETMAPPERFLAGS         = 0x0231
META_EXTTEXTOUT             = 0x0a32
META_SETDIBTODEV            = 0x0d33
META_SELECTPALETTE          = 0x0234
META_REALIZEPALETTE         = 0x0035
META_ANIMATEPALETTE         = 0x0436
META_SETPALENTRIES          = 0x0037
META_POLYPOLYGON            = 0x0538
META_RESIZEPALETTE          = 0x0139
META_DIBBITBLT              = 0x0940
META_DIBSTRETCHBLT          = 0x0b41
META_DIBCREATEPATTERNBRUSH  = 0x0142
META_STRETCHDIB             = 0x0f43
META_EXTFLOODFILL           = 0x0548
META_RESETDC                = 0x014C
META_STARTDOC               = 0x014D
META_STARTPAGE              = 0x004F
META_ENDPAGE                = 0x0050
META_ABORTDOC               = 0x0052
META_ENDDOC                 = 0x005E
META_DELETEOBJECT           = 0x01f0
META_CREATEPALETTE          = 0x00f7
META_CREATEBRUSH            = 0x00F8
META_CREATEPATTERNBRUSH     = 0x01F9
META_CREATEPENINDIRECT      = 0x02FA
META_CREATEFONTINDIRECT     = 0x02FB
META_CREATEBRUSHINDIRECT    = 0x02FC
META_CREATEBITMAPINDIRECT   = 0x02FD
META_CREATEBITMAP           = 0x06FE
META_CREATEREGION           = 0x06FF

META_ALTERNATE  = 1
META_WINDING    = 2

MM_TEXT         = 1
MM_LOMETRIC     = 2
MM_HIMETRIC     = 3
MM_LOENGLISH    = 4
MM_HIENGLISH    = 5
MM_TWIPS        = 6
MM_ISOTROPIC    = 7
MM_ANISOTROPIC  = 8

PS_SOLID        = 0
PS_DASH         = 1
PS_DOT          = 2
PS_DASHDOT      = 3
PS_DASHDOTDOT   = 4
PS_NULL         = 5
PS_INSIDEFRAME  = 6

BS_SOLID        = 0
BS_NULL         = 1
BS_HOLLOW       = 1 #BS_NULL
BS_HATCHED      = 2
BS_PATTERN      = 3
BS_INDEXED      = 4
BS_DIBPATTERN   = 5

META_END        = 0x0000

META_MAGICNUMBER= 0x9AC6CDD7
META_KEYLOW		= 0x0000FFFF
META_KEYHIGH	= 0xFFFF0000
META_END_SIZE	= 0x00000003

META_KEYSHIFT               = 16
META_DEFAULT_RECORD_SIZE    = 3
META_STANDARD_HEADER_SIZE   = 9
META_PLACEABLE_HEADER_SIZE  = 11
META_RESTORE_DC_PARAM       = -1

#TWIP_PER_INCH		=  1270
TWIP_PER_INCH		=  2000
POINTS_PER_INCH		=  72
MAX_DEFAULT_COLOR   =  17
