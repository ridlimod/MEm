import pymel.core as pym
import json
from maya import mel


def referenceMultiple(file, namespace, start, quantity):
    for i in range(start, start+quantity):
        refNS = namespace + "_{0:0>2}".format(i)
        print refNS
        frO = pym.system.createReference(
            file, namespace=refNS, sharedReferenceFile=True
        )
        frO.unload()


def fixEditsSubstring(refnode, pfix, namespace):
    # pfix = "conservaEnch_v01_proxy_"
    pl = len(pfix)
    # namespace = "conservaEnch_01:"
    # refnode = "conservaEnch_v01_proxyRN"
    bad_neds = []
    for es in pym.system.referenceQuery(refnode, es=True):
        print "es:", es
        cmd = es.split(" ")
        ncmd = []
        print "cmd:", cmd
        print "ncmd:", ncmd
        for attr in cmd:
            if attr.startswith("\""):
                attr = attr.strip("\"")
                quotes = True
            else:
                quotes = False
            if "|" in attr:
                paths = attr.split("|")
            else:
                paths = [attr]
            npaths = []
            print "paths:", paths
            print "npaths:", npaths
            for path in paths:
                print "iterpath:", path
                if path.startswith(pfix):
                    # conseva fix
                    npaths.append(
                        namespace + path[pl:].replace("conseva", "conserva")
                    )
                else:
                    npaths.append(path)
            if quotes:
                newattr = "\"" + "|".join(npaths) + "\""
            else:
                newattr = "|".join(npaths)
            print "npaths:", npaths
            print "newattr", newattr
            ncmd.append(newattr)

        neds = " ".join(ncmd)
        print "ncmd:", ncmd
        print "ns:", neds
        try:
            pym.mel.eval(neds)
        except Exception as e:
            bad_neds.append(neds)
            print e

    return bad_neds


def fixEditsNS(rn, bad, new):
    bad_neds = []
    for es in pym.system.referenceQuery(rn, es=True):
        ns = es.replace(bad + ":", new + ":")
        try:
            pym.mel.eval(ns)
        except Exception as e:
            print e
            bad_neds.append([ns, e])
    return bad_neds


def exportEDS(refnode, file):
    edlist = []
    for es in pym.system.referenceQuery(refnode, es=True):
        edlist.append(es.split(" "))
    with open(file, "w") as fh:
        json.dump(edlist, fh, indent=4)


def attrExists(attr):
    try:
        pym.PyNode(attr)
    except Exception as e:
        print e
        return False
    return True


def edeval(ed):
    try:
        mel.eval(ed)
    except Exception as e:
        print "Error:", e
        return False
    return True


def unquote(attr):
    quoted = False
    if attr.startswith("\""):
        quoted = True
    return attr.strip("\""), quoted


def quote(attr):
    return "\"" + attr + "\""


def findAttr(attr, lNS):
    attr, quoted = unquote(attr)
    found = False
    if attrExists(attr):
        found = True
    else:
        for ns in lNS:
            nsAttr = ns + ":" + attr
            if attrExists(nsAttr):
                found = True
                attr = nsAttr
                break
    if found:
        if quoted:
            attr = quote(attr)
        return attr
    else:
        return None


def evalSetAttr(ed, lNS, replaceList):
    edp = ed[:]
    attr = edp[1]
    for istr, irep in replaceList:
        attr = attr.replace(istr, irep)
    attr = findAttr(attr, lNS)
    if attr is None:
        print "Attr:", attr, "from:", ed[1], "not found"
        return False
    edp[1] = attr
    if not edeval(" ".join(ed)):
        return False
    return True


def importEDS(refnode, file, replacelist):
    tgtNS = pym.system.referenceQuery(refnode, namespace=True)
    tgtNS = tgtNS[1:]
    with open(file, "r") as fh:
        edlist = json.load(fh)

    while edlist:
        ed = edlist[0]
        skip = False
        cmd = ed[0]
        if cmd == "setAttr":
            if evalSetAttr(ed, [tgtNS], replacelist):
                edlist.pop(0)
            else:
                return edlist
        elif cmd == "connectAttr":
            attr1 = ed[1]
            attr2 = ed[2]
            for istr, irep in replacelist:
                attr1 = attr1.replace(istr, irep)
                attr2 = attr2.replace(istr, irep)

            for attr in (attr1, attr2):
                if "MayaNodeEditorSavedTabsInfo" in attr:
                    skip = True
                    break

            if skip:
                print "Skip:", ed
                edlist.pop(0)
            else:
                for attr in (attr1, attr2):
                    if not attrExists(attr.strip("\"")):
                        if "\"" in attr:
                            quotes = True
                            attr = attr.strip("\"")
                        else:
                            quotes = False
                        # ### Try in namespace:
                        attr = tgtNS + ":" + attr
                        if not attrExists(attr):
                            return edlist
                        if quotes:
                            attr = "\"" + attr + "\""
                attr1_tmp = ed[1]
                attr2_tmp = ed[2]
                ed[1] = attr1
                ed[2] = attr2
                if not edeval(" ".join(force(ed))):
                    ed[1] = attr1_tmp
                    ed[2] = attr2_tmp
                    return edlist
                edlist.pop(0)
        else:
            edlist.pop(0)


def force(ed):
    return [ed[0]] + ["-force"] + ed[1:]


def fixLilli():
    rplist = (
        ("lilli1:", "lilli_01:lilli:"),
    )
    edlist = importEDS(
        "lilli_01RN", "E:\\FreeLanceWork\\Genoma\\lilli_rest.json", rplist
    )
    return edlist

def fixSinistra():
    #### sinistra
    srcRN = "sinistra_v70_namespaceRN"
    tgtRN = "sinistra_01RN"
    json_file, json_file_left = "sinistra_06_34.json","sinistra_06_34_left.json"
    refT.exportEDS(srcRN, json_file)
    refT.exportEDS(srcRN, json_file_left)

    rplist = (
        ("sinistra:", "sinistra_01:sinistra:"),
        ("sinistra2:", "sinistra_01:sinistra:"),
        ("sinistra1:", "sinistra_01:sinistra:")
    )

    edleft = refT.importEDS(tgtRN, json_file_left, rplist)

    with open("lilli_06_33_left.json", "w") as fh:
        json.dump(edleft, fh, indent=4)
    edleft[0]
