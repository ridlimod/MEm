import reference as ref
import json
import os
import pymel.core as pym
reload(ref)


def fixLilli(
    srcRN="lilli_v70_namespaceRN",
    tgtRN="lilli_01RN",
    irplist=None, skip=False, searchNS=None
):
    # ### sinistra
    print "DEBUG: query tgt"
    tgtNS = pym.referenceQuery(tgtRN, namespace=True)
    print "DEBUG: queried tgt"
    json_file, json_file_left = (
        "lilli_eds", "lilli_eds_left"
    )

    rplist = irplist or (
        ("lilli:", "{0}:lilli:".format(tgtNS)),
        ("lilli4:", "{0}:lilli:".format(tgtNS)),
        ("lilli1:", "{0}:lilli:".format(tgtNS))
    )

    return fix(
        srcRN, tgtRN, json_file, json_file_left, rplist, skip=skip,
        searchNS=searchNS
    )


def sinistraToClon(s=1, c=1, n=1, skip=True):
    sinistra = "sinistra"
    clon = "clonSinistra"
    for idx in range(0, n):
        inxs = s + idx
        inxc = c + idx
        sinistraRN = "{0}_{1:0>2}RN".format(sinistra, inxs)
        clonRN = "{0}_{1:0>2}RN".format(clon, inxc)
        print "DEBUG:", sinistraRN, clonRN
        sinistraNS = sinistraRN[:-2]
        clonNS = clonRN[:-2]
        try:
            os.remove("{0}_eds.json".format(sinistra))
        except Exception:
            print "already deleted"

        try:
            os.remove("{0}_eds_left.json".format(sinistra))
        except Exception:
            print "already deleted"

        rplist = (
            (
                "{0}:{1}:".format(sinistraNS, sinistra),
                "{0}:{1}:".format(clonNS, clon)
            ),
            (
                "|{0}fosterParent1|".format(sinistraRN),
                ""
            ),
            (
                "{0}:{1}:{2}".format(clonNS, clon, sinistra),
                "{0}:{1}:{2}".format(clonNS, clon, clon)
            )
        )
        for srch, repl in rplist:
            print "replace:", srch, "with:", repl

        print sinistraRN, clonRN
        print "fixSinistra({0}, {1}, irplist={2}, skip={3})".format(
            sinistraRN, clonRN, rplist, skip
        )
        fixSinistra(sinistraRN, clonRN, rplist, skip=skip)
    return None


def fixSinistra(
    srcRN="sinistra_v60_namespaceRN", tgtRN="sinistra_01RN",
    irplist=None, skip=False, searchNS=None
):
    # ### sinistra
    print "DEBUG: query tgt"
    tgtNS = pym.referenceQuery(tgtRN, namespace=True)
    print "DEBUG: queried tgt"
    json_file, json_file_left = (
        "sinistra_eds.json", "sinistra_eds_left.json"
    )

    rplist = irplist or (
        ("sinistra:", "{0}:sinistra:".format(tgtNS)),
        ("sinistra2:", "{0}:sinistra:".format(tgtNS)),
        ("sinistra1:", "{0}:sinistra:".format(tgtNS))
    )

    return fix(
        srcRN, tgtRN, json_file, json_file_left, rplist, skip=skip,
        searchNS=searchNS
    )


def fixGabyBird():
    srcRN = "gabyBird_v67RN"
    tgtRN = "gabyBird_01RN"
    json_file, json_file_left = (
        "gabyBird_eds.json", "gabyBird_eds_left.json"
    )

    rplist = (
        ("gabyBird:", "gabyBird_01:gabyBird:"),
    )

    return fix(srcRN, tgtRN, json_file, json_file_left, rplist)


def fixZachiel(
    srcRN="zachiel_v56_namespaceRN", tgtRN="zachiel_01RN",
    irplist=None
):
    json_file, json_file_left = (
        "zachiel_eds.json", "zachiel_eds_left.json"
    )
    tgtNS = pym.referenceQuery(tgtRN, namespace=True)
    rplist = irplist or (
        ("zachiel:", "{0}:zachiel:".format(tgtNS)),
        ("zachiel1:", "{0}:zachiel:".format(tgtNS)),
    )

    return fix(srcRN, tgtRN, json_file, json_file_left, rplist)


def fixHairbrush(
    srcRN="hairBrush_v03RN", tgtRN="hairbrush_01RN",
    irplist=None
):
    json_file, json_file_left = (
        "hairbrush_eds.json", "hairbrush_eds_left.json"
    )
    rplist = irplist or []

    return fix(srcRN, tgtRN, json_file, json_file_left, rplist)


def fix(
    srcRN, tgtRN, json_file,
    json_file_left, rplist, skip=False,
    searchNS=None
):
    ref.exportEDS(srcRN, json_file)
    if not os.path.exists(json_file_left):
        ref.exportEDS(srcRN, json_file_left)
    edleft = ref.importEDS(
        tgtRN, json_file_left, rplist, skip=skip, searchNS=searchNS
    )
    if edleft:
        with open(json_file_left, "w") as fh:
            json.dump(edleft, fh, indent=4)
        return edleft
    return None
