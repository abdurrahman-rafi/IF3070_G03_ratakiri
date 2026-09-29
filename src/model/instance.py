import json

#check
OUTSIDE = -1
#check


def load_instance(path):
    # baca file json
    # vehicles = {id: {w, l, fee, weight, eta}}
    # ships = {id: {w, l, capacity}}
    # cek: id vehicle tidak boleh duplikat, id ship tidak boleh duplikat dan tidak boleh OUTSIDE
    # ret vehicles, ships
    raise NotImplementedError


#check
def footprint(vehicle_info, orient):
    if orient == "H":
        return vehicle_info["w"], vehicle_info["l"]
    return vehicle_info["l"], vehicle_info["w"]
#check


def other_orient(orient):
    # H -> V, V -> H
    raise NotImplementedError


def fits(vehicle_info, orient, ship_info):
    # w, l = footprint(vehicle_info, orient)
    # ret w <= ship W and l <= ship L
    raise NotImplementedError
