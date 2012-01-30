#!/usr/bin/python
from dxfwrite import DXFEngine as dxf

# get name, setup the dxf file
fname = raw_input('What to name this dxf? ') + '.dxf'
dwg = dxf.drawing(fname)

# rack configuration variables
deep = 1 #single deep
bay = 3 #pallets per bay
bays = 10 #length in bays
aisles = 1 #number of aisles


# variables
palx = 1016 #pallet width
paly = 1220 #pallet length
palz = 144 #pallet height
loadx = 1016 #load width
loady = 1200 #load length
loadz = 1016 #load height (excluding pallet)
palgap = 70 #gap between pallets
upgap = 80 #gap between pallet and upright
