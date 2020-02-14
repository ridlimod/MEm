import pymel.core as pym


def getLights():
    return (
        lgt for lgt in pym.ls(type=pym.listNodeTypes("light"))
        if lgt.type() in pym.nodeType("shape", derived=True, isTypeName=True)
    )


def selectLinked():
    sel = pym.selected()[0]
    shapes = sel.listRelatives(shapes=True)
    if shapes:
        shape = shapes[0]
        if shape not in getLights():
            print "you must select a light first"
            return
    else:
        print "you must select a light first"
    print "getting"
    objects = pym.lightlink(
            light=shape, q=True, set=False, shp=False, t=True, h=False
    )
    pym.select(objects)
