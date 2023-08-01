#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

#include "libtgx.h"

#define DASH '-'
#define NEWLINE '\n'
#define LINE_FEED 0x0A
#define CARRIAGE_RETURN 0x0D
#define NEWLINE_COUNT 10
#define REFERENCE 'R'
#define MAX_HFONT_BUF 256
#define SPACE ' '
#define START_ASCII 32
#define STOP_ASCII 126

#define FORMATED_FONT_DATA

int TG_FIO_SkipSpace(FILE* reader)
{
	int two;
	do {
		two = fgetc(reader);
		if(two == NEWLINE) break;
		else if(feof(reader)) return -1; 
	} while(isspace(two));
	return two; /* return the last non-space character */
}

/* return the number of digit size */
int TG_HMP_GetDigit(FILE* reader, char* buffer, int* two)
{
	int count=0, three;
	
	while(1) {
		three = fgetc(reader);
		if(feof(reader)) break;
		else if(isdigit(three)) {
			*buffer++ = three;
			count++;
		}
		else break;
	}
	
	*two = three; /* in case of End of file, *two has EOF */
	*buffer = NULL;
	return count;
}

void TG_ExpandHersheyMap(const char* hmp, const char* font_name, const char* xhmp)
{
	int two, count, start, end, i, hcount = 0;
	char buffer1[16], buffer2[16];
	char* pbuf1 = buffer1, *pbuf2 = buffer2;
	FILE* reader = fopen(hmp, "rt");
	FILE* writer = fopen(xhmp, "wt");
	
	if(!reader) return;
	if(!writer) { fclose(reader); return; }

	fprintf(writer, "%s\n", font_name);
	
	while(!feof(reader))
	{
		two = TG_FIO_SkipSpace(reader);
		
		if(isdigit(two)) 
		{
			*pbuf1++ = two;
			count = TG_HMP_GetDigit(reader, pbuf1, &two);
			start = atoi(buffer1);

			fprintf(writer, "%-4d, ", start);
			pbuf1 = buffer1;
			hcount++;
			
			if(hcount == NEWLINE_COUNT) {
				fputc(NEWLINE, writer);
				hcount = 0;
			}
			
			/* only one digit */
			if(two == DASH) 
			{
				two = TG_FIO_SkipSpace(reader);
				if(isdigit(two)) 
				{
					*pbuf2++ = two;
					count = TG_HMP_GetDigit(reader, pbuf2, &two);
					end = atoi(buffer2);
					
					for(i = start+1; i <= end; i++)
					{
						fprintf(writer, "%-4d, ", i);
						hcount++;
						if(hcount == NEWLINE_COUNT) {
							fputc(NEWLINE, writer);
							hcount = 0;
						}
					}
					pbuf2 = buffer2;
				}
				else 
				{
					fprintf(stderr, "Error dash must be followed by a number\n"); 
					break;
				}
			}
		}
	}
	fclose(reader);
	fclose(writer);
}
	
/*
astrology: 33-39, 42-43, 45, 47, 58-64, 91, 93-96,123-126 = 7+2+1+1+7+1+4+4=27
markers: 65-80=16
mathlow: 33-35, 37-38, 43, 58-64, 94-122, 124, 126 = 3+2+1+7+29+1+1=44
meterology: 33-36, 38-41=4+4=8
*/

typedef struct {int x, y; } TG_IntPoint;

FILE* math_writer;

struct MathSymbol
{
	char* name;
	int npos;
	TG_IntPoint pos[8];
}
	mathsymbol_list[] =
	{
		{"Astrology"  , 8, {{33,39}, {42,43}, {45,45}, {47,47}, {58,64}, {91,91}, {93,96}, {123,126}}},
		{"Markers"    , 1, {{65,80}, }},
		{"MathLower"  , 8, {{33,35}, {37,38}, {43,43}, {58,64}, {94,122}, {124,124}, {126,126}}},
		{"Meteorology", 2, {{33,36}, {38,41}, }}
	};

int TG_ParseHersheyFont(const char* hfont, const char* cfont, const char* font_name)
{
	#define NEWLINE_VERT 10
	static int ilist=0, end=0;
	int ipos, jpos, kpos, begin=0, xpos[95], pos1, pos2;
	char buffer1[MAX_HFONT_BUF], buffer2[16],*pbuf=NULL;
	int chid, nvert, lpos, rpos, i=0,j=0,ivert=0, x, y, jvert, iascii; 
	FILE* reader=NULL, *writer=NULL;
	int lx_min=1000, ly_min=1000, rx_max=-1000, ry_max=-1000;
	
	reader = fopen(hfont, "rt");
	writer = fopen(cfont, "wt");
	
	if(!reader) {
		fprintf(stderr, "Error: can't open %s at TG_ParseHersheyFont\n", hfont);
		return 0;
	}
	
	if(!writer) {
		fclose(reader);
		fprintf(stderr, "Error: can't open %s at TG_ParseHersheyFont\n", cfont);
		return 0;
	}
	
	if(!end && strcmp(mathsymbol_list[ilist].name, font_name)==0)
	{
		int val = -1;
		begin = 1;
		kpos = 0;
		memset(xpos, val, sizeof(int)*95);

		for(ipos = 0; ipos < mathsymbol_list[ilist].npos; ipos++)
		{
			pos1 = mathsymbol_list[ilist].pos[ipos].x;
			pos2 = mathsymbol_list[ilist].pos[ipos].y;
			
			for(jpos = pos1; jpos <= pos2; jpos++)	xpos[kpos++] = jpos;
		}
		kpos=0;
		ilist++;
	}
	
	fputs("#include \"libtg.h\"\n\n", writer);

	if(begin && ilist==1)
		fputs("#include \"libtg.h\"\n\n", math_writer);
	
	//fprintf(writer, "int %s[%d][%d] = \n{\n", font_name, MAX_FONTMAP_CHAR, MAX_CHAR_VERT);
	fprintf(writer, "TG_HersheyFontMap %s_FontMap = \n{\n\t\"%s\", {\n", font_name, font_name);
	
	if(begin && ilist==1)
		fprintf(math_writer, "TG_HersheyFontMap %s_FontMap = \n{\n\t\"%s\", {\n", "MathSymbol", "MathSymbol");
	
	if(begin) fprintf(math_writer, "/* %s */\n", font_name);
		
	iascii = START_ASCII;
	
	while(!feof(reader))
	{
		/* read one line */
		fgets(buffer1, MAX_HFONT_BUF-1, reader);
		
		if(strlen(buffer1) < 10) continue;

		for(j=0,i=0; i < 5; i++,j++) buffer2[j] = buffer1[i];
		buffer2[j] = NULL;
		chid = atoi(buffer2);
		
		if(chid < 1 || chid > 4000) {
			fprintf(stderr, "Error: %d is not a valid id (1< chid <4000)\n", chid);
			//continue;
		}
		
		/* i = 5-7 */
		for(j=0; i < 8; i++, j++) buffer2[j] = buffer1[i];
		buffer2[j] = NULL;
		nvert = atoi(buffer2);
		
		/* i = 8-9 */
		for(j=0; i < 10; i++, j++) buffer2[j] = buffer1[i];
		
		lpos = buffer2[0] - REFERENCE;
		rpos = buffer2[1] - REFERENCE;
		
		pbuf = &buffer1[i];
		ivert = 1;

		if(iascii > STOP_ASCII) break;
	
		#ifdef FORMATED_FONT_DATA
		fprintf(writer, "\t{\t%3d, /* Ascii %c:%d */\n\t\t{", nvert-1, (char)iascii, iascii);
		#else
		fprintf(writer, "\t{\t%d, /* Ascii %c:%d */ {", nvert-1, (char)iascii, iascii);
		#endif
		
		if(begin && iascii==xpos[kpos]) 
			fprintf(math_writer, "\t{\t%3d, /* Ascii %c:%d */\n\t\t{", nvert-1, (char)iascii, iascii);
			
		jvert = 0;
					
		if(ivert < nvert) {
			fputs("\n\t\t", writer);
			if(begin && iascii==xpos[kpos]) fputs("\n\t\t", math_writer);
		}
		else 
			fputs("\t0,", writer);
		
		lx_min=1000, ly_min=1000, rx_max=-1000, ry_max=-1000;
		
		while(ivert < nvert)
		{
			if(!*pbuf && ivert < nvert)
			{
				fgets(buffer1, MAX_HFONT_BUF, reader);
				pbuf = buffer1;
			}
			
			if(*pbuf == NEWLINE) pbuf++;
			else 
			{
				if(*pbuf == SPACE && *(pbuf+1) == REFERENCE) /* pen up & next char is R */
				{
					fprintf(writer, "%3d,%3d,", -1, -1);
					
					if(begin && iascii==xpos[kpos]) 
					fprintf(math_writer, "%3d,%3d,", -1, -1);
					pbuf++; pbuf++;
				}
				else
				{
					x = *pbuf++ - REFERENCE;
					y = *pbuf++ - REFERENCE;
					
					if(lx_min > x) lx_min = x;
					if(ly_min > y) ly_min = y;
					if(rx_max < x) rx_max = x;
					if(ry_max < y) ry_max = y;
					
					fprintf(writer, "%3d,%3d,", x, y);
					
					if(begin && iascii==xpos[kpos]) 
					fprintf(math_writer, "%3d,%3d,", x, y);
				}
				ivert++;
				jvert++;
				if(jvert == NEWLINE_VERT && ivert < nvert) { 
					fputs("\n\t\t", writer); 
					if(begin && iascii==xpos[kpos]) fputs("\n\t\t", math_writer); 
					jvert=0; 
				}
			}
		}
		
		if(iascii == START_ASCII) {
			lx_min = -8;
			ly_min = -12;
			rx_max = 8;
			ry_max = 9;
		}

		fputs("\n\t\t},\n\t\t", writer);
		fprintf(writer, "{%3d,%3d}, {%3d,%3d}\n\t},\n\n", lx_min, ly_min, rx_max, ry_max);		

		if(begin && iascii==xpos[kpos]) 
		{
			fputs("\n\t\t},\n\t\t", math_writer);
			fprintf(math_writer, "{%3d,%3d}, {%3d,%3d}\n\t},\n\n", lx_min, ly_min, rx_max, ry_max);
			kpos++;
		}
		iascii++;
	}
	fputs("}};", writer);
	
	if(begin && ilist > 3) {
		fputs("}};", math_writer);
		end = 1;
	}
	
	fclose(reader);
	fclose(writer);
	
	return 1;
}

int TG_ParseHersheyFont_Python(const char* hfont, const char* cfont, const char* font_name)
{
	#define NEWLINE_VERT 10
	static int ilist=0, end=0;
	int ipos, jpos, kpos, begin=0, xpos[95], pos1, pos2;
	char buffer1[MAX_HFONT_BUF], buffer2[16],*pbuf=NULL;
	int chid, nvert, lpos, rpos, i=0,j=0,ivert=0, x, y, jvert, iascii; 
	FILE* reader=NULL, *writer=NULL;
	int lx_min=1000, ly_min=1000, rx_max=-1000, ry_max=-1000;
	
	reader = fopen(hfont, "rt");
	writer = fopen(cfont, "wt");
	
	if(!reader) {
		fprintf(stderr, "Error: can't open %s at TG_ParseHersheyFont\n", hfont);
		return 0;
	}
	
	if(!writer) {
		fclose(reader);
		fprintf(stderr, "Error: can't open %s at TG_ParseHersheyFont\n", cfont);
		return 0;
	}
	
	if(!end && strcmp(mathsymbol_list[ilist].name, font_name)==0)
	{
		int val = -1;
		begin = 1;
		kpos = 0;
		memset(xpos, val, sizeof(int)*95);

		for(ipos = 0; ipos < mathsymbol_list[ilist].npos; ipos++)
		{
			pos1 = mathsymbol_list[ilist].pos[ipos].x;
			pos2 = mathsymbol_list[ilist].pos[ipos].y;
			
			for(jpos = pos1; jpos <= pos2; jpos++)	xpos[kpos++] = jpos;
		}
		kpos=0;
		ilist++;
	}
	
	//fputs("#include \"libtg.h\"\n\n", writer);
    //
	//if(begin && ilist==1)
	//	fputs("#include \"libtg.h\"\n\n", math_writer);
	
	//fprintf(writer, "int %s[%d][%d] = \n{\n", font_name, MAX_FONTMAP_CHAR, MAX_CHAR_VERT);
	//fprintf(writer, "TG_HersheyFontMap %s_FontMap = \n{\n\t\"%s\", {\n", font_name, font_name);
	fprintf(writer, "font_name = \"%s\"\n\nfont_map = [\n", font_name, font_name);
	
	if(begin && ilist==1)
		//fprintf(math_writer, "TG_HersheyFontMap %s_FontMap = \n{\n\t\"%s\", {\n", "MathSymbol", "MathSymbol");
		fprintf(math_writer, "font_name = \"%s\"\n\nfont_map = [\n", "MathSymbol", "MathSymbol");
	
	//if(begin) fprintf(math_writer, "/* %s */\n", font_name);
		
	iascii = START_ASCII;
	
	while(!feof(reader))
	{
		/* read one line */
		fgets(buffer1, MAX_HFONT_BUF-1, reader);
		
		if(strlen(buffer1) < 10) continue;

		for(j=0,i=0; i < 5; i++,j++) buffer2[j] = buffer1[i];
		buffer2[j] = NULL;
		chid = atoi(buffer2);
		
		if(chid < 1 || chid > 4000) {
			fprintf(stderr, "Error(%s): %d is not a valid id (1< chid <4000)\n", font_name, chid);
			//continue;
		}
		
		/* i = 5-7 */
		for(j=0; i < 8; i++, j++) buffer2[j] = buffer1[i];
		buffer2[j] = NULL;
		nvert = atoi(buffer2);
		
		/* i = 8-9 */
		for(j=0; i < 10; i++, j++) buffer2[j] = buffer1[i];
		
		lpos = buffer2[0] - REFERENCE;
		rpos = buffer2[1] - REFERENCE;
		
		pbuf = &buffer1[i];
		ivert = 1;

		if(iascii > STOP_ASCII) break;
	
		#ifdef FORMATED_FONT_DATA
		//fprintf(writer, "\t{\t%3d, /* Ascii %c:%d */\n\t\t{", nvert-1, (char)iascii, iascii);
		fprintf(writer, "\t(\t%3d, # Ascii %c:%d \n\t\t(", nvert-1, (char)iascii, iascii);
		#else
		//fprintf(writer, "\t{\t%d, /* Ascii %c:%d */ {", nvert-1, (char)iascii, iascii);
		fprintf(writer, "\t(\t%d, # Ascii %c:%d(", nvert-1, (char)iascii, iascii);
		#endif
		
		if(begin && iascii==xpos[kpos]) 
			//fprintf(math_writer, "\t{\t%3d, /* Ascii %c:%d */\n\t\t{", nvert-1, (char)iascii, iascii);
			fprintf(math_writer, "\t(\t%3d, # Ascii %c:%d \n\t\t(", nvert-1, (char)iascii, iascii);
			
		jvert = 0;
					
		if(ivert < nvert) {
			fputs("\n\t\t", writer);
			if(begin && iascii==xpos[kpos]) fputs("\n\t\t", math_writer);
		}
		else 
			fputs("\t0,", writer);
		
		lx_min=1000, ly_min=1000, rx_max=-1000, ry_max=-1000;
		
		while(ivert < nvert)
		{
			if(!*pbuf && ivert < nvert)
			{
				fgets(buffer1, MAX_HFONT_BUF, reader);
				pbuf = buffer1;
			}
			
			if(*pbuf == NEWLINE) pbuf++;
			else 
			{
				if(*pbuf == SPACE && *(pbuf+1) == REFERENCE) /* pen up & next char is R */
				{
					//fprintf(writer, "%3d,%3d,", -1, -1);
					fprintf(writer, "(%3d,%3d),", -1, -1);
					
					if(begin && iascii==xpos[kpos]) 
					//fprintf(math_writer, "%3d,%3d,", -1, -1);
					fprintf(math_writer, "(%3d,%3d),", -1, -1);
					pbuf++; pbuf++;
				}
				else
				{
					x = *pbuf++ - REFERENCE;
					y = *pbuf++ - REFERENCE;
					
					if(lx_min > x) lx_min = x;
					if(ly_min > y) ly_min = y;
					if(rx_max < x) rx_max = x;
					if(ry_max < y) ry_max = y;
					
					//fprintf(writer, "%3d,%3d,", x, y);
					fprintf(writer, "(%3d,%3d),", x, y);
					
					if(begin && iascii==xpos[kpos]) 
					//fprintf(math_writer, "%3d,%3d,", x, y);
					fprintf(math_writer, "(%3d,%3d),", x, y);
				}
				ivert++;
				jvert++;
				if(jvert == NEWLINE_VERT && ivert < nvert) { 
					fputs("\n\t\t", writer); 
					if(begin && iascii==xpos[kpos]) fputs("\n\t\t", math_writer); 
					jvert=0; 
				}
			}
		}
		
		if(iascii == START_ASCII) {
			lx_min = -8;
			ly_min = -12;
			rx_max = 8;
			ry_max = 9;
		}

		//fputs("\n\t\t},\n\t\t", writer);
		//fprintf(writer, "{%3d,%3d}, {%3d,%3d}\n\t},\n\n", lx_min, ly_min, rx_max, ry_max);		
		fputs("\n\t\t),\n\t\t", writer);
		fprintf(writer, "((%3d,%3d), (%3d,%3d))\n\t),\n\n", lx_min, ly_min, rx_max, ry_max);		

		if(begin && iascii==xpos[kpos]) 
		{
			//fputs("\n\t\t},\n\t\t", math_writer);
			//fprintf(math_writer, "{%3d,%3d}, {%3d,%3d}\n\t},\n\n", lx_min, ly_min, rx_max, ry_max);
			fputs("\n\t\t),\n\t\t", math_writer);
			fprintf(math_writer, "((%3d,%3d), (%3d,%3d)\n\t),\n\n", lx_min, ly_min, rx_max, ry_max);
			kpos++;
		}
		iascii++;
	}
	//fputs("}};", writer);
	fputs("]", writer);
	
	if(begin && ilist > 3) {
		//fputs("}};", math_writer);
		fputs("]", math_writer);
		end = 1;
	}
	
	fclose(reader);
	fclose(writer);
	
	return 1;
}

void run_py_hershey()
{
	FILE* py = fopen("getfont.py","wt");
	
	int nfont = 31;
	char* font_name[] = {
		"RomanSimplex",
		"RomanTriplex",
		"RomanDuplex",
		"Astrology",
		"Cursive",
		"Cyrilic1",
		"CyrillicComplex",
		"Futural",
		"Futuram",
		"GothicEnglishTriplex",
		"GothicGermanTriplex",
		"GothicEnglish",
		"GothicGerman",
		"GothicItalian",
		"GothicItalianTriplex",
		"Greek",
		"GreekComplex",
		"GreekSimplex",
		"Markers",
		"MathLower",
		"MathUpper",
		"Meteorology",
		"Music",
		"ScriptComplex",
		"ScriptSimplex",
		"Symbol",
		"TimesGreek",
		"TimesItalian",
		"TimesItalianBold",
		"TimesRoman",
		"TimesRomanBold",
	};
	
	math_writer = fopen("mathsymbol.py", "wt");
	TG_ParseHersheyFont_Python("..\\rowmans.jhf"    , "romans.py"     , "RomanSimplex");
	TG_ParseHersheyFont_Python("..\\rowmant.jhf"    , "romant.py"     , "RomanTriplex");
	TG_ParseHersheyFont_Python("..\\rowmand.jhf"    , "romand.py"     , "RomanDuplex");
	TG_ParseHersheyFont_Python("..\\astrology.jhf"  , "astrology.py"  , "Astrology");
	TG_ParseHersheyFont_Python("..\\cursive.jhf"    , "cursive.py"    , "Cursive");
	TG_ParseHersheyFont_Python("..\\cyrilc_1.jhf"   , "cyrilc1.py"    , "Cyrilic1");
	TG_ParseHersheyFont_Python("..\\cyrillic.jhf"   , "cyillic.py"    , "CyrillicComplex");
	TG_ParseHersheyFont_Python("..\\futural.jhf"    , "futural.py"    , "Futural");
	TG_ParseHersheyFont_Python("..\\futuram.jhf"    , "futuram.py"    , "Futuram");
	TG_ParseHersheyFont_Python("..\\gothgbt.jhf"    , "gothgbt.py"    , "GothicEnglishTriplex");
	TG_ParseHersheyFont_Python("..\\gothgrt.jhf"    , "gothgrt.py"    , "GothicGermanTriplex");
	TG_ParseHersheyFont_Python("..\\gothiceng.jhf"  , "gothiceng.py"  , "GothicEnglish");
	TG_ParseHersheyFont_Python("..\\gothicger.jhf"  , "gothicger.py"  , "GothicGerman");
	TG_ParseHersheyFont_Python("..\\gothicita.jhf"  , "gothicita.py"  , "GothicItalian");
	TG_ParseHersheyFont_Python("..\\gothitt.jhf"    , "gothitt.py"    , "GothicItalianTriplex");
	TG_ParseHersheyFont_Python("..\\greek.jhf"      , "greek.py"      , "Greek");
	TG_ParseHersheyFont_Python("..\\greekc.jhf"     , "greekc.py"     , "GreekComplex");
	TG_ParseHersheyFont_Python("..\\greeks.jhf"     , "greeks.py"     , "GreekSimplex");
	TG_ParseHersheyFont_Python("..\\markers.jhf"    , "marker.py"     , "Markers");
	TG_ParseHersheyFont_Python("..\\mathlow.jhf"    , "mathlow.py"    , "MathLower");
	TG_ParseHersheyFont_Python("..\\mathupp.jhf"    , "mathupp.py"    , "MathUpper");
	TG_ParseHersheyFont_Python("..\\meteorology.jhf", "meteorology.py", "Meteorology");
	TG_ParseHersheyFont_Python("..\\music.jhf"      , "music.py"      , "Music");
	TG_ParseHersheyFont_Python("..\\scriptc.jhf"    , "scriptc.py"    , "ScriptComplex");
	TG_ParseHersheyFont_Python("..\\scripts.jhf"    , "scripts.py"    , "ScriptSimplex");
	TG_ParseHersheyFont_Python("..\\symbolic.jhf"   , "symbol.py"     , "Symbol");
	TG_ParseHersheyFont_Python("..\\timesg.jhf"     , "timesg.py"     , "TimesGreek");
	TG_ParseHersheyFont_Python("..\\timesi.jhf"     , "timesi.py"     , "TimesItalian");
	TG_ParseHersheyFont_Python("..\\timesib.jhf"    , "timesib.py"    , "TimesItalianBold");
	TG_ParseHersheyFont_Python("..\\timesr.jhf"     , "timesr.py"     , "TimesRoman");
	TG_ParseHersheyFont_Python("..\\timesrb.jhf"    , "timesrb.py"    , "TimesRomanBold");
	fclose(math_writer);
	
	fprintf(py, "font_name = (\n");
	for(int i = 0; i < nfont; i++)
		fprintf(py, "\t\"%s\",\n", font_name[i]);
	fprintf(py, ")\n");
	fclose(py);

}
void run_c_hershey()
{
	math_writer = fopen("d:\\programming\\libtg\\codeproj\\mathsymbol.c", "wt");
	
	TG_ParseHersheyFont("d:\\programming\\libtg\\codeproj\\HersheyFont\\rowmans.jhf"    , "d:\\programming\\libtg\\codeproj\\romans.c"     , "RomanSimplex");
	TG_ParseHersheyFont("d:\\programming\\libtg\\codeproj\\HersheyFont\\rowmant.jhf"    , "d:\\programming\\libtg\\codeproj\\romant.c"     , "RomanTriplex");
	TG_ParseHersheyFont("d:\\programming\\libtg\\codeproj\\HersheyFont\\rowmand.jhf"    , "d:\\programming\\libtg\\codeproj\\romand.c"     , "RomanDuplex");
	TG_ParseHersheyFont("d:\\programming\\libtg\\codeproj\\HersheyFont\\astrology.jhf"  , "d:\\programming\\libtg\\codeproj\\astrology.c"  , "Astrology");
	TG_ParseHersheyFont("d:\\programming\\libtg\\codeproj\\HersheyFont\\cursive.jhf"    , "d:\\programming\\libtg\\codeproj\\cursive.c"    , "Cursive");
	TG_ParseHersheyFont("d:\\programming\\libtg\\codeproj\\HersheyFont\\cyrilc_1.jhf"   , "d:\\programming\\libtg\\codeproj\\cyrilc1.c"    , "Cyrilic1");
	TG_ParseHersheyFont("d:\\programming\\libtg\\codeproj\\HersheyFont\\cyrillic.jhf"   , "d:\\programming\\libtg\\codeproj\\cyillic.c"    , "CyrillicComplex");
	TG_ParseHersheyFont("d:\\programming\\libtg\\codeproj\\HersheyFont\\futural.jhf"    , "d:\\programming\\libtg\\codeproj\\futural.c"    , "Futural");
	TG_ParseHersheyFont("d:\\programming\\libtg\\codeproj\\HersheyFont\\futuram.jhf"    , "d:\\programming\\libtg\\codeproj\\futuram.c"    , "Futuram");
	TG_ParseHersheyFont("d:\\programming\\libtg\\codeproj\\HersheyFont\\gothgbt.jhf"    , "d:\\programming\\libtg\\codeproj\\gothgbt.c"    , "GothicEnglishTriplex");
	TG_ParseHersheyFont("d:\\programming\\libtg\\codeproj\\HersheyFont\\gothgrt.jhf"    , "d:\\programming\\libtg\\codeproj\\gothgrt.c"    , "GothicGermanTriplex");
	TG_ParseHersheyFont("d:\\programming\\libtg\\codeproj\\HersheyFont\\gothiceng.jhf"  , "d:\\programming\\libtg\\codeproj\\gothiceng.c"  , "GothicEnglish");
	TG_ParseHersheyFont("d:\\programming\\libtg\\codeproj\\HersheyFont\\gothicger.jhf"  , "d:\\programming\\libtg\\codeproj\\gothicger.c"  , "GothicGerman");
	TG_ParseHersheyFont("d:\\programming\\libtg\\codeproj\\HersheyFont\\gothicita.jhf"  , "d:\\programming\\libtg\\codeproj\\gothicita.c"  , "GothicItalian");
	TG_ParseHersheyFont("d:\\programming\\libtg\\codeproj\\HersheyFont\\gothitt.jhf"    , "d:\\programming\\libtg\\codeproj\\gothitt.c"    , "GothicItalianTriplex");
	TG_ParseHersheyFont("d:\\programming\\libtg\\codeproj\\HersheyFont\\greek.jhf"      , "d:\\programming\\libtg\\codeproj\\greek.c"      , "Greek");
	TG_ParseHersheyFont("d:\\programming\\libtg\\codeproj\\HersheyFont\\greekc.jhf"     , "d:\\programming\\libtg\\codeproj\\greekc.c"     , "GreekComplex");
	TG_ParseHersheyFont("d:\\programming\\libtg\\codeproj\\HersheyFont\\greeks.jhf"     , "d:\\programming\\libtg\\codeproj\\greeks.c"     , "GreekSimplex");
	TG_ParseHersheyFont("d:\\programming\\libtg\\codeproj\\HersheyFont\\markers.jhf"    , "d:\\programming\\libtg\\codeproj\\marker.c"     , "Markers");
	TG_ParseHersheyFont("d:\\programming\\libtg\\codeproj\\HersheyFont\\mathlow.jhf"    , "d:\\programming\\libtg\\codeproj\\mathlow.c"    , "MathLower");
	TG_ParseHersheyFont("d:\\programming\\libtg\\codeproj\\HersheyFont\\mathupp.jhf"    , "d:\\programming\\libtg\\codeproj\\mathupp.c"      , "MathUpper");
	TG_ParseHersheyFont("d:\\programming\\libtg\\codeproj\\HersheyFont\\meteorology.jhf", "d:\\programming\\libtg\\codeproj\\meteorology.c", "Meteorology");
	TG_ParseHersheyFont("d:\\programming\\libtg\\codeproj\\HersheyFont\\music.jhf"      , "d:\\programming\\libtg\\codeproj\\music.c"      , "Music");
	TG_ParseHersheyFont("d:\\programming\\libtg\\codeproj\\HersheyFont\\scriptc.jhf"    , "d:\\programming\\libtg\\codeproj\\scriptc.c"    , "ScriptComplex");
	TG_ParseHersheyFont("d:\\programming\\libtg\\codeproj\\HersheyFont\\scripts.jhf"    , "d:\\programming\\libtg\\codeproj\\scripts.c"    , "ScriptSimplex");
	TG_ParseHersheyFont("d:\\programming\\libtg\\codeproj\\HersheyFont\\symbolic.jhf"   , "d:\\programming\\libtg\\codeproj\\symbol.c"     , "Symbol");
	TG_ParseHersheyFont("d:\\programming\\libtg\\codeproj\\HersheyFont\\timesg.jhf"     , "d:\\programming\\libtg\\codeproj\\timesg.c"     , "TimesGreek");
	TG_ParseHersheyFont("d:\\programming\\libtg\\codeproj\\HersheyFont\\timesi.jhf"     , "d:\\programming\\libtg\\codeproj\\timesi.c"     , "TimesItalian");
	TG_ParseHersheyFont("d:\\programming\\libtg\\codeproj\\HersheyFont\\timesib.jhf"    , "d:\\programming\\libtg\\codeproj\\timesib.c"    , "TimesItalianBold");
	TG_ParseHersheyFont("d:\\programming\\libtg\\codeproj\\HersheyFont\\timesr.jhf"     , "d:\\programming\\libtg\\codeproj\\timesr.c"     , "TimesRoman");
	TG_ParseHersheyFont("d:\\programming\\libtg\\codeproj\\HersheyFont\\timesrb.jhf"    , "d:\\programming\\libtg\\codeproj\\timesrb.c"    , "TimesRomanBold");
	
	fclose(math_writer);

}

void main()
{
	run_py_hershey();
}