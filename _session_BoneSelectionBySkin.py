### Bone Selection by skincluster

import pymel.core as pym
bodyjoints = []
for jnt in pym.skinCluster("BODY", inf=True, q=True):
    bodyjoints.append(jnt.name())

pym.select(bodyjoints)

tongue = []
for jnt in pym.skinCluster("TONGUE", inf=True, q=True):
    tongue.append(jnt.name())

pym.select(tongue)

leg_l = []
for jnt in pym.skinCluster("LEG_L", inf=True, q=True):
    leg_l.append(jnt.name())

pym.select(leg_l)

leg_r = []
for jnt in pym.skinCluster("LEG_R", inf=True, q=True):
    leg_r.append(jnt.name())

pym.select(leg_r)

for node in pym.ls(sl=1, type="transform"):
    bsNode = pym.listHistory(node, type='blendShape')[0]
    name = bsNode.name().upper()
    bsNode.rename(name)
