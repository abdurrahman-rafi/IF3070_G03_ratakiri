import argparse
import json
import os
import random

from .model.instance import load_instance
from .model.state import DockState
from .model.objective import evaluate
from .model.constraints import is_feasible
from .algorithms import hill_climbing
from .algorithms.simulated_annealing import simulated_annealing
from .algorithms.genetic import genetic_algorithm
from .experiments.runner import run_repeated
from .experiments.ga_experiments import run_all as run_ga_experiments
from .visualization.plot_run import plot_run

ALGORITHMS = {
    "steepest": (hill_climbing.steepest_ascent, ("max_iterations",)),
    "stochastic": (hill_climbing.stochastic, ("max_iterations",)),
    "sideways": (hill_climbing.sideways_move, ("max_sideways", "max_iterations")),
    "restart": (hill_climbing.random_restart, ("max_restart", "max_iterations")),
    "sa": (simulated_annealing, ("initial_temp", "cooling_rate", "min_temp", "stagnation_limit")),
    "ga": (genetic_algorithm, ("population_size", "iterations", "crossover_rate", "mutation_rate")),
}
PARAMETER_TYPES = {
    "max_iterations": int, "max_sideways": int, "max_restart": int,
    "initial_temp": float, "cooling_rate": float, "min_temp": float,
    "stagnation_limit": int,
    "population_size": int, "iterations": int, "crossover_rate": float, "mutation_rate": float,
}


# Mencetak satu baris ringkasan per run: value awal -> akhir, iterasi, durasi, extra.
def print_summary(results):
    for result in results:
        print(f"{result['algorithm']:20} run{result['run']} seed{result['seed']} "
              f"{result['initial_value']:>5} -> {result['final_value']:>5}  "
              f"iterasi={result['iterations']:<5} durasi={result['duration_sec']:.2f}s  {result['extra']}")


# CLI.
#   tanpa --algo / --all : preview satu initial state random
#   --algo <nama>        : jalankan satu algoritma --runs kali
#   --all                : semua varian HC dan SA (--runs kali) + eksperimen GA
# Tiap run disimpan sebagai json + png di out_dir/<instance>/<algorithm>/.
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--instance", required=True)
    parser.add_argument("--seed", type=int, default=945)
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--out", default="output")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--algo", choices=ALGORITHMS)
    mode.add_argument("--all", action="store_true")
    for name, cast in PARAMETER_TYPES.items():
        parser.add_argument("--" + name.replace("_", "-"), type=cast)
    args = parser.parse_args()

    vehicles, ships = load_instance(args.instance)
    given = {name: getattr(args, name) for name in PARAMETER_TYPES if getattr(args, name) is not None}

    if args.algo:
        algorithm, allowed = ALGORITHMS[args.algo]
        unused = set(given) - set(allowed)
        if unused:
            parser.error(f"parameter {sorted(unused)} tidak dipakai oleh --algo {args.algo}")
        results = run_repeated(algorithm, args.instance, n_runs=args.runs, base_seed=args.seed,
                               out_dir=args.out, **given)
    elif args.all:
        if given:
            parser.error("--all memakai parameter default; jalankan --algo untuk parameter lain")
        results = []
        for name, (algorithm, _) in ALGORITHMS.items():
            if name != "ga":
                results += run_repeated(algorithm, args.instance, n_runs=args.runs,
                                        base_seed=args.seed, out_dir=args.out)
        results += run_ga_experiments(args.instance, args.seed, args.out)
    else:
        state = DockState.initial_state(vehicles, ships, random.Random(args.seed))
        print(json.dumps(state.to_dict(), indent=2))
        print("value:", evaluate(state))
        print("feasible:", is_feasible(state))
        return

    for result in results:
        plot_run(result, vehicles, ships, os.path.splitext(result["path"])[0] + ".png")
    print_summary(results)
    print(f"{len(results)} hasil disimpan di {args.out}/")


if __name__ == "__main__":
    main()
