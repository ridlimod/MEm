from oiio_wrap import compare
from fnmatch import fnmatch
import os


texturefilters = ["*.tif"]


def compareFolders(A, B):
    filesA = (
        f for f in os.listdir(A)
        if any(map(lambda x: fnmatch(f, x), texturefilters))
    )

    for f in filesA:
        src = os.path.join(A, f)
        tgt = os.path.join(B, f)
        if os.path.exists(tgt):
            yield (src, tgt, compare(src, tgt))
        else:
            yield (src, None, None)


if __name__ == "__main__":
    A = (
        r"E:\FreeLanceWork\Genoma\PRJ_FLOWER\033_IN_shaders"
        r"\EMILIO_2019-08-08_storkShades\Stork V03\_maps"
    )
    B = (
        r"E:\FreeLanceWork\Genoma\PRJ_FLOWER\031_IN_modelers"
        r"\EMILIO_2019_05_27_stork_v03\_maps"
    )

    B = (
        r"E:\FreeLanceWork\Genoma\PRJ_FLOWER\210_ASSETS_CH\CH_stork\_maps"
    )

    for src, tgt, diff in compareFolders(A, B):
        print os.path.basename(src), os.path.basename(tgt), diff
