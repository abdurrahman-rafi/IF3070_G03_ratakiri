import argparse
import statistics

from .runner import run_repeated
from ..algorithms.genetic import genetic_algorithm

# Eksperimen GA sesuai sperifikasi: 2 skenario * 3 variasi * 3 run = 18 run.
CONTROL_POPULATION = 50 # skenario 1: populasi tetap, iteriasi divariasikan
ITERATION_VARIANTS = (50, 100, 200)
CONTROL_ITERATIONS = 50 # skenario 2: iterasi tetap, populasi divariasikan
POPULATION_VARIANTS = (20, 50, 100)


# Menjalankan kedua skenario dan mencetak ringkasan tiap konfigurasi.
# Masukan: path_instance, base_seed, out_dir.
# Keluaran: list semua hasil (18 dict)
def run_all(instance_path, base_seed=945, out_dir="output"):
    configs = [(CONTROL_POPULATION, it) for it in ITERATION_VARIANTS]
    configs += [(pop, CONTROL_ITERATIONS) for pop in POPULATION_VARIANTS]
    all_results = []
    for population, iterations in configs:
        results = run_repeated(genetic_algorithm, instance_path, n_runs=3, base_seed=base_seed,
                               out_dir=out_dir, population_size=population, iterations=iterations)
        values = [r["final_value"] for r in results]
        times = [r["duration_sec"] for r in results]
        print(f"populasi={population<4}, iterasi={iterations<4}: "
              f"final={values} rata-rata={statistics.mean(values):.1f} "
              f"durasi rata-rata={statistics.mean(times):.2f}s")
        all_results.extend(results)
    return all_results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--instance", required=True)
    parser.add_argument("--seed", type=int, default=945)
    parser.add_argument("--out", default="output")
    args = parser.parse_args()
    run_all(args.instance, args.seed, args.out)
    