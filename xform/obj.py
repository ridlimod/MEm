import pymel.core as pym


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
