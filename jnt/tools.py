import pymel.core as pym


jntDrawStyle = {
    "None": 2,
    "Bone": 0,
    "Multi": 1
}


def setDrawStyle(jnt, drawStyle=jntDrawStyle["Bone"]):
    jnt.drawStyle.set(drawStyle)


def renameChain(jnt, namepattern, indxs, step=1):
    for jnt in pym.ls(jnt, dag=True, type="joint"):
        newname = namepattern.format(**indxs)
        pym.rename(jnt, newname)
        for key in indxs:
            indxs[key] += step

def rename():
    pass
    
