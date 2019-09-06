import pymel.core as pym
import maya.cmds as mc


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


def removeEmptySets():
    oseIt = [
        ose.name(long=True) for ose in pym.ls(type="objectSet")
        if not ose.members()
        and ose.type() != "MASH_Waiter"
        and ose.type() != "animLayer"
        and len(ose.listConnections(type="materialOverride")) == 0
    ]
    for ose in oseIt:
        print "DEB: Try deleting:", ose
        try:
            mc.delete(ose)
        except Exception as e:
            print "Not deletable", e


def removeLegacyLayers():
    for layer in (
        layer for layer in pym.ls(type="renderLayer")
        if not layer.name().startswith("rs")
    ):
        try:
            pym.delete(layer)
        except Exception as e:
            print layer, "can't be delete"


def removeAll():
    print("remove UI Event")
    removeOnModelEditChange()
    print("remove Unknown Nodes")
    removeUnknownNodes()
    print("remove Unknown Plugins")
    removeUnknownPlugings()
    print("remove Empty Sets")
    removeEmptySets()
    print("remove legacy layers")
    removeLegacyLayers()
    print("FINISHED")
