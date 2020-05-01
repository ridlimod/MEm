### Constraint serialization
import pymel.core as pym

serConst = {}
for obj in pym.ls(sl=1, dag=True, type="constraint"):
    dnsObj = obj.name().split(":")[-1]
    dnsParent = obj.getParent().name().split(":")[-1]
    type = obj.type()
    conns = map(lambda x: (x[0].split(":")[-1], x[1].split(":")[-1]), obj.listConnections(c=True, p=True))
    if dnsObj not in serConst:
        serConst[dnsObj]=[dnsParent, type, conns]
    else:
        raise Exception("LOL")
serConst

# import json
# with open("iBird22_defconst.json", "w") as fh:
#     json.dump(serConst, fh)
    
