# print_font.py

import vgl

for fid in vgl.fontid._FONT_LIST:
    vgl.print_hershey_font(fid, vgl.devutil._dev_img)    

# print font with all formats
#for fid in vgl.fontid._FONT_LIST:
#    for div in vgl.devutil._dev_list:
#        vgl.print_hershey_font(fid, div)
#    