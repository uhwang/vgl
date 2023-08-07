'''
msymsrch.py
'''

from . import fontid
from . import fontm

math_symbol_table = {
"\\deg"     : (fontid.FONT_MATHSYMBOL  , 0x5A),
"\\alpha"   : (fontid.FONT_GREEKSIMPLEX, 0x61),
"\\beta"    : (fontid.FONT_GREEKSIMPLEX, 0x62),
"\\gamma"   : (fontid.FONT_GREEKSIMPLEX, 0x63),
"\\delta"   : (fontid.FONT_GREEKSIMPLEX, 0x64),
"\\epsilon" : (fontid.FONT_GREEKSIMPLEX, 0x65),
"\\zeta"    : (fontid.FONT_GREEKSIMPLEX, 0x66),
"\\eta"     : (fontid.FONT_GREEKSIMPLEX, 0x67),
"\\theta"   : (fontid.FONT_GREEKSIMPLEX, 0x68),
"\\iota"    : (fontid.FONT_GREEKSIMPLEX, 0x69),
"\\kappa"   : (fontid.FONT_GREEKSIMPLEX, 0x6A),
"\\lambda"  : (fontid.FONT_GREEKSIMPLEX, 0x6B),
"\\mu"      : (fontid.FONT_GREEKSIMPLEX, 0x6C),
"\\nu"      : (fontid.FONT_GREEKSIMPLEX, 0x6D),
"\\xi"      : (fontid.FONT_GREEKSIMPLEX, 0x6E),
"\\omicron" : (fontid.FONT_GREEKSIMPLEX, 0x6F),
"\\pi"      : (fontid.FONT_GREEKSIMPLEX, 0x70),
"\\rho"     : (fontid.FONT_GREEKSIMPLEX, 0x71),
"\\sigma"   : (fontid.FONT_GREEKSIMPLEX, 0x72),
"\\tau"     : (fontid.FONT_GREEKSIMPLEX, 0x73),
"\\upsilon" : (fontid.FONT_GREEKSIMPLEX, 0x74),
"\\phi"     : (fontid.FONT_GREEKSIMPLEX, 0x75),
"\\chi"     : (fontid.FONT_GREEKSIMPLEX, 0x76),
"\\psi"     : (fontid.FONT_GREEKSIMPLEX, 0x77),
"\\omega"   : (fontid.FONT_GREEKSIMPLEX, 0x78)
}

def get_symbol_glyp(token):
    glyp = None
    
    if token in math_symbol_table:
        f_info = math_symbol_table[token]
        glyp = fontm.get_glyp(f_info[0], f_info[1]-ord(' '))
        
    return glyp