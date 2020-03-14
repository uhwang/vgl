# vgl
Vector Graphic Library for Python

# Why?
I wanted a simple and light raster & vector graphic plot library.
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
Import necessary modules
from frame import Frame, FrameManager
from data import Data
from device import DeviceWindowsMetafile, DeviceAggdraw
import color
import symbol

Create a frame manager or a frame.
fmm = FrameManager()

Define limits of world coordinate system with Data
data = Data(-3,3,-1,10)

Create a frame
frm = fmm.create(0.0,0.0,2,4, data)

Define a symbol
sym = symbol.Circle(0.02, dev.frm.hgt(), 0.005)
0.02 : symbol size
hgt : frame height
0.005: symbol line thickness

Create a device such as DevicePygame, DeviceAggdraw, DeviceWindowsMetafile
dev_wmf = DeviceWindowsMetafile(fname, gbbox)
user_function(dev_wmf)

Close DeviceAggdraw or DeviceWindowsMetafile.
dev_wmf.close()
