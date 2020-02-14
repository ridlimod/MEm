import pymel.core as pym
import maya.cmds as mc
import maya.mel as mel


def copyTM(ob1, ob2):
    tm = pym.xform(ob1, q=1, ws=1, m=1)
    pym.xform(ob2, ws=1, m=tm)


def copyRot(ob1, ob2):
    gRot = pym.xform(ob1, q=1, ws=1, ro=1)
    pym.xform(ob2, ws=1, ro=gRot)


def copyLRot(ob1, ob2):
    gRot = pym.xform(ob1, q=1, ro=1)
    pym.xform(ob2, ro=gRot)


def copyLTM(ob1, ob2):
    tm = pym.xform(ob1, q=1, m=1)
    pym.xform(ob2, m=tm)


def copyWStoL(ob1, ob2):
    wsTM = pym.xform(ob1, q=1, ws=1, m=1)
    pym.xform(ob2, m=wsTM)


def addLRot(ob1, ob2):
    gRot = pym.xform(ob1, q=1, ro=1)
    pym.xform(ob2, r=1, eu=1, ro=gRot)


def addRot(ob1, ob2):
    gRot = pym.xform(ob1, ws=1, q=1, ro=1)
    pym.xform(ob2, ws=1, r=1, eu=1, ro=gRot)


def subLRot(ob1, ob2):
    ob1Rot = pym.xform(ob1, q=1, ro=1)
    pym.xform(ob2, r=1, eu=1, ro=neg(ob1Rot))


def neg(vector):
    return [-1 * e for e in vector]


def bakePivot(ob, pos=1, ori=1):
    currentCtx = mc.currentCtx()
    contextList = [
        "moveSuperContext", "manipMoveContext", "RotateSuperContext",
        "manipRotateContext", "scaleSuperContext", "manipScaleContext"
    ]

    if currentCtx not in contextList:
        mc.error("m_bakeCustomToolPivot.kWrongToolError")
        return None

    # Check 3) must be in custom orientation mode
    customOri = []
    pivotModeActive = 0
    customModeActive = 0
    if currentCtx == "moveSuperContext" or currentCtx == "manipMoveContext":
        customOri = mc.manipMoveContext('Move', q=1, orientAxes=1)
        pivotModeActive = mc.manipMoveContext('Move', q=1, editPivotMode=1)
        customModeActive = mc.manipMoveContext('Move', q=1, mode=1) / 6
    elif (
        currentCtx == "RotateSuperContext"
        or currentCtx == "manipRotateContext"
    ):
        customOri = mc.manipRotateContext('Rotate', q=1, orientAxes=1)
        pivotModeActive = mc.manipRotateContext('Rotate', q=1, editPivotMode=1)
        customModeActive = mc.manipRotateContext('Rotate', q=1, mode=1) / 3
    elif (
        currentCtx == "scaleSuperContext" or currentCtx == "manipScaleContext"
    ):
        customOri = mc.manipScaleContext('Scale', q=1, orientAxes=1)
        pivotModeActive = mc.manipScaleContext('Scale', q=1, editPivotMode=1)
        customModeActive = mc.manipScaleContext('Scale', q=1, mode=1) / 6

    if ori and not pos and not customModeActive:
        mc.error("m_bakeCustomToolPivot.kWrongAxisOriModeError")
        return None

    # Get custom orientation
    if ori and customModeActive:
        customOri[0] = mel.eval('rad_to_deg({})'.format(customOri[0]))
        customOri[1] = mel.eval('rad_to_deg({})'.format(customOri[1]))
        customOri[2] = mel.eval('rad_to_deg({})'.format(customOri[2]))
        # Set object(s) rotation to the custom one
        # (preserving child transform positions and geometry positions)
        mc.rotate(
            customOri[0], customOri[1], customOri[2],
            ob, a=1, pcp=1, pgp=1, ws=1, fo=1
        )

    if pos:
        # Get pivot in parent space
        # object = 'pSphere4'
        old = [0, 0, 0]
        m = mc.xform(ob, q=1, m=1)
        p = mc.xform(ob, q=1, os=1, sp=1)
        old[0] = (p[0] * m[0] + p[1] * m[4] + p[2] * m[8] + m[12])
        old[1] = (p[0] * m[1] + p[1] * m[5] + p[2] * m[9] + m[13])
        old[2] = (p[0] * m[2] + p[1] * m[6] + p[2] * m[10] + m[14])

        # Zero out pivots
        mc.xform(ob, zeroTransformPivots=1)

        # Translate object(s) back to previous pivot
        # (preserving child transform positions and geometry positions)
        new = mc.getAttr(ob + ".translate")[0]
        mc.move(
            (old[0] - new[0]),
            (old[1] - new[1]),
            (old[2] - new[2]),
            ob, pcp=1, pgp=1, ls=1, r=1
        )

    # Exit pivot mode
    if pivotModeActive:
        mel.eval('ctxEditMode;')

    # Set the axis orientation mode back to object
    if ori and customModeActive:
        if (
            currentCtx == "moveSuperContext"
            or currentCtx == "manipMoveContext"
        ):
            mc.manipMoveContext('Move', e=1, mode=0)
        elif (
            currentCtx == "RotateSuperContext"
            or currentCtx == "manipRotateContext"
        ):
            mc.manipRotateContext('Rotate', e=True, mode=0)
        elif (
            currentCtx == "scaleSuperContext"
            or currentCtx == "manipScaleContext"
        ):
            mc.manipScaleContext('Scale', e=1, mode=0)
