import reference as ref
import json
import os
reload(ref)


def fixLilli():
    srcRN = "lilli_v70_namespaceRN"
    tgtRN = "lilli_01RN"
    json_file, json_file_left = (
        "lilli_eds", "lilli_eds_left"
    )
    rplist = (
        ("lilli:", "lilli_01:lilli:"),
    )

    return fix(srcRN, tgtRN, json_file, json_file_left, rplist)


def fixSinistra():
    # ### sinistra
    srcRN = "sinistra_v60_namespaceRN"
    tgtRN = "sinistra_01RN"
    json_file, json_file_left = (
        "sinistra_eds.json", "sinistra_eds_left.json"
    )

    rplist = (
        ("sinistra:", "sinistra_01:sinistra:"),
        ("sinistra2:", "sinistra_01:sinistra:"),
        ("sinistra1:", "sinistra_01:sinistra:")
    )

    return fix(srcRN, tgtRN, json_file, json_file_left, rplist)


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


def fixZachiel():
    srcRN = "zachiel_v56_namespaceRN"
    tgtRN = "zachiel_01RN"
    json_file, json_file_left = (
        "zachiel_eds.json", "zachiel_eds_left.json"
    )

    rplist = (
        ("zachiel:", "zachiel_01:zachiel:"),
    )

    return fix(srcRN, tgtRN, json_file, json_file_left, rplist)


def fix(srcRN, tgtRN, json_file, json_file_left, rplist):
    ref.exportEDS(srcRN, json_file)
    if not os.path.exists(json_file_left):
        ref.exportEDS(srcRN, json_file_left)

    edleft = ref.importEDS(tgtRN, json_file_left, rplist)
    if edleft:
        with open(json_file_left, "w") as fh:
            json.dump(edleft, fh, indent=4)
        return edleft
    return None
