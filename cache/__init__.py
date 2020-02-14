import pymel.core as pym


def fixInheritance():
    ninObj = []
    for obj in pym.ls(sl=1, dag=True, type="transform"):
        if not obj.inheritsTransform.get():
            print obj.name()
            pym.parent(obj, w=True, a=True)
            ninObj.append(obj)

    for obj in ninObj:
        if any(map(lambda x: x.type() == "mesh", pym.ls(obj, dag=True))):
            print obj.name()
            obj.inheritsTransform.set(True)
        else:
            pym.delete(obj)
