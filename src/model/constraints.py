from .instance import footprint


# Cek apakah dua persegi panjang di grid beririsan.
# Masukan : (x, y) sel kiri bawah (mulai dari 1) dan ukuran (w, l) masing-masing.
# Keluaran: True kalau overlap di sumbu x dan sumbu y sekaligus.
# Dua vehicle yang hanya bersentuhan sisi tidak dihitung overlap.
def rectangles_overlap(ax, ay, aw, al, bx, by, bw, bl):
    x_overlap = (ax < bx + bw) and (bx < ax + aw)
    y_overlap = (ay < by + bl) and (by < ay + al)
    return x_overlap and y_overlap


# Cek apakah satu vehicle boleh ditaruh di (ship, x, y, orient) tanpa melanggar constraint,
# dengan menganggap posisi vehicle itu sendiri sekarang kosong.
# Yang dicek: di dalam deck, capacity ship tidak terlewati, tidak overlap dengan vehicle lain.
# Berat dan overlap dicek dalam satu loop atas vehicle lain di ship yang sama.
# Dipakai initial_state, hill climbing, dan repair GA.
def can_place(state, vid, ship, x, y, orient):
    ship_info = state.ships[ship]
    w, l = footprint(state.vehicles[vid], orient)
    if x < 1 or y < 1 or x + w - 1 > ship_info["w"] or y + l - 1 > ship_info["l"]:
        return False
    load = state.vehicles[vid]["weight"]
    for other in state.order:
        p = state.placement[other]
        if other == vid or p["ship"] != ship:
            continue
        load += state.vehicles[other]["weight"]
        ow, ol = footprint(state.vehicles[other], p["orient"])
        if rectangles_overlap(x, y, w, l, p["x"], p["y"], ow, ol):
            return False
    return load <= ship_info["capacity"]


# tidak boleh ada bagian satu kendaraan yang ada diluar kapal
# Keluaran: True kalau ada vehicle placed yang x + w - 1 > W ship atau y + l - 1 > L ship
# (atau x, y < 1).
def has_out_of_bounds(state):
    for vid in state.placed_vehicles():
        p = state.placement[vid]
        ship_info = state.ships[p["ship"]]
        w, l = footprint(state.vehicles[vid], p["orient"])
        if p["x"] < 1 or p["y"] < 1 or p["x"] + w - 1 > ship_info["w"] or p["y"] + l - 1 > ship_info["l"]:
            return True
    return False


# tidak boleh ada yang overlap
# Keluaran: True kalau ada dua vehicle di ship yang sama yang overlap.
# Tiap pasangan dicek sekali (j mulai dari i + 1); vehicle di ship berbeda dilewati.
def has_overlap(state):
    placed = state.placed_vehicles()
    for i in range(len(placed)):
        for j in range(i + 1, len(placed)):
            a, b = state.placement[placed[i]], state.placement[placed[j]]
            if a["ship"] != b["ship"]:
                continue
            aw, al = footprint(state.vehicles[placed[i]], a["orient"])
            bw, bl = footprint(state.vehicles[placed[j]], b["orient"])
            if rectangles_overlap(a["x"], a["y"], aw, al, b["x"], b["y"], bw, bl):
                return True
    return False


# tidak boleh total weight melebihi
# Keluaran: True kalau total weight vehicle placed di salah satu ship > capacity ship itu.
def is_overweight(state):
    for ship, ship_info in state.ships.items():
        if state.ship_load(ship) > ship_info["capacity"]:
            return True
    return False


# Keluaran: True kalau state tidak melanggar satu pun dari tiga constraint di atas.
# Draft awal memakai penalty per constraint (fee * 1.5 dst.); sekarang cukup feasible atau tidak,
# karena state yang melanggar langsung bernilai 0 di evaluate.
def is_feasible(state):
    return not (has_out_of_bounds(state) or has_overlap(state) or is_overweight(state))
