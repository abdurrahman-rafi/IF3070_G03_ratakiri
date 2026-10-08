import json

OUTSIDE = -1


# Membaca file json instance permasalahan.
# Masukan : path file json yang berisi list "ships" dan "vehicles".
# Keluaran: (vehicles, ships)
#   vehicles = {id: {w, l, fee, weight, eta}}
#   ships    = {id: {w, l, capacity}}
# Dua-duanya statis: di-share ke semua state dan tidak pernah diubah algoritma.
# Id vehicle tidak boleh duplikat, id ship tidak boleh duplikat dan tidak boleh OUTSIDE.
def load_instance(path):
    with open(path, encoding="utf-8") as instance_file:
        data = json.load(instance_file)

    vehicles = {}
    for vehicle in data["vehicles"]:
        if vehicle["id"] in vehicles:
            raise ValueError(f"id vehicle duplikat: {vehicle['id']}")
        vehicles[vehicle["id"]] = {key: vehicle[key] for key in ("w", "l", "fee", "weight", "eta")}

    ships = {}
    for ship in data["ships"]:
        if ship["id"] == OUTSIDE or ship["id"] in ships:
            raise ValueError(f"id ship duplikat atau sama dengan OUTSIDE: {ship['id']}")
        ships[ship["id"]] = {key: ship[key] for key in ("w", "l", "capacity")}

    return vehicles, ships


# Ukuran (w, l) vehicle sesuai orientasinya: "H" pakai (w, l) apa adanya, "V" ditukar.
# Ukuran asli vehicle tidak pernah diubah, rotasi cukup mengganti orient.
# Titik acuan tetap di kiri bawah karena hasil rotasi pasti tetap persegi panjang.
def footprint(vehicle_info, orient):
    if orient == "H":
        return vehicle_info["w"], vehicle_info["l"]
    return vehicle_info["l"], vehicle_info["w"]


# Orientasi kebalikan: H -> V, V -> H.
def other_orient(orient):
    if orient == "H":
        return "V"
    return "H"


# Cek apakah vehicle dengan orientasi tertentu muat di geladak ship, tanpa melihat vehicle lain.
# Keluaran: True kalau w <= W ship dan l <= L ship.
def fits(vehicle_info, orient, ship_info):
    w, l = footprint(vehicle_info, orient)
    return w <= ship_info["w"] and l <= ship_info["l"]
