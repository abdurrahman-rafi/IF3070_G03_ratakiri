import json
import os
import random

from ..model.instance import load_instance
from ..model.state import DockState


# Menjalankan satu algoritma n_runs kali pada instance yang sama.
# Tiap run memakai seed sendiri (base_seed + run) untuk initial state dan rng algoritma,
# jadi hasilnya bisa diulang persis dan tiap run mulai dari state awal yang berbeda.
# Masukan: algorithm (fungsi (initial_state, rng, **params) -> dict hasil),
# instance path, n_runs, base_seed, out_dir, dan **params yang diteruskan ke algoritma.
# Keluaran: list dict hasil; tiap hasil juga disimpan ke out_dir lewat save_result.
def run_repeated(algorithm, instance_path, n_runs=3, base_seed=945, out_dir="output", **params):
    vehicles, ships = load_instance(instance_path)
    results = []
    for run in range(n_runs):
        seed = base_seed + run
        rng = random.Random(seed)
        state = DockState.initial_state(vehicles, ships, rng)
        result = algorithm(state, rng, **params)
        result["seed"] = seed
        result["run"] = run + 1
        result["instance"] = os.path.basename(instance_path)
        result["path"] = save_result(result, out_dir)
        results.append(result)
    return results


# Menyimpan satu hasil ke JSON.
# Lokasi: out_dir/instance/<algorithm>/run<run>_seed<seed>_<params>.json.
# Nama instance ada di path supaya hasil dari instance berbeda tidak saling menimpa.
# Params ada di nama file supaya variasi nama parameter tidak saling menimpa.
# Keluaran: path file yang ditulis.
def save_result(result, out_dir="output"):
    instance_name = os.path.splitext(result.get("instance", "unknown"))[0]
    folder = os.path.join(out_dir, instance_name,result["algorithm"])
    os.makedirs(folder, exist_ok=True)
    param_text = "_".join(f"{key}{value}" for key, value in sorted(result["params"].items()))
    name = f"run{result['run']}_seed{result['seed']}_{param_text}.json"
    path = os.path.join(folder, name)
    with open(path, "w", encoding="utf-8") as out_file:
        json.dump(result, out_file, indent=2)
    return path
