from .instance import OUTSIDE, footprint, other_orient, fits
from ..moves import moves


class DockState:
    def __init__(self, vehicles, ships, placement):
        # self.vehicles = vehicles  (static, di-share, tidak pernah di copy)
        # self.ships = ships        (static)
        # self.placement = placement (dynamic: {vid: {ship, x, y, orient}})
        #check
        self.ship_options = list(ships) + [OUTSIDE]
        #check
        #check
        self.order = sorted(vehicles)
        #check

    @classmethod
    def initial_state(cls, vehicles, ships, rng):
        # state = cls(vehicles, ships, {})
        # for vid in state.order
        #     orient = rng.choice(H, V)
        #     ship = rng.choice(state.ship_options)
        #     x, y = None, None
        #     if ship != OUTSIDE
        #         kalau tidak fits(orient) coba other_orient(orient)
        #         kalau dua-duanya tidak fits -> ship = OUTSIDE
        #         else
        #             w, l = footprint(vehicle, orient)
        #             x = rng.randint(1, W - w + 1)
        #             y = rng.randint(1, L - l + 1)
        #     state.placement[vid] = {ship, x, y, orient}
        # ret state
        raise NotImplementedError

    def copy(self):
        #check
        new_placement = {vid: dict(p) for vid, p in self.placement.items()}
        #check
        # new = DockState baru, vehicles / ships / ship_options / order di-share
        # new.placement = new_placement
        # ret new
        raise NotImplementedError

    def placed_vehicles(self):
        # ret list vid (urut sesuai self.order) yang ship != OUTSIDE
        raise NotImplementedError

    def random_neighbor(self, rng):
        # ret moves.random_neighbor(self, rng)
        raise NotImplementedError

    def all_neighbors(self):
        # ret moves.all_neighbors(self)
        raise NotImplementedError

    def to_dict(self):
        # ret {vid: copy placement[vid]} untuk disimpan ke json
        raise NotImplementedError

    def build_grids(self):
        # per ship: grid numpy ukuran (L, W) isi -1
        # for idx, vid in enumerate(self.order) yang placed
        #     w, l = footprint(vehicle, orient)
        #     isi sel [y-1 : y-1+l, x-1 : x-1+w] dengan idx   (koordinat 1-indexed)
        # ret {ship_id: grid}
        raise NotImplementedError

    #check
    def to_chromosome(self):
        return [dict(self.placement[vid]) for vid in self.order]
    #check

    def from_chromosome(self, chromosome):
        # new = self.copy()
        # new.placement = {vid: copy gene} dengan zip(self.order, chromosome)
        # ret new
        raise NotImplementedError
