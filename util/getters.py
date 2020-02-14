import pymel.core as pym


def findInNS(obj, NS="CHARS_C01", stripNamespace=True):
    lname = obj.name(long=True, stripNamespace=stripNamespace)[1:]
    sparts = map(
        lambda x: NS + "::" + x,
        lname.split("|")
    )
    parts = []
    while sparts:
        parts.insert(0, sparts.pop())
        search = "|".join(parts)
        print "search:", search
        el = pym.ls(search)
        if el and len(el) == 1:
            return el
    return None
