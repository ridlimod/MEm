import pymel.core as pym
import json
import evaluators as eva
reload(eva)


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


def importEDS(refnode, file, replacelist, searchNS=None):
    if searchNS is None:
        searchNS = []

    tgtNS = pym.system.referenceQuery(refnode, namespace=True)
    tgtNS = tgtNS[1:]
    with open(file, "r") as fh:
        edlist = json.load(fh)

    while edlist:
        ed = edlist[0]
        cmd = ed[0]
        if cmd == "setAttr":
            if eva.evalSetAttr(ed, [tgtNS] + searchNS, replacelist):
                edlist.pop(0)
            else:
                print "ERROR: setAttr"
                return edlist
        elif cmd == "connectAttr":
            if eva.evalConnectAttr(ed, [tgtNS] + searchNS, replacelist):
                edlist.pop(0)
            else:
                print "ERROR: connectAttr"
                return edlist
        else:
            edlist.pop(0)
