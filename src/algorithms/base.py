import math
import time

from ..model.constraints import is_feasible
from ..model.objective import evaluate


class SearchRecorder:
    # Pencatat hasil pencarian yang dipakai semua algoritma.
    # Dibuat tepat sebelum pencarian mulai, karena timer durasi jalan dari sini.
    # Masukan: algorithm (nama algoritma), initial_state, params (parameter algoritma untuk dicatat).
    def __init__(self, algorithm, initial_state, params=None):
        self.algorithm = algorithm
        self.params = params or {}
        self.initial_state = initial_state.copy()
        self.start = time.perf_counter()
        self.history = []
        self.accept_probs = []
        self.avg_history = []
        self.best_feasible = None
        self.best_feasible_value = float("-inf")
        self.extra = {}

    # Dipanggil sekali tiap iterasi: mencatat value state sekarang ke history
    # dan memperbarui state feasible terbaik yang pernah ditemui.
    # Masukan : state, value (kalau None dihitung dengan evaluate). Keluaran: value.
    def record(self, state, value=None):
        if value is None:
            value = evaluate(state)
        self.history.append(value)
        if value > self.best_feasible_value and is_feasible(state):
            self.best_feasible = state.copy()
            self.best_feasible_value = value
        return value

    # Versi record untuk GA, dipanggil sekali tiap generasi.
    # Masukan: population (list state) dan values (value tiap state, urutan sama).
    # Mencatat max ke history, rata-rata ke avg_history, dan memperbarui best_feasible.
    def record_population(self, population, values):
        self.history.append(max(values))
        self.avg_history.append(sum(values) / len(values))
        for state, value in zip(population, values):
            if value > self.best_feasible_value and is_feasible(state):
                self.best_feasible = state.copy()
                self.best_feasible_value = value

    # Khusus Simulated Annealing: menghitung dan mencatat peluang diterima e^(delta / T).
    # Masukan : delta (value neighbor - value sekarang), temperature (> 0).
    # Keluaran: peluangnya; delta >= 0 selalu diterima sehingga peluangnya 1.
    def record_acceptance(self, delta, temperature):
        p = math.exp(delta / temperature) if delta < 0 else 1.0
        self.accept_probs.append(p)
        return p

    # Menutup pencarian.
    # Masukan : final_state, iterations, extra (variabel khusus algoritma, misal jumlah restart).
    # Keluaran: dict hasil yang siap disimpan ke json.
    def finish(self, final_state, iterations, extra=None):
        self.extra.update(extra or {})
        return {
            "algorithm": self.algorithm,
            "params": self.params,
            "initial": self.initial_state.to_dict(),
            "initial_value": evaluate(self.initial_state),
            "final": final_state.to_dict(),
            "final_value": evaluate(final_state),
            "final_feasible": is_feasible(final_state),
            "best_feasible": self.best_feasible.to_dict() if self.best_feasible else None,
            "best_feasible_value": self.best_feasible_value if self.best_feasible else None,
            "history": self.history,
            "avg_history": self.avg_history,
            "accept_probs": self.accept_probs,
            "iterations": iterations,
            "duration_sec": time.perf_counter() - self.start,
            "extra": self.extra,
        }
