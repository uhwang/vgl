# print_font.py

import vgl

def save():
    import chkfld
    
    path = "./vgl-fonts"
    chkfld.create_folder(path)
    
    for fid in vgl.fontid._FONT_LIST:
        vgl.print_hershey_font(fid, vgl.devutil._dev_img, path)    
    
    # print font with all formats
    #for fid in vgl.fontid._FONT_LIST:
    #    for div in vgl.devutil._dev_list:
    #        vgl.print_hershey_font(fid, div)
    #    
    
    
if __name__ == "__main__":
    save()    