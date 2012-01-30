#!/usr/bin/python
from dxfwrite import DXFEngine as dxf

# get name, setup the dxf file
fname = raw_input('What to name this dxf? ') + '.dxf'
dwg = dxf.drawing(fname)

# rack configuration variables
deep = 1 #single deep
bay = 3 #pallets per bay
bays = 10 #length in bays
aisles = 5 #number of aisles
levels = 5 #loads in y
lapproach = 830 #lower approach of the exyz crane
uapproach = 410 #upper approach min
aislew = 1500 #width of aisle
backgap = 300 #back to back pallet gap

# variables
palx = 1016 #pallet width
paly = 1220 #pallet length
palz = 144 #pallet height
loadx = palx #1016 #load width --- logic to pick the bigger of the two not implemented yet
loady = paly #1220 #load length
loadz = 1500 #load height (excluding pallet)
palgap = 70 #gap between pallets
upgap = 80 #gap between load and upright
upx = 100 #upright width in the x direction
upy = 100 #in the y (z when considering HBW as a whole)
up2up = 800 #width between uprights (looking down aisle)
datz = 60 #down aisle tie height
daty = 20 #down aisle tie width
lift = 140 #lift off gap

def createblock(bname, x,y,z):
    '''Block adding boilerplate-pass it the name of the block as a string and where to stick it.'''
    block = dxf.block(name=bname)
    dwg.blocks.add(block)
    blockref = dxf.insert(blockname=bname, insert=(x,y,z))

def blockfaces(bname, x,y,z, lx, ly, lz):
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


# create the various components
# pallets
#createblock('pallet', 0,0,0)
pallet = dxf.block(name='pallet')
dwg.blocks.add(pallet)
blockfaces(pallet, palx, paly, palz, 0, 0, 0)

# Outermost loop for creating levels
for m in range(levels):
    levelheight = datz + palz + loadz + lift
    lh = levelheight * m
    # Outer loop to create all the aisles
    for l in range(aisles):
        # Calc distance between aisles
        aislewidth = (2 * paly) + aislew + backgap
        aisle2 = aislewidth * l
        # Inner loop to create one aisle
        for k in range(bays):
            # calculate bay length
            blen = upx + (2 * upgap) + (3 * loadx) + (2 * palgap)
            blength = blen * k
            # create first bay
            for i in range(bay):
                blockref = dxf.insert(blockname='pallet', insert=((i*(loadx+palgap)+upx+upgap)+blength,(aislew/2)+aisle2,lapproach+lh))
                dwg.add(blockref)
            # create opposite side
            for j in range(bay):
                blockref = dxf.insert(blockname='pallet', insert=((j*(loadx+palgap)+upx+upgap)+blength,0-(aislew/2)-loady+aisle2,lapproach+lh))
                dwg.add(blockref)

# Uprights
upright = dxf.block(name='upright')
dwg.blocks.add(upright)
# calculate upright height
upz = lapproach + (levels * (palz + loadz + lift + datz)) - datz + uapproach
blockfaces(upright, upx, upy, upz, 0, 0, 0)
# Outer loop to create all the aisles
for l in range(aisles):
    # Calc distance between aisles
    aislewidth = (2 * paly) + aislew + backgap
    aisle2 = aislewidth * l
    # Inner loop to create one aisle
    for k in range(bays+1):
        # calculate bay length
        blen = upx + (2 * upgap) + (3 * loadx) + (2 * palgap)
        blength = blen * k
        # create inner upright
        blockref1 = dxf.insert(blockname='upright', insert=((blength,(aislew/2)+(loady/2)+(up2up/2)+aisle2, 0)))
        dwg.add(blockref1)
        # create outer upright
        blockref2 = dxf.insert(blockname='upright', insert=((blength,(aislew/2)+(loady/2)-(up2up/2)-upy+aisle2, 0)))
        dwg.add(blockref2)
        # create inner upright (opposite)
        blockref1 = dxf.insert(blockname='upright', insert=((blength,0-(aislew/2)-(loady/2)+(up2up/2)+aisle2, 0)))
        dwg.add(blockref1)
        # create outer upright (opposite)
        blockref2 = dxf.insert(blockname='upright', insert=((blength,0-(aislew/2)-(loady/2)-(up2up/2)-upy+aisle2, 0)))
        dwg.add(blockref2)

dwg.save()