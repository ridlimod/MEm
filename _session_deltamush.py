### DELTAMUSH FIXES
import MEm.deformer.deltaMush as dM; reload(dM)
import pymel.core as pym

dM.reset("iBird43:BODY")
p
dm = pym.ls(sl=1)[0]
dm.name()
dm.listAttr()
pym.workspace.path

mainCTL = pym.ls("main_control", type="transform", r=True)[0]
wiregrp = pym.ls("WIRE", r=True)[0]
for child in wiregrp.listRelatives(ad=True, type="mesh"):
    dMN = child.listHistory(type="deltaMush")
    if dMN:
        print child.name()
        dM.connectScale(child, mainCTL)

dM.connectScale("iBird43:BODY", "iBird43:main_control")

dm = pym.deltaMush("BODY", n="iBird43_BODY_dm")
pym.deltaMush("deltaMush20", g=["BODY"], rm=True, e=True)
pym.deltaMush("BODY", n="iBird43_deltaMush")
dm20 = pym.PyNode("BODY")
dm20.namespace()
pym.delete(dm20)
pym.sceneName()
dmN = pym.listHistory("BODY", type="deltaMush")[0]
pym.deformerWeights("deltamush_BODY_iBird43.xml", export=True, path="E:/FreeLanceWork/Genoma/PRJ_FLOWER/scenes/iBird43/_deformer_wm", deformer=dmN)
dmN.setGeometry(["BODY"], rm=True)
pym.delete(dmN)
dmN = pym.deltaMush("BODY", n="iBird43_deltaMush")
pym.deformerWeights("deltamush_BODY_iBird43.xml", im=True, path="E:/FreeLanceWork/Genoma/PRJ_FLOWER/scenes/iBird43/_deformer_wm", deformer=dmN)
