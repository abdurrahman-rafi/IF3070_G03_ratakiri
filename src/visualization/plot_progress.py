import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


# Menyimpan plot hasil eksperimen satu run.
# Semua algoritma: value objective terhadap iterasi (iterasi 0 = initial state).
# GA: max dan rata-rata populasi per generasi. Random restart: garis putus-putus di tiap restart.
# Simulated Annealing: subplot kedua e^(dE/T) terhadap iterasi.
# Masukan: result (dict hasil algoritma), path file png.
def plot_progress(result, path):
    has_sa = bool(result["accept_probs"])
    fig, axes = plt.subplots(2 if has_sa else 1, 1, figsize=(9, 7 if has_sa else 4), squeeze=False)
    ax = axes[0][0]
    history = result["history"]

    if result["avg_history"]:
        ax.plot(range(len(history)), history, label="max populasi")
        ax.plot(range(len(result["avg_history"])), result["avg_history"], label="rata-rata populasi")
        ax.legend()
    else:
        ax.plot(range(len(history)), history)

    iterations_per_restart = result["extra"].get("iterations_per_restart", [])
    boundary = 0
    for index, iterations in enumerate(iterations_per_restart[:-1]):
        boundary += iterations + 1
        ax.axvline(boundary - 0.5, color="gray", linestyle=":", linewidth=0.8,
                   label="restart" if index == 0 else None)
    if len(iterations_per_restart) > 1:
        ax.legend()

    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_xlabel("iterasi")
    ax.set_ylabel("objective (ShippingFee)")
    ax.set_title(f"{result['algorithm']} - final {result['final_value']}, "
                 f"{result['iterations']} iterasi, {result['duration_sec']:.2f} s", fontsize=10)

    if has_sa:
        ax_sa = axes[1][0]
        ax_sa.plot(range(1, len(result["accept_probs"]) + 1), result["accept_probs"], ".", markersize=2)
        ax_sa.set_ylim(-0.05, 1.05)
        ax_sa.set_xlabel("iterasi")
        ax_sa.set_ylabel(r"$e^{\Delta E / T}$")
        ax_sa.set_title(f"stuck: {result['extra'].get('stuck_count', '-')} kali", fontsize=10)

    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
