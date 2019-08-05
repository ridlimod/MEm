import subprocess as subp
import os


OIIO_BINS = os.path.normpath(
    "E:/MayaDev/MEm/textures/staticBins/oiio-1.5.0/bin"
)
DEFAULTCHANNELS = ["R", "G", "B"]

oiio = [
    "oiiotool",
    "iinfo",
]

oiio = dict(map(lambda x: (x, os.path.join(OIIO_BINS, x)), oiio))
# def oiio(oiiofn):
#     def oiiopath(*args, **kwargs):
#         args[0] = os.path.join(OIIO_BINS, args[0])


def shuffle(input, output=None, channels=DEFAULTCHANNELS):
    cmd = [oiio["oiiotool"]]
    cmd.append(input)
    cmd.extend(["-ch", ",".join(channels)])
    cmd.extend(["-o", output or input])

    print " ".join(cmd)
    rc = subp.call(cmd, shell=False, stderr=subp.PIPE)
    print rc


def info(input):
    cmd = [oiio["iinfo"]]
    cmd.append(input)

    rc = subp.check_output(cmd, shell=False, stderr=subp.PIPE)
    return rc


if __name__ == "__main__":
    prj = "e:/freelancework/genoma/prj_flower/"
    maps = prj + "210_assets_ch/ch_lilli/_maps"
    # input = prj + "210_assets_ch/ch_lilli/_maps/lilli_body_bump_tx.tif"
    # maps = prj + "220_assets_set/set_conservaench/_maps"
    # maps = prj + "210_assets_ch/ch_sinistra/_maps"
    # maps = prj + "210_assets_ch/ch_gabybird/_maps"
    # shuffle(input, channels=["A", "A", "A"])
    # print info(input)
    for d, ds, fs in os.walk(maps):
        for f in fs:
            texture = os.path.normpath(os.path.join(d, f))
            if not texture.endswith(".ini"):
                if "1 channel" in info(texture):
                    print "convert:", texture
                    shuffle(texture, channels=["A", "A", "A"])
