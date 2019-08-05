import pymel.core as pym
import os


def arnoldlogname():
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
