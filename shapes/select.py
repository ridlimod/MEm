import pymel.core as pym


def selectVisibleMesh(root=None):
    if root:
        meshes = (
            obj.getParent() for obj in pym.ls(root, dag=True, type="mesh")
            if obj.isVisible()
            and not obj.isIntermediate()
        )
    else:
        meshes = (
            obj.getParent() for obj in pym.ls(type="mesh")
            if obj.isVisible()
            and not obj.isIntermediate
        )
    return meshes
