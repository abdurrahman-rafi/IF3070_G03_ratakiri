from .base import SearchRecorder


#check
def one_point_crossover(parent_a, parent_b, rng):
    k = rng.randrange(1, len(parent_a))
    return [dict(g) for g in parent_a[:k]] + [dict(g) for g in parent_b[k:]]
#check


def genetic_algorithm(initial_state, rng, population_size=50, iterations=100):
    raise NotImplementedError #implement
