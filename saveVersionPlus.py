import pymel.core as pym
import re

sceneName = pym.cmds.file(sn=1, q=1)
asset, ver = os.path.basename(sceneName).split("_")[0:2]
oM = re.match("v([0-9]+)", ver)
iV = int(oM.groups()[0])
nV = iV + 1
newFile = "scenes/{0}/{0}_v{1}_rig.ma".format(asset,nV)
pym.cmds.file(rn=newFile)
pym.cmds.file(s=1)
