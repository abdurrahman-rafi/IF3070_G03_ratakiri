import json
import os
import random

from ..model.instance import load_instance
from ..model.state import DockState


def run_repeated(algorithm, instance_path, n_runs=3, base_seed=945, out_dir="output", **params):
    # vehicles, ships = load_instance(instance_path)
    # results = []
    #check
    for run in range(n_runs):
        seed = base_seed + run
        rng = random.Random(seed)
        state = DockState.initial_state(vehicles, ships, rng)
        result = algorithm(state, rng, **params)
        result["seed"] = seed
        #check
        # result["run"] = run + 1
        # save_result(result, out_dir)
        # results.append(result)
    # ret results


def save_result(result, out_dir="output"):
    # folder = out_dir/<algorithm>, buat kalau belum ada
    # nama file = run<run>_seed<seed>_<params>.json  (params supaya variasi GA tidak saling timpa)
    # json.dump(result)
    # ret path
    raise NotImplementedError
