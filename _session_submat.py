shapesSet = pym.PyNode("shot01_Chars_RenderSet")

for shape in shapesSet.members():
    print shape
    matSEs = shape.listConnections(type="shadingEngine", et=True, c=True)
    for inp, se in matSEs:
        print "\t", inp, se
        print se.members()
    print matSEs
    matSEs = set(matSEs)
    if len(matSEs) > 1:
        print shape.name(), matSEs


pShape = pym.PyNode("incidentalME:body_proxyShape")
pShape.listAttr()
dir(pShape.instObjGroups)
pShape.instObjGroups.getArrayIndices()
oGrp = pShape.instObjGroups

for i in oGrp.getArrayIndices():
    e =  oGrp.elementByPhysicalIndex(i)
    for j in e.getArrayIndices():
        el = e.elementByPhysicalIndex(j)
        print el

for e in oGrp.iterDescendants():
    print desc
pym.select(pShape)
dir(oGrp)
oGrp

iOG = pym.PyNode("incidentalME:body_proxyShape.instObjGroups[0]")
dir(iOG)
iOG.numChildren()
oG=iOG.getChildren()
oG[0].getArrayIndices()
oG2 = oG[0].elementByLogicalIndex(2)
oG2.listConnections(type="shadingEngine", et=True)
comp, id, color = oG8.iterDescendants()
comp.get()
id.get()
color.get()
for d in oG8.iterDescendants():
    print d

for el in oGrp.iterDescendants():
    if "Id" in el.name():
        print el.get()
    if "GrpCompList" in el.name():
        print el.get()

mOver = pym.ls(sl=1)
dir(mOver)
mOver.listAttr()
mOver
mOver.append("shot01_Chars_RenderSet")

pym.selected()
shader = pym.PyNode("square:aiMixShader1SG")
shader = pym.ls(sl=1)[0]
shader
object = pym.PyNode("square:FLOOR_SECTION_04")
object = pym.ls(sl=1)[0]
object
dir(shader)

shader.forceElement(object)
shader.add(pym.selected()[0])
help(shader.add)


pym.ls("::aiMixShader2SG")

new_mats = pym.ls("square_new::*", type="shadingEngine")
new_mats

for se in new_mats:
    print "SE:", se.name()
    mats = pym.ls(se.listConnections(), materials=True)
    for mat in (mat.name(stripNamespace=True) for mat in mats):
        print "\tmats:", mat
        smat = pym.ls("\tmats:" + mat)
        if smat:
            print "\tFound ori mat:", smat

pym.ls("mats::*fountain*")

    # print se.listConnections(type="shape")
pym.ls(materials=True)
pym.ls(type="shader")

mat = pym.PyNode('square_new:street_mud_MAT15')

dir(mat)
mat.listAttr()
pym.allNodeTypes()

pym.nodeType(mat, i=True)
pym.nodeType("THdependNode", d=True, itn=True)


for e in pym.ls(materials=True):
    print e.name(), e.type(), pym.getClassification(e.type())
    if not pym.getClassification(e.type(), satisfies="shader"):
        print e.name()
    elif e.type() == "shadingEngine":
        print "SE:", e.name()

pym.ls(type="shader")
pym.ls("mats::*noise*")
pym.ls("::*aiShadowMatte*")
pym.select(pym.ls("::*STONESCA*", type="transform"))
pym.select('::*STONESCA*')
