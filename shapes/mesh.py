import pymel.core as pym


def copyVertexPos(src, tgt):
    try:
        map(lambda x, y: y.setPosition(x.getPosition()), src.vtx, tgt.vtx)
    except Exception as e:
        print "Error:", e
        return False
    return True


def same(mesh1, mesh2):
    if mesh1.numVertices() != mesh2.numVertices():
        return False
    i = 0
    while i < mesh1.numVertices():
        if mesh1.vtx[i].getPosition() != mesh2.vtx[i].getPosition():
            return False
        i += 1
    return True


def same2(mesh1, mesh2):
    r = pym.shapeCompare(mesh1, mesh2)
    if r == 0:
        return True
    return False


def clasify(*objs):
    dObjs = {}
    shapes = pym.ls(objs, dag=True, ni=True, g=True, v=True, r=True)
    count = len(shapes)
    for shp in shapes:
        print count
        count -= 1
        shpN = shp.name(long=True)
        tm = shp.getParent()
        tmN = tm.name(long=True)
        if tm not in dObjs:
            obj = find(shp, dObjs)
            if not obj:
                print "new obj"
                dObjs[tmN] = {
                    "shape": shpN,
                    "instances": []
                }
            else:
                objN = obj.name(long=True)
                print "same shp, add instance"
                dObjs[objN]["instances"].append(tm)

    return dObjs


def clasify2(*objs):
    dObjs = {}
    # shapes = pym.ls(objs, dag=True, ni=True, g=True, v=True, r=True)
    count = len(objs)
    for tm in objs:
        print count
        count -= 1
        for shp in tm.listRelatives(shapes=True, ni=True):
            shpN = shp.name(long=True)
            tmN = tm.name(long=True)
            if tm not in dObjs:
                obj = find(shp, dObjs)
                if not obj:
                    print "new obj"
                    dObjs[tmN] = {
                        "shape": shpN,
                        "instances": []
                        }
                else:
                    objN = obj.name(long=True)
                    print "same shp, add instance"
                    dObjs[objN]["instances"].append(tm)

    return dObjs


def find(shp, objs):
    for objn in objs:
        if same2(shp, pym.PyNode(objs[objn]["shape"])):
            return pym.PyNode(objn)
    return None


def instances(dObj):
    for objn in dObj:
        dElm = dObj[objn]
        # obj = pym.PyNode(objn)
        for inst in dElm["instances"]:
            oInst = pym.PyNode(inst)
            shape = pym.PyNode(dElm["shape"])
            for oshape in oInst.listRelatives(shapes=True):
                if not shape.isIntermediate():
                    pym.parent(oshape, rm=True, s=True)
            pym.parent(shape, oInst, add=True, s=True)


if __name__ == "__main__":
    import MEm.shapes.mesh as mop; reload(mop)
    dC = mop.clasify(*pym.selected())


    print dC

    a,b = pym.ls(sl=1, dag=True, g=True, ni=True)
    a,b
    print mop.same(a,b)
