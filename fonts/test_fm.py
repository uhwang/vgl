# test_fm.py

import vgl

for fid in vgl.fontid._FONT_LIST:
    for did in vgl.devutil._dev_list:
        vgl.print_hershey_font(fid, did)    
#vgl.print_hershey_font(vgl.fontid.FONT_ROMANSIMPLEX, vgl.devutil._dev_ppt)    