pym.namespace(setNamespace=':')
namespaces = pym.namespaceInfo(listOnlyNamespaces=True, recurse=True, an=True)
namespaces.reverse()
namespaces
for ns in namespaces:
    objects = pym.ls(ns+ "::*")
    if not objects:
        try:
            print ns
            pym.namespace(rm=ns)
        except Exception as e:
            print e

pym.ls("UI::*")
pym.namespace(rm=u':windowa3:purple_houses1')
pym.ls(u':windowa3:purple_houses1' + "::*")


pym.namespace(exists=u':windowa3:purple_houses1')


pym.namespace(add='square_in')

pym.select("square_new::*")

pym.namespace(rm="square_new", dnc=True)

for obj in pym.namespaceInfo("square_new", lod=True, dp=True, recurse=True):
    print obj
    try:
        objN = pym.PyNode(obj)
    except:
        continue
    if objN.isLocked():
        print obj
        obj.unlock()

pym.namespaceInfo(cur=1)
pym.ls(sl=1)[0].listRelatives(shapes=True)[0].type()
col = []
for el in pym.ls(sl=True, dag=True):
    shapes = el.listRelatives(shapes=True)
    if shapes and shapes[0].type() == "mesh":
        col.append(shapes[0].name())
pym.select(col)
pym.select("square_windows_02_MAT")
