import pymel.core as pym


class Cache(object):
    def __init__(self, type="CHAR"):
        if type == "CHAR":
            self.job = (
                "-frameRange {start} {end} "
                "-ro -stripNamespaces -uvWrite "
                "-writeVisibility -dataFormat ogawa "
                "-root {rootObj} "
                "-file {filepath}"
            )

    def mkChar(self, rootObj, filepath, start=None, end=None):
        if start is None:
            start = pym.playbackOptions(ast=True, q=True)
        if end is None:
            end = pym.playbackOptions(aet=True, q=True)

        job = self.job.format(
            start=start, end=end, rootObj=rootObj, filepath=filepath
        )

        pym.AbcExport(j=job)
