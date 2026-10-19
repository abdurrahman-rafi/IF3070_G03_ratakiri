from ..model.instance import OUTSIDE, footprint, other_orient, fits

# Bobot peluang tiap jenis move di random_neighbor, sesuai tiga langkah neighbor di spesifikasi
# (swap, pindah koordinat, ubah orientasi).
MOVE_WEIGHTS = {"swap": 0.4, "relocate": 0.4, "rotate": 0.2}


# Menukar (ship, x, y) dua vehicle, orient tetap milik masing-masing.
# Kalau salah satunya OUTSIDE, yang di luar masuk dan yang di dalam keluar.
# Dua posisi dibaca dulu, baru ditulis, supaya tidak saling timpa.
# Input state dan dua vid, output state baru yang boleh tidak feasible.
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
# Input state dan vid, output state baru yang boleh tidak feasible.
def rotate_move(state, vid):
    new = state.copy()
    new.placement[vid]["orient"] = other_orient(new.placement[vid]["orient"])
    return new


# Memindahkan satu vehicle ke (ship, x, y): dari luar ke dalam, antar ship,
# atau ke koordinat lain di ship yang sama.
# Input state, vid, ship, x, y, output state baru yang boleh overlap atau overweight.
def place_move(state, vid, ship, x, y):
    new = state.copy()
    new.placement[vid].update(ship=ship, x=x, y=y)
    return new


# Semua posisi (x, y) yang bisa ditempati vid di ship dengan orient sekarang, yaitu
# x in [1, W - w + 1] dan y in [1, L - l + 1], tanpa posisi sekarang.
# Opsi yang keluar deck tidak pernah dibuat. Overlap sengaja tidak disaring
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


# Daftar vid placed yang w != l.
# Rotasi vehicle persegi (w == l) tidak mengubah apa-apa, jadi opsinya dibuang.
def rotatable_vehicles(state):
    return [vid for vid in state.placed_vehicles() if state.vehicles[vid]["w"] != state.vehicles[vid]["l"]]


# Memilih pasangan vehicle random untuk di-swap.
# a selalu vehicle placed, karena swap dua vehicle yang sama-sama OUTSIDE tidak mengubah state.
# Output (a, b), atau None kalau tidak ada vehicle placed atau vehicle kurang dari dua.
def pick_swap(state, rng):
    placed = state.placed_vehicles()
    if not placed or len(state.order) < 2:
        return None
    a = rng.choice(placed)
    b = rng.choice([vid for vid in state.order if vid != a])
    return a, b


# Memilih satu vehicle random yang bisa dirotasi.
# Output (vid,), atau None kalau tidak ada kandidat.
def pick_rotate(state, rng):
    candidates = rotatable_vehicles(state)
    if not candidates:
        return None
    return (rng.choice(candidates),)


# Memilih vid, ship, dan posisi baru secara random.
# Pasangan (vid, ship) diambil dari yang ukurannya muat, lalu x dan y diacak langsung.
# Kalau kebetulan sama dengan posisi sekarang, diacak ulang.
# Output (vid, ship, x, y), atau None kalau tidak ada vehicle yang muat di ship mana pun.
def pick_relocate(state, rng):
    pairs = [(vid, ship) for vid in state.order for ship in state.ships
             if fits(state.vehicles[vid], state.placement[vid]["orient"], state.ships[ship])]
    if not pairs:
        return None
    for _ in range(100):
        vid, ship = rng.choice(pairs)
        p = state.placement[vid]
        w, l = footprint(state.vehicles[vid], p["orient"])
        x = rng.randint(1, state.ships[ship]["w"] - w + 1)
        y = rng.randint(1, state.ships[ship]["l"] - l + 1)
        if (ship, x, y) != (p["ship"], p["x"], p["y"]):
            return vid, ship, x, y
    return None


PICKERS = {"swap": pick_swap, "relocate": pick_relocate, "rotate": pick_rotate}
APPLIERS = {"swap": swap_move, "relocate": place_move, "rotate": rotate_move}


# Satu neighbor random, atau None kalau tidak ada move yang mungkin.
# Jenis move dipilih dulu sesuai MOVE_WEIGHTS, lalu detailnya dipilih fungsi pick_.
# Kalau satu jenis move tidak punya pilihan, jenis itu dicoret dan jenis lain dicoba.
# Neighbor tidak disaring: yang melanggar constraint tetap dikembalikan dan bernilai 0.
def random_neighbor(state, rng):
    types = list(MOVE_WEIGHTS)
    while types:
        move_type = rng.choices(types, weights=[MOVE_WEIGHTS[t] for t in types])[0]
        args = PICKERS[move_type](state, rng)
        if args is not None:
            return APPLIERS[move_type](state, *args)
        types.remove(move_type)
    return None


# Generator semua neighbor sebagai (vid yang dipindah, state baru), termasuk yang tidak feasible.
# vid yang dipindah dipakai hill climbing supaya cukup mengecek vehicle itu saja.
#   rotate   : tiap vehicle placed yang w != l
#   relocate : tiap vid x tiap ship x tiap posisi, tanpa posisi sekarang
#   swap     : tiap pasangan (a, b) dengan i < j, dilewati kalau dua-duanya OUTSIDE
def all_neighbors(state):
    for vid in rotatable_vehicles(state):
        yield (vid,), rotate_move(state, vid)
    for vid in state.order:
        for ship in state.ships:
            for x, y in relocate_positions(state, vid, ship):
                yield (vid,), place_move(state, vid, ship, x, y)
    for i, a in enumerate(state.order):
        for b in state.order[i + 1:]:
            if state.placement[a]["ship"] != OUTSIDE or state.placement[b]["ship"] != OUTSIDE:
                yield (a, b), swap_move(state, a, b)
