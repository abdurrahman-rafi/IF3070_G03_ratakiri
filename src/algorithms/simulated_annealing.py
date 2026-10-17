import math

from .base import SearchRecorder
from ..model.objective import evaluate


def simulated_annealing(initial_state, rng, initial_temp=100.0,
                        cooling_rate=0.99, min_temp=0.01,
                        evaluation_bias=0.0):
    if not (math.isfinite(initial_temp) and math.isfinite(min_temp)
            and 0 < min_temp < initial_temp):
        raise ValueError(
            "Suhu harus finite dan memenuhi 0 < min_temp < initial_temp"
        )

    if not 0 < cooling_rate < 1:
        raise ValueError("cooling_rate harus antara 0 dan 1")

    # evaluation_bias baru dicatat, belum memengaruhi pencarian.
    params = {
        "initial_temp": initial_temp,
        "cooling_rate": cooling_rate,
        "min_temp": min_temp,
        "evaluation_bias": evaluation_bias,
    }

    recorder = SearchRecorder(
        "simulated_annealing", initial_state, params
    )

    current = initial_state.copy()
    current_value = evaluate(current)
    temperature = initial_temp
    iterations = 0

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

        iterations += 1
        recorder.record(current, current_value)
        temperature *= cooling_rate

    # Laporkan solusi valid terbaik yang pernah dikunjungi.
    final_state = recorder.best_feasible
    if final_state is None:
        final_state = current

    return recorder.finish(
        final_state,
        iterations,
        extra={"last_value": current_value},
    )
