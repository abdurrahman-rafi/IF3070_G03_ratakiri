import numpy as np

from .instance import OUTSIDE, footprint, other_orient, fits
from .constraints import can_place
from ..moves import moves


class DockState:
    # Masukan:
    #   vehicles  = {vid: {w, l, fee, weight, eta}}  (static, di-share, tidak pernah di copy)
    #   ships     = {ship: {w, l, capacity}}         (static)
    #   placement = {vid: {ship, x, y, orient}}      (dynamic; ship OUTSIDE berarti x, y None)
    # ship_options = semua id ship + OUTSIDE, dipakai saat memilih ship secara random.
    # order = urutan vid yang tetap, supaya gen ke-i di GA selalu vehicle yang sama.
    def __init__(self, vehicles, ships, placement):
        self.vehicles = vehicles
        self.ships = ships
        self.placement = placement
        self.ship_options = list(ships) + [OUTSIDE]
        self.order = sorted(vehicles)

    # Membuat state awal random yang pasti feasible.
    # Tiap vehicle diberi orient random dan ship random (atau OUTSIDE). Kalau dapat ship:
    # orient yang tidak fits diganti other_orient, lalu x random di [1, W - w + 1] dan
    # y random di [1, L - l + 1] dicoba sampai max_attempts kali sampai lolos can_place.
    # Kalau tidak ada yang lolos, vehicle tetap OUTSIDE.
    # Masukan : vehicles, ships, rng (random.Random), max_attempts. Keluaran: DockState.
    @classmethod
    def initial_state(cls, vehicles, ships, rng, max_attempts=50):
        state = cls(vehicles, ships, {})
        for vid in state.order:
            state.placement[vid] = {"ship": OUTSIDE, "x": None, "y": None, "orient": rng.choice(["H", "V"])}

        for vid in state.order:
            orient = state.placement[vid]["orient"]
            ship = rng.choice(state.ship_options)
            if ship == OUTSIDE:
                continue
            if not fits(vehicles[vid], orient, ships[ship]):
                orient = other_orient(orient)
                if not fits(vehicles[vid], orient, ships[ship]):
                    continue
            w, l = footprint(vehicles[vid], orient)
            for _ in range(max_attempts):
                x = rng.randint(1, ships[ship]["w"] - w + 1)
                y = rng.randint(1, ships[ship]["l"] - l + 1)
                if can_place(state, vid, ship, x, y, orient):
                    state.placement[vid] = {"ship": ship, "x": x, "y": y, "orient": orient}
                    break
        return state

    # Keluaran: DockState baru dengan placement yang di copy.
    # vehicles / ships / ship_options / order di-share, jadi copy murah dan state asal aman.
    def copy(self):
        new_state = DockState.__new__(DockState)
        new_state.vehicles = self.vehicles
        new_state.ships = self.ships
        new_state.ship_options = self.ship_options
        new_state.order = self.order
        new_state.placement = {vid: dict(p) for vid, p in self.placement.items()}
        return new_state

    # Keluaran: list vid (urut sesuai self.order) yang ship != OUTSIDE.
    def placed_vehicles(self):
        return [vid for vid in self.order if self.placement[vid]["ship"] != OUTSIDE]

    # Keluaran: total weight vehicle yang placed di satu ship.
    def ship_load(self, ship):
        return sum(self.vehicles[vid]["weight"] for vid in self.order if self.placement[vid]["ship"] == ship)

    # Keluaran: satu neighbor random (boleh tidak feasible), atau None kalau tidak ada move.
    # Untuk algoritma yang hanya butuh satu neighbor per iterasi.
    def random_neighbor(self, rng):
        return moves.random_neighbor(self, rng)

    # Keluaran: generator (deskripsi move, state baru) untuk semua neighbor.
    # Untuk algoritma yang butuh semua neighbor.
    def all_neighbors(self):
        return moves.all_neighbors(self)

    # Keluaran: {vid: copy placement[vid]} untuk disimpan ke json.
    def to_dict(self):
        return {vid: dict(self.placement[vid]) for vid in self.order}

    # Bahan visualisasi geladak.
    # Keluaran: {ship: grid numpy ukuran (L, W)}; sel kosong -1, sel terisi berisi index
    # vehicle di self.order. Koordinat state 1-indexed, jadi vehicle mengisi
    # sel [y-1 : y-1+l, x-1 : x-1+w].
    def build_grids(self):
        grids = {ship: np.full((ship_info["l"], ship_info["w"]), -1, dtype=int)
                 for ship, ship_info in self.ships.items()}
        for idx, vid in enumerate(self.order):
            p = self.placement[vid]
            if p["ship"] == OUTSIDE:
                continue
            w, l = footprint(self.vehicles[vid], p["orient"])
            grids[p["ship"]][p["y"] - 1:p["y"] - 1 + l, p["x"] - 1:p["x"] - 1 + w] = idx
        return grids

    # Keluaran: chromosome untuk GA, yaitu list gen {ship, x, y, orient} urut sesuai self.order.
    def to_chromosome(self):
        return [dict(self.placement[vid]) for vid in self.order]

    # Masukan : chromosome (list gen urut sesuai self.order).
    # Keluaran: DockState baru dengan placement dari chromosome; belum tentu feasible.
    def from_chromosome(self, chromosome):
        new_state = self.copy()
        new_state.placement = {vid: dict(gene) for vid, gene in zip(self.order, chromosome)}
        return new_state
