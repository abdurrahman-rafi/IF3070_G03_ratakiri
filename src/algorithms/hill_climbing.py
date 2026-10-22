# Pseudocode dan implementasi diambil dari S. Russell dan P. Norvig, Artificial Intelligence: A Modern Approach, ed. ke-4, Bab 4,
# serta M. L. Khodra, "Beyond Classical Search: Hill-climbing Search", YouTube, 2021.

from .base import SearchRecorder
from ..model.instance import OUTSIDE
from ..model.constraints import can_place
from ..model.objective import total_fee
from ..model.state import DockState


# Value neighbor tanpa mengecek ulang seluruh state.
# State asal di hill climbing selalu feasible, jadi cukup cek vehicle yang dipindah dengan can_place.
# Hasilnya sama dengan evaluate(neighbor) selama state asal feasible.
# Input neighbor dan vid yang dipindah, output 0 kalau melanggar constraint, selain itu total fee.
def neighbor_value(neighbor, moved_vehicles):
    for vid in moved_vehicles:
        p = neighbor.placement[vid]
        if p["ship"] != OUTSIDE and not can_place(neighbor, vid, p["ship"], p["x"], p["y"], p["orient"]):
            return 0
    return total_fee(neighbor)


# Generator (neighbor, value) untuk semua neighbor dari state.
def scored_neighbors(state):
    for moved_vehicles, neighbor in state.all_neighbors():
        yield neighbor, neighbor_value(neighbor, moved_vehicles)


# Semua neighbor dengan value tertinggi beserta value-nya, atau ([], None) kalau tidak ada neighbor.
def best_neighbors(state):
    best, best_value = [], None
    for neighbor, value in scored_neighbors(state):
        if best_value is None or value > best_value:
            best, best_value = [neighbor], value
        elif value == best_value:
            best.append(neighbor)
    return best, best_value


# Loop steepest ascent yang dipakai steepest_ascent, sideways_move, dan random_restart.
# Pindah ke neighbor terbaik selama value-nya naik. Value yang sama (sideways) diterima
# paling banyak max_sideways kali berturut-turut, dan hitungannya di-reset tiap kali value naik.
# max_sideways = 0 berarti steepest ascent biasa.
# Output (state akhir, value akhir, jumlah iterasi, alasan berhenti, total sideways).
def climb(state, rng, max_iterations, max_sideways, recorder):
    value = recorder.record(state)
    iterations = sideways = total_sideways = 0
    while iterations < max_iterations:
        candidates, candidate_value = best_neighbors(state)
        if not candidates or candidate_value < value:
            return state, value, iterations, "local_maximum", total_sideways
        if candidate_value == value:
            if sideways == max_sideways:
                return state, value, iterations, "max_sideways" if max_sideways else "local_maximum", total_sideways
            sideways += 1
            total_sideways += 1
        else:
            sideways = 0
        state, value = rng.choice(candidates), candidate_value
        iterations += 1
        recorder.record(state, value)
    return state, value, iterations, "max_iterations", total_sideways


# Steepest Ascent: pindah ke neighbor terbaik selama value-nya naik.
def steepest_ascent(initial_state, rng, max_iterations=1000):
    recorder = SearchRecorder("steepest_ascent", initial_state, {"max_iterations": max_iterations})
    state, _, iterations, stop_reason, _ = climb(initial_state, rng, max_iterations, 0, recorder)
    return recorder.finish(state, iterations, {"stop_reason": stop_reason})


# Sideways Move: seperti steepest ascent, tetapi neighbor terbaik yang value-nya sama tetap diterima.
def sideways_move(initial_state, rng, max_sideways=100, max_iterations=1000):
    recorder = SearchRecorder("sideways_move", initial_state,
                              {"max_sideways": max_sideways, "max_iterations": max_iterations})
    state, _, iterations, stop_reason, total_sideways = climb(initial_state, rng, max_iterations,
                                                              max_sideways, recorder)
    return recorder.finish(state, iterations, {"stop_reason": stop_reason, "total_sideways": total_sideways})


# Stochastic: pilih satu neighbor random dari semua neighbor yang value-nya naik (uphill).
# Berhenti kalau tidak ada neighbor uphill (local maximum) atau max_iterations tercapai.
def stochastic(initial_state, rng, max_iterations=1000):
    recorder = SearchRecorder("stochastic", initial_state, {"max_iterations": max_iterations})
    state, value = initial_state, recorder.record(initial_state)
    iterations, stop_reason = 0, "max_iterations"
    while iterations < max_iterations:
        uphill = [(neighbor, neighbor_value) for neighbor, neighbor_value in scored_neighbors(state)
                  if neighbor_value > value]
        if not uphill:
            stop_reason = "local_maximum"
            break
        state, value = rng.choice(uphill)
        iterations += 1
        recorder.record(state, value)
    return recorder.finish(state, iterations, {"stop_reason": stop_reason})


# Random Restart: steepest ascent dari initial_state, lalu diulang max_restart kali dari state random baru.
# History semua percobaan disambung, dan final adalah state terbaik dari semua percobaan.
def random_restart(initial_state, rng, max_restart=10, max_iterations=1000):
    recorder = SearchRecorder("random_restart", initial_state,
                              {"max_restart": max_restart, "max_iterations": max_iterations})
    best_state, best_value = None, -1
    iterations_per_restart = []
    for restart in range(max_restart + 1):
        start = initial_state if restart == 0 else DockState.initial_state(initial_state.vehicles,
                                                                           initial_state.ships, rng)
        state, value, iterations, _, _ = climb(start, rng, max_iterations, 0, recorder)
        iterations_per_restart.append(iterations)
        if value > best_value:
            best_state, best_value = state, value
    return recorder.finish(best_state, sum(iterations_per_restart),
                           {"restarts": max_restart, "iterations_per_restart": iterations_per_restart})
