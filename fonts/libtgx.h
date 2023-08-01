/*------------------------------------------------------------------
	Copyright (c) Uisang Hwang 2011
	
	LibTGx : Expanded Library for Technical Graph v0.01

	Tested on 
	Visual C++ 2005
	Visual C++ 2010
	Open Watcom C/C++ v1.9

	Permission to use, copy, modify, and distribute this software
	for any use is hereby granted provided
	this notice is kept intact within the source file
 ------------------------------------------------------------------*/

#ifndef __libtgx_h__
#define __libtgx_h__

//#if defined(__WATCOMC__) || defined (__WATCOM_CPLUSPLUS__)
//#pragma disable_message (202) /*... symbol has been defined but not used ...*/
//#pragma disable_message (138) /*... no new line at end of file ...*/
//#endif

#if defined(_MSC_VER)
#pragma warning (disable: 4018 4305 4244 4996)
#endif

/* Define a DLL export symbol */
//#if defined(_MSC_VER)
//	#if defined(TGX_DLL)
//		#define TGX_API __declspec(dllexport)
//	#elif !defined(TGX_LIB)
//		#define TGX_API __declspec(dllimport)
//	#endif
//#endif

#ifdef __TG_DOUBLE__
	#define TG_Float double
#else
	#define TG_Float float
#endif

#ifdef __cplusplus
extern "C" {
#endif

#define __EXPORT_BMP__
#define __EXPORT_WMF__
//#define __WX_DEVICE__
//#define __WIN_DEVICE__
//#define __HAVE_LIBJPG__
//#define __HAVE_LIBPNG__
//#define __HAVE_ZLIB__
//#define __HAVE_LIBAGG__

//#define __USE_DISKMEMORY__

/*#define __NO_GUI__*/

//#define __USE_DLL__

#ifdef __WIN_DEVICE__
#include <windows.h>
#endif

#if defined(__USE_DLL__) && defined(__WIN_DEVICE__)
#define TG_DLL_EXPORT __declspec(dllexport)
#    ifndef TG_DLL_IMPORT
#      define TG_DLL_IMPORT __declspec(dllimport)
#    endif
#endif

#ifndef TG_IMPEXP
#  if defined(__USE_DLL__) && defined(TG_DLL_IMPORT)
#    define TG_IMPEXP TG_DLL_IMPORT
#  endif
#  ifndef TG_IMPEXP
#    define TG_IMPEXP extern
#  endif
#endif

#ifndef NULL
#define NULL 0
#endif

#if !defined(_pi) || !defined(_pi2)
#define _pi				3.141592653589793238
#define _pi2			(_pi*0.5)
#endif

#ifndef _tg_max_real_
#define _tg_max_real_  1.e+10
#endif

#ifndef _tg_min_real_
#define _tg_min_real_  -1.e+10
#endif

#define _to_degree(r) ((r)*180/_pi)
#define _to_radian(d) ((d)*_pi/180)

#ifndef _max
#define _max(x,y) ((x)>(y)?(x):(y))
#endif

#ifndef _min
#define _min(x,y) ((x)>(y)?(y):(x))
#endif

#ifndef _cm_per_inch
#define _cm_per_inch 2.54
#endif

#ifndef _mm_per_inch
#define _mm_per_inch 25.4
#endif

#define TG_Fail 					0x0000
#define TG_Success 					0x0001
#define TG_ERROR_INVALID_PAPERNAME 	0x0002

typedef unsigned char 	ubyte;
typedef unsigned short 	ushort;
typedef unsigned int 	ulong;
typedef unsigned char* 	ubyte_ptr;

typedef char            TG_Byte;
typedef unsigned char   TG_UByte;
typedef char*           TG_Byte_Ptr;
typedef short int 		TG_Short;
typedef short int* 		TG_Short_Ptr;
typedef int 			TG_Symbol;
typedef int             TG_DataType;
typedef int             TG_FrameId;
typedef int             TG_Int;
typedef unsigned int 	TG_Status;
typedef unsigned int 	TG_Error;
//typedef ulong 			TG_Color;
typedef       char*     TG_StrPtr;
typedef const char*     TG_CStrPtr;
typedef int				TG_Font;
typedef unsigned short 	TG_UShort;
typedef void*           TG_Amorphous;
typedef void*           TG_WidgetDataPtr;
typedef int             TG_Index;
typedef int             TG_FrameType;
//typedef int             TG_PaperOrientation;
typedef short int       TG_TickDirection;
typedef int             TG_LayerId;
typedef int             TG_Id;
typedef int             TG_ZoneId;
typedef int             TG_LinePattern;
//typedef int             TG_DeviceType;
typedef int             TG_ObjectType;
typedef int             TG_ObjectId;
typedef void*           TG_ListItemId; 
typedef TG_Float*       TG_Float_Ptr;

typedef enum { TG_DEV_RST, TG_DEV_PS, TG_DEV_EPS, TG_DEV_WMF, TG_DEV_WIDGET } TG_DeviceType;
typedef enum { TG_DEV_QT, TG_DEV_WX, TG_DEV_WIN32 } TG_WidgetType;
typedef enum { TG_True = 1, TG_False = 0 } TG_Bool;

/*... Paper Orientation ...*/

//#define TG_LANDSCAPE                0
//#define TG_PORTRAIT                 1

typedef enum {TG_LANDSCAPE, TG_PORTRAIT} TG_PaperOrientation;

/*... Bool value ...*/

#define TG_TRUE                     1
#define TG_FALSE                    0

/*... Default color ...*/
#define TG_DEFAULTCOLOR_COUNT       17
#define TG_BLACK 		            0
#define TG_RED			            1
#define TG_GREEN		            2
#define TG_BLUE			            3
#define TG_YELLOW		            4
#define TG_CYAN			            5
#define TG_MAGENTA		            6
#define TG_BROWN		            7
#define TG_PURPLE		            8
#define TG_LIGHTGRAY	            9
#define TG_DARKGRAY		            10
#define TG_LIGHTBLUE	            11
#define TG_LIGHTGREEN	            12
#define TG_LIGHTCYAN	            13
#define TG_LIGHTRED		            14
#define TG_LIGHTMAGENTA	            15
#define TG_WHITE		            16
#define TG_CUSTOM1                  17 //.. under construction
#define TG_CUSTOM2                  18
#define TG_CUSTOM3                  19
#define TG_CUSTOM4                  20
#define TG_CUSTOM5                  21
#define TG_CUSTOM6                  22
#define TG_CUSTOM7                  23
#define TG_CUSTOM8                  24

typedef enum { TG_COLOR_RGB, TG_COLOR_MULTI } TG_ColorType;
typedef enum { TG_RSTDEV_BMP, TG_RSTDEV_JPG, TG_RSTDEV_PNG, TG_RSTDEV_PPM } TG_RstdevType;

/*... Line Patterns: valid only for plot frame ...*/
/*
#define TG_SOLID                    0
#define TG_DASHED                   1
#define TG_DASHDOT                  2
#define TG_DOTTED                   3
#define TG_LONGDASH                 4
#define TG_DASHDOTDOT               5
*/

typedef enum 
{
	TG_SOLID     ,
	TG_DASHED    ,
	TG_DASHDOT   ,
	TG_DOTTED    ,
	TG_LONGDASH  ,
	TG_DASHDOTDOT 
}
	TG_LinePattern_t;

/*... Default Symbol ...*/

#define MAX_DEFAULT_SYMBOL          7
#define TG_SYM_CIRCLE		        0
#define TG_SYM_DELTA		        1
#define TG_SYM_GRADIENT		        2
#define TG_SYM_RTRIANGLE	        3
#define TG_SYM_LTRIANGLE	        4
#define TG_SYM_DIAMOND		        5
#define TG_SYM_SQUARE		        6
#define TG_SYM_CUSTOM               7 /*... not supported ...*/
#define TG_SYM_CHAR                 8 /*... not supported ...*/

typedef enum { TG_SYM_DEFAULT, TG_SYM_USER } TG_SymbolType;

/*... Data Type: plot data type ...*/
/*
#define TG_PLOTDATA_CHAR           0
#define TG_PLOTDATA_INT            1
#define TG_PLOTDATA_FLOAT          2
#define TG_PLOTDATA_DOUBLE         3
*/
typedef enum 
{
	TG_PLOTDATA_CHAR,
	TG_PLOTDATA_INT  ,
	TG_PLOTDATA_FLOAT ,
}
	TG_DataType_t;
	
/*... Frame Type ...*/

#define TG_FRAME_SINGLE            0
#define TG_FRAME_PLOT              1

/*... Tick Direction ...*/

#define TG_TickDirection_IN        0
#define TG_TickDirection_OUT       1
#define TG_TickDirection_CENTER    2

/*... Objects ...*/

#define TG_OBJ_LINE                0
#define TG_OBJ_POLYLINE            1 /* Open / Closed */
#define TG_OBJ_RECTANGLE           2
#define TG_OBJ_POLYGON             3
#define TG_OBJ_ARC                 4
#define TG_OBJ_SPLINE              5
#define TG_OBJ_BSPLINE             6

/*... Device ...*/

#define TG_DEV_TERMINAL
#define TG_DEV_WINDOW
#define TG_DEV_RASTER

/*... Data type ...*/

typedef enum { TG_ZONEFORMAT_POINT, TG_ZONEFORMAT_BLOCK } TG_ZoneFormat;

/*... Raster Devices list from rstdrv.h of grace-5.1.22...*/

typedef enum 
{
	RST_FORMAT_PNM,
	RST_FORMAT_JPG,
	RST_FORMAT_PNG,
	RST_FORMAT_BMP
} 
	TG_RasterFormat;

/*... Spacing ...*/

typedef enum 
{
	TG_SPC_EQUAL,
	TG_SPC_COS,
	TG_SPC_LHALFCOS,
	TG_SPC_RHALFCOS
}	
	TG_Spacing;

typedef struct TG_Rgb_
{
	ubyte r,g,b;
}
	TG_Rgb, *TG_Rgb_Ptr;

typedef struct TG_Color_
{
	//union { ulong colref, TG_Rgb color } 
	ubyte r,g,b;
}
	TG_Color, *TG_Color_Ptr;


typedef struct TG_Point_ 
{
	TG_Float x, y;
} 
	TG_Point,
	*TG_Point_Ptr;

typedef struct TG_PontInt_
{
	int x, y;
}
	TG_PointInt, 
	*TG_PointInt_Ptr; 

typedef struct TG_ShortPoint_
{
	TG_Short x, y;
}
	TG_ShortPoint, 
	*TG_ShortPoint_Ptr; 

typedef struct TG_Point3_ 
{
	TG_Float x, y, z;
} 
	TG_Point3,
	*TG_Point3_Ptr;
	
typedef struct TG_Size_
{
	TG_Float sx, sy, width, height;
}
	TG_Size,
	*TG_Size_Ptr;

typedef struct TG_TupleInt_
{
	TG_Int v1, v2;
}
	TG_TupleInt, *TG_TupleInt_Ptr;
	
typedef struct TG_Sizei_
{
	int sx, sy, width, height;
}
	TG_Sizei,
	*TG_Sizei_Ptr;

typedef struct TG_Margin_
{
	TG_Float left, top, right, bottom;
}
	TG_Margin, *TG_Margin_Ptr;
	
typedef struct TG_Rectangle_
{
	TG_Float sx, sy, ex, ey;
}
	TG_Rectangle, TG_Box, TG_BBox, 
	*TG_Rectangle_Ptr, *TG_Box_Ptr, *TG_BBox_Ptr; 

typedef struct TG_Paper_
{
	char type[10];
	TG_Float wid_inch, hgt_inch;
	TG_Float wid_mm, hgt_mm;
}
	TG_Paper,
	*TG_Paper_Ptr;

typedef struct TG_LineAttribute_
{
	TG_Color       color;
	TG_Float       thick;
	TG_LinePattern pat;
	TG_Float       pat_length;
} 
	TG_LineAttribute, *TG_LineAttribute_Ptr;

/*... Plot Definitions ...*/

typedef struct TG_ListItem_
{
	TG_ListItemId item; /* void* */
	struct TG_ListItem_* next;
}
	TG_ListItem, *TG_ListItem_Ptr;
	
typedef struct TG_List_
{
	int count;
	TG_ListItem_Ptr first, last;
}
	TG_List, *TG_List_Ptr;

	
/*... Plot Properties ...*/

typedef enum  
{
	TG_ERRBARDIR_VERT,
	TG_ERRBARDIR_HORZ
} 
	TG_BarPlotDir;

typedef enum 
{
	TG_CRUVFIT_LINEAR,
	TG_CRUVFIT_POLY,
	TG_CRUVFIT_EXPO,
	TG_CRUVFIT_SPLINE,
	TG_CRUVFIT_BSPLINE
} 
	TG_CurvFitType;

typedef enum 
{
	TG_EBAR_TOP,
	TG_EBAR_BOTTOM,
	TG_EBAR_LEFT,
	TG_EBAR_RIGHT,
	TG_EBAR_HORZ,
	TG_EBAR_VERT,
	TG_EBAR_CROSS
} 
	TG_ErrBarType;

typedef enum 
{
	TG_WIREFRAME,
	TG_HIDDENLINE
} 
	TG_MeshPlotType;

typedef enum  
{
	TG_CONT_LINES,
	TG_CONT_FLOOD,
	TG_CONT_LINES_FLOOD,
	TG_CONT_AVERAGE_CELL
} 
	TG_ContourPlotType;

typedef enum  
{
	TG_VEC_TAIL_AT_POINT,
	TG_VEC_HEAD_AT_POINT,
	TG_VEC_ANCHOR_AT_MIDPOINT,
	TG_VEC_HEAD_ONLY,
	TG_VEC_TAIL_ONLY
} 
	TG_VectorPlotType;

typedef enum  
{
	TG_VEC_PLAIN,
	TG_VEC_FILLED,
	TG_VEC_HOLLOW
} 
	TG_VectorHeadStypeType;

typedef enum 
{
	TG_MESH_FILL_0,
	TG_MESH_FILL_1
} 
	TG_MeshFillType;

typedef struct 
{
	TG_Float c1, c2;
	TG_Float k1, k2;
	TG_Float *poly;
	TG_Float *cubic;
	TG_Float *bspl;
} 
	TG_CurvFitCoeff;

typedef struct TG_XYPlotAttr_ 
{
	TG_Bool             line_show;  
	int                 indept_var; // assign a variable to x-axis
	int                 dept_var;   // assign a variable to y-axis
	TG_Color            col;
	TG_LinePattern      pat;
	TG_Float            len; // line length
	TG_Float            thk; // line thickness
	//... Symbol            
	TG_Bool             sym_show;
	TG_SymbolType       sym_type;
	TG_Symbol           sym;
	TG_Bool             sym_line, sym_fill;
	TG_Color            sym_lcol, sym_fcol; // line and fill color
	TG_Float            sym_size;
	int                 sym_skip;
	TG_Float            sym_skip_percent;
	//... Scat plot         
	TG_Bool             scat_show;
	TG_Float            scat_size;
	TG_ColorType        scat_col_type; // default: RGB, multi: rainbow color
	TG_Color            scat_col;
	int                 scat_var;
	//... Bar Graph Attr.
	TG_Bool             bar_show;
	TG_BarPlotDir       bar_dir;
	TG_Color            bar_col;
	TG_Bool             bar_fill;
	TG_Color            bar_fcol;
	TG_Float            bar_size;
	TG_Float            bar_thk;
	int                 bar_skip;
	//... Curve Attr.
	TG_Bool             curv_show;
	int                 curv_points;
	int                 poly_degree;
	int                 bspl_degree;
	TG_CurvFitType      curv_type;
	TG_Bool             curv_update;
	TG_CurvFitCoeff     curv_coeff;
	//... Error Bar Attr.
	TG_Bool             ebar_show;
	int                 ebar_var;
	TG_ErrBarType       ebar_type;
	TG_Color            ebar_col;
	TG_Float            ebar_size;
	TG_Float            ebar_thk;
	int                 ebar_skip;
} 
	TG_XYPlotAttr, *TG_XYPlotAttr_Ptr;

typedef enum { TG_SCATSIZE_NORMAL, TG_SCATSIZE_VARIABLE } TG_ScatSizeType;

typedef struct TG_FieldPlotAttr_
{
	//... Symbol or Scatter
	TG_Bool             scat_show;
	TG_SymbolType       scat_type;
	TG_Symbol           scat;
	TG_Bool             scat_line, scat_fill;
	TG_ColorType        scat_lcol_type; // default: RGB, multi: rainbow color
	TG_ColorType        scat_fcol_type; // default: RGB, multi: rainbow color
	TG_Color            scat_lcol; // scat outline color
	TG_Color            scat_fcol; // scat fill color
	TG_ScatSizeType     scat_size_type;
	TG_Float            scat_size; 
	int                 scat_iskip, scat_jskip;
	TG_Float            scat_iskip_percent;
	TG_Float            scat_jskip_percent;
	TG_Bool             scat_end_points; // force plot end points
	//... Mesh          
	TG_Bool             mesh_show;
	TG_MeshPlotType     mesh_plot_type;
	TG_MeshFillType     mesh_fill_type;
	TG_ColorType        mesh_lcol_type;
	TG_ColorType        mesh_fcol_type;
	TG_Color            mesh_lcol, mesh_fcol;
	TG_LineAttribute    mesh;
	//... Contour       
	TG_Bool             cont_show;
	int                 cont_var;
	TG_ContourPlotType  cont_type;
	TG_LineAttribute    cont_lattr;
	//svcContour2D* pcont;
	//... Vector
	TG_Bool             vect_show;
	TG_VectorPlotType   vect_plot_type;
	//TG_VectorHeadType   vect_head_type;
	TG_LineAttribute    vect_line_type;
	int                 vect_var_x, vect_var_y, vect_var_z;
	int                 vect_iskip, vect_jskip;
	//... Shade
	TG_Bool             shade_show; // only 3D
	TG_Bool             shade_strength; // only 3D
} 
	TG_FieldPlotAttr, *TG_FieldPlotAttr_Ptr;

typedef struct TG_PlotAttributes_
{
	char*                map_name;
	TG_Bool              map_show;
	int                  zone_index;
	TG_XYPlotAttr        xy;
	TG_FieldPlotAttr_Ptr field2d;
	TG_FieldPlotAttr_Ptr field3d;
	void*                z_ptr; // zone pointer
}
	TG_PlotAttributes, *TG_PlotAttributes_Ptr;

/*... ZONE ...*/

#define TG_MAXVARIABLE 50

typedef struct TG_Zone_
{
	TG_ZoneId     id;
	TG_ZoneFormat format;
	int           ni, nj, nk;
	TG_Float      max[TG_MAXVARIABLE], min[TG_MAXVARIABLE];
	void          *data; // data size = ni * nvar, ni * nj * nvar, or ni * nj * nk * nvar
	void          *pi;   // (&pi[i])[j]            (&pi[i*nj])[j]
}
	TG_Zone,
	*TG_Zone_Ptr,
	**TG_ZoneArray_Ptr;	

typedef struct TG_Dataset_
{
	int         nvar;  /* number of variables, nvar equals number of columns of Zoneset */
	TG_DataType type;
	TG_Float    *max, *min; /* max or min of all zones */
	TG_List     zone_list;
	void        *f_ptr;
}
	TG_Dataset,
	*TG_Dataset_Ptr;

/*... Object Defs ...*/
/*... String Properties ...*/

/*... Font ...*/

/*... Type 1 font name ...*/
  
#define TG_FONT_COURIER             0
#define TG_FONT_COURIER_BOLD        1
#define TG_FONT_HELVETICA           2
#define TG_FONT_HELVETICA_BOLD      3
#define TG_FONT_TIMES               4
#define TG_FONT_TIMES_BOLD          5
#define TG_FONT_TIMES_ITALIC        6
#define TG_FONT_TIMES_ITALIC_BOLD   7
//#define TG_FONT_GREEK               8
#define TG_FONT_MATH                9

/*... Hershey font data ...*/
#define MAX_FONTMAP_CHAR            95 
#define MAX_CHAR_VERT               210
#define MAX_TG_FONT                 19

#define TG_FONT_ROMANSIMPLEX        0
#define TG_FONT_ROMANDUPLEX         1
#define TG_FONT_ROMANTRIPLEX        2
#define TG_FONT_CURSIVE             3
#define TG_FONT_FUTURAL             4
#define TG_FONT_FUTURAM             5
#define TG_FONT_GREEK               6
#define TG_FONT_GREEKCOMPLEX        7
#define TG_FONT_GREEKSIMPLEX        8
#define TG_FONT_MUSIC               9
#define TG_FONT_SCRIPTCOMPLEX      10
#define TG_FONT_SCRIPTSIMPLEX      11
#define TG_FONT_SYMBOL             12
#define TG_FONT_TIMESGREEK         13
#define TG_FONT_TIMESITALIAN       14
#define TG_FONT_TIMESITALIANBOLD   15
#define TG_FONT_TIMESROMAN         16
#define TG_FONT_TIMESROMANBOLD     17
#define TG_FONT_MATHSYMBOL         18

#define TG_FONT_VCENTER            0x0001
#define TG_FONT_LEFT               0x0002
#define TG_FONT_RIGHT              0x0004
#define TG_FONT_TOP                0x0008
#define TG_FONT_BOTTOM             0x0010
#define TG_FONT_HCENTER            0x0020

#define TG_FONT_BOX       0X0040
#define TG_FONT_FILLEDBOX 0X0080

typedef enum { TG_FNT_HERSHEY, TG_FNT_T1 } TG_FontType;
typedef enum { TG_COORD_RAW, TG_COORD_FRM } TG_CoordType;

#define STRING_VCENTER(a) ((a)&TG_FONT_VCENTER)
#define STRING_LEFT   (a) ((a)&TG_FONT_LEFT   )
#define STRING_RIGHT  (a) ((a)&TG_FONT_RIGHT  )
#define STRING_TOP    (a) ((a)&TG_FONT_TOP    )
#define STRING_BOTTOM (a) ((a)&TG_FONT_BOTTOM )
#define STRING_HCENTER(a) ((a)&TG_FONT_HCENTER)

typedef enum 
{
	TG_RST_JPG,
	TG_RST_PNG,
	TG_RST_BMP
}
	TG_RasterType;
	
typedef struct TG_StringAttribute_
{
	TG_FontType  font_type;
	TG_CoordType coord_type;
	TG_Float     size;
	TG_UShort    align;
	TG_Bool      box; 
	TG_Bool      fill_box; 
	TG_Bool      under_line;
	TG_Bool      upper_line;
}
	TG_StringAttribute, *TG_StringAttribute_Ptr;

typedef struct TG_String_
{
	TG_Byte_Ptr str;
	TG_StringAttribute attr;
}
	TG_String, *TG_String_Ptr;
	
typedef struct TG_ObjectPolyline_
{
	int              npoint;
	TG_LineAttribute attr;
//	TG_LineEndType   arrow_start, arrow_end;
	TG_Point_Ptr     start, end;
}
	TG_ObjectPolyline, *TG_ObjectPolyline_Ptr;

typedef struct TG_ObjectLine_
{
	TG_Point start,  end;
	TG_LineAttribute attr;
}
	TG_ObjectLine, *TG_ObjectLine_Ptr;
	
typedef struct TG_ObjectRectangle_
{
	TG_Point start,  end;
	TG_LineAttribute attr;
}
	TG_ObjectRectangle, *TG_ObjectRectangle_Ptr;


typedef struct TG_Object_
{
	TG_ObjectId id;
	TG_ObjectType type;
	int raw;
	void* data;
}
	TG_Object, *TG_Object_Ptr;
	
typedef struct TG_AxisTick_ 
{
	TG_Bool          show;
	TG_Bool          auto_spacing;
	TG_Bool          show_major_tick;
	TG_Bool          show_minor_tick;
	TG_LineAttribute major_tick_line;
	TG_LineAttribute minor_tick_iine;
	TG_TickDirection major_tick_direction;
	TG_TickDirection minor_tick_direction;
	int              nmajor_tick;
	int              nminor_tick;
	TG_Float         spacing; /*... between Major ticks ...*/
	int              first_number_of_minor_tick;
	TG_Float         first_major_tick_position;
	TG_Float         first_minor_tick_position;
} 
	TG_AxisTick,
	*TG_AxisTick_Ptr;
	
typedef struct TG_Axis_
{
	char*            axis_title;
	TG_Bool          axis_show;     /*... 0: hide, 1: show ...*/
	TG_Point         axis_position; /*... X and Y coordinate ...*/
	TG_LineAttribute axis_line;     /*... color, thick, pattern ...*/
	TG_AxisTick      tick;         /*... major, minor tick ...*/
}
	TG_Axis,
	*TG_Axis_Ptr;

typedef struct TG_PlotActuator_
{
	TG_Axis_Ptr x_axis_3d, y_axis_3d, z_axis_3d;
	TG_Axis_Ptr x_axis_2d, y_axis_2d;
	TG_Axis_Ptr x_axis_xy, y_axis_xy;
	TG_Size     viewport_size; /* plot area size */
	/*... XY plot ...*/
	TG_Bool     line;
	TG_Bool     symbol;
	TG_Bool     bar;
	TG_Bool     ebar;
	TG_Bool     curve;
	/*... 2D plot ...*/
	TG_Bool     mesh2d;
	TG_Bool     cont2d;
	TG_Bool     vect2d;
	TG_Bool     scat2d;
	TG_Bool     bond2d;
	/*... 3D plot ...*/
	TG_Bool     mesh3d;
	TG_Bool     cont3d;
	TG_Bool     vect3d;
	TG_Bool     scat3d;
	TG_Bool     bond3d;
	TG_Bool     shade;
}
	TG_PlotActuator,
	*TG_PlotActuator_Ptr;
	
typedef struct TG_FrameAttr_
{
	TG_Bool  border; /* show frame border */
	TG_Bool  header; /* show frame header */
	TG_Bool  background; /* show frame background */
	TG_Color border_color;
	TG_Color header_color;
	TG_Color background_color;
}
	TG_FrameAttr, *TG_FrameAttr_Ptr;

typedef struct TG_FrameViewportAttr_
{
	TG_Bool  clip;
	TG_Bool  show;
	TG_Bool  border;
	TG_Color bk_color; /* background color */
}
	TG_FrameViewportAttr, *TG_FrameViewportAttr_Ptr;

typedef struct TG_Frame_ 
{
	TG_FrameType type;
	TG_FrameId   id;
	TG_Size      frame_size;
	TG_FrameAttr prop;

	TG_Float     fxl, fyl; /*... scaling factor for logical unit ...*/
	TG_Float     fxp, fyp; /*... scaling factor for physical unit ...*/
	TG_Float     fx;       /*... the smallest value of fxl, fyl ...*/
	TG_Float     minx, maxx, miny, maxy, minz, maxz; /*... World coordinate ...*/	
	
	TG_List              dataset; 
	TG_PlotActuator_Ptr  plot_actuator;
	TG_Size              viewport_size;
	TG_FrameViewportAttr viewport_prop;
} 
	TG_Frame,
	*TG_Frame_Ptr,
	**TG_FrameArray_Ptr;
	
typedef struct TG_Ruler_
{
	TG_Font font;
	float   fsize; /* font size: 0.4 * ruler height */
	float   height; /* 0.01 * paper height */
	float   major_tick_size; /* 0.8 * ruler height */
	float   minor_tick_size; /* 0.6 * ruler height */
}
	TG_Ruler, *TG_Ruler_Ptr;
	
typedef struct TG_CanvasAttr_
{
	TG_Float paper_skip_left;   /* 0.3409 */
	TG_Float paper_skip_right;  /* 0.454  */
	TG_Float paper_skip_top;    /* 0.1    */
	TG_Float paper_skip_bottom; /* 0.2    */
}
	TG_CanvasAttr, TG_CanvasAttr_Ptr;

typedef struct TG_Canvas_
{
	int             dpi;
	TG_Bool         vruler, hruler; /* show: 1/0 */
	TG_Bool         paper_background_show;       /* paper background show: 1/0 */
	TG_Bool         paper_marker_show;       /* paper marker show: 1/0, '+' */
	TG_Bool         printible_area; /* show: 1/0 */
	TG_Color        paper_marker_color; /* marker color */
	TG_Color        paper_background_color; /* background color */
	TG_Color        canvas_background_color;
	TG_Ruler        ruler_property;
	TG_CanvasAttr   property;
	TG_BBox         frame_bbox;     /* the largest rectangle in which all frames are */
#ifdef __TG_USING_INDEXED_COLOR__
	TG_Colormap_Ptr color_map;
	int             ncolor;
	int             max_color;
#endif
}
	TG_Canvas, *TG_Canvas_Ptr;
	
#define MAX_ID_POOL 100

typedef struct TG_IdPool_
{
	TG_Id pool_index;
	TG_Id pool[MAX_ID_POOL];
}
	TG_IdPool, *TG_IdPool_Ptr;

typedef struct TG_FrameManager_
{
	TG_Int            frame_pool_size;
	TG_Int            active_frame;
	TG_Int            current_frame;
	TG_Int            nframe;
	TG_IdPool         frame_id;
	TG_FrameArray_Ptr frame_pool; 
}
	TG_FrameManager, *TG_FrameManager_Ptr;

typedef struct TG_Workspace_
{
	TG_Paper               paper;
	TG_Rectangle           prn_area;
	TG_Canvas              canvas;
	TG_PaperOrientation    paper_orientation;
	TG_FrameManager        frm_manager;
} 
	TG_Workspace, *TG_Workspace_Ptr;

typedef struct TG_Layer_
{
	TG_Bool show;
	TG_LayerId id;
	TG_Workspace workspace;
	struct TG_Layer_* next;
}
	TG_Layer, *TG_Layer_Ptr;

typedef struct TG_LayerList_
{
	int count; /* equals to the number of workspaces */
	TG_IdPool layer_id; /* workspace id pool */
	TG_Layer_Ptr first, last;
}
	TG_LayerList, *TG_LayerList_Ptr;

typedef struct TG_Library_
{
	TG_LayerList layer_list;
}
	TG_Library, *TG_Library_Ptr;
	
typedef void(*tg_dev_convcoord)(struct TG_Device_*, TG_Point*, TG_Point*);

typedef struct TG_Device_
{
	TG_Bool          yreverse;
	TG_DeviceType    type;
	TG_Float         zoom;
	tg_dev_convcoord w2v; /* world    to viewport*/
	tg_dev_convcoord v2d; /* viewport to device  */
	tg_dev_convcoord l2d; /* length   to device  */
	TG_Frame_Ptr     f;
	void*            canvas;
	void*           data;
}
	TG_Device, *TG_Device_Ptr;
	
typedef struct TG_RasterDeviceData_
{
	TG_RasterType type;
	int dpi;
	int wid, hgt;
	TG_BBox bbox;
	TG_Float fx;
	void* rasterizer_data;
}
	TG_RasterDeviceData, *TG_RasterDeviceData_Ptr;
	
typedef struct TG_HersheyFontData_
{
	TG_Short nvert;
	TG_Byte vert_pair[MAX_CHAR_VERT];
	TG_ShortPoint ll, rt; /* ll: lower left, rt: right top */
}
	TG_HersheyFontData, *TG_HersheyFontData_Ptr;

typedef struct TG_HersheyFontMap_
{
	char font_name[40];
	TG_HersheyFontData ascii_to_hershey[MAX_FONTMAP_CHAR];
}
	TG_HersheyFontMap,
	*TG_HersheyFontMap_Ptr;


typedef TG_Size  TG_FrameSize;
typedef TG_Size* TG_FrameSize_Ptr;

typedef struct TG_WidgetDeviceData_
{
	TG_WidgetType    type;
	TG_Float         window_scale; 
	TG_Rectangle     window_size;
	TG_Rectangle     paper_pos; /* paper position in pixel coord */
	TG_PointInt      ref_paper;
	TG_PointInt      ref_frame;
	TG_WidgetDataPtr data;
	//void*        wxwin_data; /* wxWindows */
	//void*        mswin_data; /* WIN32     */
}
	TG_WidgetDeviceData, *TG_WidgetDeviceData_Ptr;

typedef void(*TG_ComputeSymbol)(TG_Float,TG_Float,TG_Float,TG_Float);

typedef struct TG_SymbolPool_
{
	int              npoint;
	TG_Float         line_thk;
	TG_Float*        pointx;
	TG_Float*        pointy;
	TG_ComputeSymbol TG_ComputeSymbolCoordinate;
}
	TG_SymbolPool, *TG_SymbolPool_Ptr;

/* Global plot function */
typedef void(*tg_dev_vp_moveto  )(TG_Device_Ptr, TG_Float , TG_Float );
typedef void(*tg_dev_vp_lineto  )(TG_Device_Ptr, TG_Float , TG_Float );
typedef void(*tg_dev_vp_putpixel)(TG_Device_Ptr, TG_Float , TG_Float, TG_Color);
typedef void(*tg_dev_makepen    )(TG_Device_Ptr, TG_Color , TG_Float, TG_LinePattern,TG_Float);
typedef void(*tg_dev_symbol     )(TG_Device_Ptr, TG_Float , TG_Float, TG_Symbol, TG_Float, TG_Color, int, TG_Color, int, TG_Float);
typedef void(*tg_dev_moveto     )(TG_Device_Ptr, TG_Float , TG_Float );
typedef void(*tg_dev_lineto     )(TG_Device_Ptr, TG_Float , TG_Float );
typedef void(*tg_dev_polyline   )(TG_Device_Ptr, TG_Float*, TG_Float*, int, int); /* npoint, raw (1) or vp(0) */
typedef void(*tg_dev_polygon    )(TG_Device_Ptr, TG_Float*, TG_Float*, int, TG_Color, int);
typedef void(*tg_dev_arc        )(TG_Device_Ptr, TG_Point*, TG_Point*, TG_Float,TG_Float);
typedef void(*tg_dev_gsave      )(TG_Device_Ptr);
typedef void(*tg_dev_grestore   )(TG_Device_Ptr);
typedef void(*tg_dev_deletepen  )(TG_Device_Ptr);
typedef void(*tg_dev_makefont   )(TG_Device_Ptr, TG_Font, TG_Color, TG_Float, TG_Float);
typedef void(*tg_dev_deletefont )(TG_Device_Ptr);
typedef void(*tg_dev_textout    )(TG_Device_Ptr, TG_StrPtr, TG_Float, TG_Float, TG_UShort, TG_Float, TG_Color,TG_Color);

extern tg_dev_makepen     _dev_makepen;
extern tg_dev_moveto      _dev_moveto;
extern tg_dev_lineto      _dev_lineto;
extern tg_dev_gsave       _dev_gsave;
extern tg_dev_grestore    _dev_grestore;
extern tg_dev_deletepen   _dev_deletepen;
extern tg_dev_symbol      _dev_symbol;
extern tg_dev_polygon     _dev_polygon;
extern tg_dev_polyline    _dev_polyline;
extern tg_dev_vp_moveto   _vp_moveto;
extern tg_dev_vp_lineto   _vp_lineto;
extern tg_dev_vp_putpixel _vp_putpixel;
extern tg_dev_makefont    _dev_makefont;
extern tg_dev_deletefont  _dev_deletefont;
extern tg_dev_textout     _dev_textout;

extern TG_Library_Ptr     TG_StartTGLibServer          (void);
extern void               TG_StopTGLibServer           (TG_Library_Ptr);
extern int                TG_IsTGServerStarted         (TG_Library_Ptr lib);
extern TG_Workspace_Ptr   TG_InitTGLibrary             (TG_Library_Ptr, const char* paper_name);
extern void               TG_CloseTGLibrary            (TG_Workspace_Ptr wo);
                          
extern void               TG_SetFrameViewportLimit     (TG_Frame_Ptr f, TG_Float minx, TG_Float maxx, TG_Float miny, TG_Float maxy);
extern void               TG_SetFrameViewportSize      (TG_Frame_Ptr f, TG_Float sx, TG_Float sy, TG_Float wid, TG_Float hgt);
extern TG_Frame_Ptr       TG_GetFramePtr               (TG_Workspace_Ptr w, TG_FrameId id);
extern TG_BBox            TG_GetFrameBBox              (TG_Frame_Ptr f);
extern TG_Frame_Ptr       TG_CreateCustomFrame         (TG_Workspace_Ptr w, TG_Float sx, TG_Float sy, TG_Float wid, TG_Float hgt);
extern TG_Frame_Ptr       TG_CreateStandardFrame       (TG_Workspace_Ptr w);
extern void               TG_DeleteFramePtr            (TG_Workspace_Ptr w, TG_Frame_Ptr f);

extern void               TG_UpdateFrameSize           (TG_Workspace_Ptr w, TG_Frame_Ptr f, TG_Float sx, TG_Float sy, TG_Float wid, TG_Float hgt);
extern void               TG_DeleteFrame               (TG_Workspace_Ptr w, TG_FrameId id);
extern void               TG_PrintFrame                (TG_Workspace_Ptr w, TG_FrameId id);
extern void               TG_SetActiveFrame            (TG_Workspace_Ptr w, TG_Frame_Ptr f);
extern void               TG_PrintFramePool            (TG_Workspace_Ptr w);
extern TG_Rectangle       TG_GetPaperGeometry          (TG_Workspace_Ptr w);
extern void               TG_SetFullFrameViewport      (TG_Frame_Ptr f);
extern void               TG_ActivateFrameForPlot      (TG_Workspace_Ptr w, TG_Device_Ptr dev, TG_Frame_Ptr f);
extern TG_Layer_Ptr       TG_CreateLayer               (TG_Library_Ptr, const char*, TG_Float, TG_Float);
extern TG_Workspace_Ptr   TG_GetCurrentWorkspace       (void);

extern void               TG_SetViewportBackgroundColor(TG_Frame_Ptr f, TG_Color);
extern void               TG_SetYReverseFrameViewport  (TG_Device_Ptr dev, TG_Bool r);
                          
extern void               TG_ExportAllFrameToImage     (TG_Workspace_Ptr w, TG_Device_Ptr dev);
extern void               TG_InstallWindowDevice       (TG_Workspace_Ptr w, TG_Device_Ptr dev);
extern void               TG_InstallWMFDevice          (TG_Workspace_Ptr w, TG_Device_Ptr dev);
extern void               TG_InstallBMPDevice          (TG_Workspace_Ptr w, TG_Device_Ptr dev);
extern void               TG_InstallPNGDevice          (TG_Workspace_Ptr w, TG_Device_Ptr dev);
extern void               TG_InstallJPGDevice          (TG_Workspace_Ptr w, TG_Device_Ptr dev);
extern void               TG_InstallPSDevice           (TG_Workspace_Ptr w, TG_Device_Ptr dev);
extern void               TG_InstallEPSDevice          (TG_Workspace_Ptr w, TG_Device_Ptr dev);
extern void               TG_InstallWXDevice           (TG_Workspace_Ptr w, TG_Device_Ptr dev);
extern int                TG_InstallRasterDevice       (TG_Workspace_Ptr w, TG_Device_Ptr dev, TG_RasterType type, int dpi, TG_BBox bbox);

extern int                TG_GetWindowWidth            (TG_Device_Ptr dev);
extern int                TG_GetWindowHeight           (TG_Device_Ptr dev);

extern void               TG_InitPlotFunction          (void);
extern void               TG_SavePlotFunction          (void);
extern void               TG_RestorePlotFunction       (void);

#ifdef __WIN_DEVICE__

extern void               TG_InstallMSWindowDevice     (TG_Workspace_Ptr w, TG_Device_Ptr dev, HWND hwnd, HDC hdc);
extern void               TG_UninstallMSWindowDevice   (TG_Device_Ptr dev);
extern void               TG_UpdateMSWindowDevice      (TG_Device_Ptr dev, int wid, int hgt, int force);
extern HDC                TG_GetMSWMemoryDC            (TG_Device_Ptr dev);
extern int                TG_IsValidMSWMemoryDC        (TG_Device_Ptr dev);

#endif
                          
extern void               TG_UninstallWindowDevice     (TG_Device_Ptr dev);
extern void               TG_UninstallWMFDevice        (TG_Device_Ptr dev);
extern void               TG_UninstallWXDevice         (TG_Device_Ptr dev);
                          
extern TG_Float           TG_GetWindowScale            (TG_Device_Ptr dev);
extern void               TG_SetShowRuler              (TG_Workspace_Ptr w, TG_Bool show);
extern void               TG_UpdateCanvas        (TG_Workspace_Ptr w, TG_Device_Ptr dev, int left, int top, int right, int bottom);
extern void               TG_DrawWorkspace       (TG_Workspace_Ptr w, TG_Device_Ptr dev);
extern TG_BBox            TG_GetFrameBBoxInCanvas      (TG_Workspace_Ptr w);

extern TG_SymbolPool_Ptr  TG_GetSymbolPool             (TG_Symbol sym);
extern void               TG_GetSymbolCoordinate       (TG_Symbol sym_index, TG_Float x, TG_Float y, TG_Float lx, TG_Float ly);

#ifdef __EXPORT_BMP__ /*... BITMAP ...*/
extern int                TG_BMP_OpenExport            (TG_Device_Ptr dev, const char* file, TG_BBox bbox);
extern void               TG_BMP_CloseExport           (void);
extern void               TG_BMP_SaveCurrentImage      (const char* fname);
extern void               TG_BMP_SetBackgroundColor    (TG_Color bkcolor);
#endif

#ifdef __EXPORT_WMF__ /*... WINDOWSMETAFILE ...*/
extern int                TG_WMF_OpenExport            (TG_Device_Ptr dev, const char* file, TG_BBox bbox);
extern void               TG_WMF_CloseExport           (void);
#endif

#ifdef __EXPORT_PSEPS__
extern int                TG_PS_OpenExport             (TG_Device_Ptr dev, const char* file);
extern int                TG_EPS_OpenExport            (TG_Device_Ptr dev, const char* file);
extern void               TG_PS_CloseExport            (void);
extern void               TG_EPS_CloseExport           (void);
#endif

extern void               TG_GetRGB                    (ulong c, int* r, int* g, int* b);
extern TG_Color           TG_GetDefaultColorRef        (int c);
extern ulong              TG_GetCustomColor            (int r, int g, int b);
extern TG_Color           TG_GetColor                  (int c);
extern int                TG_RGBtoGRAY                 (int R, int G, int B);
extern ulong              TG_GetColorRef               (TG_Color col);
extern void               TG_CreateColorTableHSV       (TG_Color* ctbl, TG_Float H1, TG_Float H2, TG_Float S, TG_Float V, int order);
extern TG_Color           TG_HSV_To_RGB                (TG_Float H, TG_Float S, TG_Float V, int* R, int* G, int* B);

/*... Object API ...*/
extern TG_Object_Ptr      TG_CreateObject              (void* owner, int owner_type);

TG_ListItem_Ptr           TG_GetFirstItem              (TG_List_Ptr list);
TG_ListItem_Ptr           TG_GetNextItem               (void);

//extern TG_Dataset_Ptr     TG_CreateDataset             (TG_Frame_Ptr f, TG_DataType type, int nvar);
extern TG_Dataset_Ptr     TG_CreateDatasetAndZone      (TG_Frame_Ptr f, TG_DataType type, int nvar, int nzone);
extern TG_Zone_Ptr        TG_CreateZone                (TG_Dataset_Ptr dset);
extern TG_Zone_Ptr        TG_AddZone                   (TG_Dataset_Ptr dset);
extern void               TG_AddXYPoint                (TG_Zone_Ptr z, ...); // ...: nvar, x, y1, y2, ...
//extern void               TG_AddXYBlockPoint           (TG_Zone_Ptr z, TG_Float x, TG_Float y);
extern void               TG_AddFieldPoint2D           (TG_Zone_Ptr z, ...); // ... : i, j, x, y, nvar, TG_Flat * nvar + 2 (x,y)

extern int                TG_LoadDataAndCreatePlotEnv(TG_Frame_Ptr f, const char* fname);
extern void               TG_PrintWorkspaceInfo      (TG_Workspace_Ptr w);

extern void               TG_ExportMultiFrameToImage (TG_Device_Ptr ratdev, int dpi, TG_FrameArray_Ptr f, int nframe);
extern void               TG_ExportSingleFrameToImage(TG_Device_Ptr ratdev, int dpi, TG_Frame_Ptr f);

extern int                TG_GetRstdeviceWidth       (TG_Device_Ptr ratdev);
extern int                TG_GetRstdeviceHeight      (TG_Device_Ptr ratdev);
extern TG_BBox            TG_ComputeMultiFrameBBox   (TG_FrameArray_Ptr f, int nframe);
extern TG_BBox            TG_ComputeSingleFrameBBox  (TG_Frame_Ptr f);
extern int                TG_AddColorRgb             (TG_Canvas_Ptr can, int r, int g, int b);
extern int                TG_AddColor                (TG_Canvas_Ptr can, ulong col);
//extern int                TG_InstallRasterDevice     (TG_Workspace_Ptr w, TG_Device_Ptr r);
#ifdef __TG_USING_INDEXED_COLOR__
extern TG_Rgb TG_GetColormapEntry(TG_Color color);
#endif
extern void               TG_UninstallRasterDevice(TG_Device_Ptr);
extern int                TG_FindColor(TG_Canvas_Ptr can, int r, int g, int b);
extern void               TG_TextOut(TG_Device_Ptr dev, TG_StrPtr str, TG_Float x, TG_Float y,TG_UShort align, TG_Float thk, TG_Color fc, TG_Color lc);
extern TG_Workspace_Ptr   TG_GetWorkspace(TG_Layer_Ptr);

extern void TG_GenericMakeFont(TG_Device_Ptr dev, TG_Font font, TG_Color col, TG_Float deg, TG_Float size);

extern TG_HersheyFontMap_Ptr TG_GetFontMap(TG_Font font);
extern int TG_HersheyFontCount(void);

extern TG_Float TG_GetFrameWidth(TG_Frame_Ptr f);
extern TG_Float TG_GetFrameHeight(TG_Frame_Ptr f);
extern void TG_SetFrameViewportSizeAsPaperSize(TG_Workspace_Ptr, TG_Frame_Ptr);
extern void TG_GetPaperSizeInch(TG_Workspace_Ptr, TG_Float_Ptr, TG_Float_Ptr);
extern TG_TupleInt TG_GetFrameImageSize(TG_RasterDeviceData_Ptr data, TG_BBox bbox);

#ifdef __cplusplus
}
#endif

extern void TG_SaveCurrentPlot(TG_Device_Ptr dev, const char* fname);

#endif

/*... End of libtg.h ...*/