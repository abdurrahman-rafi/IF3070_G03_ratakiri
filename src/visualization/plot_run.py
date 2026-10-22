import matplotlib.pyplot as plt

from ..model.instance import OUTSIDE
from .plot_state import draw_state
from .plot_progress import draw_progress


# Menyimpan satu gambar per run dengan tiga bagian berjajar horizontal:
# initial state, final state, dan plot hasil eksperimen.
# Tinggi gambar menyesuaikan ukuran ship dan panjang daftar vehicle di luar kapal.
# Tinggi deck dan kotak daftar dihitung dalam satuan lebar deck.
def plot_run(result, vehicles, ships, path):
    cmap = plt.get_cmap("tab20")
    colors = {vid: cmap(i % 20) for i, vid in enumerate(sorted(vehicles))}
    most_outside = max(sum(p["ship"] == OUTSIDE for p in result[key].values()) for key in ("initial", "final"))
    list_height = 0.07 * (most_outside + 1) + 0.1
    deck_width = 3.2
    height = deck_width * (sum(ship["l"] / ship["w"] for ship in ships.values()) + list_height) + 1.2
    fig = plt.figure(figsize=(2 * deck_width + 7, height), layout="constrained")
    initial, final, progress = fig.subfigures(1, 3, width_ratios=[deck_width, deck_width, 7])

    draw_state(initial, vehicles, ships, result["initial"], "Initial", result["initial_value"], colors, list_height)
    draw_state(final, vehicles, ships, result["final"], "Final", result["final_value"], colors, list_height)
    draw_progress(progress, result)

    fig.suptitle(f"{result['algorithm']} - run {result['run']}, seed {result['seed']}")
    fig.savefig(path, dpi=120)
    plt.close(fig)
