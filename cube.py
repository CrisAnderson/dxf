#!/usr/bin/python

from dxfwrite import DXFEngine as dxf

# set up the basic drawing
drawing = dxf.drawing('cube.dxf')

def cblock(bname,x,y,z,lx,ly,lz):
    # create a block
    board1 = dxf.block(name=bname)
    drawing.blocks.add(board1)

    # create 3dfaces for cube
    face1 = dxf.face3d([(0,0,0),(x,0,0),(x,y,0),(0,y,0)])
    face2 = dxf.face3d([(0,0,0),(x,0,0),(x,0,z),(0,0,z)])
    face3 = dxf.face3d([(0,0,0),(0,0,z),(0,y,z),(0,y,0)])
    face4 = dxf.face3d([(x,0,0),(x,0,z),(x,y,z),(x,y,0)])
    face5 = dxf.face3d([(0,y,z),(0,0,z),(x,0,z),(x,y,z)])
    face6 = dxf.face3d([(0,y,0),(x,y,0),(x,y,z),(0,y,z)])
    
    # add 3dface to block
    board1.add(face1)
    board1.add(face2)
    board1.add(face3)
    board1.add(face4)
    board1.add(face5)
    board1.add(face6)

    # insert the block-create ref, then add to drawing
    blockref = dxf.insert(blockname=bname, insert=(lx,ly,lz))
    drawing.add(blockref)

cblock("board1",100,200,100,0,0,0)
drawing.save()

