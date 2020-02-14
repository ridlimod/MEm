### SHAPES WORK WITH Birds
import MEm.shapes.shapes as shp; reload(shp)
shp.matchBSN()
shp.CleanShapes()

import MEm.shapes.shapes as shp; reload(shp)

for e in shp.iterConns("MEm.shapes.connsGaby"):
    print e
oShp = shp.Shapes("BODY")
oShp.exportShapes()
oShp.extractShapes()
oShp.insertShapes("BODY", "BODY_BS_grp")
shp.clear(filter = ["BODY_BS"], conns="MEm.shapes.connsErna")
shp.connect(filter = ["BODY_BS"], conns="MEm.shapes.connsErna")
shp.connect(conns="MEm.shapes.connsYellow")
# shp.fixNames("body_BS", "BODY_BS")
# shp.matchBSN()
from MEm.shapes import shapes; reload(shapes)
oSHP = shapes.Shapes("EYELASH_L")
oSHP.extractShapes()
oSHP.insertShapes("EYELASH_L", "eyelashL_BS_grp")
shapes.CleanShapes()
shapes.clear()
shapes.connect()
oSHP = shapes.Shapes("BODY_BS")
shapes.fixNames("BODY_BS", "BODY_BS")
shapes.connect(filter = ["EYELASH_L_BS"])
