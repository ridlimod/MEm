def arnoldlogname():
    import pymel.core as pym
    import os
    current = pym.nodetypes.RenderLayer.currentLayer().name()
    scene = os.path.splitext(os.path.basename(pym.sceneName()))[0]
    aiARO = pym.PyNode("defaultArnoldRenderOptions")
    logfile = aiARO.log_filename.get()
    print "DEBUG: arnoldlog:", current, logfile
    newlogfile = os.path.join(
        os.path.dirname(logfile),
        "{0}_{1}.log".format(scene, current)
    )
    aiARO.log_filename.set(newlogfile)
    print "DEBUG: newlog:", newlogfile


pym.ls("::*Arnold*")
aiARO = pym.PyNode("defaultArnoldRenderOptions")
aiARO.listAttr()
for attr in (attr for attr in aiARO.listAttr() if "log" in attr.name().lower()):
    print attr.name()
print aiARO.log_filename.get()
pym.nodetypes.RenderLayer.currentLayer().name()
pym.sceneName()

arnoldlogname()

import os
print "\n".join(os.environ["PYTHONPATH"].split(";"))
print os.environ["MAYA_CMD_FILE_OUTPUT"]
