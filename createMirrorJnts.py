from MEm.xform.obj import copyTM

def createDef(root, p=None):
    nf = root.name()
    newname = nf.replace("_ll_", "_l_")
    newJnt = pym.createNode("joint", n=newname)
    copyTM(root, newJnt)
    pym.makeIdentity(newJnt, apply=True, translate=True, rotate=True, scale=True)

    if p:
        pym.parent(newJnt, p)

    for child in root.getChildren(type="joint"):
        createDef(child, p=newJnt)

jntO = pym.ls(sl=1, type="joint")[0]
createDef(jntO)

for obj in pym.ls(sl=1, dag=True):
    name = obj.name()
    newname = name.replace("_l_", "_ll_")
    obj.rename(newname)


##fix Scale
from MEm.xform.obj import copyTM

def fixScale(root, p=None):
    newJnt = pym.createNode("joint", n=root.name() + "_fix")
    copyTM(root, newJnt)
    pym.makeIdentity(newJnt, apply=True, translate=True, rotate=True, scale=True)

    if p:
        pym.parent(newJnt, p)

    for child in root.getChildren(type="joint"):
        fixScale(child, p=newJnt)

jntO = pym.ls(sl=1, type="joint")[0]
fixScale(jntO)
