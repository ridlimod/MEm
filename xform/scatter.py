gnd = pym.selected()[0]

mesh = pym.listRelatives(shapes=True)[0]

dir(gnd)
gBB = gnd.getBoundingBox(space="world")
gT = gnd.getTranslation(space="world")
gT
gYMin = gBB[0][1]
gYMin



o = pym.selected()[0]
oBB = o.getBoundingBox(space="world")
oT = o.getTranslation(space="world")
oOff = oT[1] - oBB[0][1]
newT = [oT[0], gYMin-oOff, oT[2]]
newT
o.setTranslation(newT, space="world")


mix = 15
for obj in pym.ls(sl=True, dag=True, type="transform"):
    print obj.name()
    shapes = obj.listRelatives(shapes=True)
    if shapes:
        oBB = obj.getBoundingBox(space="world")
        oT = obj.getTranslation(space="world")
        oOF = oBB[0][1] - oT[1]
        iP = mesh.intersect(oT, [0, -1, 0], space="world")
        if iP[0]:
            point = iP[1][0]
            newT = [point[0], point[1]-oOF-mix, point[2]]
            print iP
            print oOF, oT, point
            obj.setTranslation(newT, space="world")
