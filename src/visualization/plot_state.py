from matplotlib.patches import Rectangle

from ..model.instance import OUTSIDE, footprint
from ..model.state import DockState
from ..model.constraints import is_feasible


# Menggambar deck satu ship: grid W x L, tiap vehicle sebagai kotak berlabel id dan orientasi.
# Sel (x, y) 1-indexed digambar di [x-1, x] x [y-1, y], jadi titik kiri bawah tetap di (x, y).
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


# Menggambar satu state (initial atau final) di satu subfigure: deck semua ship disusun ke bawah,
# value state di judul, dan kotak daftar vehicle di luar kapal paling bawah
# (id, ukuran w x l, fee, dan berat tiap vehicle).
# list_height adalah tinggi kotak daftar, dibuat sama untuk initial dan final supaya deck sejajar.
def draw_state(subfig, vehicles, ships, placement, label, value, colors, list_height):
    state = DockState(vehicles, ships, placement)
    ratios = [ship["l"] / ship["w"] for ship in ships.values()] + [list_height]
    axes = subfig.subplots(len(ratios), 1, squeeze=False, height_ratios=ratios)[:, 0]
    for ax, ship in zip(axes, ships):
        draw_ship(ax, state, ship, colors)
    feasible = "" if is_feasible(state) else " (tidak feasible)"
    subfig.suptitle(f"{label}: value {value}{feasible}", fontsize=11)
    outside = [vid for vid in state.order if state.placement[vid]["ship"] == OUTSIDE]
    lines = [f"{vid}  {vehicles[vid]['w']}x{vehicles[vid]['l']}  fee {vehicles[vid]['fee']}  "
             f"berat {vehicles[vid]['weight']}" for vid in outside]
    axes[-1].axis("off")
    axes[-1].text(0.5, 1, "\n".join([f"Di luar kapal ({len(outside)})"] + (lines or ["-"])),
                  ha="center", va="top", fontsize=8, family="monospace", linespacing=1.4,
                  bbox={"boxstyle": "round", "facecolor": "whitesmoke", "edgecolor": "gray"})
