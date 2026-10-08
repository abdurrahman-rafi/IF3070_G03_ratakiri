from ..model.instance import OUTSIDE, footprint, other_orient, fits

# Bobot peluang tiap jenis move di random_neighbor. Bobot 0 berarti move dimatikan,
# baik di random_neighbor maupun all_neighbors. "remove" mati karena bukan salah satu
# dari tiga langkah neighbor di spesifikasi (swap, pindah koordinat, ubah orientasi).
MOVE_WEIGHTS = {"swap": 0.4, "relocate": 0.4, "rotate": 0.2, "remove": 0.0}


# Mengeluarkan satu vehicle dari ship: ship jadi OUTSIDE, x dan y jadi None.
# Masukan : state, vid. Keluaran: state baru (state asal tidak diubah).
def remove_from_ship(state, vid):
    new = state.copy()
    new.placement[vid].update(ship=OUTSIDE, x=None, y=None)
    return new


# Menukar (ship, x, y) dua vehicle; orient tetap milik masing-masing.
# Kalau salah satunya OUTSIDE, yang di luar masuk dan yang di dalam keluar.
# Dua posisi dibaca dulu, baru ditulis, supaya tidak saling timpa.
# Masukan : state, vid a, vid b. Keluaran: state baru, boleh tidak feasible.
def swap_move(state, a, b):
    new = state.copy()
    pa, pb = new.placement[a], new.placement[b]
    a_pos = (pa["ship"], pa["x"], pa["y"])
    b_pos = (pb["ship"], pb["x"], pb["y"])
    pa["ship"], pa["x"], pa["y"] = b_pos
    pb["ship"], pb["x"], pb["y"] = a_pos
    return new


# Mengubah orientasi satu vehicle (H <-> V). w dan l asli tidak diubah,
# titik kiri bawah tetap di tempat.
# Masukan : state, vid. Keluaran: state baru, boleh tidak feasible.
def rotate_move(state, vid):
    new = state.copy()
    new.placement[vid]["orient"] = other_orient(new.placement[vid]["orient"])
    return new


# Memindahkan satu vehicle ke (ship, x, y): dari luar ke dalam, antar ship,
# atau ke koordinat lain di ship yang sama.
# Masukan : state, vid, ship, x, y. Keluaran: state baru, boleh overlap atau overweight.
def place_move(state, vid, ship, x, y):
    new = state.copy()
    new.placement[vid].update(ship=ship, x=x, y=y)
    return new


# Keluaran: list (x, y) yang bisa ditempati vid di ship dengan orient sekarang, yaitu
# x in [1, W - w + 1] dan y in [1, L - l + 1], tanpa posisi sekarang.
# Opsi yang keluar geladak tidak pernah dibuat; overlap sengaja tidak disaring
# karena state yang overlap cukup bernilai 0.
def relocate_positions(state, vid, ship):
    p = state.placement[vid]
    ship_info = state.ships[ship]
    if not fits(state.vehicles[vid], p["orient"], ship_info):
        return []
    w, l = footprint(state.vehicles[vid], p["orient"])
    return [(x, y)
            for x in range(1, ship_info["w"] - w + 2)
            for y in range(1, ship_info["l"] - l + 2)
            if (ship, x, y) != (p["ship"], p["x"], p["y"])]


# Keluaran: list vid placed yang w != l.
# Rotasi vehicle persegi (w == l) tidak mengubah apa-apa, jadi opsinya dibuang.
def rotatable_vehicles(state):
    return [vid for vid in state.placed_vehicles() if state.vehicles[vid]["w"] != state.vehicles[vid]["l"]]


# Memilih satu vehicle placed secara random untuk dikeluarkan.
# Keluaran: (vid,), atau None kalau tidak ada vehicle placed.
def pick_remove(state, rng):
    placed = state.placed_vehicles()
    if not placed:
        return None
    return (rng.choice(placed),)


# Memilih pasangan vehicle random untuk di-swap.
# a selalu vehicle placed, karena swap dua vehicle yang sama-sama OUTSIDE tidak mengubah state.
# Keluaran: (a, b), atau None kalau tidak ada vehicle placed atau vehicle kurang dari dua.
def pick_swap(state, rng):
    placed = state.placed_vehicles()
    if not placed or len(state.order) < 2:
        return None
    a = rng.choice(placed)
    b = rng.choice([vid for vid in state.order if vid != a])
    return a, b


# Memilih satu vehicle random yang bisa dirotasi.
# Keluaran: (vid,), atau None kalau tidak ada kandidat.
def pick_rotate(state, rng):
    candidates = rotatable_vehicles(state)
    if not candidates:
        return None
    return (rng.choice(candidates),)


# Memilih vid, ship, dan posisi baru secara random.
# Kandidat = pasangan (vid, ship) yang punya minimal satu posisi selain posisi sekarang.
# Keluaran: (vid, ship, x, y), atau None kalau tidak ada kandidat.
def pick_relocate(state, rng):
    candidates = [(vid, ship) for vid in state.order for ship in state.ships
                  if relocate_positions(state, vid, ship)]
    if not candidates:
        return None
    vid, ship = rng.choice(candidates)
    x, y = rng.choice(relocate_positions(state, vid, ship))
    return vid, ship, x, y


PICKERS = {"swap": pick_swap, "relocate": pick_relocate, "rotate": pick_rotate, "remove": pick_remove}
APPLIERS = {"swap": swap_move, "relocate": place_move, "rotate": rotate_move, "remove": remove_from_ship}


# Keluaran: satu neighbor random, atau None kalau tidak ada move yang mungkin.
# Jenis move dipilih dulu sesuai MOVE_WEIGHTS, lalu detailnya dipilih fungsi pick_.
# Kalau satu jenis move tidak punya pilihan, jenis itu dicoret dan jenis lain dicoba.
# Neighbor tidak disaring: yang melanggar constraint tetap dikembalikan dan bernilai 0.
def random_neighbor(state, rng):
    types = [t for t in MOVE_WEIGHTS if MOVE_WEIGHTS[t] > 0]
    while types:
        move_type = rng.choices(types, weights=[MOVE_WEIGHTS[t] for t in types])[0]
        args = PICKERS[move_type](state, rng)
        if args is not None:
            return APPLIERS[move_type](state, *args)
        types.remove(move_type)
    return None


# Generator semua neighbor sebagai (deskripsi move, state baru), termasuk yang tidak feasible.
# Hanya move type dengan MOVE_WEIGHTS > 0; pakai yield supaya tidak semua neighbor disimpan sekaligus.
#   rotate   : tiap vehicle placed yang w != l
#   relocate : tiap vid x tiap ship x tiap posisi, tanpa posisi sekarang
#   swap     : tiap pasangan (a, b) dengan i < j, dilewati kalau dua-duanya OUTSIDE
#   remove   : tiap vehicle placed
def all_neighbors(state):
    if MOVE_WEIGHTS["rotate"] > 0:
        for vid in rotatable_vehicles(state):
            yield ("rotate", vid), rotate_move(state, vid)

    if MOVE_WEIGHTS["relocate"] > 0:
        for vid in state.order:
            for ship in state.ships:
                for x, y in relocate_positions(state, vid, ship):
                    yield ("relocate", vid, ship, x, y), place_move(state, vid, ship, x, y)

    if MOVE_WEIGHTS["swap"] > 0:
        for i, a in enumerate(state.order):
            for b in state.order[i + 1:]:
                if state.placement[a]["ship"] == OUTSIDE and state.placement[b]["ship"] == OUTSIDE:
                    continue
                yield ("swap", a, b), swap_move(state, a, b)

    if MOVE_WEIGHTS["remove"] > 0:
        for vid in state.placed_vehicles():
            yield ("remove", vid), remove_from_ship(state, vid)
