from .instance import footprint


# tidak boleh ada bagian satu kendaraan yang ada diluar kapal
def out_of_bounds_penalty(state):
    # penalty = 0
    # for every vehicle v in state.placed_vehicles()
    #     w, l = footprint(v, orient)
    #     if x + w - 1 > ship W or y + l - 1 > ship L
    #         penalty = penalty + v.fee * 1.5
    # ret penalty
    raise NotImplementedError


# tidak boleh ada yang overlap
def overlap_penalty(state):
    # penalty = 0
    # placed = state.placed_vehicles()
    # for i in range(len(placed))
    #     for j in range(i + 1, len(placed))
    #         a, b = placed[i], placed[j]
    #         if a.ship != b.ship
    #             continue
    #         aw, al = footprint(a) ; bw, bl = footprint(b)
    #         x_overlap = (a.x < b.x + bw) and (b.x < a.x + aw)
    #         y_overlap = (a.y < b.y + bl) and (b.y < a.y + al)
    #         if x_overlap and y_overlap
    #             penalty = penalty + 1.5 * (a.fee + b.fee)
    # ret penalty
    raise NotImplementedError


# tidak boleh total weight melebihi
def weight_penalty(state):
    # factor = 1.5 * max(fee / weight) dari semua vehicle
    # load = {ship_id: 0}
    # for every vehicle v in state.placed_vehicles()
    #     load[v.ship] += v.weight
    # penalty = 0
    # for every ship
    #     excess = load[ship] - ship.capacity
    #     if excess > 0
    #         penalty = penalty + factor * excess
    # ret penalty
    raise NotImplementedError


def total_penalty(state):
    # ret out_of_bounds_penalty + overlap_penalty + weight_penalty
    raise NotImplementedError


def is_feasible(state):
    # ret total_penalty(state) == 0
    raise NotImplementedError
