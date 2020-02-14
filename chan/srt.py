import pymel.core as pym


class srt(object):
    s = ["scaleX", "scaleY", "scaleZ"]
    r = ["rotateX", "rotateY", "rotateZ"]
    t = ["translateX", "translateY", "translateZ"]
    rt = r + t
    sr = s + r
    srt = s + r + t
    v = ["visibility"]
    all = s + r + t + v

    @classmethod
    def lockAttrs(cls, node, bPar, attrs=None):
        if attrs is None:
            attrs = cls.all
        for attr in attrs:
            if node.hasAttr(attr):
                oAttr = node.attr(attr)
                print "locking:", oAttr.name()
                oAttr.setLocked(bPar)

    @classmethod
    def keyAttrs(cls, node, bPar, attrs=None):
        if attrs is None:
            attrs = cls.all
        for attr in attrs:
            if node.hasAttr(attr):
                oAttr = node.attr(attr)
                print "locking:", oAttr.name()
                oAttr.setKeyable(bPar)

    @classmethod
    def getState(cls, node, attrs=None):
        if attrs is None:
            attrs = cls.all
        dState = {}
        for attr in attrs:
            if node.hasAttr(attr):
                oAttr = node.attr(attr)
                dState[attr] = [oAttr.isLocked(), oAttr.isKeyable()]
        return dState

    @classmethod
    def setState(cls, node, dState):
        for attr in dState:
            if node.hasAttr(attr):
                locked, keyable = dState[attr]
                oAttr = node.attr(attr)
                oAttr.setLocked(locked)
                oAttr.setKeyable(keyable)
