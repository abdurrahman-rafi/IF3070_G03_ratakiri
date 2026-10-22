from matplotlib.ticker import MaxNLocator


# Menggambar plot hasil eksperimen satu run di satu subfigure.
# Semua algoritma: value objective terhadap iterasi (iterasi 0 = initial state).
# GA: max dan rata-rata populasi per generasi. Random restart: garis putus-putus di tiap restart.
# Simulated Annealing: plot kedua e^(dE/T) terhadap iterasi beserta jumlah stuck.
def draw_progress(subfig, result):
    has_sa = bool(result["accept_probs"])
    axes = subfig.subplots(2 if has_sa else 1, 1, squeeze=False)[:, 0]
    ax = axes[0]
    history = result["history"]

    if result["avg_history"]:
        ax.plot(range(len(history)), history, label="max populasi")
        ax.plot(range(len(result["avg_history"])), result["avg_history"], label="rata-rata populasi")
    else:
        ax.plot(range(len(history)), history)

    iterations_per_restart = result["extra"].get("iterations_per_restart", [])
    boundary = 0
    for index, iterations in enumerate(iterations_per_restart[:-1]):
        boundary += iterations + 1
        ax.axvline(boundary - 0.5, color="gray", linestyle=":", linewidth=0.8,
                   label="restart" if index == 0 else None)
    if ax.get_legend_handles_labels()[0]:
        ax.legend()

    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_xlabel("iterasi")
    ax.set_ylabel("objective (ShippingFee)")
    ax.set_title(f"final {result['final_value']}, {result['iterations']} iterasi, "
                 f"{result['duration_sec']:.2f} s", fontsize=10)

    if has_sa:
        ax_sa = axes[1]
        ax_sa.plot(range(1, len(result["accept_probs"]) + 1), result["accept_probs"], ".", markersize=2)
        ax_sa.set_ylim(-0.05, 1.05)
        ax_sa.set_xlabel("iterasi")
        ax_sa.set_ylabel(r"$e^{\Delta E / T}$")
        ax_sa.set_title(f"stuck: {result['extra'].get('stuck_count', '-')} kali", fontsize=10)
