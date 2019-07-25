def isQuoted(attr):
    if attr.startswith("\"") and attr.endswith("\""):
        return True


def deenvelop(attr):
    envelop = ["", ""]
    if isQuoted(attr):
        envelop = ["\"", "\""]
        attr = attr.strip("\"")
    if attr.endswith("]"):
        attr, elems = attr.split("[", 1)
        elems = "[" + elems
        envelop[1] = elems + envelop[1]
    return attr, envelop


def reenvelop(attr, envelop):
    return envelop[0] + attr + envelop[1]


if __name__ == "__main__":
    attr = "\"asasd.asdasd[1:3][2,3]\""
    attr, envelop = deenvelop(attr)
    print attr, envelop, reenvelop(attr, envelop)
    attr = "asasd.asdasd[1:3][2,3]"
    attr, envelop = deenvelop(attr)
    print attr, envelop, reenvelop(attr, envelop)
    attr = "asasd.asdasd"
    attr, envelop = deenvelop(attr)
    print attr, envelop, reenvelop(attr, envelop)
