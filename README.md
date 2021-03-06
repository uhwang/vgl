# vgl
Vector Graphic Library for Python

# Why?
More than 20 years ago, I used Tecplot with image and vector graphic(PS, EPS, WMF) file export. 
However, I can't use it because it is a expensive software. I wanted a simple and light raster & vector graphic plot library.
It was hard to find a package which provides saving Windows metafile. 

# Purpose
Simple xy plot
Simple math or physics simulation
Save screen to image files or WMF(Windows Metafile)
Dependent Python Package
Pygame
Aggdraw
PIL
Note
This library is not full-fledged.

# Terminology
Frame:
A frame is individual plot window.
Users can create multiple frames.

Plotdomain:
A plotdomain is actual plot area inside a frame.
Users can adjust the size of plotdomain but the maximum cannot exceed the frame size.

Frame coordinate:
In the frame coordinates, the measuring unit is inch.
The origin is left top corner.
X value increases on right side.
Y value increases on down side.

World coordinate:
This is the Cartesian coordinate system. It depends on a data plotted on a plotdomain

Windows Metafile:
Windows metafile is one of vector graphic file format.

Frame manager:
A frame manager make it easy to create, delete, or modify frame.

gbbox:
global bounding box. Gbbox is the big box where all frames are included.
DeviceAggdraw and DeviceWindowsMetafile needs the gbbox.
FrameManager provides get_gbbox which returns the gbbox.

dpi:
Dots per inch. DevicePygame needs dpi because screen size depends on both frame size and dpi.
Bigger dpi, bigger screen size.

Symbol:
Symbols are defined in symbol.py.
There are five symbols: Circle, Gradient, Right triangle, Left triangle, Diamond, Square

size:
Line thickness(lthk) and symbol size are the percentage of frame height.
If symbol size 0.001 and a frame height is 3 inch, the logical symbol size will be 0.003 inch.
In DeviceWindowsMetafile, 0.003 is converted to twip.
0.003 x 1270 = 3.81

# Usage
