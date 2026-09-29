import math
import time

from ..model.constraints import total_penalty
from ..model.objective import evaluate


class SearchRecorder:
    def __init__(self, algorithm, initial_state, params=None):
        # self.algorithm = algorithm
        # self.params = params or {}
        # self.initial_state = initial_state.copy()
        #check
        self.start = time.perf_counter()
        self.history = []
        self.accept_probs = []
        #check
        # self.avg_history = []   (GA)
        #check
        self.best_feasible = None
        self.best_feasible_value = float("-inf")
        #check
        # self.extra = {}

    def record(self, state, value=None):
        # kalau value None -> value = evaluate(state)
        # self.history.append(value)
        #check
        if value > self.best_feasible_value and total_penalty(state) == 0:
            self.best_feasible = state.copy()
            self.best_feasible_value = value
        #check
        # ret value

    def record_population(self, population, values):
        # self.history.append(max(values))
        # self.avg_history.append(rata-rata values)
        # untuk tiap (state, value): update best_feasible seperti di record()
        raise NotImplementedError

    def record_acceptance(self, delta, temperature):
        #check
        p = math.exp(delta / temperature) if delta < 0 else 1.0
        self.accept_probs.append(p)
        #check
        return p

    def finish(self, final_state, iterations, extra=None):
        # self.extra.update(extra or {})
        #check
        return {
            "algorithm": self.algorithm,
            "params": self.params,
            "initial": self.initial_state.to_dict(),
            "initial_value": evaluate(self.initial_state),
            "final": final_state.to_dict(),
            "final_value": evaluate(final_state),
            "final_feasible": total_penalty(final_state) == 0,
            "best_feasible": self.best_feasible.to_dict() if self.best_feasible else None,
            "best_feasible_value": self.best_feasible_value if self.best_feasible else None,
            "history": self.history,
            "avg_history": self.avg_history,
            "accept_probs": self.accept_probs,
            "iterations": iterations,
            "duration_sec": time.perf_counter() - self.start,
            "extra": self.extra, # untuk algoritma yang butuh variabel ekstra
        }
        #check
