import pymel.core as pym


def removeOnModelEditChange():
    for item in pym.lsUI(editors=True):
        if isinstance(item, pym.ui.ModelEditor):
            pym.modelEditor(item, edit=True, editorChanged="")


def removeUnknownNodes():
    for node in pym.ls(type="unknown"):
        print "Deleting: {0}".format(node.name)
        pym.delete(node)


def removeUnknownPlugings():
    plugins = pym.unknownPlugin(q=True, list=True) or []
    for plug in plugins:
        print "Deleting: {0}".format(plug)
        pym.unknownPlugin(plug, remove=True)


def removeAll():
    print("remove UI Event")
    removeOnModelEditChange()
    print("remove Unknown Nodes")
    removeUnknownNodes()
    print("remove Unknown Plugins")
    removeUnknownPlugings()
