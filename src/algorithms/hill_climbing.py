from .base import SearchRecorder


def steepest_ascent(initial_state, rng, max_iterations=1000):
    raise NotImplementedError


def stochastic(initial_state, rng, max_iterations=1000):
    raise NotImplementedError


def sideways_move(initial_state, rng, max_sideways=100, max_iterations=1000):
    raise NotImplementedError


def random_restart(initial_state, rng, max_restart=10, max_iterations=1000):
    raise NotImplementedError
