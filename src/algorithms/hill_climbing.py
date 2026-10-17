from .base import SearchRecorder
from ..model.objective import evaluate
from ..model.state import DockState


# Semua neighbor dengan value tertinggi dengan valuenya, ([], None) kalau tidak ada neighbor.
def best_neighbors(state):
    best, best_value = [], None
    for _, neighbor in state.all_neighbors():
        value = evaluate(neighbor)
        if best_value is None or value > best_value:
            best, best_value = [neighbor], value # Ganti nilai
        elif value == best_value:
            best.append(neighbor) # best state append
    return best, best_value


# Untuk steepest ascent dan random restart
# Keluaran: (state akhir, value akhir, jumlah iterasi, alasan berhenti).
def climb(state, rng, max_iterations, recorder):
    value = recorder.record(state)
    iterations = 0
    while iterations < max_iterations:
        candidates, candidate_value = best_neighbors(state)
        if not candidates or candidate_value <= value:
            return state, value, iterations, "local_maximum" # Kalau gak nemu
        state, value = rng.choice(candidates), candidate_value
        iterations += 1
        recorder.record(state, value)
    return state, value, iterations, "max_iterations"


# Steepest Ascent, pindah ke neighbor terbaik selama value-nya naik.
def steepest_ascent(initial_state, rng, max_iterations=1000):
    recorder = SearchRecorder("steepest_ascent", initial_state, {"max_iterations": max_iterations})
    state, _, iterations, stop_reason = climb(initial_state, rng, max_iterations, recorder)
    return recorder.finish(state, iterations, {"stop_reason": stop_reason})


# Stochastic, ambil satu neighbor random tiap iterasi, pindah hanya kalau value-nya naik.
def stochastic(initial_state, rng, max_iterations=1000):
    recorder = SearchRecorder("stochastic", initial_state, {"max_iterations": max_iterations})
    state = initial_state
    value = recorder.record(state)
    iterations = 0
    stop_reason = "max_iterations"
    while iterations < max_iterations:
        neighbor = state.random_neighbor(rng)
        if neighbor is None:
            stop_reason = "no_neighbor"
            break
        iterations += 1
        neighbor_value = evaluate(neighbor)
        if neighbor_value > value:
            state, value = neighbor, neighbor_value
        recorder.record(state, value)
    return recorder.finish(state, iterations, {"stop_reason": stop_reason})


# Sideways Move, neighbor terbaik yang value-nya sama tetap diterima.
# Sideways berturut-turut dibatasi max_sideways dan di-reset tiap kali value naik.
def sideways_move(initial_state, rng, max_sideways=100, max_iterations=1000):
    recorder = SearchRecorder("sideways_move", initial_state,
                              {"max_sideways": max_sideways, "max_iterations": max_iterations})
    state = initial_state
    value = recorder.record(state)
    iterations = 0
    consecutive_sideways = 0
    total_sideways = 0
    stop_reason = "max_iterations"
    while iterations < max_iterations:
        candidates, candidate_value = best_neighbors(state)
        if not candidates or candidate_value < value:
            stop_reason = "local_maximum"
            break
        if candidate_value == value:
            if consecutive_sideways >= max_sideways:
                stop_reason = "max_sideways"
                break
            consecutive_sideways += 1
            total_sideways += 1
        else:
            consecutive_sideways = 0
        state, value = rng.choice(candidates), candidate_value
        iterations += 1
        recorder.record(state, value)
    return recorder.finish(state, iterations, {"stop_reason": stop_reason, "total_sideways": total_sideways})


# Random Restart, steepest ascent dari initial_state, lalu diulang max_restart kali dari state random baru.
# History semua percobaan disambung dengan final = state terbaik dari semua percobaan.
def random_restart(initial_state, rng, max_restart=10, max_iterations=1000):
    recorder = SearchRecorder("random_restart", initial_state,
                              {"max_restart": max_restart, "max_iterations": max_iterations})
    best_state, best_value = None, float("-inf")
    iterations_per_restart = []
    start = initial_state
    for restart in range(max_restart + 1):
        if restart > 0:
            start = DockState.initial_state(initial_state.vehicles, initial_state.ships, rng)
        state, value, iterations, _ = climb(start, rng, max_iterations, recorder)
        iterations_per_restart.append(iterations)
        if value > best_value:
            best_state, best_value = state, value
    return recorder.finish(best_state, sum(iterations_per_restart),
                           {"restarts": max_restart, "iterations_per_restart": iterations_per_restart})
