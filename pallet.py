#!/usr/bin/python
'''
Create a parametric pallet.
Keep in mind that the XY plane is looking down from the 'top'
'''
from dxfwrite import DXFEngine as dxf

# set up the basic drawing
drawing = dxf.drawing('pallet.dxf')

# Function to create a parametric cubic block
def cblock(bname,x,y,z,lx,ly,lz):
    '''This function takes the block name that the faces will be added to, an xyz of the cube itself, and an xyz for location'''
    # create 3dfaces for cube
    face1 = dxf.face3d([(lx,ly,lz),(x+lx,ly,lz),(x+lx,y+ly,lz),(lx,y+ly,lz)])
    face2 = dxf.face3d([(lx,ly,lz),(x+lx,ly,lz),(x+lx,ly,z+lz),(lx,ly,z+lz)])
    face3 = dxf.face3d([(lx,ly,lz),(lx,ly,z+lz),(lx,y+ly,z+lz),(lx,y+ly,lz)])
    face4 = dxf.face3d([(x+lx,ly,lz),(x+lx,ly,z+lz),(x+lx,y+ly,z+lz),(x+lx,y+ly,lz)])
    face5 = dxf.face3d([(lx,y+ly,z+lz),(lx,ly,z+lz),(x+lx,ly,z+lz),(x+lx,y+ly,z+lz)])
    face6 = dxf.face3d([(lx,y+ly,lz),(x+lx,y+ly,lz),(x+lx,y+ly,z+lz),(lx,y+ly,z+lz)])
    
    # add 3dface to block
    bname.add(face1)
    bname.add(face2)
    bname.add(face3)
    bname.add(face4)
    bname.add(face5)
    bname.add(face6)


# Block adding boilerplate, spaces in name not OK
pallet = dxf.block(name='Europallet')
drawing.blocks.add(pallet)
palref = dxf.insert(blockname='Europallet', insert=(0,0,0))

# Create a Euro pallet by adding faces to one block
# Make bottom boards
cblock(pallet, 100, 1200, 22, 0,0,0)
cblock(pallet, 145, 1200, 22, 327.5, 0, 0)
cblock(pallet, 100, 1200, 22, 700, 0, 0)

#make blocks
cblock(pallet, 100, 145, 78, 0, 0, 22)
cblock(pallet, 100, 145, 78, 0, 527.5, 22)
cblock(pallet, 100, 145, 78, 0, 1055, 22)
cblock(pallet, 145, 145, 78, 327.5, 0, 22)

drawing.add(palref)

drawing.save()

