import pymel.core as pym
node = pym.PyNode("ExocortexAlembicPolyMeshDeform6")
node.listAttr()

print node.ExocortexAlembic_GeomParams.get()
