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
        print "DEBUG:", "is locked:", "is locked" in e
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
            lAttr = pym.ls(ns + "::" + attr.split("|")[-1].split(":")[-1])
            if len(lAttr) == 1:
                found = True
                attr = lAttr[0].name(fullDagPath=True, fullAttrPath=True)
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


def evalConnectAttr(ed, lNS, replaceList):
    skip = False
    edp = ed[:]
    attr1 = edp[1]
    attr2 = edp[2]
    for istr, irep in replaceList:
        attr1 = attr1.replace(istr, irep)
        attr2 = attr2.replace(istr, irep)

    for attr in (attr1, attr2):
        if "MayaNodeEditorSavedTabsInfo" in attr:
            skip = True
            break

    if skip:
        print "Skip:", ed
        return True
    else:
        oAttr1, attr1 = findAttr(attr1, lNS)
        if attr1 is None:
            print "Attr:", attr1, "from:", edp, "not found"
            return False
        oAttr2, attr2 = findAttr(attr2, lNS)
        if attr2 is None:
            print "Attr:", attr1, "from:", edp, "not found"
            return False

        if edp[0].startswith("connect") and oAttr2.isLocked():
            print "Skip Locked:", ed
            return True

        edp[1] = attr1
        edp[2] = attr2

        if edp[0].startswith("connect"):
            if edeval(" ".join(force(edp))):
                return True
        else:
            if edeval(" ".join(edp)):
                return True
    return False
