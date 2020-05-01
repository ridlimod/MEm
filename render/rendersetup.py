import pymel.core as pym


class layersStatic(object):
    RS_sets = set([
        "RS_charSet",
        "RS_charMatteSet",
        "RS_charCastersSet",
        "RS_bgSet",
        "RS_bgMatteSet",
        "RS_bgCastersSet",
        "RS_skySet",
        "RS_shSmatteSet",
        "RS_shCastersSet",
        "RS_extSet",
        "RS_extCastersSet",
        "RS_extMatteSet"
    ])

    def __init__(self):
        self.spawnSets()
        self.charS = pym.PyNode("RS_charSet")
        self.shCS = pym.PyNode("RS_shCastersSet")
        self.shS = pym.PyNode("RS_shSmatteSet")
        self.charMS = pym.PyNode("RS_charMatteSet")
        self.extS = pym.PyNode("RS_extSet")
        self.bgCS = pym.PyNode("RS_bgCastersSet")
        self.bgS = pym.PyNode("RS_bgSet")
        self.skyS = pym.PyNode("RS_skySet")
        self.extCastersSet = pym.PyNode("RS_extCastersSet")

    def char(self):
        self.charS.addMembers(pym.selected())
        self.shCS.addMembers(pym.selected())

    def BG(self):
        self.bgS.addMembers(pym.selected())
        self.shS.addMembers(pym.selected())
        self.charMS.addMembers(pym.selected())

    def EXT(self):
        self.extS.addMembers(pym.selected())
        self.charMS.addMembers(pym.selected())
        self.bgCS.addMembers(pym.selected())

    def sky(self):
        self.skyS.addMembers(pym.selected())

    def EXTcasters(self):
        self.extCastersSet.addMembers(pym.selected())

    def spawnSets(self):
        for RS in self.RS_sets:
            nset = pym.ls(":{0}".format(RS))
            if not nset:
                print "creating:", RS
                pym.createNode("objectSet", n=RS)

    def clean(self):
        sel = pym.selected()
        for rset in pym.ls("RS_*", type="objectSet"):
            for el in sel:
                try:
                    rset.remove(el)
                except Exception:
                    pass


class layerACam(layersStatic):
    def __init__(self):
        super(layerACam, self).__init__()

    def char(self):
        self.charS.addMembers(pym.selected())
        self.bgCS.addMembers(pym.selected())

    def BG(self):
        self.bgS.addMembers(pym.selected())
        self.charMS.addMembers(pym.selected())
