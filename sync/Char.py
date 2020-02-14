import re
import sync
import os
from shutil import copy
reload(sync)


class CharMan(object):
    def __init__(
        self,
        facts=None
    ):
        if facts is None:
            import facts
            reload(facts)
            self.__facts__ = facts.facts
        else:
            self.__facts__ = facts
        self.__src__ = os.path.join(
            self.__facts__["src"], self.__facts__["CH_ASSETS_FOLDER"]
        )
        self.__tgt__ = os.path.join(
            self.__facts__["tgt"], self.__facts__["CH_ASSETS_FOLDER"]
        )
        self.__folderre__ = self.__facts__["CH_FOLDER_RE"]
        self.__foldertpl__ = self.__facts__["CH_FOLDER_TPL"]
        self.__filere__ = self.__facts__["CH_FILE_RE"]
        self.__filetpl__ = self.__facts__["CH_FILE_TPL"]

    def list(self, local=False):
        src = local and self.__tgt__ or self.__src__
        for e in os.listdir(src):
            oM = re.match(self.__folderre__, e)
            if oM:
                yield oM.groupdict()["name"]

    def __getitem__(self, name):
        return Char(name)

    def __iter__(self):
        for e in self.list():
            yield Char(e)

    @property
    def facts(self):
        return self.__facts__

    @property
    def src(self):
        return self.__src__

    @property
    def tgt(self):
        return self.__tgt__


class CharInvalidName(Exception):
    pass


class Char(object):
    def __init__(
        self,
        name,
        version=1,
        fpath=None,
        charMan=None
    ):
        if charMan is None:
            oCM = CharMan()
            self.__facts__ = oCM.facts
            self.__src__ = oCM.src
            self.__tgt__ = oCM.tgt
        else:
            self.__facts__ = charMan.facts
            self.__src__ = charMan.src
            self.__tgt__ = charMan.tgt

        folder = self.__folder__(name)
        basename = self.__basename__(name, version)
        if (
            re.match(self.__facts__["CH_FOLDER_RE"], folder)
            and re.match(self.__facts__["CH_FILE_RE"], basename)
        ):
            self.__name__ = name
            self.__version__ = version
        else:
            raise CharInvalidName()

        if fpath is None:
            self.fpath = os.path.join(
                self.__src__,
                self.__folder__(self.__name__),
                self.__basename__(self.__name__, self.__version__)
            )
        else:
            self.__fpath__ = fpath

    def getLatest(self):
        # print "DEBUG:", fpath
        latest = sync.Sync().getLatest(self.fpath)
        oM = re.match(self.__facts__["CH_FILE_RE"], latest.basename())
        if oM:
            dM = oM.groupdict()
            version = int(dM["version"])
            if version != self.__version__:
                return Char(self.__name__, version, latest)
            else:
                self.__fpath__ = latest
                return self

    def __folder__(self, name):
        return self.__facts__["CH_FOLDER_TPL"].format(name=name)

    def __basename__(self, name, version):
        return self.__facts__["CH_FILE_TPL"].format(
            name=name, version=version
        )

    def __str__(self):
        return self.__name__

    def __repr__(self):
        return "Char<\"{0}_v{1:0>2}\">".format(self.__name__, self.__version__)

    def getPath(self, local=False):
        if local:
            fpath = os.path.relpath(self.__fpath__, self.__src__)
            fpath = os.path.join(self.__tgt__, fpath)
        else:
            fpath = self.__fpath__
        return fpath

    def get(self):
        ftgt = self.getPath(local=True)
        fsrc = self.__fpath__
        folder = os.path.dirname(ftgt)
        if not os.path.exists(folder):
            os.makedirs(folder)
        copy(fsrc, ftgt)


if __name__ == "__main__":
    oChar = CharMan()
    print "\n".join(oChar.list())
