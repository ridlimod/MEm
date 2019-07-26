import pymel.core as pym
import re


class PrjPathError(Exception):
    def __init__(self, path):
        msg = "Path: {0} not in project".format(path)
        super(Exception, self).__init__(msg)


class Sync(object):
    assetPatt = r"([A-Za-z0-9]+)_v([0-9]{2}).*"

    def __init__(self, src="G:/Mi Unidad"):
        self.__src__ = pym.Path(src)
        self.__prj__ = pym.workspace.path
        self.__baseFolders__ = [
            str(path.name)
            for path in self.__src__.listdir() if path.isdir()
        ]

    @property
    def base(self):
        return self.__baseFolders__

    def getLatest(self, src):
        print "DEBUG:", "latest:", src
        if type(src) == "str":
            src = pym.util.path(src)
        src = self.__src__ / self.__strip__(src)
        cont = src.parent
        name = str(src.name)
        assert cont.exists(), cont + " not exists in prj:" + self.__prj__
        oM = re.match(self.assetPatt, name)
        if oM:
            refName, refV = oM.groups()
            refV = int(refV)
            ext = src.splitext()[1]
            dynPatt = refName + r"_v([0-9]{2})_?.*" + ext
            latest = refV
            latestP = None
            for fn in (fn for fn in cont.listdir() if fn.isfile()):
                # print "DEBUG: read:", fn.name
                searchName = fn.name
                # print "DEBUG:", dynPatt, searchName
                rPatt = re.compile(dynPatt, re.UNICODE)
                iM = rPatt.match(searchName)
                if iM:
                    v = int(iM.groups()[0])
                    if v > latest:
                        latest = v
                        latestP = fn
            if latest != refV:
                return latestP
        print "DEBUG:", "latest:", "out:", src
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


if __name__ == "__main__":
    syncReferences()
