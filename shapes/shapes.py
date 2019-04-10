import pymel.core as pym
from collections import OrderedDict


def mirrorLR(name):
    if "_R_" in name:
        return name.replace("_R_", "_L_")
    if name.endswith("_R"):
        return name[:-2] + "_L"
    if name.startswith("R_"):
        return "L_" + name[2:]
    if "_L_" in name:
        return name.replace("_L_", "_R_")
    if name.endswith("_L"):
        return name[:-2] + "_R"
    if name.startswith("L_"):
        return "R_" + name[2:]
    if "_r_" in name:
        return name.replace("_r_", "_l_")
    if name.endswith("_r"):
        return name[:-2] + "_l"
    if name.startswith("r_"):
        return "l_" + name[2:]
    if "_l_" in name:
        return name.replace("_l_", "_r_")
    if name.endswith("_l"):
        return name[:-2] + "_r"
    if name.startswith("l_"):
        return "r_" + name[2:]


class Shapes(object):
    def __init__(self, obj):
        """
        Create Shapes Class for operate obj shapes at high level
        :obj object to opearate on blendshape nodes
        """
        self.bsNode = pym.listHistory(obj, type='blendShape')[0]
        self.defNode = self.bsNode.getBaseObjects()[0]
        indxList = self.bsNode.weightIndexList()
        self.__attrs__ = OrderedDict()
        for iw in indxList:
            attr = self.bsNode.attr("weight[{0}]".format(iw))
            alias = attr.getAlias()
            self.__attrs__[alias] = attr

        self.__store__()

    def __store__(self):
        """
        Store the weigh index value on self.__oriwi__
        """
        self.__oriwi__ = {}
        for key, attr in self.__attrs__.iteritems():
            self.__oriwi__[key] = attr.get()

    def __restore__(self):
        for key, val in self.__oriwi__.iteritems():
            self.__attrs__[key].set(val)

    def __reset__(self):
        for attr in self.__attrs__.itervalues():
            attr.set(0.0)

    def insertShapes(cls, obj, shpGrp):
        obj = pym.PyNode(obj)
        shpGrp = pym.PyNode(shpGrp)
        shpGrpP = shpGrp.name().split("_")
        bsName = "_".join(shpGrpP[:-1])
        bsNode = pym.listHistory(obj, type='blendShape')
        if bsNode:
            bsNode = bsNode[0]
        else:
            bsNode = pym.blendShape(obj, n=bsName)
        i = 0
        for child in shpGrp.getChildren(type="transform"):
            pym.blendShape(bsNode, edit=True, t=(obj, i, child, 1.0))
            i += 1
        return obj

    def extractShapes(self):
        """
        extract Shapes from targets
        : obj obj with shapes to extract
        """
        self.__reset__()
        parent = pym.createNode("transform", n=self.bsNode.name()+"_grp")
        for key, attr in self.__attrs__.iteritems():
            attr.set(1.0)
            dup = pym.duplicate(self.defNode, n=key)
            pym.parent(dup, parent, a=True)
            attr.set(0.0)
        self.__restore__()
        return parent

    def mirrorShapes(self, obj):
        """
        mirror Shapes from a _L or _R geometry to the other
        :obj object to apply mirrored shapes
        """
        obj = pym.PyNode(obj)
        self.__reset__()
        mirrTM = pym.createNode("transform", n="mirror")
        lDups = []
        for key, attr in self.__attrs__.iteritems():
            attr.set(1.0)
            dup = pym.duplicate(self.defNode, n=mirrorLR(key))
            lDups.append(dup)
            pym.parent(dup, mirrTM)
            attr.set(0.0)

        mirrTM.scaleX.set(-1.0)
        for dup in lDups:
            pym.parent(dup, w=1, a=1)
            pym.makeIdentity(dup, a=1, pn=1)
        pym.delete(mirrTM)
        shapes = lDups + [obj]
        bsN = pym.blendShape(*shapes)[0]
        bsN.rename(obj.name() + "_BS")
        pym.delete(*lDups)

        self.__restore__()

    def __getitem__(self, key):
        if key in self.__attrs__:
            return self.__attrs__[key]
        else:
            return None


def iterConns():
    import conns
    reload(conns)
    conns = conns.conns
    for ctl in conns:
        dChan = conns[ctl]
        for chan in dChan:
            dTgt = dChan[chan]
            for tgt in dTgt:
                dAlias = dTgt[tgt]
                for alias in dAlias:
                    for drv, val in dAlias[alias]:
                        yield ctl, chan, drv, tgt, alias, val


def clear():
    """
    clear blendshapes driven keys on conns map
    """
    for ctl, chan, drv, tgt, alias, val in iterConns():
        print "CLEAR:", tgt, alias
        try:
            pym.cutKey(tgt, at=alias, cl=True)
        except Exception as e:
            print e
            continue


def connect():
    """
    conenct shape control panel with blendshapes based on map
    """
    for ctl, chan, drv, tgt, alias, val in iterConns():
        try:
            oSHP = Shapes(tgt)
        except Exception as e:
            print e
            continue
        drvAttr = "{0}.{1}".format(ctl, chan)
        tgtAttr = oSHP[alias]
        print "Create key from",
        print "{0}:{1} to {2}:{3}".format(
                drvAttr, drv, tgtAttr.name(), val
        )
        oDrvAttr = pym.PyNode(drvAttr)
        print "Value:", oDrvAttr.get()
        oDrvAttr.set(drv)
        tgtAttr.set(val)
        pym.setDrivenKeyframe(
            tgtAttr.name(),
            cd=drvAttr,
            ott="linear",
            itt="linear"
        )


def clean(obj):
    pym.delete(obj, ch=True)
    pym.makeIdentity(obj, a=True)


def CleanShapes():
    for obj in pym.ls(sl=1):
        print "get node"
        oSHP = Shapes(obj)
        print "extract Shapes"
        shpGrp = oSHP.extractShapes()
        print "clean obj"
        clean(obj)
        print "clean childs"
        map(clean, shpGrp.getChildren())
        print "insert Shapes"
        oSHP.insertShapes(obj, shpGrp)
        print "mirror shapes name"
        otherSide = mirrorLR(obj.name())
        print "get node mirror"
        osObj = pym.PyNode(otherSide)
        print "clean mirror"
        clean(osObj)
        print "get node"
        oSHP = Shapes(obj)
        print "mirror other side"
        oSHP.mirrorShapes(otherSide)
    # print bsNodes
    # print pym.aliasAttr(bsNodes[0], q=True)
    # print pym.blendShape(obj, q=True, w=1)
    # print bsNodes[0].numWeights()
    # print bsNodes[0].weightIndexList()
    #
    # print bsNodes[0].getTarget()

    # print "\n".join(dir(bsNodes[0]))
    # print sourceShapes
    # print  pym.listHistory(obj)
    # print pym.blendShape(bsNode, q=1, g=1)
    # print pym.blendShape(obj, q=1, g=1)
    # print "\n".join(pym.listAttr(bsNode))
    # print bsNode.w.get
if __name__ == "__main__":
    clear()
    # test()
    # oEYE_S = Shapes("EYELID_DOWN_L")
    # oEYE_S.mirrorShapes("EYELID_DOWN_R")
