import pymel.core as pym
from maya import mel
from strops import deenvelop, reenvelop


def force(ed):
    return [ed[0]] + ["-force"] + ed[1:]


def edeval(ed):
    try:
        mel.eval(ed)
    except Exception as e:
        print "Error:", e
        return False
    return True


def attrExists(attr):
    try:
        pym.PyNode(attr)
    except Exception as e:
        print e
        return False
    return True


def findAttr(attr, lNS):
    attr, envelop = deenvelop(attr)
    found = False
    if attrExists(attr):
        found = True
    else:
        for ns in lNS:
            attrLastHierachy = attr.split("|")[-1]
            attrStripNamespace = attrLastHierachy.split(":")[-1]
            searchWildCard = ns + "::" + attrStripNamespace
            lAttr = pym.ls(searchWildCard)
            if len(lAttr) == 1:
                found = True
                if type(lAttr[0]) == pym.Attribute:
                    attr = lAttr[0].name(fullDagPath=True, fullAttrPath=True)
                elif type(lAttr[0]) == pym.general.Pivot:
                    attr = lAttr[0].name()
                else:
                    attr = lAttr[0].name(long=True)
                break

    if found:
        oAttr = pym.PyNode(attr)
        if any(envelop):
            attr = reenvelop(attr, envelop)
        return oAttr, attr
    else:
        return None, None


def evalSetAttr(ed, lNS, replaceList):
    edp = ed[:]
    attr = edp[1]
    for istr, irep in replaceList:
        attr = attr.replace(istr, irep)
    oAttr, attr = findAttr(attr, lNS)
    if attr is None:
        print "Attr:", attr, "from:", edp, "not found"
        return False
    edp[1] = attr
    if edeval(" ".join(edp)):
        return True
    return False


def evalAddAttr(ed, lNS, replaceList):
    edp = ed[:]
    attr = edp[-1]
    for istr, irep in replaceList:
        attr = attr.replace(istr, irep)
    oAttr, attr = findAttr(attr, lNS)
    if attr is None:
        print "Attr:", attr, "from:", edp, "not found"
        return False
    edp[-1] = attr
    if edeval(" ".join(edp)):
        return True
    return False


def evalParent(ed, lNS, replaceList):
    edp = ed[:]
    attr1 = edp[-2]
    attr2 = edp[-1]
    for istr, irep in replaceList:
        attr1 = attr1.replace(istr, irep)
        attr2 = attr2.replace(istr, irep)

    oAttr1, fattr1 = findAttr(attr1, lNS)
    if fattr1 is None:
        print "Attr1:", attr1, "from:", edp, "not found"
        return False
    oAttr2, fattr2 = findAttr(attr2, lNS)
    if attr2 is None:
        print "Attr2:", attr2, "from:", edp, "not found"
        return False
    edp[-2] = fattr1
    edp[-1] = fattr2
    if edeval(" ".join(edp)):
        return True
    return False


def evalConnectAttr(ed, lNS, replaceList):
    # print "DEBUG:", "ed:", ed
    skip = False
    edp = ed[:]
    attr1 = edp[1]
    attr2 = edp[2]
    for istr, irep in replaceList:
        attr1 = attr1.replace(istr, irep)
        attr2 = attr2.replace(istr, irep)

    # print "DEBUG:", "attr1:", attr1, "attr2:", attr2
    for attr in (attr1, attr2):
        if "MayaNodeEditorSavedTabsInfo" in attr:
            skip = True
            break

    if skip:
        print "Skip:", ed
        return True
    else:
        oAttr1, fattr1 = findAttr(attr1, lNS)
        if fattr1 is None:
            print "Attr1:", attr1, "from:", edp, "not found"
            return False
        oAttr2, fattr2 = findAttr(attr2, lNS)
        if attr2 is None:
            print "Attr2:", attr2, "from:", edp, "not found"
            return False

        if edp[0].startswith("connect") and oAttr2.isLocked():
            print "Skip Locked:", ed
            return True

        edp[1] = fattr1
        edp[2] = fattr2
        if edp[0].startswith("connect"):
            # print "DEBUG:", "eval:", " ".join(force(edp))
            if edeval(" ".join(force(edp))):
                return True
        else:
            # print "DEBUG:", "eval:", " ".join(edp)
            if edeval(" ".join(edp)):
                return True
    return False
