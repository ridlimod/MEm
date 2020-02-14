import pymel.core as pym
from chan import srt
reload(srt)


def lockAll():
    oSRT = srt.srt()
    for og in pym.ls("::*_offgrp", type="transform"):
        print "locking:", og.name()
        oSRT.lockAttrs(og, True)
        oSRT.keyAttrs(og, False)


def unlockAll():
    oSRT = srt.srt()
    for og in pym.ls("::*_offgrp", type="transform"):
        print "locking:", og.name()
        oSRT.lockAttrs(og, False)
        oSRT.keyAttrs(og, True)
