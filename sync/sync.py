import pymel.core as pym
import re
import facts
reload(facts)


class PrjPathError(Exception):
    def __init__(self, path):
        msg = "Path: {0} not in project".format(path)
        super(Exception, self).__init__(msg)


class Sync(object):
    assetPatt = r"([A-Za-z0-9]+)_v([0-9]{2}).*"

    def __init__(self, src=facts.facts["src"]):
        self.__src__ = pym.Path(src)
        self.__prj__ = pym.workspace.path
        self.__baseFolders__ = [
            str(path.name)
            for path in self.__src__.listdir() if path.isdir()
        ]

    @property
    def base(self):
        return self.__baseFolders__

    def getLatest(self, src, local=False):
        # print "DEBUG:", "latest:", src
        base = local and self.__prj__ or self.__src__
        src = pym.util.path(src)
        src = base / self.__strip__(src)
        cont = src.parent
        name = str(src.name)
        assert cont.exists(), cont + " not exists in prj:" + self.__prj__
        oM = re.match(self.assetPatt, name)
        if oM:
            refName, refV = oM.groups()
            refV = int(refV)
            ext = src.splitext()[1]
            dynPatt = refName + r"_v([0-9]{2}).*?" + ext
            latest = 0
            latestP = None
            rPatt = re.compile(dynPatt, re.UNICODE)
            for fn in (fn for fn in cont.listdir() if fn.isfile()):
                searchName = fn.name
                iM = rPatt.match(searchName)
                if iM:
                    v = int(iM.groups()[0])
                    if not latestP:
                        latestP = fn
                    if v >= latest:
                        latest = v
                        latestP = fn
            if latestP:
                return latestP

        raise PrjPathError(src)

    def copyRef(self, path):
        relPath = self.__strip__(pym.util.path(path))
        src = self.__src__ / relPath
        src = (src.exists() and src) or self.getLatest(src)
        print src
        if src.exists():
            dst = self.__prj__ / self.__strip__(src)
            dstCont = dst.parent
            dstCont.makedirs_p()
            pym.util.path.copy(src, dst)
            return self.__strip__(dst)

    def local_exists(self, path):
        path = self.__strip__(pym.util.path(path))
        return (self.__prj__ / path).exists()

    def remote_exists(self, path):
        path = self.__strip__(pym.util.path(path))
        return (self.__src__ / path).exists()

    def __strip__(self, path):
        parts = path.splitall()
        i = 0
        while i != len(parts):
            if parts[i] in self.__baseFolders__:
                return pym.util.path("/".join(parts[i:]))
            i += 1

        raise PrjPathError(path)

    def strip(self, path):
        return self.__strip__(path)


def setLatestLocal(filter=[]):
    oSync = Sync()
    for FR in pym.system.iterReferences():
        if FR not in filter:
            src = oSync.getLatest(FR.path, local=True)
            print "DEBUG:", src, FR.path
            if src.canonicalpath() != FR.path.canonicalpath():
                FR.replaceWith(oSync.strip(src))


def syncReferences():
    oSync = Sync()
    for FR in pym.system.iterReferences():
        print "searching for", FR.path
        if not oSync.remote_exists(FR.path):
            src = oSync.getLatest(FR.path)
            print "Latest:", src
        else:
            src = FR.path
        if oSync.local_exists(src):
            print "Exists", src
            if not FR.path.samepath(src):
                FR.replaceWith(oSync.strip(src))
        else:
            print "Copying...", src
            reffile = oSync.copyRef(src)
            FR.replaceWith(reffile)


def syncTextures(error=False):
    oSync = Sync()
    for fn in pym.ls(type="file"):
        ftn = fn.fileTextureName.get()
        try:
            exists = oSync.local_exists(ftn)
        except Exception as e:
            if error:
                print "Raise:", e
                raise e
            else:
                print "Error:", e
                print "Skip"
                continue

        if not exists:
            print "Copying...", ftn
            try:
                sftn = oSync.copyRef(ftn)
            except Exception as e:
                if error:
                    print "Raise:", e
                    raise e
                else:
                    print "Error:", e
                    print "Skip"
                    continue

            fn.fileTextureName.set(sftn)


def syncAudios():
    oSync = Sync()
    for fn in pym.ls(type="audio"):
        ftn = fn.filename.get()
        if not oSync.local_exists(ftn):
            print "Copying...", ftn
            sftn = oSync.copyRef(ftn)
            fn.filename.set(sftn)


def syncAll():
    syncReferences()
    syncTextures()
    syncAudios()


def allTexturesToRelative():
    oSync = Sync()
    prjpath = pym.workspace.path
    notfound = []
    for filenode in pym.ls(type="file"):
        if filenode.hasAttr("fileTextureName"):
            path = pym.Path(filenode.fileTextureName.get())
            if not path.startswith(prjpath):
                if oSync.local_exists(path):
                    filenode.fileTextureName.set(oSync.strip(path))
                elif oSync.remote_exists(path):
                    path = oSync.copyRef(path)
                    filenode.fileTextureName.set(oSync.strip(path))
                else:
                    newpath = oSync.getLatest(path)
                    if newpath:
                        filenode.fileTextureName.set(oSync.strip(newpath))
                    else:
                        notfound.append(filenode, path)
    return notfound


if __name__ == "__main__":
    syncReferences()
