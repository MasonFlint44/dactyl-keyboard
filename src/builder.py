from numpy import pi

from clusters.default_cluster import DefaultCluster

debug_exports = False
debug_trace = False


def deg2rad(degrees: float) -> float:
    return degrees * pi / 180


def rad2deg(rad: float) -> float:
    return rad * 180 / pi


def debugprint(info):
    if debug_trace:
        print(info)


class Builder:
    column_style = "asymetric"
    centerrow = 3
    lastrow = 4
    cornerrow = 3
    lastcol = 5

    def __init__(self, parent_locals):
        # TODO: don't use globals
        for item in parent_locals:
            globals()[item] = parent_locals[item]
        cluster = DefaultCluster(parent_locals)
        origin = cluster.thumborigin()
        print("Locals imported")
        print(parent_locals["thumb_style"])


print("It built!")
