### Mirror LABELS
for ljnt in pym.ls(sl=1):
    if "_l_" in ljnt.name():
        rjnt = pym.PyNode(ljnt.name().replace("_l_", "_r_"))
        rjnt.side.set(2)
        ljnt.side.set(1)
        rjnt.attr("type").set(18)
        ljnt.attr("type").set(18)
        othertype = rjnt.name().replace("_r_", "_")
        ljnt.otherType.set(othertype)
        rjnt.otherType.set(othertype)
    if "_c_" in ljnt.name():
        othertype = ljnt.name().replace("_l_", "_")
        ljnt.side.set(0)
        ljnt.attr("type").set(18)
