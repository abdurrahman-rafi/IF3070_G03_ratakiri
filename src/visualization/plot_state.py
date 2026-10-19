import textwrap

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from ..model.instance import OUTSIDE, footprint
from ..model.state import DockState
from ..model.constraints import is_feasible


# Menggambar geladak satu ship: grid W x L, tiap vehicle sebagai kotak berlabel id.
# Sel (x, y) 1-indexed digambar di [x-1, x] x [y-1, y], jadi titik kiri bawah tetap di (x, y).
# Masukan: ax matplotlib, state, id ship, colors {vid: warna}.
def draw_ship(ax, state, ship, colors):
    ship_info = state.ships[ship]
    for vid in state.placed_vehicles():
        p = state.placement[vid]
        if p["ship"] != ship:
            continue
        w, l = footprint(state.vehicles[vid], p["orient"])
        ax.add_patch(Rectangle((p["x"] - 1, p["y"] - 1), w, l, facecolor=colors[vid],
                               edgecolor="black", linewidth=1, alpha=0.85))
        ax.text(p["x"] - 1 + w / 2, p["y"] - 1 + l / 2, f"{vid}\n({p['orient']})",
                ha="center", va="center", fontsize=7)
    ax.set_xlim(0, ship_info["w"])
    ax.set_ylim(0, ship_info["l"])
    ax.set_xticks(range(ship_info["w"] + 1))
    ax.set_yticks(range(ship_info["l"] + 1))
    ax.tick_params(labelbottom=False, labelleft=False, length=0)
    ax.grid(True, linewidth=0.3, color="gray")
    ax.set_aspect("equal")
    ax.set_title(f"Ship {ship} ({ship_info['w']}x{ship_info['l']}) "
                 f"load {state.ship_load(ship)}/{ship_info['capacity']}", fontsize=9)


# Menyimpan gambar initial state (kiri) dan final state (kanan) dari satu hasil run.
# Tiap kolom: geladak semua ship, value state, dan daftar vehicle yang di luar kapal.
# Masukan: result (dict hasil algoritma), vehicles, ships, path file png.
def plot_state(result, vehicles, ships, path):
    columns = [("Initial", result["initial"], result["initial_value"]),
               ("Final", result["final"], result["final_value"])]
    cmap = plt.get_cmap("tab20")
    colors = {vid: cmap(i % 20) for i, vid in enumerate(sorted(vehicles))}
    ratio = max(ship["l"] / ship["w"] for ship in ships.values())
    panel = 3.5
    fig, axes = plt.subplots(len(ships), 2, squeeze=False,
                             figsize=(2 * panel + 1, len(ships) * min(panel * ratio, 9) + 2))

    for column, (label, placement, value) in enumerate(columns):
        state = DockState(vehicles, ships, {vid: dict(p) for vid, p in placement.items()})
        for row, ship in enumerate(ships):
            draw_ship(axes[row][column], state, ship, colors)
        feasible = "" if is_feasible(state) else " (tidak feasible)"
        axes[0][column].set_title(f"{label}: value {value}{feasible}\n" + axes[0][column].get_title(),
                                  fontsize=10)
        outside = [vid for vid in state.order if state.placement[vid]["ship"] == OUTSIDE]
        axes[-1][column].set_xlabel(textwrap.fill("Di luar: " + (", ".join(outside) or "-"), 45),
                                    fontsize=8)

    fig.suptitle(f"{result['algorithm']} - run {result.get('run', '-')}, seed {result.get('seed', '-')}")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
