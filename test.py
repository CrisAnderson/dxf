#!/usr/bin/python

from dxfwrite import DXFEngine as dxf

# set up the basic drawing
drawing = dxf.drawing('basic.dxf')

# create a block
board1 = dxf.block(name="board")
drawing.blocks.add(board1)

# create 3dfaces for cube
face1 = dxf.face3d([(0,0,0),(100,0,0),(100,100,0),(0,100,0)])
face2 = dxf.face3d([(0,0,0),(100,0,0),(100,0,100),(0,0,100)])
face3 = dxf.face3d([(0,0,0),(0,0,100),(0,100,100),(0,100,0)])
face4 = dxf.face3d([(100,0,0),(100,0,100),(100,100,100),(100,100,0)])
face5 = dxf.face3d([(0,0,100),(100,0,100),(100,100,100),(0,100,100)])
face6 = dxf.face3d([(0,100,0),(100,100,0),(100,100,100),(0,100,100)])

# add 3dface to block
board1.add(face1)
board1.add(face2)
board1.add(face3)
board1.add(face4)
board1.add(face5)
board1.add(face6)


# insert the block-create ref, then add to drawing
blockref = dxf.insert(blockname='board', insert=(0,0,0))
drawing.add(blockref)
drawing.save()

