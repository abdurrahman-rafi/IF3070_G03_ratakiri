from ..model.instance import OUTSIDE, footprint, other_orient, fits

#check
MOVE_WEIGHTS = {"swap": 0.4, "relocate": 0.4, "rotate": 0.2, "remove": 0.0}
#check


def remove_from_ship(state, vid):
    # new = state.copy()
    # new.placement[vid] = ship OUTSIDE, x None, y None
    # ret new
    raise NotImplementedError


def swap_move(state, a, b):
    # new = state.copy()
    # a_pos = (a.ship, a.x, a.y)
    # b_pos = (b.ship, b.x, b.y)      (baca dua-duanya dulu, baru tulis)
    # a.ship, a.x, a.y = b_pos
    # b.ship, b.x, b.y = a_pos
    # ret new
    raise NotImplementedError


def rotate_move(state, vid):
    # new = state.copy()
    # new.placement[vid].orient = other_orient(orient)   (w dan l tidak diubah)
    # ret new
    raise NotImplementedError


def place_move(state, vid, ship, x, y):
    # new = state.copy()
    # new.placement[vid] = ship, x, y
    # ret new
    raise NotImplementedError


def pick_remove(state, rng):
    # placed = state.placed_vehicles()
    # kalau kosong ret None
    # ret (rng.choice(placed),)
    raise NotImplementedError


def pick_swap(state, rng):
    # placed = state.placed_vehicles()
    # kalau kosong ret None
    # a = rng.choice(placed)
    # b = rng.choice(semua vid selain a)
    # ret a, b
    raise NotImplementedError


def pick_rotate(state, rng):
    # candidates = vehicle placed yang w != l
    # kalau kosong ret None
    # ret (rng.choice(candidates),)
    raise NotImplementedError


def pick_relocate(state, rng):
    # candidates = (vid, ships yang fits dengan orient sekarang), buang vid tanpa ship
    # kalau kosong ret None
    # pilih vid dan ship random
    # w, l = footprint(vid, orient)
    # max_x, max_y = W - w + 1, L - l + 1
    # kalau cuma ada 1 posisi dan itu posisi sekarang -> ret None
    # random x in [1, max_x], y in [1, max_y] sampai beda dari posisi sekarang
    # ret vid, ship, x, y
    raise NotImplementedError


PICKERS = {"swap": pick_swap, "relocate": pick_relocate, "rotate": pick_rotate, "remove": pick_remove}
APPLIERS = {"swap": swap_move, "relocate": place_move, "rotate": rotate_move, "remove": remove_from_ship}


#check
def random_neighbor(state, rng):
    types = [t for t in MOVE_WEIGHTS if MOVE_WEIGHTS[t] > 0]
    while types:
        move_type = rng.choices(types, weights=[MOVE_WEIGHTS[t] for t in types])[0]
        args = PICKERS[move_type](state, rng)
        if args is not None:
            return APPLIERS[move_type](state, *args)
        types.remove(move_type)
    return None
#check


def all_neighbors(state):
    # hanya move type dengan MOVE_WEIGHTS > 0, pakai yield (generator)
    # rotate   : tiap vehicle placed yang w != l -> yield ("rotate", vid), rotate_move(...)
    # relocate : tiap vid x tiap ship x tiap x in [1, W-w+1] x tiap y in [1, L-l+1],
    #            skip posisi sekarang -> yield ("relocate", vid, ship, x, y), place_move(...)
    # swap     : tiap pasangan (a, b) dengan i < j, skip kalau dua-duanya OUTSIDE
    #            -> yield ("swap", a, b), swap_move(...)
    # remove   : tiap vehicle placed -> yield ("remove", vid), remove_from_ship(...)
    raise NotImplementedError
