#!/usr/bin/python
from dxfwrite import DXFEngine as dxf

# rack configuration variables
deep = 1 #single deep = 1, double deep = 2
bay = 3 #pallets per bay
bays = 10 #length in bays
aisles = 5 #number of aisles
levels = 10 #loads in y
lapproach = 830 #lower approach of the exyz crane
uapproach = 410 #upper approach min
aislew = 1500 #width of aisle
backgap = 300 #back to back pallet gap
deepgap = 100 #gap between pallets in Y in double deep configuration
palgap = 70 #gap between pallets
upgap = 80 #gap between load and upright
upx = 100 #upright width in the x direction
upy = 100 #in the y (z when considering HBW as a whole)
up2up = 800 #width between uprights (looking down aisle)
datz = 220 #down aisle tie height
daty = 60 #down aisle tie width
lift = 153 #lift off gap
zoffset = 140 #difference in height between the two rack levels in double deep

# variables
palx = 1016 #pallet width
paly = 1220 #pallet length
palz = 144 #pallet height
loadx = 1116 #load width
loady = 1320 #load length
loadz = 1500 #load height (excluding pallet)

# get name for file, setup the dxf file
fname = raw_input('What to name this dxf? ') + '.dxf'
dwg = dxf.drawing(fname)

# set up layer scheme
dwg.add_layer('CLT_RAK_Pallet_Rack', color=94)
dwg.add_layer('CLT_PLT_Load')
dwg.add_layer('CLT_PLT_Pallet', color=3)

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

# figure out which is larger out of the pallet/load and use that for calculations
if loadx > palx:
    maxx = loadx
else:
    maxx = palx
    
if loady > paly:
    maxy = loady
else:
    maxy = paly
    
# create the various components
def createpallets(spacing):
    ##### Pallets
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
            #spacing = (2 * maxy) + aislew + backgap + (2 * (maxy + deepgap) * ydeep)
            aisle2 = spacing * l
            # Inner loop to create one aisle
            for k in range(bays):
                # calculate bay length
                blen = upx + ((bay - 1) * upgap) + (bay * maxx) + ((bay - 1) * palgap)
                blength = blen * k
                # create first bay
                for i in range(bay):
                    blockref = dxf.insert(blockname='pallet', layer='CLT_PLT_Pallet', insert=(upx+upgap+(maxx/2)-(palx/2)+(i*(maxx + palgap))+blength,(aislew/2)+(maxy/2)-(paly/2)+aisle2,lapproach+lh))
                    dwg.add(blockref)
                # create opposite side
                for j in range(bay):
                    blockref = dxf.insert(blockname='pallet', layer='CLT_PLT_Pallet', insert=(upx+upgap+(maxx/2)-(palx/2)+(j*(maxx + palgap))+blength,0-(aislew/2)-(maxy/2)-(paly/2)+aisle2,lapproach+lh))
                    dwg.add(blockref)

def createloads(spacing):
    ##### Loads
    load = dxf.block(name='load')
    dwg.blocks.add(load)
    blockfaces(load, loadx, loady, loadz, 0, 0, 0)

    # Outermost loop for creating levels
    for m in range(levels):
        levelheight = datz + palz + loadz + lift
        lh = levelheight * m
        # Outer loop to create all the aisles
        for l in range(aisles):
            # Calc distance between aisles
            #spacing = (2 * maxy) + aislew + backgap + (2 * (maxy + deepgap) * ydeep)
            aisle2 = spacing * l
            # Inner loop to create one aisle
            for k in range(bays):
                # calculate bay length
                blen = upx + ((bay - 1) * upgap) + (bay * maxx) + ((bay - 1) * palgap)
                blength = blen * k
                # create first bay
                for i in range(bay):
                    blockref = dxf.insert(blockname='load', layer='CLT_PLT_Load', insert=(upx+upgap+(maxx/2)-(loadx/2)+(i*(maxx + palgap))+blength,(aislew/2)+(maxy/2)-(loady/2)+aisle2,lapproach+lh+palz))
                    dwg.add(blockref)
                # create opposite side
                for j in range(bay):
                    blockref = dxf.insert(blockname='load', layer='CLT_PLT_Load', insert=(upx+upgap+(maxx/2)-(loadx/2)+(j*(maxx + palgap))+blength,0-(aislew/2)-(maxy/2)-(loady/2)+aisle2,lapproach+lh+palz))
                    dwg.add(blockref)

def createuprights(spacing):                
    ##### Uprights
    upright = dxf.block(name='upright')
    dwg.blocks.add(upright)
    # calculate upright height
    upz = lapproach + (levels * (palz + loadz + lift + datz)) - datz - lift + uapproach
    blockfaces(upright, upx, upy, upz, 0, 0, 0)
    # Outer loop to create all the aisles
    for l in range(aisles):
        # Calc distance between aisles
        #spacing = (2 * maxy) + aislew + backgap + (2 * (maxy + deepgap) * ydeep)
        aisle2 = spacing * l
        # Inner loop to create one aisle
        for k in range(bays+1):
            # calculate bay length
            blen = upx + ((bay - 1) * upgap) + (bay * maxx) + ((bay - 1) * palgap)
            blength = blen * k
            # create inner upright
            blockref1 = dxf.insert(blockname='upright', layer='CLT_RAK_Pallet_Rack', insert=((blength,(aislew/2)+(maxy/2)+(up2up/2)+aisle2, 0)))
            dwg.add(blockref1)
            # create outer upright
            blockref2 = dxf.insert(blockname='upright', layer='CLT_RAK_Pallet_Rack', insert=((blength,(aislew/2)+(maxy/2)-(up2up/2)-upy+aisle2, 0)))
            dwg.add(blockref2)
            # create inner upright (opposite)
            blockref1 = dxf.insert(blockname='upright', layer='CLT_RAK_Pallet_Rack', insert=((blength,0-(aislew/2)-(maxy/2)+(up2up/2)+aisle2, 0)))
            dwg.add(blockref1)
            # create outer upright (opposite)
            blockref2 = dxf.insert(blockname='upright', layer='CLT_RAK_Pallet_Rack', insert=((blength,0-(aislew/2)-(maxy/2)-(up2up/2)-upy+aisle2, 0)))
            dwg.add(blockref2)

def createdat(spacing):
    ##### Down Aisle Ties
    tie = dxf.block(name='tie')
    dwg.blocks.add(tie)
    # calculate tie length
    datx = ((bays + 1) * upx) + (bays * (((bay - 1) * upgap) + (bay * maxx) + ((bay - 1) * palgap)))
    blockfaces(tie, datx, daty, datz, 0, 0, 0)
    # Create ties for all levels
    for m in range(levels):
        levelheight = datz + palz + loadz + lift
        lh = levelheight * m
        # Outer loop to create all the aisles
        for l in range(aisles):
            # Calc distance between aisles
            #spacing = (2 * maxy) + aislew + backgap + (2 * (maxy + deepgap) * ydeep)
            aisle2 = spacing * l
            # create outer tie
            blockref1 = dxf.insert(blockname='tie', layer='CLT_RAK_Pallet_Rack', insert=((0,(aislew/2)+(maxy/2)+(up2up/2)+upy+aisle2, lapproach-datz+lh)))
            dwg.add(blockref1)
            # create inter tie
            blockref2 = dxf.insert(blockname='tie', layer='CLT_RAK_Pallet_Rack', insert=((0,(aislew/2)+(maxy/2)-(up2up/2)-upy-daty+aisle2, lapproach-datz+lh)))
            dwg.add(blockref2)
            # create outer tie (opposite)
            blockref1 = dxf.insert(blockname='tie', layer='CLT_RAK_Pallet_Rack', insert=((0,0-(aislew/2)-(maxy/2)-(up2up/2)-upy-daty+aisle2, lapproach-datz+lh)))
            dwg.add(blockref1)
            # create inter tie (opposite)
            blockref2 = dxf.insert(blockname='tie', layer='CLT_RAK_Pallet_Rack', insert=((0,0-(aislew/2)-(maxy/2)+(up2up/2)+upy+aisle2, lapproach-datz+lh)))
            dwg.add(blockref2)

if deep == 1:
    # single deep racking
    spacing = (2 * maxy) + aislew + backgap
    createloads(spacing)
    createpallets(spacing)
    createuprights(spacing)
    createdat(spacing)
else:
    # create inner rack, make the
    spacing = (2 * maxy) + aislew + backgap + (2 * ( maxy + deepgap))
    lift = lift + zoffset
    createloads(spacing)
    createpallets(spacing)
    createuprights(spacing)
    createdat(spacing)

    #create outer rack-redefine some variables first
    lapproach = lapproach + zoffset
    uapproach = uapproach - zoffset

    aislew = aislew + (2 * (maxy + deepgap))
    createloads(spacing)
    createpallets(spacing)
    createuprights(spacing)
    createdat(spacing)
    


dwg.save()