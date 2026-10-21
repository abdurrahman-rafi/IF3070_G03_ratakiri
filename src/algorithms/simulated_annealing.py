import math

from .base import SearchRecorder
from ..model.objective import evaluate


def simulated_annealing(initial_state, rng, initial_temp=100.0,
                        cooling_rate=0.99, min_temp=0.01, stagnation_limit=50):
    """Cari solusi valid terbaik sambil mencatat penolakan dan episode stagnasi.

    Satu episode stagnasi tercatat saat best feasible tidak membaik selama
    stagnation_limit iterasi beruntun. Episode baru hanya dapat dihitung
    setelah best feasible membaik. Metrik ini tidak menghentikan pencarian
    dan tidak membuktikan bahwa state berada di local optimum.
    """
    if not (math.isfinite(initial_temp) and math.isfinite(min_temp)
            and 0 < min_temp < initial_temp):
        raise ValueError(
            "Suhu harus finite dan memenuhi 0 < min_temp < initial_temp"
        )

    if not 0 < cooling_rate < 1:
        raise ValueError("cooling_rate harus antara 0 dan 1")

    if (isinstance(stagnation_limit, bool)
            or not isinstance(stagnation_limit, int) or stagnation_limit < 1):
        raise ValueError("stagnation_limit harus bilangan bulat positif")

    params = {
        "initial_temp": initial_temp,
        "cooling_rate": cooling_rate,
        "min_temp": min_temp,
        "stagnation_limit": stagnation_limit,
    }

    recorder = SearchRecorder(
        "simulated_annealing", initial_state, params
    )

    current = initial_state.copy()
    current_value = evaluate(current)
    temperature = initial_temp
    iterations = 0
    rejected_count = 0
    stuck_count = 0
    stagnation_iterations = 0

    recorder.record(current, current_value)

    while temperature > min_temp:
        neighbor = current.random_neighbor(rng)

        if neighbor is None:
            break

        neighbor_value = evaluate(neighbor)
        delta = neighbor_value - current_value
        probability = recorder.record_acceptance(delta, temperature)

        if delta >= 0 or rng.random() < probability:
            current = neighbor
            current_value = neighbor_value
        else:
            rejected_count += 1

        iterations += 1
        previous_best = recorder.best_feasible_value
        recorder.record(current, current_value)
        if recorder.best_feasible_value > previous_best:
            stagnation_iterations = 0
        else:
            stagnation_iterations += 1
            if stagnation_iterations == stagnation_limit:
                stuck_count += 1
        temperature *= cooling_rate

    # Laporkan solusi valid terbaik yang pernah dikunjungi.
    final_state = recorder.best_feasible
    if final_state is None:
        final_state = current

    return recorder.finish(
        final_state,
        iterations,
        extra={
            "last_value": current_value,
            "rejected_count": rejected_count,
            "stuck_count": stuck_count,
            "stagnation_iterations": stagnation_iterations,
        },
    )
